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
from ImageID import path_relatiu

CAMPS = ("Prompt", "Seed", "CFG_Scale", "Steps", "Sampler", "Model", "Generated", "Created_Date")


class ImageData:

    def __init__(self):
        self.imatges = {}       # uuid-> dades
    def add_image(self, uuid, file):
        if not isinstance(uuid, str) or uuid == "" or not isinstance(file, str):
            print("ERROR: Imatge [{}] o arxiu [{}] no vàlids. No s'afegeix".format(uuid, file))
            return
        dades= {camp: None for camp in CAMPS}
        dades["file"] =path_relatiu(file)
        dades["dimensions"] = None
        self.imatges[uuid] = dades

    def remove_image(self, uuid):
        self.imatges.pop(uuid, None)

    def load_metadata(self, uuid):
        dades = self.imatges.get(uuid)
        if dades is None:
            print("ERROR: Imatge {} inexistent!".format(uuid))
            return
        path= path_disc(dades["file"])
        if not os.path.isfile(path):
            print("ERROR: Arxiu [{}] inexistent! S'elimina la imatge {}".format(dades["file"], uuid))
            self.remove_image(uuid)
            raise FileNotFoundError(path)
        meta, mida = llegir_png(path)
        for camp in CAMPS:
            valor = meta.get(camp) if meta is not None else None
            dades[camp] = str(valor) if valor else "None"
        dades["dimensions"] = mida

    def _camp(self, uuid, camp):
        dades = self.imatges.get(uuid)
        if dades is None:
            return None
        return dades[camp]

    def get_prompt(self, uuid):
        return self._camp(uuid, "Prompt")

    def get_model(self, uuid):
        return self._camp(uuid, "Model")
        
    def get_seed(self, uuid):
        return self._camp(uuid, "Seed")

    
    def get_cfg_scale(self, uuid):
        return self._camp(uuid, "CFG_Scale")
        
    def get_steps(self, uuid):
        return self._camp(uuid, "Steps")

    def get_sampler(self, uuid):
        return self._camp(uuid, "Sampler")

    def get_generated(self, uuid):
        return self._camp(uuid, "Generated")

    def get_created_date(self, uuid):
        return self._camp(uuid, "Created_Date")

    def get_dimensions(self, uuid):
        return self._camp(uuid, "dimensions")

    def get_filename(self, uuid):
        return self._camp(uuid, "file")

    def get_uuids(self):
        return list(self.imatges)

    def __len__(self):
        return len(self.imatges)

    def __contains__(self, uuid):
        return uuid in self.imatges

    def __iter__(self):
        return iter(self.get_uuids())

    def __str__(self):
        return "ImageData({} imatges)".format(len(self.imatges))

def path_disc(file):
    """Path real de l'arxiu."""
    if not file:
        return ""
    if os.path.isabs(file):
        return file
    p = os.path.join(cfg.get_root(), path_relatiu(file))
    if not os.path.isfile(p) and os.path.isfile(file):
        return file
    return p


def llegir_png(path):
    """Text chunks i mida d'un PNG."""
    meta ={}
    mida= (None, None)
    try:
        with open(path, "rb") as f:
            if f.read(8) != b"\x89PNG\r\n\x1a\n":
                print("ERROR: {} no és un PNG vàlid".format(path))
                return None, (None, None)
            while True:
                cap = f.read(8)
                if len(cap) < 8:
                    break
                n = int.from_bytes(cap[:4], "big")
                tipus = cap[4:]
                if tipus == b"IEND":
                    break
                if tipus not in (b"IHDR", b"tEXt", b"iTXt"):
                    f.seek(n + 4, os.SEEK_CUR)      # salta la imatge
                    continue
                dades = f.read(n)
                if len(dades) < n:
                    break
                f.seek(4, os.SEEK_CUR)
                if tipus == b"IHDR":
                    mida = (int.from_bytes(dades[0:4], "big"), int.from_bytes(dades[4:8], "big"))
                elif b"\x00" in dades:
                    clau, text = dades.split(b"\x00", 1)
                    if tipus == b"tEXt":
                        meta[clau.decode("latin-1")] = text.decode("latin-1")
                    elif len(text) > 2 and text[0] == 0:
                        parts = text[2:].split(b"\x00", 2)      # iTXt sense comprimir
                        if len(parts) == 3:
                            meta[clau.decode("latin-1")] = parts[2].decode("utf-8", errors="ignore")
    except OSError as e:
        print("ERROR llegint {}: {}".format(path, e))
        return None, (None, None)
    return meta, mida
