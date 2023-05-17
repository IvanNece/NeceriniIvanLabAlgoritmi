import numpy as np
from numpy import ndarray
import os, sys
from copy import deepcopy
from functools import partial
import timeit
import matplotlib.pyplot as plt


from abstractQueue import Queue
from maxHeap import MaxHeap
from linkedList import LinkedListQueue
from sortedLinkedList import SortedLinkedListQueue


# SETTING THE PARAMETERS

# Set the recursion limit to 10000 to avoid RecursionError in the MaxHeap class (in the extractMax() method)
# But this can slow down the execution of the program
# Default value is 1000
sys.setrecursionlimit(10000)

n = 800
nrTestEachIteration = 30
step = 50


# DEFINING THE FUNCTIONS
def measureMaximum(queue: Queue, nrTestEachIteration: int):
    """It returns the average execution time (in milliseconds) of the search for the maximum value in the queue.
    It executes the search `nrTestEachIteration` times"""
    # partial() is used to pass the function queue.maximum() as an argument to timeit.timeit()
    f = partial(queue.maximum)
    return (
        timeit.timeit(stmt=f, number=nrTestEachIteration) / nrTestEachIteration * 1000
    )


def measureExtractMax(queue: Queue, nrTestEachIteration: int):
    """It returns the average execution time (in milliseconds) of the extraction of the maximum value in the queue.
    It executes the extraction `nrTestEachIteration` times"""
    durations = []
    oneNumberTimeit = partial(timeit.timeit, number=1)
    for i in range(nrTestEachIteration):
        # deepcopy is used otherwise with insert() repeated the values are inserted several times!
        copiedQueue = deepcopy(queue)
        # it measures the execution time of a single iteration
        durations.append(oneNumberTimeit(lambda: copiedQueue.extractMax()))
    return np.mean(durations) * 1000


def insertValues(queue: Queue, values: list):
    for v in values:
        queue.insert(v)


# this method is used to insert the values in the queue
def insertMeasures(queue: Queue, values: list | ndarray):
    """It returns the average execution time (in milliseconds) of the insertion of the values in the queue.
    It executes the insertion `nrTestEachIteration` times"""
    copiedQueue = deepcopy(queue)
    insertValuesCopiedQueue = partial(insertValues, copiedQueue, values)

    durations = []
    for i in range(nrTestEachIteration):
        # it measures the execution time of a single iteration
        durations.append(timeit.timeit(insertValuesCopiedQueue, number=1))
    # it returns the average execution time of the `nrTestEachIteration` iterations (in milliseconds)
    return np.mean(durations) * 1000


def tracePlots(
    data: list[list[any]],
    titles: list[str],
    plotTitle: str = None,
) -> None:
    # define list of colors for the plots
    colors = ["red", "purple", "#FFCC00"]

    x = np.linspace(1, n, len(data[0]))

    # plot the data
    for i, dataList in enumerate(data):
        # it uses the original values of x
        xVals = x
        plt.plot(xVals, dataList, label=titles[i], color=colors[i])

    # add title, labels and legend
    plt.title(plotTitle)
    plt.xlabel("Dimensione della lista: [n]")
    plt.ylabel("Tempo di esecuzione [ms]")
    plt.legend()

    # Save the plot as a png file
    plt.savefig(f"plots/{plotTitle}.png")
    # Clear figure for the next plot
    plt.clf()


def traceTables(columns: list, headers: tuple, title: str):
    fig, ax = plt.subplots(figsize=(8, 10))

    # Data for plotting the table (it is necessary to convert the list of lists into a numpy array)
    data = np.column_stack(columns)

    # Set the title of the table
    ax.axis("off")
    table = ax.table(cellText=data, colLabels=headers, loc="center", cellLoc="center")
    table.auto_set_column_width(col=list(range(len(columns))))
    table.scale(1, 1.5)

    # Color the headers and the even rows
    # Dictionary comprehension
    cell_colors = {
        cell: ("#ffd1d1", {"weight": "bold"})
        if table[cell].get_text().get_text() in headers
        else ("#ffe4e4", {})
        for cell in table._cells
        if cell[0] % 2 == 0
    }
    for cell, (color, text_props) in cell_colors.items():
        # set the color of the cell
        table[cell].set_facecolor(color)
        # set the text properties of the cell
        table[cell].set_text_props(**text_props)
        # ** used to expand the dictionary

    # save the plot as a png file
    fig.savefig(f"tables/{title}.png", dpi=300, bbox_inches="tight")
    # clear figure for the next plot
    plt.clf()


# MAIN PROGRAM
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------------------
    # CREATION OF THE LIST OF VALUES
    maxHeapMaximumDuration = []
    linkedListMaximumDuration = []
    sortedLinkedListMaximumDuration = []

    maxHeapExtractMaxDuration = []
    linkedListExtractMaxDuration = []
    sortedLinkedListExtractMaxDuration = []

    maxHeapInsertDuration = []
    linkedListInsertDuration = []
    sortedLinkedListInsertDuration = []

    # --------------------------------------------------------------------------------------------------------------
    # EXECUTION OF THE TESTS
    print(
        "STEP_1: execution of the tests: searching of the maximum, extraction of the maximum and insertion of a value ..."
    )
    for i in range(1, n, step):
        print("Test {}/{} ({:.2f}%)".format(i, n, round(i / n * 100, 2)))

        # Creation of the queues
        mHeap = MaxHeap()
        llQueue = LinkedListQueue()
        sllQueue = SortedLinkedListQueue()

        # 1_TESTS OF THE INSERTION
        # It creates an array of random values between 1 and 99 (extremes included)
        valuesToInsert = np.random.randint(1, 100, size=i)

        # Test of max heap value insertion
        maxHeapInsertDuration.append(insertMeasures(mHeap, valuesToInsert))
        # Test of linked list value insertion
        linkedListInsertDuration.append(insertMeasures(llQueue, valuesToInsert))
        # Test of sorted linked list value insertion
        sortedLinkedListInsertDuration.append(insertMeasures(sllQueue, valuesToInsert))

        # Add the values to the queue (insertMeasures() works on a copy of the queues)
        insertValues(mHeap, valuesToInsert)
        insertValues(llQueue, valuesToInsert)
        insertValues(sllQueue, valuesToInsert)

        # 2_TESTS OF THE SEARCH OF THE MAXIMUM
        # Test of max heap maximum search
        maxHeapMaximumDuration.append(measureMaximum(mHeap, nrTestEachIteration))
        # Test of linked list maximum search
        linkedListMaximumDuration.append(measureMaximum(llQueue, nrTestEachIteration))
        # Test of sorted linked list maximum search
        sortedLinkedListMaximumDuration.append(
            measureMaximum(sllQueue, nrTestEachIteration)
        )

        # 3_TEST OF THE EXTRACTION OF THE MAXIMUM
        # Test of max heap maximum extraction
        maxHeapExtractMaxDuration.append(measureExtractMax(mHeap, nrTestEachIteration))
        # Test of linked list maximum extraction
        linkedListExtractMaxDuration.append(
            measureExtractMax(llQueue, nrTestEachIteration)
        )
        # Test of sorted linked list maximum extraction
        sortedLinkedListExtractMaxDuration.append(
            measureExtractMax(sllQueue, nrTestEachIteration)
        )

    # --------------------------------------------------------------------------------------------------------------
    # GENERATION OF THE GRAPHS
    print("STEP_2: generation of the graphs ...")
    # Create the plots folder if it does not exist
    if not os.path.exists("plots"):
        os.makedirs("plots")

    # Draw maximum search graphs
    tracePlots(
        # it creates a list of lists (each list contains the data of a graph)
        *[
            [
                maxHeapMaximumDuration,
                linkedListMaximumDuration,
                sortedLinkedListMaximumDuration,
            ],
            ["Max heap", "Linked List", "Sorted Linked List"],
            "Ricerca del massimo",
        ],
    )

    # Draw maximum extraction graphs
    tracePlots(
        *[
            [
                maxHeapExtractMaxDuration,
                linkedListExtractMaxDuration,
                sortedLinkedListExtractMaxDuration,
            ],
            ["Max heap", "Linked List", "Sorted Linked List"],
            "Estrazione del massimo",
        ],
    )

    # Draw insertion graphs
    tracePlots(
        *[
            [
                maxHeapInsertDuration,
                linkedListInsertDuration,
                sortedLinkedListInsertDuration,
            ],
            ["Max Heap", "Lista concatenata", "Lista concatenta ordinata"],
            "Inserimento dei valori",
        ],
    )

    # --------------------------------------------------------------------------------------------------------------
    # GENERATION OF THE TABLES
    print("STEP_3: generation of the tables...")
    # create the tables folder if it doesn't exist
    if not os.path.exists("tables"):
        os.makedirs("tables")

    # Draw maximum search table
    traceTables(
        *[
            [
                [i for i in range(1, n, step)],
                ["{:.3e}".format(val) for val in maxHeapMaximumDuration],
                ["{:.3e}".format(val) for val in linkedListMaximumDuration],
                ["{:.3e}".format(val) for val in sortedLinkedListMaximumDuration],
            ],
            (
                "Nr elementi",
                "Max Heap",
                "Lista concatenata",
                "Lista concatenata ordinata",
            ),
            "Tempo di ricerca del massimo",
        ]
    )

    # Draw maximum extraction table
    traceTables(
        *[
            [
                [i for i in range(1, n, step)],
                ["{:.3e}".format(val) for val in maxHeapExtractMaxDuration],
                ["{:.3e}".format(val) for val in linkedListExtractMaxDuration],
                ["{:.3e}".format(val) for val in sortedLinkedListExtractMaxDuration],
            ],
            (
                "Nr elementi",
                "Max Heap",
                "Lista concatenata",
                "Lista concatenata ordinata",
            ),
            "Tempo di estrazione del massimo",
        ]
    )

    # Draw insertion table
    traceTables(
        *[
            [
                [i for i in range(1, n, step)],
                ["{:.3e}".format(val) for val in maxHeapInsertDuration],
                ["{:.3e}".format(val) for val in linkedListInsertDuration],
                ["{:.3e}".format(val) for val in sortedLinkedListInsertDuration],
            ],
            (
                "Nr elementi",
                "Max Heap",
                "Lista concatenata",
                "Lista concatenata ordinata",
            ),
            "Tempo di inserimento dei valori",
        ]
    )

    # --------------------------------------------------------------------------------------------------------------
    print("END, DEBUG")
