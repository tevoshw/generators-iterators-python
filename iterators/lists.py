list =  [10, 20, 30, 40, 50, 60]

list_iter = iter(list)


print(f'Show the list: {list}')
print(f'Show the iter list: {list_iter}')
print(f'Show the first number of the list number: {next(list_iter)}')
print(f'Show the second number of the list number: {next(list_iter)}')
print(f'Show the fourth number of the list number: {next(list_iter)}')
print(f'Show the fifth number of the list number: {next(list_iter)}')
print(f'Show the sixth number of the list number: {next(list_iter)}')
print(f'Show the seventh number of the list number: {next(list_iter)}')

