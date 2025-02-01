from tabnanny import check

from src.modules.avl_tree.avl_tree import AVLTree

if __name__ == "__main__":
    a = AVLTree()
    b = AVLTree()
    for i in range(100):
        a.insert(i+1000)
    for i in range(100):
        b.insert(i)
    print(a.check())
    print(b.height())
    print(a.height())
    print(b.breadth_first_search())
    print(a.breadth_first_search())
    a.merge(b)
    print(a.check())
    print(a.in_order())
    print(a.breadth_first_search())

