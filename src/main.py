from src.modules.avl_tree.avl_tree import AVLTree

if __name__ == "__main__":
    a = AVLTree()
    for i in range(100):
        a.insert(i)
        print(a.check())
        #print(a.breadth_first_search())
    print(42 in a)
    for i in range(100):
        a.remove(i)
        print(a.check())

