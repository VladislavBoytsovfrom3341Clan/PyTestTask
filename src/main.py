from src.modules.associative_array.associative_array import AssociativeArray
import random

from src.modules.avl_tree.avl_tree import AVLTree
if __name__ == "__main__":
    a = AVLTree()
    for i in range(100):
        a.insert(i)
    t1, t2 = a.split(50)
    print(t1.check())
    print(t1.in_order())
    print(t1.breadth_first_search())
    print(t2.check())
    print(t2.in_order())
    print(t2.breadth_first_search())
    a= AssociativeArray(50)
    for i in range(50):
        a.insert(i, i**2)
    for i in range(50):
        assert a.find(i) == i**2
    for i in range(15, 35):
        a.remove(i)
    for i in range(50):
        if 15<=i<35:
            assert a.find(i) is None
        else:
            assert a.find(i) == i**2
