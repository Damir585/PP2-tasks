n = int(input())
numbers=list(map(int , input().split()))
u_numbers = set(numbers)
print(*sorted(u_numbers))