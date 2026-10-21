class MyHashMap:
    def __init__(self, cap=13):
        self._table = cap * [None]   
        self._n = 0                  

    def _hash_function(self, key):
        return key % len(self._table)         


    def _bucket_get(self, j, key):
        bucket = self._table[j]
        if bucket is None:
            return -1
        for parella in bucket:
            if parella[0] == key:
                return parella[1]
        return -1

    def _bucket_put(self, j, key, value):
        """Retorna True si la clau és nova, False si s'ha actualitzat."""
        if self._table[j] is None:
            self._table[j] = []
        bucket = self._table[j]
        for parella in bucket:
            if parella[0] == key:
                parella[1] = value
                return False
        bucket.append([key, value])
        return True

    def _bucket_remove(self, j, key):
        """Retorna True si s'ha esborrat la clau."""
        bucket = self._table[j]
        if bucket is None:
            return False
        for i in range(len(bucket)):
            if bucket[i][0] == key:
                bucket.pop(i)
                if len(bucket) == 0:
                    self._table[j] = None
                return True
        return False

    # ---------- Mètodes públics ----------

    def put(self, key: int, value: int) -> None:
        j = self._hash_function(key)
        if self._bucket_put(j, key, value):
            self._n += 1
        if self._n > len(self._table) // 2:
            self._resize(2 * len(self._table) - 1)

    def get(self, key: int) -> int:
        j = self._hash_function(key)
        return self._bucket_get(j, key)

    def remove(self, key: int) -> None:
        j = self._hash_function(key)
        if self._bucket_remove(j, key):
            self._n -= 1

    def __len__(self):
        return self._n

    def _resize(self, c):
        old = self._table
        self._table = c * [None]
        for bucket in old:
            if bucket is not None:
                for k, v in bucket:
                    self._bucket_put(self._hash_function(k), k, v)
