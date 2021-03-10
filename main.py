from task1_1 import ModelWithoutQueue
from task1_2 import ModelWithBoundedQueue

if __name__ == '__main__':
    model_without_queue = ModelWithBoundedQueue()
    model_with_bounded_queue = ModelWithBoundedQueue()

    # ModelWithoutQueue.solve()
    model_with_bounded_queue.solve()
