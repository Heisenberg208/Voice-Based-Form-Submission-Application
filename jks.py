import math

def harmonic_sum(n):
    if n == 0:
        return 0.0
    elif n == 1:
        return 1.0
    elif n == 2:
        return 1.5
    else:
        return round(math.log(n) + 0.577, 2)  # Approximation for larger n

n = int(input("Enter a positive integer: "))
print(harmonic_sum(n))
