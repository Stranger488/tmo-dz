from task1_1 import ModelWithoutQueue
from task1_2 import ModelWithBoundedQueue
from task1_3 import ModelWithInfiniteQueue
from task1_4 import ModelWithLeft

from task2 import ModelProduction

if __name__ == '__main__':
    model_without_queue = ModelWithoutQueue()
    model_with_bounded_queue = ModelWithBoundedQueue()
    model_with_infinite_queue = ModelWithInfiniteQueue()
    model_with_left = ModelWithLeft()

    model_production = ModelProduction()

    # model_without_queue.solve()
    # model_with_bounded_queue.solve()
    # model_with_infinite_queue.solve()
    # model_with_left.solve()

    model_production.solve()
