from task1_1 import ModelWithoutQueue
from task1_2 import ModelWithBoundedQueue
from task1_3 import ModelWithInfiniteQueue

if __name__ == '__main__':
    model_without_queue = ModelWithBoundedQueue()
    model_with_bounded_queue = ModelWithBoundedQueue()
    mode_with_infinite_queue = ModelWithInfiniteQueue()

    # model_without_queue.solve()
    # model_with_bounded_queue.solve()
    mode_with_infinite_queue.solve()
