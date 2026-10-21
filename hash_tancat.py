# Estats d'una posició de la taula (hash tancat). NO canvieu aquests valors.
LLIURE = "L"
OCUPAT = "O"
ESBORRAT = "B"


class MyHashMap:

    def __init__(self, cap=13):
        self._table = [[None, None, LLIURE] for _ in range(cap)]   # m posicions, inicialment buides
        self._n = 0                  # nombre de claus desades
    def _hash_function(self, key):
        return key % len(self._table)          # h(x) = x % m


    def _find(self, key):
        M = len(self._table)
        j = self._hash_function(key)
        for i in range(M):
            p = (j + i) % M
            casella = self._table[p]
            if casella[2] == LLIURE:
                return None
            if casella[2] == OCUPAT and casella[0] == key:
                return p
        return None


    def put(self, key: int, value: int) -> None:
        M = len(self._table)
        j = self._hash_function(key)
        primer_forat = None
        for i in range(M):
            p = (j + i) % M
            casella = self._table[p]
            if casella[2] == OCUPAT:
                if casella[0] == key:
                    casella[1] = value
                    return
            elif casella[2] == ESBORRAT:
                if primer_forat is None:
                    primer_forat = p
            else:
                if primer_forat is None:
                    primer_forat = p
                break
        self._table[primer_forat] = [key, value, OCUPAT]
        self._n += 1
        if self._n > len(self._table) //2:
            self._resize(2 * len(self._table) - 1)

    def get(self, key: int) -> int:
        p = self._find(key)
        if p is None:
            return -1
        return self._table[p][1]

    def remove(self, key: int) -> None:
        p = self._find(key)
        if p is not None:
            self._table[p] =[None, None, ESBORRAT]
            self._n -= 1

    def __len__(self):
        return self._n

    def _resize(self, c):
        old = self._table
        self._table = [[None, None, LLIURE] for _ in range(c)]
        for casella in old:
            if casella[2] == OCUPAT:
                k, v = casella[0], casella[1]
                p = self._hash_function(k)
                while self._table[p][2] != LLIURE:
                    p = (p + 1) % c
                self._table[p]=[k, v, OCUPAT]