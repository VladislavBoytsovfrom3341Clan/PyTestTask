from src.modules.avl_tree.avl_tree import AVLTree

if __name__ == "__main__":
    a = AVLTree()
    for i in range(100):
        print(i)
        a.insert(i)
        print(len(a))
        #print(a.breadth_first_search())
    print(420 in a)
    for i in range(100):
        a.remove(i)
        print(len(a))
        print(a.breadth_first_search())
