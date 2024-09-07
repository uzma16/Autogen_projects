Sure, here is a simple Python code to find the factorial of a number.

```python
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

num = int(input("Enter a number: "))
if num < 0:
   print("Sorry, factorial does not exist for negative numbers")
elif num == 0:
   print("The factorial of 0 is 1")
else:
   print("The factorial of", num, "is", factorial(num))
```

This program asks for a number from the user, checks if the number is negative, zero or positive. If the number is positive, it calls the factorial function to calculate the factorial of the number. The factorial function uses recursion to calculate the factorial.