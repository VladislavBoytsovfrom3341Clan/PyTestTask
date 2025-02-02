from tabnanny import check

from src.modules.associative_array.associative_array import AssociativeArray
import random

from src.modules.avl_tree.avl_tree import AVLTree
if __name__ == "__main__":
    for size in range(100):
        for p in range(size):
            a = AVLTree()
            for i in range(size):
                a.insert(i)
            a_i = a.in_order()
            t1, t2 = a.split(p)
            assert (t1.check())
            assert (t2.check())
            assert(t1.in_order() + t2.in_order() == a_i)
            print(len(t1.in_order()), len(t1))



