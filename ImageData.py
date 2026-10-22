# -*- coding: utf-8 -*-
"""
ImageData.py : ** REQUIRED ** El vostre codi de la classe ImageData.

Aquesta classe s'encarrega d'emmagatzemar i gestionar les metadades de les
imatges generades per IA.

Funcionalitat:
    - Afegir i eliminar imatges de la col·lecció
    - Llegir les metadades embegudes dins els arxius PNG
    - Proporcionar accés a totes les metadades d'una imatge

Mètodes a implementar:
    - add_image(uuid: str, file: str) -> None
        Crea una entrada per a la imatge amb l'UUID i el path especificats.
        Inicialment les metadades estan buides (no llegides del disc).

    - remove_image(uuid: str) -> None
        Elimina la imatge i totes les seves metadades de la col·lecció.

    - load_metadata(uuid: str) -> None
        Llegeix les metadades embegudes en l'arxiu PNG i les emmagatzema.
        Aquest mètode es pot cridar múltiples vegades (p.ex. si l'arxiu canvia).

    - get_prompt(uuid: str) -> str
        Retorna el prompt utilitzat per generar la imatge.

    - get_model(uuid: str) -> str
        Retorna el model d'IA utilitzat (p.ex. "SD2", "DALL-E", "Midjourney").

    - get_seed(uuid: str) -> str
        Retorna la llavor aleatòria utilitzada en la generació.

    - get_cfg_scale(uuid: str) -> str
        Retorna el CFG Scale (guidance scale) utilitzat.

    - get_steps(uuid: str) -> str
        Retorna el nombre de passos d'iteració del model.

    - get_sampler(uuid: str) -> str
        Retorna l'algorisme de mostreig utilitzat.

    - get_generated(uuid: str) -> str
        Retorna "true" si la imatge està marcada com a generada.

    - get_created_date(uuid: str) -> str
        Retorna la data de creació en format YYYY-MM-DD.

    - get_dimensions(uuid: str) -> tuple
        Retorna una tupla (width, height) amb les dimensions de la imatge.

Notes:
    - Utilitzeu la llibreria PIL/Pillow per llegir metadades:
      img = Image.open(file)
      metadata = img.text
    - Si un camp no existeix, retorneu "None" (string)
    - Les dimensions es llegeixen amb img.width i img.height
    - Tots els camps de metadades es guarden com a strings
"""

import os

import cfg
from ImageID import canonical_file


# Camps de metadades obligatoris (nom del text chunk dins el PNG)
FIELDS = ("Prompt", "Seed", "CFG_Scale", "Steps", "Sampler", "Model",
          "Generated", "Created_Date")

EMPTY = "None"


class ImageData:
    """Metadades de cada imatge, indexades pel seu UUID."""

    def __init__(self):
        # UUID -> {"file": path de l'arxiu, "dimensions": (w, h), <camp>: str, ...}
        self._images = {}

    def add_image(self, uuid: str, file: str) -> None:
        """Crea l'entrada de la imatge amb les metadades buides."""
        if uuid is None:
            return
        entry = {field: EMPTY for field in FIELDS}
        entry["file"] = file
        entry["dimensions"] = (None, None)
        self._images[uuid] = entry

    def remove_image(self, uuid: str) -> None:
        """Elimina la imatge i les seves metadades (si existeix)."""
        self._images.pop(uuid, None)

    def load_metadata(self, uuid: str) -> None:
        """Llegeix (o torna a llegir) les metadades embegudes al PNG."""
        entry = self._images.get(uuid)
        if entry is None:
            print("ERROR: Imatge {} inexistent!".format(uuid))
            return

        metadata, dimensions = read_png_info(self.get_full_path(uuid))
        for field in FIELDS:
            value = metadata.get(field)
            entry[field] = str(value) if value else EMPTY
        entry["dimensions"] = dimensions

    def _get(self, uuid: str, field: str) -> str:
        """Valor del camp ("None" si és buit), o None si la imatge no existeix."""
        entry = self._images.get(uuid)
        if entry is None:
            return None
        return entry[field]

    def get_prompt(self, uuid: str) -> str:
        return self._get(uuid, "Prompt")

    def get_model(self, uuid: str) -> str:
        return self._get(uuid, "Model")

    def get_seed(self, uuid: str) -> str:
        return self._get(uuid, "Seed")

    def get_cfg_scale(self, uuid: str) -> str:
        return self._get(uuid, "CFG_Scale")

    def get_steps(self, uuid: str) -> str:
        return self._get(uuid, "Steps")

    def get_sampler(self, uuid: str) -> str:
        return self._get(uuid, "Sampler")

    def get_generated(self, uuid: str) -> str:
        return self._get(uuid, "Generated")

    def get_created_date(self, uuid: str) -> str:
        return self._get(uuid, "Created_Date")

    def get_dimensions(self, uuid: str) -> tuple:
        entry = self._images.get(uuid)
        if entry is None:
            return None
        return entry["dimensions"]

    def get_filename(self, uuid: str) -> str:
        """Path de l'arxiu tal com es va passar a add_image(), o None."""
        entry = self._images.get(uuid)
        if entry is None:
            return None
        return entry["file"]

    def get_file(self, uuid: str) -> str:
        return self.get_filename(uuid)

    def get_full_path(self, uuid: str) -> str:
        """Path de l'arxiu físic al disc, o None si la imatge no existeix."""
        file = self.get_file(uuid)
        if file is None:
            return None
        return resolve_path(file)

    def get_uuids(self) -> list:
        """Llista dels UUID de totes les imatges (en ordre d'inserció)."""
        return list(self._images)

    def __len__(self) -> int:
        return len(self._images)

    def __contains__(self, uuid: str) -> bool:
        return uuid in self._images

    def __iter__(self):
        return iter(self.get_uuids())

    def __str__(self) -> str:
        return "ImageData({} imatges)".format(len(self._images))


PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'


def read_png_info(path: str) -> tuple:
    """Llegeix els text chunks i les dimensions (IHDR) d'un PNG.

    Interpreta els chunks igual que cfg.read_png_metadata() (tEXt i iTXt sense
    comprimir), però salta amb seek() la resta de chunks (les dades de la
    imatge) en lloc de llegir-los: és el que fa ràpida la càrrega de milers
    d'imatges.

    Retorna (metadata: dict, (width, height)). Si hi ha error: ({}, (None, None)).
    """
    metadata = {}
    dimensions = (None, None)
    try:
        with open(path, 'rb') as f:
            if f.read(8) != PNG_SIGNATURE:
                print("ERROR: {} no és un PNG vàlid".format(path))
                return {}, (None, None)
            while True:
                header = f.read(8)
                if len(header) < 8:
                    break
                length = int.from_bytes(header[:4], byteorder='big')
                chunk_type = header[4:]

                if chunk_type in (b'IHDR', b'tEXt', b'iTXt'):
                    data = f.read(length)
                    if len(data) < length:
                        break
                    f.seek(4, os.SEEK_CUR)      # CRC
                    if chunk_type == b'IHDR':
                        dimensions = (int.from_bytes(data[0:4], byteorder='big'),
                                      int.from_bytes(data[4:8], byteorder='big'))
                    else:
                        _parse_text_chunk(chunk_type, data, metadata)
                elif chunk_type == b'IEND':
                    break
                else:
                    f.seek(length + 4, os.SEEK_CUR)     # dades + CRC
    except OSError as e:
        print("ERROR llegint {}: {}".format(path, e))
        return {}, (None, None)
    return metadata, dimensions


def _parse_text_chunk(chunk_type: bytes, data: bytes, metadata: dict) -> None:
    """Afegeix a 'metadata' el parell keyword/text d'un chunk tEXt o iTXt."""
    try:
        null_pos = data.index(b'\x00')
        keyword = data[:null_pos].decode('latin-1')
        rest = data[null_pos + 1:]
        if chunk_type == b'tEXt':
            metadata[keyword] = rest.decode('latin-1')
            return
        # iTXt: compression_flag, compression_method, language\0, translated\0, text
        if len(rest) < 2 or rest[0] != 0:
            return      # text comprimit: no el processem (igual que cfg)
        rest = rest[2:]
        rest = rest[rest.index(b'\x00') + 1:]
        rest = rest[rest.index(b'\x00') + 1:]
        metadata[keyword] = rest.decode('utf-8', errors='ignore')
    except (ValueError, UnicodeDecodeError):
        pass


def resolve_path(file: str) -> str:
    """Converteix un path relatiu a ROOT_DIR en el path de l'arxiu al disc."""
    if not isinstance(file, str) or file == "":
        return ""
    if os.path.isabs(file):
        return file
    full_path = os.path.join(cfg.get_root(), canonical_file(file))
    if not os.path.isfile(full_path) and os.path.isfile(file):
        return file     # ja era un path vàlid des del directori actual
    return full_path
