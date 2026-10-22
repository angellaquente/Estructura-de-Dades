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
    """Representació a memòria dels arxius PNG presents al disc."""

    def __init__(self):
        self._files = set()     # paths relatius de la darrera lectura del disc
        self._added = []        # arxius nous respecte la lectura anterior
        self._removed = []      # arxius desapareguts respecte la lectura anterior

    def reload_fs(self, path: str = None) -> None:
        """Torna a llegir el disc a partir de 'path' i calcula els canvis."""
        if path is None:
            path = cfg.get_root()

        found = []
        for root, dirs, files in os.walk(path):
            dirs.sort()                     # recorregut determinista
            for filename in sorted(files):
                if filename.lower().endswith('.png'):
                    full_path = os.path.join(root, filename)
                    found.append(cfg.get_canonical_pathfile(full_path))

        found_set = set(found)
        self._added = [file for file in found if file not in self._files]
        self._removed = sorted(self._files - found_set)
        self._files = found_set

    def files_added(self) -> list:
        """Arxius afegits des de la darrera crida a reload_fs()."""
        return list(self._added)

    def files_removed(self) -> list:
        """Arxius eliminats des de la darrera crida a reload_fs()."""
        return list(self._removed)

    def get_files(self) -> list:
        """Tots els arxius presents a la darrera lectura del disc."""
        return sorted(self._files)

    def __len__(self) -> int:
        return len(self._files)
