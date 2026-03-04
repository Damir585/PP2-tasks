def square(a, b):
    for i in range(a , b+ 1):
        yield i * i

a, b = map(int, input().split())
for c in square(a, b):
    print(c)