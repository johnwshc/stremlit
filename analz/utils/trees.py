class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children: list[TreeNode] = []
    def add_child(self, child):
        if isinstance(child, TreeNode):
            self.children.append(child)
        else:
            raise Exception("Invalid Node Type")

# Create a function for depth-first traversal (pre-order)
def pre_order_traversal(node: TreeNode):
    if node is None:
        return
    print(node.data)
    for child in node.children:
        pre_order_traversal(child)


# Create a function for depth-first search
def depth_first_search(node: TreeNode, target):
    if node is None:
        return False
    if node.data == target:
        return True
    for child in node.children:
        if depth_first_search(child, target):
            return True
    return False


# Create a function for insertion
def insert_node(root: TreeNode, node: TreeNode):
    if root is None:
        root = node
    else:
        root.add_child(node)

# Create a function for deletion
def delete_node(root: TreeNode, target):
    if root is None:
        return None
    root.children = [child for child in root.children if child.data != target]
    for child in root.children:
        delete_node(child, target)


# Create a function to calculate the height of a tree
def tree_height(node: TreeNode):
    if node is None:
        return 0
    if not node.children:
        return 1
    return 1 + max(tree_height(child) for child in node.children)


# Create a self-balancing tree (AVL tree)
# AVL tree implementation is complex, so we'll provide a basic example with the concept
class AVLTreeNode(TreeNode):
    def __init__(self, data):
        super().__init__(data)
        self.height = 1

    def balance_factor(self):
        left_height = self.children[0].height if self.children and len(self.children) > 0 else 0
        right_height = self.children[1].height if self.children and len(self.children) > 1 else 0
        return left_height - right_height

    def update_height(self):
        left_height = self.children[0].height if self.children and len(self.children) > 0 else 0
        right_height = self.children[1].height if self.children and len(self.children) > 1 else 0
        self.height = 1 + max(left_height, right_height)

    def rotate_left(self):
        new_root = self.children[1]
        self.children[1] = new_root.children[0]
        new_root.children[0] = self
        self.update_height()
        new_root.update_height()
        return new_root

    def rotate_right(self):
        new_root = self.children[0]
        self.children[0] = new_root.children[1]
        new_root.children[1] = self
        self.update_height()
        new_root.update_height()
        return new_root

def test2():
    # Sample usage:
    root = TreeNode("A")
    child1 = TreeNode("B")
    child2 = TreeNode("C")
    child3 = TreeNode("D")

    root.add_child(child1)
    root.add_child(child2)
    root.add_child(child3)

    # Traversal example (pre-order)
    print("Pre-order traversal:")
    pre_order_traversal(root)

    # Searching example
    target_value = "D"
    print(f"Is {target_value} present in the tree? {depth_first_search(root, target_value)}")

    # Insertion example
    new_node = TreeNode("E")
    insert_node(child1, new_node)
    print("After insertion:")
    pre_order_traversal(root)

    # Deletion example
    delete_node(root, "C")
    print("After deletion:")
    pre_order_traversal(root)

    # Height calculation example
    print("Height of the tree:", tree_height(root))

    # AVL tree example (basic concept)
    avl_root = AVLTreeNode("M")
    avl_child1 = AVLTreeNode("L")
    avl_child2 = AVLTreeNode("R")

    avl_root.add_child(avl_child1)
    avl_root.add_child(avl_child2)

    avl_child1.add_child(TreeNode("A"))
    avl_child1.add_child(TreeNode("B"))

    avl_child2.add_child(TreeNode("X"))

    avl_root = avl_root.rotate_left()
    print("After rotation (left):")
    pre_order_traversal(avl_root)

    avl_root = avl_root.rotate_right()
    print("After rotation (right):")
    pre_order_traversal(avl_root)

def test():
    root = TreeNode("A")
    child1 = TreeNode("B")
    child2 = TreeNode("C")
    child3 = TreeNode("D")
    # Add children to root
    root.add_child(child1)
    root.add_child(child2)
    root.add_child(child3)