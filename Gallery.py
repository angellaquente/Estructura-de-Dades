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

    def __init__(self, image_id=None, image_viewer=None, gallery_name=""):
        self.image_id = image_id
        self.image_viewer = image_viewer
        self.gallery_name = gallery_name if isinstance(gallery_name, str) else ""
        self.description = ""
        self.created_date = ""
        self.images = []        # uuids en ordre

    @property
    def name(self):
        return self.gallery_name

    @name.setter
    def name(self, value):
        self.gallery_name = "" if value is None else str(value)

    def load_file(self, file):
        self.gallery_name = ""
        self.description = ""
        self.created_date = ""
        self.images = []

        path = file
        if isinstance(file, str) and not os.path.isfile(file) and not os.path.isabs(file):
            path = os.path.join(cfg.get_root(), file)
        if isinstance(path, str) and path != "" and not os.path.exists(path):
            print("ERROR: Galeria [{}] inexistent!".format(file))
            raise FileNotFoundError(path)
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
        for img in data.get("images", []):
            uuid = None
            if self.image_id is not None and isinstance(img, str):
                uuid = self.image_id.get_uuid(img)
            if uuid is None:
                print("WARNING: La imatge [{}] no és a la col·lecció. S'ignora.".format(img))
            else:
                self.images.append(uuid)

    def show(self):
        if self.image_viewer is None:
            print("ERROR: Galeria sense visualitzador!")
            return
        print("Galeria [{}]: {} imatges".format(self.gallery_name, len(self.images)))
        for uuid in list(self.images):
            self.image_viewer.show_image(uuid, cfg.DISPLAY_MODE)

    def add_image_at_end(self, uuid):
        if uuid is not None:
            self.images.append(uuid)

    def remove_first_image(self):
        if self.images:
            self.images.pop(0)

    def remove_last_image(self):
        if self.images:
            self.images.pop()

    def __len__(self):
        return len(self.images)

    def __iter__(self):
        return iter(list(self.images))

    def __str__(self):
        return "Gallery('{}', {} imatges)".format(self.gallery_name, len(self.images))
