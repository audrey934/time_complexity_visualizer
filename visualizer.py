import time
import matplotlib
matplotlib.use('Agg')  # save to file
import matplotlib.pyplot as plt
from stackqueue import Stack, Queue
from collections import deque


# Visualizer 
def time_complexity_visualizer(algorithm, n_min, n_max, n_step, save_path):
    times = []
    input_sizes = list(range(n_min, n_max + 1, n_step))

   
    fig, ax = plt.subplots()
    ax.set_xlabel('Input size')
    ax.set_ylabel('Running time (seconds)') 
    ax.set_title('Algorithm time complexity visualization (Live)')
    line, = ax.plot([], [], 'o-')

    for i, n in enumerate(input_sizes):
        run = algorithm(n)
        start_time = time.perf_counter()
        run()
        end_time = time.perf_counter()
        times.append(end_time - start_time)

        line.set_data(input_sizes[:i + 1], times)
        ax.relim()
        ax.autoscale_view()
      

    plt.ioff()
    fig.savefig(save_path)
    plt.close(fig)
    return input_sizes, times

# Algorithms

def linear_search(n):
    data = list(range(n))
    target = n  # not in the list -> worst case, checks every element

    def run():
        for item in data:
            if item == target:
                return True
        return False
    return run


def binary_search(n):
    data = list(range(n))  # sorted, as binary search requires
    target = n  

    def run():
        low, high = 0, n - 1
        while low <= high:
            mid = (low + high) // 2
            if data[mid] == target:
                return mid
            if data[mid] < target:
                low = mid + 1
            else:
                high = mid - 1
        return -1
    return run


def bubble_sort(n):
    data = list(range(n, 0, -1))  
    def run():
        for i in range(n):
            for j in range(n - i - 1):
                if data[j] > data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]
    return run


def nested_loops(n):
    def run():
        count = 0
        for _ in range(n):
            for _ in range(n):
                count += 1
        return count
    return run



def selection_sort(n):
    data = list(range(n, 0, -1))

    def run():
        for i in range(n):
            smallest = i
            for j in range(i + 1, n):
                if data[j] < data[smallest]:
                    smallest = j
            data[i], data[smallest] = data[smallest], data[i]
    return run


def insertion_sort(n):
    data = list(range(n, 0, -1))  # reversed -> worst case

    def run():
        for i in range(1, n):
            key = data[i]
            j = i - 1
            while j >= 0 and data[j] > key:
                data[j + 1] = data[j]
                j -= 1
            data[j + 1] = key
    return run

def stack_push_pop(n):
    def run():
        s = Stack()
        for i in range(n):
            s.push(i)
        while not s.is_empty():
            s.pop()
    return run


def queue_enqueue_dequeue(n):
    def run():
        q = Queue()
        for i in range(n):
            q.enqueue(i)
        while not q.is_empty():
            q.dequeue()  # pop(0): this is the slow part
    return run

# Other algorithms for queue and stack
def stack_balanced_parens(n):
    # n pairs, e.g. n=3 -> "((()))" (already balanced -> worst case, no early exit)
    text = "(" * n + ")" * n

    def run():
        s = Stack()
        for char in text:
            if char == "(":
                s.push(char)
            else:
                if s.is_empty():
                    return False
                s.pop()
        return s.is_empty()
    return run



def queue_deque_enqueue_dequeue(n):
    def run():
        d = deque()
        for i in range(n):
            d.append(i)
        while d:
            d.popleft()
    return run


ALGORITHMS = {
    "linear_search": linear_search,
    "binary_search": binary_search,
    "bubble_sort": bubble_sort,
    "nested_loops": nested_loops,
    "selection_sort": selection_sort,
    "insertion_sort": insertion_sort,
    "stack_push_pop": stack_push_pop,
    "stack_balanced_parens": stack_balanced_parens,
    "queue_enqueue_dequeue": queue_enqueue_dequeue,
    "queue_deque_enqueue_dequeue": queue_deque_enqueue_dequeue,

}



