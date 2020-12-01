class HashTable(object):
    """
    A class used to represent a Hash Table-based associative array.

    ...

    Attributes
    ----------
    max_size : int
        Maximum size of the inner array
    size : int
        Current size of the inner array
    elems : int
        Current number of elements
    nonempty : int
        Current number of occupied buckets
    data : list(list)
        Inner array of arrays

    Methods
    -------
    rehash()
        Increases the size of the inner array if possible
    insert(key, value)
        Inserts a key, value pair into the hash table
    remove(key)
        Removes element from the hash table by key
    get(key)
        Returns element from the hash table by key.
        If there is no such element returns None
    """

    def __init__(self, max_size=1024):
        self.max_size = max_size
        self.elems = 0
        self.nonempty = 0
        self.size = max_size // 4
        self.data = [list() for _ in range(self.size)]


    def rehash(self):
        if self.size < self.max_size:
            self.size *= 2
            self.nonempty = 0
            self.elems = 0
            old_data = self.data
            self.data = [list() for _ in range(self.size)]
            for bucket in old_data:
                for key, value in bucket:
                    self.insert(key, value)


    def insert(self, key, value):
        bucket = self.data[key % self.size]
        for i in range(len(bucket)):
            if bucket[i][0] == key:
                bucket[i] = (key, value)
                return None
        if len(self.data[key % self.size]) == 0:
            self.nonempty += 1
        self.data[key % self.size].append((key, value))
        self.elems += 1


    def remove(self, key):
        bucket = self.data[key % self.size]
        for i in range(len(bucket)):
            if bucket[i][0] == key:
                del bucket[i]
                self.elems -= 1
                if len(bucket) == 0:
                    self.nonempty += 1
                return None

    def get(self, key):
        if self.nonempty / self.size > 0.7 and self.elems / self.size > 5:
            self.rehash()
        for element in self.data[key % self.size]:
            if element[0] == key:
                return element[1]
        return None

    def __len__(self):
        return self.elems
