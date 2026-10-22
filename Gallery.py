# -*- coding: utf-8 -*-
"""
Gallery.py : ** REQUIRED ** El vostre codi de la classe Gallery.

Aquesta classe s'encarrega de gestionar galeries d'imatges en format JSON.

Funcionalitat:
    - Llegir galeries des d'arxius JSON
    - Visualitzar totes les imatges d'una galeria
    - Afegir i eliminar imatges de la galeria

Format JSON d'una galeria:
{
  "gallery_name": "Cyberpunk Cities",
  "description": "Collection of futuristic urban landscapes",
  "created_date": "2025-09-30",
  "images": [
    "generated_images/city_001.png",
    "generated_images/city_neon_12.png",
    "generated_images/urban_street_45.png"
  ]
}

Mètodes a implementar:
    - load_file(file: str) -> None
        Llegeix un arxiu JSON amb la definició de la galeria.
        Ha de validar que cada imatge referenciada existeix a la col·lecció.
        Si una imatge no existeix, l'ignora i continua processant.
        Emmagatzema internament els UUID de les imatges vàlides.

    - show() -> None
        Visualitza totes les imatges de la galeria en ordre utilitzant
        ImageViewer.show_image().

    - add_image_at_end(uuid: str) -> None
        Afegeix una imatge al final de la galeria.

    - remove_first_image() -> None
        Elimina la primera imatge de la galeria.

    - remove_last_image() -> None
        Elimina l'última imatge de la galeria.

Notes:
    - Utilitzeu la llibreria json per llegir els arxius
    - Els paths dins el JSON són relatius a ROOT_DIR
    - Cada galeria és un objecte independent (instància de Gallery)
    - Podeu tenir múltiples galeries actives simultàniament
    - Les operacions d'afegir/eliminar són ràpides (no busquen a la llista)
"""

import json
import os

import cfg


class Gallery:
    """Llista ordenada d'imatges (UUID) amb el nom, descripció i data de la galeria."""

    def __init__(self, image_id=None, image_viewer=None):
        # Acceptem els dos objectes en qualsevol ordre
        if hasattr(image_id, "show_image") and not hasattr(image_id, "get_uuid"):
            image_id, image_viewer = image_viewer, image_id
        self._ids = image_id            # ImageID: path relatiu -> UUID
        self._viewer = image_viewer     # ImageViewer: visualització
        self.gallery_name = ""
        self.description = ""
        self.created_date = ""
        self.images = []                # UUID de les imatges, en ordre

    @property
    def name(self) -> str:
        return self.gallery_name

    def load_file(self, file: str) -> None:
        """Carrega la galeria d'un JSON. Les imatges fora de la col·lecció s'ignoren.

        El contingut anterior es descarta: si el JSON no es pot llegir, la
        galeria queda buida.
        """
        self.gallery_name = ""
        self.description = ""
        self.created_date = ""
        self.images = []

        path = file
        if isinstance(file, str) and not os.path.isfile(path) and not os.path.isabs(file):
            path = os.path.join(cfg.get_root(), file)

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, TypeError, ValueError) as e:
            print("ERROR: No es pot llegir la galeria [{}]: {}".format(file, e))
            return
        if not isinstance(data, dict) or not isinstance(data.get("images", []), list):
            print("ERROR: Format de galeria incorrecte [{}]".format(file))
            return

        self.gallery_name = str(data.get("gallery_name", ""))
        self.description = str(data.get("description", ""))
        self.created_date = str(data.get("created_date", ""))
        for image_file in data.get("images", []):
            uuid = self._find_uuid(image_file)
            if uuid is None:
                print("WARNING: La imatge [{}] no és a la col·lecció. S'ignora."
                      .format(image_file))
                continue
            self.images.append(uuid)

    def _find_uuid(self, image_file) -> str:
        """UUID d'un path del JSON, acceptant diferents formats del path."""
        if self._ids is None or not isinstance(image_file, str):
            return None
        candidates = [image_file, os.path.normpath(image_file).replace(os.sep, "/")]
        try:
            candidates.append(cfg.get_canonical_pathfile(image_file))
        except ValueError:
            pass
        for candidate in candidates:
            uuid = self._ids.get_uuid(candidate)
            if uuid is not None:
                return uuid
        return None

    def show(self) -> None:
        """Visualitza en ordre totes les imatges de la galeria."""
        if self._viewer is None:
            print("ERROR: Galeria sense visualitzador!")
            return
        print("Galeria [{}]: {} imatges".format(self.gallery_name, len(self.images)))
        for uuid in list(self.images):
            self._viewer.show_image(uuid, cfg.DISPLAY_MODE)

    def add_image_at_end(self, uuid: str) -> None:
        if uuid is not None:
            self.images.append(uuid)

    def remove_first_image(self) -> str:
        """Treu i retorna el UUID de la primera imatge (None si és buida)."""
        if self.images:
            return self.images.pop(0)
        return None

    def remove_last_image(self) -> str:
        """Treu i retorna el UUID de l'última imatge (None si és buida)."""
        if self.images:
            return self.images.pop()
        return None

    def __len__(self) -> int:
        return len(self.images)

    def __iter__(self):
        return iter(list(self.images))

    def __str__(self) -> str:
        return "Gallery('{}', {} imatges)".format(self.gallery_name, len(self.images))
