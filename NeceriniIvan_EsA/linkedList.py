from abstractQueue import Queue


class LinkedListNode:
    """Class that represents a node of a linked list
    First we define a node and then we define a linked list as a collection of nodes
    A node contains a value and a pointer to the next node
    """

    def __init__(self, initData):
        self.value = initData
        self.next = None

    def __repr__(self):
        # special method used to represent a class's objects as a string, for example when printing a node object
        # the string returned by this method is the one that is printed
        return "Node: {}".format(self.value)


class LinkedListQueue(Queue):
    """Class for priority queue data structure implemented as a linked list of nodes
    A queue is a FIFO (First In First Out) data structure
    The priority is given by the value of the node (the higher the value, the higher the priority)
    """

    def __init__(self):
        self.head = None
        self.tail = None

    def isEmpty(self):
        return self.head == None

    # -------------------------------------------------------------------------------------------------------------------
    # METHODS TO TEST IN THE MAIN PROGRAM
    def maximum(self):
        # returns the maximum value in the queue
        if self.isEmpty():
            return None
        else:
            currentNode = self.head
            maximumNode = self.head
            # iterate over the queue and find the node with the maximum value
            while currentNode is not None:
                if currentNode.value > maximumNode.value:
                    maximumNode = currentNode
                currentNode = currentNode.next
            return maximumNode

    def extractMax(self):
        # returns and removes the maximum value in the queue
        # if the queue is empty, return None
        if self.isEmpty():
            return None
        # if the queue contains only one node, the head and the tail are set to None
        elif self.head == self.tail:
            self.tail = None
            node = self.head
            self.head = None
            return node
        # if the queue contains more than one node, find the node with the maximum value
        else:
            maximumNode = self.head
            oldMaximumNode = None
            currentNode = self.head
            oldCurrentNode = None
            while currentNode is not None:
                if currentNode.value > maximumNode.value:
                    maximumNode = currentNode
                    oldMaximumNode = oldCurrentNode
                oldCurrentNode = currentNode
                currentNode = currentNode.next

            # remove the node with the maximum value from the queue
            if maximumNode == self.head:
                # max is the first node
                self.head = self.head.next
                return maximumNode
            elif maximumNode == self.tail:
                # max is the last node
                self.tail = oldMaximumNode
                oldMaximumNode.next = None
                return maximumNode
            else:
                oldMaximumNode.next = maximumNode.next
                return maximumNode

    def insert(self, value):
        # inserts the value at the end of the queue
        newNode = LinkedListNode(value)
        # if the queue is empty, the new node is both the head and the tail
        if self.isEmpty():
            self.head = newNode
            self.tail = newNode
        else:
            self.tail.next = newNode
            self.tail = newNode

    # --------------------------------------------------------------------------------------------------------------------

    def __iter__(self):
        # returns an iterator for the queue to use in the next method
        currentNode = self.head
        while currentNode:
            # yield is used to return a generator object that can be iterated over
            yield currentNode
            currentNode = currentNode.next

    def __repr__(self):
        # returns a string representation of the queue
        nodes = [
            str(node.value) for node in self
        ]  # list comprehension to get the values of the nodes as strings
        # the string representation of the queue is a string of the values of the nodes separated by "->"
        return "->".join(nodes)


if __name__ == "__main__":
    queue = LinkedListQueue()

    print("TEST WITH 7 NUMBERS")
    queue.insert(5)
    queue.insert(8)
    queue.insert(3)
    queue.insert(4)
    queue.insert(10)
    queue.insert(12)
    queue.insert(2)

    # DEBUG
    print(queue, "\n")
    print("Max: ", queue.maximum())
    print("Extract the max: ", queue.extractMax(), "\n")
    print("List without the maximum:\n", queue)

    # TEST WITH 50 RANDOM NUMBERS
    import random

    print("\nTEST WITH 50 RANDOM NUMBERS")

    for i in range(50):
        queue.insert(random.randint(0, 50))
    print(queue, "\n")
    print("Extract the max: ", queue.extractMax(), "\n")
    print("List without the maximum:\n", queue)
