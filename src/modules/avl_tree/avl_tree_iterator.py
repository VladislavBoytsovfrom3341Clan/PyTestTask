from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from src.modules.avl_tree.avl_tree import AVLTree

class AVLTreeIterator:
    """
    Iterator class for AVLTree.
    Traverses the tree in a centered traversal
    """
    def __init__(self, tree: "AVLTree"):
        self._tree = tree
        self.node: "AVLTree.Node" | None = tree._get_min(tree._root)

    def __iter__(self):
        return self

    def __next__(self):
        if self.node is None:
            raise StopIteration

        result = self.node.val
        self.node = self._tree._successor(self.node)
        return result
