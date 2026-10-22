# -*- coding: utf-8 -*-
"""
p1_main.py : ** OPTIONAL ** Si heu fet un main vostre, poseu aquí el codi.
                            Aquest arxiu no s'avalua automàticament.

Aquí podeu posar el vostre codi de proves per testejar les funcionalitats
implementades.

Exemples d'ús:
    - Carregar la col·lecció d'imatges
    - Generar UUID per a totes les imatges
    - Llegir metadades d'algunes imatges
    - Visualitzar imatges
    - Carregar i mostrar galeries
    - Fer cerques i crear galeries a partir dels resultats
"""

import os
import time

import cfg
from ImageFiles import ImageFiles
from ImageID import ImageID
from ImageData import ImageData
from ImageViewer import ImageViewer
from Gallery import Gallery
from SearchMetadata import SearchMetadata


def update_collection(files: ImageFiles, ids: ImageID, data: ImageData) -> None:
    """Sincronitza ImageID i ImageData amb els canvis del disc (Func1, Func2, Func3)."""
    files.reload_fs(cfg.get_root())

    for file in files.files_removed():
        uuid = ids.get_uuid(file)
        if uuid is not None:
            data.remove_image(uuid)
            ids.remove_uuid(uuid)

    for file in files.files_added():
        uuid = ids.generate_uuid(file)
        if uuid is not None:
            data.add_image(uuid, file)
            data.load_metadata(uuid)


def gallery_from_list(name: str, uuids: list, ids: ImageID, viewer: ImageViewer) -> Gallery:
    """Crea una galeria a partir del resultat d'una cerca (Func7)."""
    gallery = Gallery(ids, viewer)
    gallery.gallery_name = name
    for uuid in uuids:
        gallery.add_image_at_end(uuid)
    return gallery


def main():
    files = ImageFiles()
    ids = ImageID()
    data = ImageData()
    viewer = ImageViewer(data)
    search = SearchMetadata(data)
    galleries = []      # totes les galeries creades

    print("=== Func1-3: càrrega de la col·lecció [{}]".format(cfg.get_root()))
    start = time.time()
    update_collection(files, ids, data)
    print("{} arxius PNG, {} UUID, {} imatges ({:.3f}s)\n"
          .format(len(files), len(ids), len(data), time.time() - start))

    print("=== Func4: visualització d'una imatge")
    uuids = data.get_uuids()
    if uuids:
        viewer.show_image(uuids[0], cfg.DISPLAY_MODE)
    print()

    print("=== Func5: galeries JSON")
    root = cfg.get_root()
    for json_file in sorted(os.listdir(root)):
        if json_file.lower().endswith(".json"):
            gallery = Gallery(ids, viewer)
            gallery.load_file(os.path.join(root, json_file))
            galleries.append(gallery)
            print("  {} -> '{}' ({} imatges)".format(json_file, gallery.gallery_name, len(gallery)))
    if galleries:
        galleries[0].show()
    print()

    print("=== Func6: cerques")
    painting = search.prompt("painting")
    sd15 = search.model("SD1.5")
    k_lms = search.sampler("k_lms")
    year_2022 = search.date("2022")
    print("  prompt 'painting':      {}".format(len(painting)))
    print("  model 'SD1.5':          {}".format(len(sd15)))
    print("  sampler 'k_lms':        {}".format(len(k_lms)))
    print("  data '2022':            {}".format(len(year_2022)))
    print("  painting AND SD1.5:     {}".format(len(search.and_operator(painting, sd15))))
    print("  painting OR k_lms:      {}".format(len(search.or_operator(painting, k_lms))))
    print()

    print("=== Func7: galeria a partir d'una cerca")
    result = search.and_operator(painting, sd15)
    gallery = gallery_from_list("Paintings SD1.5", result, ids, viewer)
    galleries.append(gallery)
    print("  '{}': {} imatges".format(gallery.gallery_name, len(gallery)))
    gallery.remove_first_image()
    gallery.remove_last_image()
    print("  després de treure la primera i l'última: {} imatges".format(len(gallery)))
    gallery.show()
    print()

    print("=== Total de galeries creades: {}".format(len(galleries)))


if __name__ == "__main__":
    main()
