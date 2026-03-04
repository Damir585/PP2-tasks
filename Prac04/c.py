def countdown(n):
    for i in range(0, n +1):
        yield n - i

n = int(input())
for c in countdown(n):
    
    print(c)