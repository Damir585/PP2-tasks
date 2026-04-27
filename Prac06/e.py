s = input()
vowels = "aieouAEIOU"

if any(ch in vowels for ch in s):
    print("Yes")
else:
    print("No")