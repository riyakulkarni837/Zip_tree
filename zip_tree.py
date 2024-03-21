# explanations for member functions are provided in requirements.py
# each file that uses a Zip Tree should import it from this file.

# explanations for member functions are provided in requirements.py
# each file that uses a Zip Tree should import it from this file.

from typing import TypeVar
from collections import deque
import random

KeyType = TypeVar('KeyType')
ValType = TypeVar('ValType')

class Node:
    def __init__(self, key: KeyType, value: ValType, rank: int):
        """Initialize a Node."""
        self.key = key
        self.value = value
        self.rank = rank
        self.left = None
        self.right = None

class ZipTree:
    def __init__(self):
        """Initialize a ZipTree."""
        self.root = None
        self.num_nodes = 0

    @staticmethod
    def get_random_rank() -> int:
        """Generate a random rank."""
        rank = 0
        while True:
            rank += 1
            val = random.randint(1, 2)
            if val == 1:
                return rank - 1

    def unzip(self, x: Node, y: Node):
        """Unzip nodes x and y."""
        def unzip_lookup(key: KeyType, node: Node):
            if node is None:
                return None, None
            if node.key < key:
                p, q = unzip_lookup(key, node.right)
                node.right = p
                return node, q
            else:
                p, q = unzip_lookup(key, node.left)
                node.left = q
                return p, node
        return unzip_lookup(x.key, y)

    def get_insert_node(self, node: Node) -> Node:
        """Get the insertion node."""
        current = self.root
        parent = None
        while current is not None:
            if current.rank < node.rank:
                return parent, current
            elif current.rank == node.rank and current.key > node.key:
                return parent, current
            else:
                parent = current
                if current.key > node.key:
                    current = current.left
                else:
                    current = current.right
        return parent, None

    def insert(self, key: KeyType, value: ValType, rank: int = -1):
        """Insert a node into the ZipTree."""
        self.num_nodes += 1
        if rank == -1:
            rank = ZipTree.get_random_rank()
        node = Node(key, value, rank)

        if self.root is None:
            self.root = node
        else:
            parent, insert_node = self.get_insert_node(node)
            if insert_node is None:
                if parent.key > key:
                    parent.left = node
                else:
                    parent.right = node
                return
            if parent is None:
                p, q = self.unzip(node, insert_node)
                node.left = p
                node.right = q
                self.root = node
                return
            if parent is not None:
                if parent.key < node.key:
                    parent.right = node
                else:
                    parent.left = node
            p, q = self.unzip(node, insert_node)
            node.left = p
            node.right = q

    def zip(self, x: Node):
        """Zip up two nodes."""
        if x is None:
            return None

        def zip_up(p: Node, q: Node):
            if p is None:
                return q
            if q is None:
                return p
            if q.rank > p.rank:
                q.left = zip_up(p, q.left)
                return q
            else:
                p.right = zip_up(p.right, q)
                return p
        return zip_up(x.left, x.right)

    def remove(self, key: KeyType):
        """Remove a node from the ZipTree."""
        self.num_nodes -= 1
        current = self.root
        parent = None
        while current is not None:
            if current.key == key:
                break
            elif current.key < key:
                parent = current
                current = current.right
            else:
                parent = current
                current = current.left

        # Check if current is None before proceeding
        if current is None:
            return

        node = self.zip(current)
        if parent is None:
            self.root = node
            return
        if parent.key > current.key:
            parent.left = node
        else:
            parent.right = node

    def find(self, key: KeyType) -> ValType:
        """Find a node with the given key."""
        node = self.root
        while node is not None:
            if node.key == key:
                return node.value
            elif node.key > key:
                node = node.left
            else:
                node = node.right
        raise KeyError("Key not found")

    def get_size(self) -> int:
        """Get the number of nodes in the ZipTree."""
        return self.num_nodes

    def get_height(self) -> int:
        """Get the height of the ZipTree."""
        if not self.root:
            return -1
        height = 0
        current_level = [self.root]
        while current_level:
            height += 1
            current_level = [child for node in current_level for child in (node.left, node.right) if child]
        return height - 1

    def get_depth(self, key: KeyType) -> int:
        """Get the depth of a node with the given key."""
        node = self.root
        depth = 0
        while node is not None:
            if node.key == key:
                return depth
            elif node.key > key:
                node = node.left
            else:
                node = node.right
            depth += 1
        raise KeyError("Key not found")


# feel free to define new classes/methods in addition to the above
# fill in the definitions of each required member function (above),
# and any additional member functions you define
