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
from ImageData import path_disc


class ImageViewer:

    def __init__(self, image_data=None):
        self.image_data = image_data

    def print_image(self, uuid):
        d = self.image_data
        if d is None or uuid not in d:
            print("ERROR: Imatge {} inexistent!".format(uuid))
            return
        w, h = d.get_dimensions(uuid) or (None, None)
        print("Visualitzant [{}]".format(d.get_filename(uuid)))
        print(" Dimensions: {}x{} pixels".format(w, h))
        print(" Prompt:     {}".format(d.get_prompt(uuid)))
        print(" Model:      {}".format(d.get_model(uuid)))
        print(" Seed:       {}".format(d.get_seed(uuid)))
        print(" CFG Scale:  {}".format(d.get_cfg_scale(uuid)))
        print(" Steps:      {}".format(d.get_steps(uuid)))
        print(" Sampler:    {}".format(d.get_sampler(uuid)))
        print(" Generated:  {}".format(d.get_generated(uuid)))
        print(" Created:    {}".format(d.get_created_date(uuid)))
        print(" UUID:       {}".format(uuid))
        print(" Arxiu:      {}".format(d.get_filename(uuid)))

    def show_file(self, file):
        self._obrir(file)
    def _obrir(self, file):
        path = path_disc(file)
        if not path or not os.path.isfile(path):
            print("ERROR: Arxiu [{}] inexistent!".format(file if file is not None else ""))
            return False
        try:
            if sys.platform.startswith("win"):
                os.startfile(path)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", path])
            else:
                subprocess.Popen(["xdg-open", path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except Exception as e:
            print("No es pot mostrar la imatge: {}".format(e))
            return False

    def show_image(self, uuid, mode=None):
        if mode is None:
            mode =cfg.DISPLAY_MODE
        if mode < 2:
            self.print_image(uuid)
        if mode > 0 and self.image_data is not None:
            if self._obrir(self.image_data.get_filename(uuid)) and sys.stdin and sys.stdin.isatty():
                input("Premi Enter per continuar...")   # només a la terminal

    def __str__(self):
        return "ImageViewer(mode {})".format(cfg.DISPLAY_MODE)
