# from typing import TypeVar, Optional
# import random
# from collections import deque

# KeyType = TypeVar('KeyType')
# ValType = TypeVar('ValType')

# class Node:
#     def __init__(self, key: KeyType, value: ValType, rank: int):
#         self.key = key
#         self.value = value
#         self.rank = rank
#         self.left = None
#         self.right = None

# class ZipTree:            
#     def __init__(self):
#         self.root = None
#         self.num_nodes = 0

#     @staticmethod
#     def get_random_rank() -> int:
#         mean_rank = 1  
#         std_dev = 0.5  
#         rank = int(random.normalvariate(mean_rank, std_dev))
#         return max(1, rank)  

#     def unzip(self, x: Node, y: Node):
#         def unzip_lookup(key: KeyType, node: Node):
#             if node is None:
#                 return None, None
#             if node.key < key:
#                 p, q = unzip_lookup(key, node.right)
#                 node.right = p
#                 return node, q
#             else:
#                 p, q = unzip_lookup(key, node.left)
#                 node.left = q
#                 return p, node
#         return unzip_lookup(x.key, y)

#     def get_insert_node(self, node: Node) -> Node:
#         current = self.root
#         parent = None
#         while current is not None:
#             if current.rank < node.rank:
#                 return parent, current
#             elif current.rank == node.rank and current.key > node.key:
#                 return parent, current
#             else:
#                 parent = current            
#                 if current.key > node.key:
#                     current = current.left
#                 else:
#                     current = current.right
#         return parent, None
        
#     def insert(self, key: KeyType, val: ValType, rank: int = -1):
#         self.num_nodes += 1
#         if rank == -1:
#             rank = self.get_random_rank()
#         node = Node(key, val, rank)
        
#         if self.root is None:
#             self.root = node            
#         else:
#             parent, insert_node = self.get_insert_node(node)
#             if insert_node is None:
#                 if parent.key > key:
#                     parent.left = node
#                 else:
#                     parent.right = node
#                 return
#             if parent is None:
#                 p, q = self.unzip(node, insert_node)
#                 node.left = p
#                 node.right = q
#                 self.root = node
#                 return
#             if parent is not None:
#                 if parent.key < node.key:
#                     parent.right = node
#                 else:
#                     parent.left = node
#             p, q = self.unzip(node, insert_node)
#             node.left = p
#             node.right = q
                    
        
#     def zip(self, x: Node):
#         """Zip up two nodes."""
#         if x is None:
#             return None

#         def zip_up(p: Node, q: Node):
#             if p is None:
#                 return q
#             if q is None:
#                 return p
#             if q.rank > p.rank:
#                 q.left = zip_up(p, q.left)
#                 return q
#             else:
#                 p.right = zip_up(p.right, q)
#                 return p
#         return zip_up(x.left, x.right)
    
#     def remove(self, key: KeyType):
#         """Remove a node from the Zip Tree."""
#         self.num_nodes -= 1
#         current = self.root
#         parent = None
#         while current is not None:
#             if current.key == key:
#                 break
#             elif current.key < key:
#                 parent = current
#                 current = current.right
#             else:
#                 parent = current
#                 current = current.left

#         # Check if current is None before proceeding
#         if current is None:
#             return

#         node = self.zip(current)
#         if parent is None:
#             self.root = node
#             return
#         if parent.key > current.key:
#             parent.left = node
#         else:
#             parent.right = node

#     def find(self, key: KeyType) -> Optional[ValType]:
#         node = self.root
#         while node:
#             if key == node.key:
#                 return node.value
#             elif key < node.key:
#                 node = node.left
#             else:
#                 node = node.right
#         return None

#     def get_size(self) -> int:
#         return self.num_nodes

#     def get_height(self) -> int:
#         if not self.root:
#             return -1
        
#         height = -1
#         current_level = deque([self.root])
#         while current_level:
#             height += 1
#             next_level = deque()
#             while current_level:
#                 node = current_level.popleft()
#                 if node.left:
#                     next_level.append(node.left)
#                 if node.right:
#                     next_level.append(node.right)
#             current_level = next_level
        
#         return height

#     def get_depth(self, key: KeyType) -> int:
#         node = self.root
#         depth = 0
#         while node:
#             if key == node.key:
#                 return depth
#             elif key < node.key:
#                 node = node.left
#             else:
#                 node = node.right
#             depth += 1
#         raise KeyError(f"Key {key} not found in the tree.")


from typing import TypeVar
from collections import deque
import random

KeyType = TypeVar('KeyType')
ValType = TypeVar('ValType')

class Node:
    def __init__(self, key: KeyType, value: ValType, rank: int):
        self.key = key
        self.value = value
        self.rank = rank
        self.left = None
        self.right = None

class ZipTree:
    def __init__(self):
        self.root = None
        self.num_nodes = 0

    @staticmethod
    def get_random_rank() -> int:
        mean_rank = 1
        std_dev = 0.5
        rank = int(random.normalvariate(mean_rank, std_dev))
        return max(1, rank)

    def unzip(self, x: Node, y: Node):
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
        """Remove a node from the Zip Tree."""
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
        node = self.root
        while node.key != key:
            if node.key > key:
                node = node.left
            else:
                node = node.right
        return node.value

    def get_size(self) -> int:
        return self.num_nodes

    def get_height(self) -> int:
        if not self.root:
            return -1
        height = 0
        current_level = [self.root]
        while current_level:
            height += 1
            next_level = []
            for node in current_level:
                if node.left:
                    next_level.append(node.left)
                if node.right:
                    next_level.append(node.right)
            current_level = next_level
        return height - 1

    def get_depth(self, key: KeyType) -> int:
        node = self.root
        depth = 0
        while node.key != key:
            if node.key > key:
                node = node.left
            else:
                node = node.right
            depth += 1
        return depth

# feel free to define new classes/methods in addition to the above
# fill in the definitions of each required member function (above),
# and any additional member functions you define
