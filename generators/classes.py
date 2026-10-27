class Test:
    def __init__(self, numbers):
        self.numbers = numbers

    def __iter__(self):
        for n in self.numbers:
            yield n

obj =  Test([1, 2, 3, 4, 5, 6, 7])
for x in obj:
    print(x)