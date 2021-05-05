class IterFib:
    def __iter__(self):
        return self
    def __init__(self, val):
        self.val = val
        self.val1 = 0
        self.val2 = 1
    def __next__(self):
        if self.val2 < self.val:
            self.temp = self.val2
            self.val2 = self.val1 + self.val2
            self.val1 = self.temp
            return self.val1
        else:
            raise StopIteration


iter = IterFib(1000)


for i in iter:
    print(i)