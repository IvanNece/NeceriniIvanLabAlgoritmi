from linkedList import LinkedListNode, LinkedListQueue


class SortedLinkedListQueue(LinkedListQueue):
    """Class for priority queue data structure implemented as a sorted linked list of nodes
    The maximum value is stored in the head of the queue and the minimum value is stored in the tail of the queue
    Inherited from LinkedListQueue, the elements are sorted in descending order"""

    def __init__(self):
        # call the constructor of the parent class
        super().__init__()

    # -------------------------------------------------------------------------------------------------------------------
    # METHODS TO TEST IN THE MAIN PROGRAM
    def insert(self, value):
        # inserts the value in the queue in the right position
        newNode = LinkedListNode(value)
        # if the queue is empty, the new node is both the head and the tail
        if self.isEmpty():
            self.head = newNode
            self.tail = newNode
        else:
            # find the right position for the new node
            currentNode = self.head
            oldNode = None
            while currentNode is not None and currentNode.value > value:
                oldNode = currentNode
                currentNode = currentNode.next
            # insert the new node in the right position
            if oldNode is None:
                self.head = newNode
                newNode.next = currentNode
            else:
                oldNode.next = newNode
                newNode.next = currentNode

            if currentNode is None:
                self.tail = newNode

    def maximum(self):
        # returns the maximum value in the queue
        return self.head

    def extractMax(self):
        # returns and removes the maximum value in the queue
        if self.isEmpty():
            return None
        else:
            maximumNode = self.head
            self.head = self.head.next
            if self.head is None:
                self.tail = None
            return maximumNode

    # -------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    queue = SortedLinkedListQueue()

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
    print("Sorted list without the maximum:\n", queue)

    # TEST WITH 50 RANDOM NUMBERS
    import random

    print("\nTEST WITH 50 RANDOM NUMBERS")

    for i in range(50):
        queue.insert(random.randint(0, 50))
    print(queue, "\n")
    print("Extract the max: ", queue.extractMax(), "\n")
    print("Sorted list without the maximum:\n", queue)
