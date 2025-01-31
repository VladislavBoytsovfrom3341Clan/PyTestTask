from typing import Any
from collections import deque

class AVLTree:
    """
    Self-balancing binary search tree.
    Supports insertion and search operations
    """
    class Node:
        def __init__(self, val: Any):
            self.val: Any = val
            self.left: AVLTree.Node | None = None
            self.right: AVLTree.Node | None = None
            self.height: int = 1


    def __init__(self):
        self._root: AVLTree.Node | None = None
        self.size = 0

    def __len__(self):
        return self.size

    @staticmethod
    def _height(root: Node | None) -> int:
        """Returns the height of a node, handling None as 0."""
        return 0 if root is None else root.height

    def _balance_factor(self, root: None | Node) -> int:
        """Returns the difference in heights of the left and right subtrees"""
        if root is None:
            return 0
        else:
            return self._height(root.left) - self._height(root.right)

    def _fix_height(self, root: None | Node) -> None:
        """
        Considering the heights of the left and right subtrees to be correct,
        sets the height value of root
        """
        if root is not None:
            root.height = max(self._height(root.left), self._height(root.right)) + 1

    def _left_rotate(self, node: None | Node) -> None | Node:
        """Performs a left rotation, making the right child the new root."""
        if node is None:
            return node
        temp: None | AVLTree.Node = node.right
        node.right = temp.left
        temp.left = node
        self._fix_height(node)
        self._fix_height(temp)
        return temp

    def _right_rotate(self, node: None | Node) -> None | Node:
        """Performs a right rotation, making the left child the new root."""
        if node is None:
            return node
        temp: None | AVLTree.Node = node.left
        node.left = temp.right
        temp.right = node
        self._fix_height(node)
        self._fix_height(temp)
        return temp

    def _balance(self, node: None|Node) -> None | Node:
        """Balances a node if its subtrees no longer satisfy the AVL properties"""
        self._fix_height(node)
        if self._balance_factor(node) <= -2:    #checks for left rotation
            if self._balance_factor(node.right) > 0:
                node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        if self._balance_factor(node) >= 2:     #checks for right rotation
            if self._balance_factor(node.left) < 0:
                node.left = self._left_rotate(node.left)
            return self._right_rotate(node)

        return node

    def _get_min(self, node: None | Node) -> None | Node:
        """Returns node with minimal value in all subtree recursively"""
        if node is None or node.left is None:
            return node
        return self._get_min(node.left)

    def _get_max(self, node: None | Node) -> None | Node:
        """Returns node with maximal value in all subtree recursively"""
        if node is None or node.right is None:
            return node
        return self._get_max(node.right)

    def _insert(self, node: None | Node, val: Any) -> None | Node:
        """
        Inserts val in subtree with root node recursively.
        Uses binary search.
        Returns root of subtree after an insertion and balancing
        """
        if node is None:
            return AVLTree.Node(val)
        if val < node.val:
            node.left = self._insert(node.left, val)
        else:
            node.right = self._insert(node.right, val)
        return self._balance(node)

    def insert(self, val: Any):
        """Inserts a val into the tree"""
        self._root = self._insert(self._root, val)
        self.size += 1

    def _find(self, node: None | Node, val: Any) -> None | Node:
        """
        Finds a val into the subtree with root node.
        Returns node if found, otherwise None
        """
        if node is None or node.val == val:
            return node
        if val < node.val:
            return self._find(node.left, val)
        return self._find(node.right, val)

    def __contains__(self, val: Any) -> bool:
        return self._find(self._root, val) is not None

    def get(self, val: Any) -> Any | None:
        """
        Returns val stored into the tree if val exists,
        otherwise None
        """
        node = self._find(self._root, val)
        return node.val if node else None

    def _in_order(self, node: None | Node, result: list) -> None:
        if node is not None:
            self._in_order(node.left, result)
            result.append(node.val)
            self._in_order(node.right, result)

    def in_order(self) -> list:
        """Implements a recursive centered tree traversal"""
        result = []
        self._in_order(self._root, result)
        return result

    def breadth_first_search(self) -> list[list[Any | None]]:
        """
        Implements iterative Breadth-first search based on deque
        Returns list of lists storing tree node values (including first met None)
        layer by layer
        """
        if self._root is None:
            return [[None]]
        search_queue = deque([self._root])
        ret_list = [[self._root.val]]
        counted_children = 1    #children found for each layer

        def handle_child(node): #checks child and appends it to deque and its value to ret_list
            counted = 0
            if node is None:
                ret_list[-1].append(None)
            else:
                search_queue.append(node)
                ret_list[-1].append(node.val)
                counted = 1
            return counted

        while len(search_queue) > 0:
            num_of_new_children = 0
            ret_list.append([])
            while counted_children>0:   #checks every child from previous layer
                if  search_queue[0] is None:
                    ret_list[-1].append([None, None])
                else:
                    num_of_new_children+=handle_child(search_queue[0].left) + handle_child(search_queue[0].right)
                    search_queue.popleft()  #current node is handled
                    counted_children-=1
            counted_children += num_of_new_children

        return ret_list




