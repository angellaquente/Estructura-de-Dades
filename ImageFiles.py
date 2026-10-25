# -*- coding: utf-8 -*-
"""
ImageFiles.py : ** REQUIRED ** El vostre codi de la classe ImageFiles.

Aquesta classe s'encarrega de gestionar el llistat d'arxius PNG dins la col·lecció d'imatges.

Funcionalitat:
    - Recórrer el filesystem a partir de ROOT_DIR per trobar tots els arxius PNG
    - Mantenir una representació en memòria dels arxius presents
    - Detectar quins arxius s'han afegit o eliminat des de l'última lectura

Mètodes a implementar:
    - reload_fs(path: str) -> None
        Recorre el directori especificat i actualitza la llista d'arxius PNG.
        Detecta els arxius nous i els que s'han eliminat.

    - files_added() -> list
        Retorna una llista (de strings) amb els paths relatius dels arxius
        que s'han afegit des de l'última crida a reload_fs().

    - files_removed() -> list
        Retorna una llista (de strings) amb els paths relatius dels arxius
        que s'han eliminat des de l'última crida a reload_fs().

Notes:
    - Els paths han de ser sempre relatius a ROOT_DIR
    - Només considereu arxius amb extensió .png (case-insensitive)
    - Heu de recórrer tots els subdirectoris recursivament
"""

import os

import cfg


class ImageFiles:

    def __init__(self):
        self.fitxers = {}       # relatiu ->path al disc
        self.afegits= []
        self.eliminats = []

    
    def reload_fs(self, path=None):
        if path is None:
            path = cfg.ROOT_DIR
        trobats = {}
        for carpeta, dirs, noms in os.walk(path):
            dirs.sort()
            for nom in sorted(noms):
                if nom.lower().endswith(".png"):
                    f = os.path.join(carpeta, nom)
                    trobats[cfg.get_canonical_pathfile(f)] = f
        self.afegits = [f for k, f in trobats.items() if k not in self.fitxers]
        self.eliminats = [f for k, f in self.fitxers.items() if k not in trobats]
        self.fitxers = trobats

    def files_added(self):
        return list(self.afegits)
    def files_removed(self):
        return list(self.eliminats)

    def __len__(self):
        return len(self.fitxers)

    def __str__(self):
        return "ImageFiles({} arxius)".format(len(self.fitxers))
