from src.modules.avl_tree.avl_tree import AVLTree

if __name__ == "__main__":
    a = AVLTree()
    for i in range(100):
        a.insert(i)
        #print(a.check())
        #print(a.in_order())
    for it in a:
        print(it)
    for i in range(100):
        a.remove(i)
        #print(a.check())
        #print(a.in_order())
    print('hehe')
    for it in a:
        print(it)
