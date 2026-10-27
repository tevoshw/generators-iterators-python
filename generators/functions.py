def func():
    print(f'Starting')
    yield 1
    print(f'Mid')
    yield 2
    print(f'Finishing')
    yield 3

x = func()

print(next(x))
print(next(x))
print(next(x))