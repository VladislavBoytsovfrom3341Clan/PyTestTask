from typing import Any

class AssociativeArray:
    """
    Simple class that implements an associative array
     on a hash table with collision resolution using chaining.
     Insert, find, and delete methods are available.
     The array size is constant
     """
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(size)]

    def _hash(self, key) -> int:
        """Basic hash function"""
        return key % self.size

    def insert(self, key, value: Any):
        """Inserts a (key, value) pair into a table"""
        index = self._hash(key)
        # Check if the key is already in the chain
        for idx, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][idx] = (key, value)  # Update the value
                return
        self.table[index].append((key, value))  # Insert new (key, val)

    def remove(self, key):
        """Removes a (key, value) pair from the table if it exists"""
        index = self._hash(key)
        for idx, (k, v) in enumerate(self.table[index]):
            if k == key:    #Finding the right key
                del self.table[index][idx]
                return

    def find(self, key) -> Any:
        """Returns the value by key if the key exists, otherwise None."""
        index = self._hash(key)
        for k, v in self.table[index]:
            if k == key:
                return v
        return None
