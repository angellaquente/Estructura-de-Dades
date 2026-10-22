# -*- coding: utf-8 -*-
"""
ImageID.py : ** REQUIRED ** El vostre codi de la classe ImageID.

Aquesta classe s'encarrega de generar i gestionar identificadors únics (UUID)
per a cada imatge de la col·lecció.

Funcionalitat:
    - Generar un UUID únic a partir del path canònic d'un arxiu
    - Mantenir un registre dels UUID generats per evitar col·lisions
    - Permetre consultar i eliminar UUID

Mètodes a implementar:
    - generate_uuid(file: str) -> str
        Genera un UUID únic per a l'arxiu especificat.
        Ha de comprovar que el UUID no estigui ja en ús.
        Si hi ha col·lisió (cas extremadament improbable), retorna None i
        mostra un missatge d'error.

    - get_uuid(file: str) -> str
        Retorna el UUID associat a l'arxiu, si ja ha estat generat.
        Si no existeix, retorna None.

    - remove_uuid(uuid: str) -> None
        Elimina el UUID del registre d'identificadors actius.
        Després d'eliminar-lo, aquest UUID es podrà tornar a utilitzar.

Notes:
    - Els UUID han de seguir el format estàndard (128 bits)
    - Podeu utilitzar la funció cfg.get_uuid() com a base
    - Els UUID s'emmagatzemen com a strings
    - Un UUID només es pot generar una vegada (fins que s'elimini)
"""

import os

import cfg


def canonical_file(file: str) -> str:
    """Path canònic (relatiu a ROOT_DIR, amb '/') d'un arxiu.

    Accepta el path tal com el retorna ImageFiles (relatiu al directori de
    treball o absolut), el path que ja és relatiu a ROOT_DIR, i també un path
    relatiu a ROOT_DIR que s'ha tornat a passar per cfg.get_canonical_pathfile()
    (p.ex. "x.png" -> "../x.png"). Si no és dins ROOT_DIR, es retorna igual.
    """
    if not isinstance(file, str) or file == "":
        return file
    roots = {os.path.abspath(cfg.ROOT_DIR), os.path.realpath(cfg.ROOT_DIR)}

    # Ja és relatiu a ROOT_DIR
    if not os.path.isabs(file):
        for root in roots:
            if os.path.exists(os.path.join(root, file)):
                return os.path.normpath(file).replace(os.sep, "/")

    # Path del disc (absolut o relatiu al directori de treball) dins ROOT_DIR
    for full_path in (os.path.abspath(file), os.path.realpath(file)):
        for root in roots:
            if full_path.startswith(root + os.sep):
                return os.path.relpath(full_path, root).replace(os.sep, "/")

    # Path relatiu a ROOT_DIR canonicalitzat dues vegades
    if file.startswith(".."):
        root = os.path.abspath(cfg.ROOT_DIR)
        try:
            original = os.path.relpath(os.path.join(root, file), os.getcwd())
        except ValueError:
            return file
        if os.path.isfile(os.path.join(root, original)):
            return original.replace(os.sep, "/")
    return file


class ImageID:
    """Registre dels UUID actius i de l'arxiu al qual pertany cadascun."""

    def __init__(self):
        self._file_to_uuid = {}     # path relatiu -> UUID
        self._uuid_to_file = {}     # UUID -> path relatiu

    def generate_uuid(self, file: str) -> str:
        """Genera i registra el UUID de l'arxiu. Retorna None si ja està en ús."""
        file = canonical_file(file)
        uuid = str(cfg.get_uuid(file))
        if uuid in self._uuid_to_file:
            print("WARNING: UUID {} ja utilitzat per [{}]. L'arxiu [{}] no s'utilitzarà."
                  .format(uuid, self._uuid_to_file[uuid], file))
            return None
        self._uuid_to_file[uuid] = file
        self._file_to_uuid[file] = uuid
        return uuid

    def get_uuid(self, file: str) -> str:
        """UUID actiu de l'arxiu, o None si no s'ha generat (o s'ha esborrat)."""
        return self._file_to_uuid.get(canonical_file(file))

    def remove_uuid(self, uuid: str) -> None:
        """Allibera el UUID perquè es pugui tornar a generar."""
        file = self._uuid_to_file.pop(uuid, None)
        if file is not None and self._file_to_uuid.get(file) == uuid:
            del self._file_to_uuid[file]

    def get_file(self, uuid: str) -> str:
        """Path relatiu de l'arxiu associat al UUID, o None."""
        return self._uuid_to_file.get(uuid)

    def __len__(self) -> int:
        return len(self._uuid_to_file)

    def __contains__(self, uuid: str) -> bool:
        return uuid in self._uuid_to_file

    def __str__(self) -> str:
        return "ImageID({} UUID actius)".format(len(self._uuid_to_file))
