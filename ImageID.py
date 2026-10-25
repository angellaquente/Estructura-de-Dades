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


def path_relatiu(file):
    """Path relatiu a ROOT_DIR."""
    if not isinstance(file, str) or file == "":
        return file
    root = os.path.abspath(cfg.ROOT_DIR)
    if not os.path.isabs(file) and os.path.exists(os.path.join(root, file)):
        return os.path.normpath(file).replace(os.sep, "/")
    ple = os.path.abspath(file)
    if ple.startswith(root + os.sep):
        return os.path.relpath(ple, root).replace(os.sep, "/")
    return file


class ImageID:

    def __init__(self):
        self._file_to_uuid = {}
        self._uuid_to_file = {}

    def generate_uuid(self, file):
        file = path_relatiu(file)
        uuid = str(cfg.get_uuid(file))
        if uuid in self._uuid_to_file:
            print("WARNING: UUID {} ja utilitzat per [{}]. L'arxiu [{}] no s'utilitzarà."
                  .format(uuid, self._uuid_to_file[uuid], file))
            return None
        self._uuid_to_file[uuid] = file
        self._file_to_uuid[file]= uuid
        return uuid

    def get_uuid(self, file):
        return self._file_to_uuid.get(path_relatiu(file))
    def remove_uuid(self, uuid):
        file = self._uuid_to_file.pop(uuid, None)
        if file is not None:
            self._file_to_uuid.pop(file, None)

    
    def __len__(self):
        return len(self._uuid_to_file)

    def __contains__(self, uuid):
        return uuid in self._uuid_to_file

    def __str__(self):
        return "ImageID({} UUID)".format(len(self._uuid_to_file))
