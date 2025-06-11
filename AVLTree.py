"""A class representing a node in an AVL tree"""


class AVLNode(object):
	"""Constructor, you are allowed to add more fields.

	@type key: int or None
	@param key: key of your node
	@type value: string
	@param value: data of your node
	"""

	def __init__(self, key, value):
		self.key = key
		self.value = value
		self.left = None
		self.right = None
		self.parent = None
		self.height = 0 if self.is_real_node() else -1
		self.bf = 0

	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""

	def is_real_node(self):
		if self.key is None:
			return False
		else:
			return True

	"""returns whether self is leaf or not

		@type node: AVLNode
		@rtype: bool
		@returns: True if self is a leaf node, False otherwise.
		"""

	def is_leaf(self):
		a = self.right
		b = self.left
		if not a.is_real_node() and not b.is_real_node():
			return True
		else:
			return False

	def compute_height(self):
		if not self.is_real_node():
			return -1
		left_height = self.left.height if self.left.is_real_node() else -1
		right_height = self.right.height if self.right.is_real_node() else -1
		return 1 + max(left_height, right_height)

	def update_height(self):
		self.height = self.compute_height()
		return self.height

	def update_bf(self):
		self.bf = self.get_BF()
		return self.bf

	def get_BF(self):
		return self.left.height - self.right.height

	def set_virtual_nodes(self):
		self.left = AVLNode(None, None)
		self.right = AVLNode(None, None)
		self.left.parent = self
		self.right.parent = self

	def set_virtual_node_right(self):
		self.right = AVLNode(None, None)
		self.right.parent = self

	def set_virtual_node_left(self):
		self.left = AVLNode(None, None)
		self.left.parent = self

	def replace_child(self, child, replacement_child):
		if child.key == self.left.key:
			self.left = replacement_child
		elif child.key == self.right.key:
			self.right = replacement_child
		else:
			return  # if none match

		replacement_child.parent = self
	# child.parent = AVLNode(None, None)


"""
A class implementing an AVL tree.
"""


class AVLTree(object):
	"""
	Constructor, you are allowed to add more fields.

	"""

	def __init__(self):
		self.root = None
		self.max = None
		self.treeSize = 0
		self.cntZero = 0

	def __repr__(self):
		def printree(node):
			if node is None or not node.is_real_node():
				return []

			root_key = f"{node.key}({node.height})"
			left = printree(node.left)
			right = printree(node.right)

			lwid = len(left[-1]) if left else 0
			rwid = len(right[-1]) if right else 0
			rootwid = len(root_key)

			result = [(lwid + 1) * " " + root_key + (rwid + 1) * " "]

			if left or right:
				ls = len(left[0].rstrip()) if left else 0
				rs = len(right[0]) - len(right[0].lstrip()) if right else 0
				result.append(ls * " " + (lwid - ls) * "_" + "/" + rootwid * " " + "\\" + rs * "_" + (rwid - rs) * " ")

			max_lines = max(len(left), len(right))
			for i in range(max_lines):
				l_line = left[i] if i < len(left) else " " * lwid
				r_line = right[i] if i < len(right) else " " * rwid
				result.append(l_line + " " * (rootwid + 2) + r_line)

			return result

		return '\n'.join(printree(self.root))

	"""searches for a node in the dictionary corresponding to the key

	@type key: int
	@param key: a key to be searched
	@rtype: AVLNode
	@returns: node corresponding to key
	"""

	def search(self, key):

		def search_rec(node, key):

			while node.is_real_node():
				if node.key == key:
					return node
				else:
					if node.key < key:
						node = node.right
					else:
						node = node.left

			return None
		return None if self.root is None else search_rec(self.root, key)

	"""
	Rotation functions for insert and delete
	returns the new "root" for the subtree
	"""

	def update_cntZero(self, node):
		if node.is_real_node():
			old = node.bf
			node.update_height()
			new = node.update_bf()
			if old == 0 and new != 0:
				self.cntZero -= 1
			elif old != 0 and new == 0:
				self.cntZero += 1

		if node.right.is_real_node():
			old = node.right.bf
			node.right.update_height()
			new = node.right.update_bf()
			if old == 0 and new != 0:
				self.cntZero -= 1
			elif old != 0 and new == 0:
				self.cntZero += 1

		if node.left.is_real_node():
			old = node.left.bf
			node.left.update_height()
			new = node.left.update_bf()
			if old == 0 and new != 0:
				self.cntZero -= 1
			elif old != 0 and new == 0:
				self.cntZero += 1

	def rotate_right(self, y):
		x = y.left
		T2 = x.right

		x.right = y
		y.left = T2

		if T2.is_real_node():
			T2.parent = y
		x.parent = y.parent
		y.parent = x

		y.update_height()
		x.update_height()
		self.update_cntZero(x)

		return x

	def rotate_left(self, x):
		y = x.right
		T2 = y.left

		y.left = x
		x.right = T2

		if T2.is_real_node():
			T2.parent = x
		y.parent = x.parent
		x.parent = y

		y.update_height()
		x.update_height()

		self.update_cntZero(y)

		return y

	def rotate_left_right(self, node):
		node.left = self.rotate_left(node.left)
		return self.rotate_right(node)

	def rotate_right_left(self, node):
		node.right = self.rotate_right(node.right)
		return self.rotate_left(node)

	"""inserts a new node into the dictionary with corresponding key and value

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@param start: can be either "root" or "max"
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""

	def insert(self, key, val, start="root"):
		self.treeSize += 1
		if self.root is None:
			self.root = AVLNode(key, val)
			self.max = self.root
			self.root.set_virtual_nodes()
			self.cntZero = 1
			return 0

		def insert_root(key, val, node):
			summ = 0

			while True:
				if key < node.key:
					if not node.left.is_real_node():
						node.left = AVLNode(key, val)
						node.left.parent = node
						node.left.set_virtual_nodes()
						break
					else:
						node = node.left
				else:
					if not node.right.is_real_node():
						node.right = AVLNode(key, val)
						node.right.parent = node
						node.right.set_virtual_nodes()
						if key > self.max.key:
							self.max = node.right
						break
					else:
						node = node.right

			self.cntZero += 1
			while node is not None:
				old_height = node.height
				node.update_height()
				old_bf = node.bf
				bf = node.update_bf()

				if abs(bf) < 2:
					if abs(old_bf) != 0 and abs(bf) == 0:
						self.cntZero += 1
					elif abs(old_bf) == 0 and abs(bf) != 0:
						self.cntZero -= 1
					if node.height == old_height:
						break
					else:
						node = node.parent
						summ += 1
				else:
					if bf == 2:
						bf_left = node.left.get_BF()
						if bf_left == 1:
							summ += 1
							newnode = self.rotate_right(node)
						else:
							summ += 2
							newnode = self.rotate_left_right(node)
					else:
						bf_right = node.right.get_BF()
						if bf_right == -1:
							summ += 1
							newnode = self.rotate_left(node)
						else:
							summ += 2
							newnode = self.rotate_right_left(node)
					if newnode.parent is None:
						self.root = newnode
					else:
						if newnode.parent.left == node:
							newnode.parent.left = newnode
						else:
							newnode.parent.right = newnode

					self.update_cntZero(node)

					node = node.parent
			return summ

		def insert_max(key, val, node):
			while node is not None and key < node.key:
				node = node.parent

			if node is None:
				node = self.root

			return insert_root(key, val, node)

		if start == "root":
			return insert_root(key, val, self.root)
		else:
			return insert_max(key, val, self.max)

	"""deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""

	def delete(self, node):
		self.treeSize -= 1
		children = 1 if node.left.is_real_node() else 0
		children += 1 if node.right.is_real_node() else 0
		if node == self.max:
			self.max = node.parent
		rotations = 0
		bf_node = None
		if children == 0:
			if node.parent is not None and node.parent.is_real_node():
				bf_node = node.parent
				node.parent.replace_child(node, AVLNode(None, None))
				self.cntZero -= 1

			else:  # node is a leaf and no parent -> arg node is the root of the tree
				self.root = None
				self.cntZero = 0
				self.max = None

				rotations = 0

		elif children == 1:  # node has 1 child
			child = node.left if node.left.is_real_node() else node.right
			if node.parent is not None and node.parent.is_real_node():
				old_bf = child.get_BF()
				node.parent.replace_child(node, child)
				child.parent = node.parent
				child.update_height()
				child.parent.update_height()
				bf_node = child
				if old_bf == 0:
					self.cntZero -= 1

			else:  # node has no parent, but has 1 child. this child cannot have another child.
				self.root = child
				child.parent = None
				bf_node = self.root
				self.cntZero = 1
				child.update_height()
				rotations = 0

		elif children == 2:  # node has 2 children

			successor = node.right
			Sr = successor
			while successor.left is not None and successor.left.is_real_node():
				successor = successor.left

			old_bf = successor.get_BF()

			if Sr.key != successor.key:
				successor.replace_child(successor.left, node.left)
				successor.left.parent = successor
				bf_node = successor.parent

				successor.parent.replace_child(successor, successor.right)
				if successor.right is not None and successor.right.is_real_node():
					successor.right.parent = successor.parent

				successor.replace_child(successor.right, Sr)
				Sr.parent = successor

			else:  # Sr = successor
				# put successor instead of node
				bf_node = successor
				if node.parent is not None and node.parent.is_real_node():
					node.parent.replace_child(node, successor)
				successor.left = node.left
				if successor.left is not None and successor.left.is_real_node():
					successor.left.parent = successor

			successor.parent = node.parent
			successor.bf = node.bf

			if old_bf == 0:
				self.cntZero -= 1

			if node.key == self.root.key:
				self.root = successor
				successor.parent = None

			self.update_cntZero(successor)

		while bf_node is not None:
			old_height = bf_node.height
			self.update_cntZero(bf_node)
			new_height = bf_node.height
			bf = bf_node.update_bf()

			if abs(bf) < 2:
				bf_node = bf_node.parent
				if old_height != new_height:
					rotations += 1
			else:
				if bf == 2:
					bf_left = bf_node.left.get_BF()
					if bf_left == 1:
						rotations += 1
						newnode = self.rotate_right(bf_node)
					else:
						rotations += 2
						newnode = self.rotate_left_right(bf_node)
				else:
					bf_right = bf_node.right.get_BF()
					if bf_right == -1:
						rotations += 1
						newnode = self.rotate_left(bf_node)
					else:
						rotations += 2
						newnode = self.rotate_right_left(bf_node)
				if newnode.parent is None:
					self.root = newnode
				else:
					if newnode.parent.left == bf_node:
						newnode.parent.left = newnode
					else:
						newnode.parent.right = newnode

				self.update_cntZero(bf_node)
				self.update_cntZero(newnode)

				bf_node = bf_node.parent
		return rotations

	"""returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""

	def avl_to_array(self):
		array = list()
		if self.root is None:
			return []

		def inorder(node, arr):
			if node.left.is_real_node():
				inorder(node.left, arr)
			arr.append((node.key, node.value))
			if node.right.is_real_node():
				inorder(node.right, arr)

		inorder(self.root, array)
		return array

	"""returns the number of items in dictionary 

	@rtype: int
	@returns: the number of items in dictionary 
	"""

	def size(self):
		return self.treeSize

	"""returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""

	def get_root(self):
		return self.root

	"""gets amir's suggestion of balance factor

	@returns: the number of nodes which have balance factor equals to 0 devided by the total number of nodes
	"""

	def get_amir_balance_factor(self):
		return self.cntZero / self.treeSize if self.cntZero != 0 else 0