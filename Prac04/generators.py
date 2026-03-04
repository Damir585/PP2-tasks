
def number_generator(n):
    for i in range(1, n + 1):
        yield i

def even_numbers(n):
    for i in range(0, n + 1, 2):
        yield i


if __name__ == "__main__":
    print("Numbers:")
    for num in number_generator(5):
        print(num)

    print("Even numbers:")
    for num in even_numbers(10):
        print(num)