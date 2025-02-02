from tabnanny import check

from src.modules.associative_array.associative_array import AssociativeArray
import random

from src.modules.avl_tree.avl_tree import AVLTree
if __name__ == "__main__":
    test = 0
    for size in range(100):
        for p in range(size):
            print(f"Running test #{test}")
            a = AVLTree()
            for i in range(size):
                a.insert(i)
            a_i = a.in_order()
            t1, t2 = a.split(p)
            assert (t1.check())
            assert (t2.check())
            assert(t1.in_order() + t2.in_order() == a_i)
            test += 1
    test = 0
    for a_i in range(1000):
        for b_i in range(0, a_i):
            print(f"Running test #{test}")
            a = AVLTree()
            for a_filler in range(0, a_i):
                a.insert(a_filler + a_i)
            l_a = a.in_order()
            b = AVLTree()
            for b_filler in range(0, b_i):
                b.insert(b_filler)
            l_b = b.in_order()
            try:
                a.merge(b)
            except:
                if len(a) == 0 or len(b) == 0:
                    print("A/B empty, OK")
                elif a.height() < b.height():
                    print("Failure if height, OK")
                elif a.min() <= b.max():
                    print("Failure in min/max, OK")
                else:
                    print("Strange thing occurred")
            else:
                assert (a.check())
                assert (l_b + l_a == a.in_order())
            test += 1

