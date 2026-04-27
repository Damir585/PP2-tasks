n = int(input())

a =list( map(int , input().split()))
min = min(a)
max = max(a)
for i in range(n):
    if a[i] == max:
        a[i]= min

print(*a)
