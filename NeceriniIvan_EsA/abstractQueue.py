from abc import abstractmethod


class Queue:
    """Class for queue data structure
    Abstract class used for inheritance
    Used to force the implementation of the methods in the concrete subclasses
    """

    """The notation "->" is not used to explicitly specify a return type for the "heapMaximum()" and "heapExtractMax()"
    abstract methods because their return type depends on the particular type of queue implemented in the
    concrete subclass. For example, if the subclass implements a queue of integers, then both methods might
    return an integer value. However, if the subclass implements a queue of objects, then the methods might
    return an instance of the object containing the maximum value. Therefore, the return type for these two
    methods depends on the specific implementation in the concrete subclass and cannot be defined in the abstract
    class.
    """

    @abstractmethod
    def isEmpty(self) -> bool:
        # returns True if the queue is empty, False otherwise
        raise NotImplementedError()

    # METHODS TO TEST IN THE MAIN PROGRAM
    @abstractmethod
    def maximum(self):
        # returns the maximum value in the queue
        raise NotImplementedError()

    @abstractmethod
    def extractMax(self):
        # returns and removes the maximum value in the queue
        raise NotImplementedError()

    @abstractmethod
    def insert(self, value: int) -> None:
        # inserts the value at the end of the queue
        raise NotImplementedError()
