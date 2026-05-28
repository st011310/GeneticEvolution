import random

def generateIntMatrix(m = None, n = None, min_val=10, max_val = 100):
    if n is None:
        n = random.randint(4, 10)
    if m is None:
        m = n
    return [
        [random.randint(min_val, max_val) for _ in range(m)]
                for _ in range(n)
    ]
