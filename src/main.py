from tabnanny import check

from src.modules.avl_tree.avl_tree import AVLTree

if __name__ == "__main__":
    a = AVLTree()
    b = AVLTree()
    for i in range(10):
        a.insert(i+11)
    for i in range(10):
        b.insert(i)
    print(a.check())
    print(b.breadth_first_search())
    print(a.breadth_first_search())
    a.merge(b)
    print(a.check())
    print(a.in_order())
    print(a.breadth_first_search())

