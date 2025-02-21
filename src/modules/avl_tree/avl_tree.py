from typing import Any
from collections import deque

from src.modules.avl_tree.avl_tree_iterator import AVLTreeIterator

class AVLTree:
    """
    Self-balancing binary search tree.
    Supports insertion, search and remove operations,
    as well as merge and split.
    """
    class Node:
        def __init__(self, val: Any):
            self.val: Any = val
            self.left: AVLTree.Node | None = None
            self.right: AVLTree.Node | None = None
            self.parent: AVLTree.Node | None = None
            self.height: int = 1
            self.subtree_size: int = 1


    def __init__(self):
        self._root: AVLTree.Node | None = None

    def __len__(self):
        return self._size(self._root)

    def __iter__(self):
        return AVLTreeIterator(self)

    @staticmethod
    def _height(root: Node | None) -> int:
        """Returns the height of a node, handling None as 0."""
        return 0 if root is None else root.height

    @staticmethod
    def _size(root: Node | None) -> int:
        """Returns number of elements in subtree with root root"""
        return 0 if root is None else root.subtree_size

    def height(self):
        return self._height(self._root)

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

    def _fix_size(self, root: Node | None) -> None:
        """
        Considering the sizes of the left and right subtrees to be correct,
        sets the size value of root
        """
        if root is not None:
            root.subtree_size = self._size(root.left) + self._size(root.right) + 1

    def _left_rotate(self, node: None | Node) -> None | Node:
        """Performs a left rotation, making the right child the new root."""
        if node is None:
            return node
        temp: None | AVLTree.Node = node.right
        node.right = temp.left
        if node.right is not None:
            node.right.parent = node
        temp.left = node
        temp.parent = node.parent
        if node.parent is not None:
            if node == node.parent.left:
                node.parent.left = temp
            else:
                node.parent.right = temp
        node.parent = temp
        self._fix_height(node)
        self._fix_height(temp)
        self._fix_size(node)
        self._fix_size(temp)
        return temp

    def _right_rotate(self, node: None | Node) -> None | Node:
        """Performs a right rotation, making the left child the new root."""
        if node is None:
            return node
        temp: None | AVLTree.Node = node.left
        node.left = temp.right
        if node.left is not None:
            node.left.parent = node
        temp.right = node
        temp.parent = node.parent
        if node.parent is not None:
            if node == node.parent.left:
                node.parent.left = temp
            else:
                node.parent.right = temp
        node.parent = temp
        self._fix_height(node)
        self._fix_height(temp)
        self._fix_size(node)
        self._fix_size(temp)
        return temp

    def _balance(self, node: None|Node) -> None | Node:
        """Balances a node if its subtrees no longer satisfy the AVL properties"""
        self._fix_height(node)
        self._fix_size(node)
        if self._balance_factor(node) <= -2:    #checks for left rotation
            if self._balance_factor(node.right) > 0:
                node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        if self._balance_factor(node) >= 2:     #checks for right rotation
            if self._balance_factor(node.left) < 0:
                node.left = self._left_rotate(node.left)
            return self._right_rotate(node)

        return node

    def _balance_up(self, node) -> "AVLTree.Node":
        """Balances subtree from node to its root"""
        while node.parent is not None:
            node = self._balance(node)
            node = node.parent
        return self._balance(node)

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

    def min(self) -> Any:
        """Returns minimal value in the tree"""
        temp = self._get_min(self._root)
        if temp is None:
            raise RuntimeError("Tree is empty")
        return temp.val

    def max(self) -> Any:
        """Returns maximal value in the tree"""
        temp = self._get_max(self._root)
        if temp is None:
            raise RuntimeError("Tree is empty")
        return temp.val

    def _insert(self, node: None | Node, val: Any) -> Node:
        """
        Inserts val in subtree with root node recursively.
        Uses binary search.
        Returns root of subtree after an insertion and balancing
        """
        if node is None:
            return AVLTree.Node(val)
        if val < node.val:
            node.left = self._insert(node.left, val)
            node.left.parent = node
        else:
            node.right = self._insert(node.right, val)
            node.right.parent = node
        return self._balance(node)

    def insert(self, val: Any):
        """Inserts a val into the tree"""
        self._root = self._insert(self._root, val)

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

    def _remove_min(self, root: Node | None)-> Node | None:
        """
        Removes node with minimal val in the root subtree recursively.
        Balances tree and returns its root
        """
        if root is None:
            return root
        if root.left is None:
            if root.right is not None:
                root.right.parent = root.parent
            else:
                root.parent = None
            return root.right
        root.left = self._remove_min(root.left)
        if root.left is not None:
            root.left.parent = root
        return self._balance(root)

    def _remove_max(self, root: Node | None) -> Node | None:
        """
        Removes node with maximal val in the root subtree recursively.
        Balances tree and returns its root
        """
        if root is None:
            return root
        if root.right is None:
            if root.left is not None:
                root.left.parent = root.parent
            else:
                root.parent = None
            return root.left
        root.right = self._remove_max(root.right)
        if root.right is not None:
            root.right.parent = root
        return self._balance(root)

    def _remove(self, node: Node | None, val: Any) -> Node | None:
        """
        Removes val from subtree node if has one.
        Performs binary search to gwt to the val.
        Returns balanced root of subtree
        """
        if node is None:
            return node
        if val < node.val:
            node.left = self._remove(node.left, val)
            if node.left is not None:
                node.left.parent = node
        elif val > node.val:
            node.right = self._remove(node.right, val)
            if node.right is not None:
                node.right.parent = node
        else:   #val found
            left = node.left
            right = node.right
            if right is None:
                if left is not None:
                    left.parent = node.parent
                return left

            #replacing node with min_node
            min_node = self._get_min(right)
            min_node.right = self._remove_min(right)
            if min_node.right is not None:
                min_node.right.parent = min_node
            min_node.left = left
            if min_node.left is not None:
                min_node.left.parent = min_node
            min_node.parent = node.parent
            return self._balance(min_node)
        return self._balance(node)

    def remove(self, val: Any) -> None:
        """Removes val from tree if has one, otherwise does nothing"""
        if self._root is None:
            raise RuntimeError("Tree is empty")
        if val in self:
            self._root = self._remove(self._root, val)


    def _check_subtree(self, root: Node | None) -> int:
        """Self-checks tree for AVL properties.
        Ignores Node.height, calculates real height by nodes
        Returns -1 if check has failed or height of the tree if it is correct
        """
        if root is None:
            return 0

        #recursively gets heights of subtrees
        left_height = self._check_subtree(root.left)
        right_height = self._check_subtree(root.right)

        #checks BST properties
        is_bst = (
                (root.left is None or root.left.val <= root.val) and
                (root.right is None or root.right.val >= root.val)
        )

        #checks connections between nodes
        parentness = (
                (root.left is None or root.left.parent == root) and
                (root.right is None or root.right.parent == root)
        )

        # If AVL balance is violated, BST properties are violated, or a subtree is invalid, return -1
        if abs(left_height - right_height) > 1 or not is_bst or left_height == -1 or right_height == -1 or not parentness:
            return -1
        return max(left_height, right_height) + 1

    def check(self):
        return self._check_subtree(self._root) != -1

    def _successor(self, node: Node) -> Node | None:
        """
        Finds the in-order successor of a given node.
        Returns the next node in in-order traversal, or None if no successor exists.
        """
        if node.right is not None:
            return self._get_min(node.right)
        temp: AVLTree.Node | None = node.parent

        #finds a successor such that node is a left child
        while temp is not None and temp.right == node:
            node = temp
            temp = temp.parent
        return temp

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

    def _merge(self, bigger_root: "AVLTree.Node", smaller_root: "AVLTree.Node") -> "AVLTree.Node":
        """
        Merges smaller_root tree into bigger_root tree.
        """
        # gets max element from tree as root for a temp tree
        temp_tree_root = self._get_max(smaller_root)
        smaller_root = self._remove_max(smaller_root)

        # finds a node from self to place the tree after
        insert_after_node = bigger_root
        while insert_after_node.left and self._height(insert_after_node) > self._height(smaller_root):
            insert_after_node = insert_after_node.left

        # places originally tree
        temp_tree_root.left = smaller_root
        if smaller_root:
            smaller_root.parent = temp_tree_root

        # inserts temp tree between found node and an old tree
        temp_tree_root.right = insert_after_node.left
        if insert_after_node.left:
            insert_after_node.left.parent = temp_tree_root

        insert_after_node.left = temp_tree_root
        temp_tree_root.parent = insert_after_node

        # balancing
        return self._balance_up(temp_tree_root)

    def merge(self, tree: "AVLTree"):
        """
        Merges two trees - self and tree - into self if
        self.min() > tree.max() and self.height() >= tree.height()
        """
        if self._root is None:
            raise RuntimeError("Empty tree")
        if tree._root is None:
            return
        if self.min() <= tree.max() or self.height()< tree.height():
            raise RuntimeError("Impossible to merge trees")

        self._root = self._merge(self._root, tree._root)


    def naive_split(self, key):
        """Naive implementation of splitting a tree into two. Need to replace"""
        t1 = AVLTree()
        t2 = AVLTree()
        traversed = self.in_order()
        for i in traversed:
            if i<=key:
                t1.insert(i)
            else:
                t2.insert(i)
        return t1, t2

    def split(self, x: Any) -> tuple["AVLTree", "AVLTree"]:
        """
        Splits self in two AVLTrees t1 and t2 such as
        t1.max() <= x and t2.min() > x.
        Recursively goes down at self,
        merging half of each subtree with t1 or t2
        Time complexity: O(log^2 n)
        """
        t1 = AVLTree() # all values <= x
        t2 = AVLTree() # all values > x

        def _detach(node):
            """Auxiliary func that erase all links to node"""
            if node.right is not None:
                node.right.parent = None
                node.right = None
            if node.left is not None:
                node.left.parent = None
                node.left = None
            return node

        current_root = self._root
        while current_root is not None:
            if current_root.val <= x:
                right_subtree = current_root.right
                left_subtree = current_root.left

                # deleting current_root from subtree, deleting all links
                current_root = _detach(current_root)

                # left_subtree is AVL
                # adding current_root after max of left_subtree
                left_subtree_max_node = self._get_max(left_subtree)

                if left_subtree_max_node:
                    left_subtree_max_node.right = current_root
                    left_subtree_max_node.right.parent = left_subtree_max_node
                    left_subtree_max_node = self._balance_up(left_subtree_max_node)
                else:
                    left_subtree_max_node = current_root

                # merging t1 and built tree
                if t1._root is None:
                    t1._root = left_subtree_max_node
                else:
                    #finds subtree p in t1: p.height <= left_subtree_max_node.height
                    p = t1._root
                    while p.right and self._height(p) > self._height(left_subtree_max_node):
                        p = p.right
                    p_parent = p.parent

                    # removing parentness for merge to not fuck up
                    if p.parent:
                        p.parent.right = None
                    p.parent = None

                    k = self._merge(left_subtree_max_node, p)

                    # attaching merged tree
                    if p_parent:
                        p_parent.right = k
                        k.parent = p_parent
                        p_parent = self._balance_up(p_parent)
                        if p_parent.parent is None:
                            t1._root = p_parent
                    else:
                        t1._root = k
                current_root = right_subtree # goes deeper

            else: # current_root.val > x
                right_subtree = current_root.right
                left_subtree = current_root.left

                # deleting current_root from subtree, deleting all links
                current_root = _detach(current_root)

                # right_subtree is AVL
                # adding current_root after min of right_subtree
                right_subtree_min_node = self._get_min(right_subtree)

                if right_subtree_min_node:
                    right_subtree_min_node.left = current_root
                    right_subtree_min_node.left.parent = right_subtree_min_node
                    right_subtree_min_node = self._balance_up(right_subtree_min_node)
                else:
                    right_subtree_min_node = current_root

                # merging t2 and built tree
                if t2._root is None:
                    t2._root = right_subtree_min_node
                else:
                    # finds subtree p in t2: p.height <= right_subtree_min_node.height
                    p = t2._root
                    while p.left and self._height(p) > self._height(right_subtree_min_node):
                        p = p.left
                    p_parent = p.parent

                    # removing parentness for merge to not fuck up
                    if p.parent:
                        p.parent.left = None
                    p.parent = None
                    k = self._merge(p, right_subtree_min_node)

                    # attaching merged tree
                    if p_parent:
                        p_parent.left = k
                        k.parent = p_parent
                        p_parent = self._balance_up(p_parent)
                        if p_parent.parent is None:
                            t2._root = p_parent
                    else:
                        t2._root = k
                current_root = left_subtree  # goes deeper
        t1._root = t1._balance(t1._root)
        t2._root = t2._balance(t2._root)
        return t1, t2

    def breadth_first_search(self) -> list[list[Any | None]]:
        """
        Implements iterative Breadth-first search based on deque
        Returns list of lists storing tree node values (including first met None)
        layer by layer
        """
        if self._root is None:
            return [[None]]
        search_queue = deque([self._root])
        ret_list = [[self._root.val, self._root.subtree_size]]
        counted_children = 1    #children found for each layer

        def handle_child(node): #checks child and appends it to deque and its value to ret_list
            counted = 0
            if node is None:
                ret_list[-1].append(None)
            else:
                search_queue.append(node)
                ret_list[-1].append((node.val, node.height, node.subtree_size))
                counted = 1
            return counted

        while len(search_queue) > 0:
            num_of_new_children = 0
            ret_list.append([])
            while counted_children>0:   #checks every child from previous layer
                if  search_queue[0] is None:
                    ret_list[-1].append([None, None])
                else:
                    num_of_new_children += handle_child(search_queue[0].left) + handle_child(search_queue[0].right)
                    search_queue.popleft()  #current node is handled
                    counted_children -= 1
            counted_children += num_of_new_children

        return ret_list






