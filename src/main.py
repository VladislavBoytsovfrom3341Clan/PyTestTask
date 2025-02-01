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


