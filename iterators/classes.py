class Test:
    def __init__(self, limite):
        self.limite = limite
        self.atual = 0

    # An special method that when you do next(x) runs this function
    # The logic here its, what gonna happend/return when the next() its called
    def __next__(self):
        self.atual += 2
        if self.atual > self.limite:
            raise StopIteration
        else:
            return self.atual


    # An special method in python that allows you to use iter()
    # The logic here its, what object will gonna be used when iter() its called, here I passed the self, so the object all their selfs
    def __iter__(self):
        print(f'Iterator called')
        return self

    
obj = Test(limite = 5)
obj_iter = iter(obj)


print(f'Printing class normal: {obj}')
print(f'Printing obj iterator: {obj_iter}')
print(f'Show the first number of the object class: {next(obj_iter)}')
print(f'Show the second number of the object class: {next(obj_iter)}')
print(f'Show the third number of the object class: {next(obj_iter)}') # Goes be an error StopIteration