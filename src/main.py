import random

from src.modules.avl_tree.avl_tree import AVLTree

if __name__ == "__main__":
    a = AVLTree()
    for i in range(1000):
        r = random.randint(0, 10000)
        if not r in a:
            a.insert(r)
        assert a.check()
    deleted = 0
    for i in range(10000):
        r = random.randint(0, 10000)
        if r in a:
            a.remove(r)
            deleted += 1
        #a._root = a._remove_max(a._root)
        print(deleted)
        if not a.check():
            print("deleting ", r)
            print("failed at ", i, " deleted ", deleted)
            print(a.in_order())
            print(a.height())
            print(a.breadth_first_search())
            break
        print(a.in_order())
