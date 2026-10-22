# -*- coding: utf-8 -*-
"""
SearchMetadata.py : ** REQUIRED ** El vostre codi de la classe SearchMetadata.

Aquesta classe s'encarrega de cercar imatges segons criteris basats en metadades.

Funcionalitat:
    - Cercar imatges que continguin una subcadena en les seves metadades
    - Combinar resultats de cerques amb operadors lògics (AND, OR)

Mètodes a implementar:
    - prompt(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Prompt.

    - model(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Model.

    - seed(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Seed.

    - cfg_scale(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp CFG_Scale.

    - steps(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Steps.

    - sampler(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Sampler.

    - date(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Created_Date.

    - and_operator(list1: list, list2: list) -> list
        Retorna una llista amb els UUID que apareixen en AMBDUES llistes.
        (Intersecció de conjunts)

    - or_operator(list1: list, list2: list) -> list
        Retorna una llista amb els UUID que apareixen en QUALSEVOL de
        les dues llistes, sense duplicats.
        (Unió de conjunts)

Notes:
    - Les cerques són case-sensitive (distingeixen majúscules/minúscules)
    - Utilitzeu str.find() per cercar subcadenes
    - Les llistes retornades poden estar buides
    - Els operadors lògics NO modifiquen les llistes originals
    - Aquests mètodes NO retornen objectes Gallery, sinó llistes simples
"""


class SearchMetadata:
    """Cerques de subcadenes dins les metadades d'un ImageData."""

    def __init__(self, image_data=None):
        self._data = image_data     # ImageData on es fan les cerques

    def _search(self, field: str, sub) -> list:
        """UUID de les imatges amb 'sub' dins el camp (case-sensitive)."""
        if self._data is None or sub is None:
            return []
        sub = str(sub)
        getter = getattr(self._data, field)
        return [uuid for uuid in self._data.get_uuids()
                if getter(uuid).find(sub) != -1]

    def prompt(self, sub: str) -> list:
        return self._search("get_prompt", sub)

    def model(self, sub: str) -> list:
        return self._search("get_model", sub)

    def seed(self, sub: str) -> list:
        return self._search("get_seed", sub)

    def cfg_scale(self, sub: str) -> list:
        return self._search("get_cfg_scale", sub)

    def steps(self, sub: str) -> list:
        return self._search("get_steps", sub)

    def sampler(self, sub: str) -> list:
        return self._search("get_sampler", sub)

    def date(self, sub: str) -> list:
        return self._search("get_created_date", sub)

    def and_operator(self, list1: list, list2: list) -> list:
        """Intersecció sense duplicats, en l'ordre de list1."""
        in_list2 = set(list2)
        result = []
        seen = set()
        for uuid in list1:
            if uuid in in_list2 and uuid not in seen:
                seen.add(uuid)
                result.append(uuid)
        return result

    def or_operator(self, list1: list, list2: list) -> list:
        """Unió sense duplicats: primer list1 i després la resta de list2."""
        result = []
        seen = set()
        for uuid in list(list1) + list(list2):
            if uuid not in seen:
                seen.add(uuid)
                result.append(uuid)
        return result
