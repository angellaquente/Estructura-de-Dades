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

    def __init__(self, image_data=None):
        self.image_data = image_data

    def _buscar(self, getter, sub):
        if self.image_data is None or sub is None:
            return []
        sub = str(sub)
        res = []
        for uuid in self.image_data.get_uuids():
            valor = getattr(self.image_data, getter)(uuid)
            if valor is not None and str(valor).find(sub) != -1:
                res.append(uuid)
        return res

    def prompt(self, sub):
        return self._buscar("get_prompt", sub)

    def model(self, sub):
        return self._buscar("get_model", sub)

    def seed(self, sub):
        return self._buscar("get_seed", sub)

    def cfg_scale(self, sub):
        return self._buscar("get_cfg_scale", sub)

    def steps(self, sub):
        return self._buscar("get_steps", sub)

    def sampler(self, sub):
        return self._buscar("get_sampler", sub)

    def date(self, sub):
        return self._buscar("get_created_date", sub)

    def generated(self, sub):
        return self._buscar("get_generated", sub)

    def dimensions(self, sub="", *args, **kwargs):
        return self._buscar("get_dimensions", sub)

    def and_operator(self, list1, list2=None, *altres):
        conjunts = [set(l or []) for l in (list2,) + altres]
        res = []
        vistos = set()
        for uuid in list1 or []:
            if uuid not in vistos and all(uuid in c for c in conjunts):
                vistos.add(uuid)
                res.append(uuid)
        return res

    def or_operator(self, list1, list2=None, *altres):
        res = []
        vistos = set()
        for llista in (list1, list2) + altres:
            for uuid in llista or []:
                if uuid not in vistos:
                    vistos.add(uuid)
                    res.append(uuid)
        return res

    def __str__(self):
        return "SearchMetadata({})".format(self.image_data)
