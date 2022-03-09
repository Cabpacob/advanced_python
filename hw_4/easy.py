from fib import fibonacci
import time
from threading import Thread
from multiprocessing import Process


def time_it(function):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = function(*args, **kwargs)
        return (time.time() - start, result)

    return wrapper


fibonacci_n = 10**5


@time_it
def test_time(entity):
    l = []
    for _ in range(10):
        l.append(entity(target=fibonacci, args=(fibonacci_n, )))

    for e in l:
        e.start()

    for e in l:
        e.join()


if __name__ == '__main__':
    class StupidThread:
        def __init__(self, *, target, args):
            self.__target = target
            self.__args = args

        def start(self):
            self.__target(*self.__args)

        def join(self):
            pass


    with open('artifacts/easy_timing.txt', 'w') as f:
        f.write(f'current thread: {test_time(StupidThread)[0]} s\n')
        f.write(f'multithreading: {test_time(Thread)[0]} s\n')
        f.write(f'multipriocessing: {test_time(Process)[0]} s\n')
