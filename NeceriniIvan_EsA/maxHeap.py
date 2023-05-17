import math
from abstractQueue import Queue
from anytree import Node, RenderTree


class MaxHeap(Queue):
    """Class for max-heap data structure
    A max-heap is a complete binary tree where the value of each node is greater than or equal to the value of its children
    The root element (i.e. the first element of the array) is the maximum element
    The maximum number of nodes at level i is 2^i
    The maximum number of nodes in a heap of height h is 2^(h+1)-1
    The maximum number of nodes in a heap of n nodes is n
    The height of a heap of n nodes is floor(log2(n))
    The heap is represented as an array with two attributes: length and size with condition 0 <= size <= length
    The heap is empty if size = 0
    The heap is full if size = length
    Valid elements are stored in the first size positions of the array
    """

    # Static methods to compute the index of the left child, right child and parent of a node
    @staticmethod
    def parent(i):
        # the parent of the i-th node is the (i-1)//2-th node
        return (i - 1) // 2

    @staticmethod
    def leftChild(i):
        # the left child of the i-th node is the (2i+1)-th node
        return 2 * i + 1

    @staticmethod
    def rightChild(i):
        # the right child of the i-th node is the (2i+2)-th node
        return 2 * i + 2

    def __init__(self):
        # Initialize an empty heap
        self.size = 0
        # The heap is represented as an array
        self.heap = []

    def isEmpty(self) -> bool:
        # returns True if the heap is empty, False otherwise
        # The heap is empty if the size is 0
        return self.size == 0

    def maxHeapify(self, i):
        # maxHeapify needs to be called only on nodes that are not leaves (i.e. nodes with at least one child)
        # The maxHeapify method assumes that the binary trees rooted at leftChild(index) and rightChild(index) are max-heaps
        # The maxHeapify method is used to restore the max-heap property
        l = self.leftChild(i)
        r = self.rightChild(i)
        max = i
        # Find the largest element among the i-th node, its left child and its right child
        # If the i-th node is not the largest, swap it with the largest child and call maxHeapify on the child
        if l < self.size and self.heap[l] > self.heap[i]:
            max = l
        if r < self.size and self.heap[r] > self.heap[max]:
            max = r
        # If the i-th node is not the largest, swap it with the largest child and call maxHeapify on the child
        # The recursive call to maxHeapify is performed only if the i-th node is not the largest
        if max != i:
            self.heap[i], self.heap[max] = self.heap[max], self.heap[i]
            self.maxHeapify(max)

    def buildMaxHeap(self, array):
        # Build a max-heap from an array
        self.heap = array
        self.size = len(array)
        for i in range(self.size // 2, -1, -1):
            self.maxHeapify(i)

    def heapIncreaseKey(self, i, key):
        # Increase the value of the i-th node to the new value if the new value is greater than the current value
        if key < self.heap[i]:
            return None

        self.heap[i] = key
        while i > 0 and self.heap[self.parent(i)] < self.heap[i]:
            # Swap the i-th node with its parent until the max-heap property is restored
            self.heap[i], self.heap[self.parent(i)] = (
                self.heap[self.parent(i)],
                self.heap[i],
            )
            i = self.parent(i)

    # --------------------------------------------------------------------------------------------------------------
    # METHODS TO TEST IN THE MAIN PROGRAM
    def maximum(self):
        # returns the maximum value in the heap (i.e. the root element) without removing it
        if self.size == 0:
            # The heap is empty
            return None
        else:
            return self.heap[0]

    def extractMax(self):
        # returns and removes the maximum value in the heap (i.e. the root element)
        if self.size == 0:
            return None

        maxValue = self.heap[0]
        # Replace the root element with the last element of the heap
        self.heap[0] = self.heap[self.size - 1]
        self.size -= 1
        # Restore the max-heap property
        self.heap.pop()
        self.maxHeapify(0)
        return maxValue

    def insert(self, value):
        # Insert a new value in the heap
        self.size += 1
        self.heap.append(-math.inf)
        self.heapIncreaseKey(self.size - 1, value)

    # --------------------------------------------------------------------------------------------------------------

    def toTree(self):
        # method to convert the heap array to a tree of Node objects
        # Convert the heap array to a tree of Node objects
        if self.size == 0:
            return None

        # Create the root node and build the tree level by level
        root = Node(str(self.heap[0]))
        queue = [root]
        i = 0
        while i < self.size:
            node = queue.pop(0)
            left = self.leftChild(i)
            right = self.rightChild(i)
            if left < self.size:
                left_node = Node(str(self.heap[left]), parent=node)
                queue.append(left_node)
            if right < self.size:
                right_node = Node(str(self.heap[right]), parent=node)
                queue.append(right_node)
            i += 1

        return root


if __name__ == "__main__":
    queue = MaxHeap()

    print("TEST WITH 7 NUMBERS")
    queue.insert(5)
    queue.insert(8)
    queue.insert(3)
    queue.insert(4)
    queue.insert(10)
    queue.insert(12)
    queue.insert(2)

    # DEBUG
    rootNode = queue.toTree()
    for pre, fill, node in RenderTree(rootNode):
        print(f"{pre}{node.name}")
    print("Max: ", queue.maximum())
    print("Extract the max: ", queue.extractMax(), "\n")
    rootNode = queue.toTree()
    for pre, fill, node in RenderTree(rootNode):
        print(f"{pre}{node.name}")
    print("\n")

    # TEST WITH 50 RANDOM NUMBERS
    import random

    print("TEST WITH 50 RANDOM NUMBERS")

    for i in range(50):
        queue.insert(random.randint(0, 50))

    rootNode = queue.toTree()
    for pre, fill, node in RenderTree(rootNode):
        print(f"{pre}{node.name}")
    print("Max: ", queue.maximum())
    print("Extract the max: ", queue.extractMax(), "\n")
    rootNode = queue.toTree()
    for pre, fill, node in RenderTree(rootNode):
        print(f"{pre}{node.name}")
