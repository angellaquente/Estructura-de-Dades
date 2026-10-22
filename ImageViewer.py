# -*- coding: utf-8 -*-
"""
ImageViewer.py : ** REQUIRED ** El vostre codi de la classe ImageViewer.

Aquesta classe s'encarrega de visualitzar imatges i mostrar les seves metadades.

Funcionalitat:
    - Imprimir per pantalla les metadades d'una imatge
    - Mostrar la imatge en pantalla
    - Combinar ambdues accions segons la configuració

Mètodes a implementar:
    - print_image(uuid: str) -> None
        Imprimeix per pantalla totes les metadades de la imatge identificada
        per l'UUID. Ha de mostrar:
        - Dimensions (width x height)
        - Prompt (truncat si és molt llarg)
        - Model
        - Seed
        - CFG Scale
        - Steps
        - Sampler
        - Generated
        - Created Date
        - UUID
        - Path de l'arxiu

    - show_file(file: str) -> None
        Mostra la imatge especificada utilitzant PIL.
        Aquesta funció NO espera que la imatge es tanqui (asíncrona).

    - show_image(uuid: str, mode: int) -> None
        Combina print_image() i show_file() segons el mode especificat:
        - mode 0: només metadades
        - mode 1: metadades + imatge
        - mode 2: només imatge

        Aquesta funció ha d'esperar que l'usuari tanqui la imatge abans
        de retornar (síncrona). Podeu utilitzar input() per fer una pausa.

Notes:
    - Utilitzeu cfg.DISPLAY_MODE per determinar el comportament per defecte
    - Per mostrar imatges: img.show() de PIL
    - Gestioneu les excepcions si la imatge no es pot mostrar
    - El format de sortida ha de ser llegible i ben organitzat
"""

import os
import subprocess
import sys

import cfg
from ImageData import resolve_path


class ImageViewer:
    """Impressió de metadades i visualització de les imatges."""

    def __init__(self, image_data=None):
        self._data = image_data     # ImageData amb les metadades a memòria

    def print_image(self, uuid: str) -> None:
        """Imprimeix les metadades (ja carregades a memòria) de la imatge."""
        data = self._data
        if data is None or uuid not in data:
            print("ERROR: Imatge {} inexistent!".format(uuid))
            return

        width, height = data.get_dimensions(uuid) or (None, None)
        print("Visualitzant [{}]".format(data.get_filename(uuid)))
        print(" Dimensions: {}x{} pixels".format(width, height))
        print(" Prompt:     {}".format(data.get_prompt(uuid)))
        print(" Model:      {}".format(data.get_model(uuid)))
        print(" Seed:       {}".format(data.get_seed(uuid)))
        print(" CFG Scale:  {}".format(data.get_cfg_scale(uuid)))
        print(" Steps:      {}".format(data.get_steps(uuid)))
        print(" Sampler:    {}".format(data.get_sampler(uuid)))
        print(" Generated:  {}".format(data.get_generated(uuid)))
        print(" Created:    {}".format(data.get_created_date(uuid)))
        print(" UUID:       {}".format(uuid))
        print(" Arxiu:      {}".format(data.get_filename(uuid)))

    def show_file(self, file: str) -> None:
        """Obre la imatge amb un visualitzador sense esperar que es tanqui."""
        self._open_file(file)

    @staticmethod
    def _open_file(file: str) -> bool:
        """Obre la imatge; retorna True si s'ha pogut obrir."""
        if not isinstance(file, str) or file == "":
            print("ERROR: Arxiu [{}] inexistent!".format(file if file is not None else ""))
            return False
        path = resolve_path(file)
        if not os.path.isfile(path):
            print("ERROR: Arxiu [{}] inexistent!".format(file))
            return False

        try:
            from PIL import Image       # opcional: no disponible a Gradescope
            Image.open(path).show()
            return True
        except ImportError:
            pass
        except Exception as e:
            print("No es pot mostrar la imatge: {}".format(e))
            return False

        # Sense PIL: visualitzador per defecte del sistema operatiu
        try:
            if sys.platform.startswith("win"):
                os.startfile(path)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", path])
            else:
                subprocess.Popen(["xdg-open", path],
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except Exception as e:
            print("No es pot mostrar la imatge: {}".format(e))
            return False

    def show_image(self, uuid: str, mode: int = None) -> None:
        """Metadades i/o imatge segons el mode (0, 1 o 2; per defecte cfg.DISPLAY_MODE)."""
        if mode is None:
            mode = cfg.DISPLAY_MODE

        if mode < 2:
            self.print_image(uuid)

        if mode > 0:
            file = self._data.get_filename(uuid) if self._data is not None else None
            if self._open_file(file):
                self._wait_user()

    def __str__(self) -> str:
        return "ImageViewer(mode per defecte {}, {})".format(cfg.DISPLAY_MODE, self._data)

    @staticmethod
    def _wait_user() -> None:
        """Pausa fins que l'usuari premi Enter (només en una terminal interactiva)."""
        try:
            if sys.stdin is not None and sys.stdin.isatty():
                input("Premi Enter per continuar...")
        except Exception:
            pass
