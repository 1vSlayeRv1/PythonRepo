import datetime


def timer(func):
    def wrapper(val):
        time = datetime.datetime.now()
        func(val)
        print("Время выполнения =", datetime.datetime.now() - time)

    return wrapper


class IterFib:
    def __iter__(self):
        self.val1 = 0
        self.val2 = 1
        return self
    def __init__(self):
        iter(self)
    def __next__(self):
        self.val1, self.val2 = self.val2, self.val1 + self.val2
        return self.val1


iterator = IterFib()

@timer
def fib(val):
    for i in range(val):
        print(next(iterator))


fib(100)
