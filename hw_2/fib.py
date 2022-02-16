def fibonacci(n):
    numbers = [1, 1]
    for i in range(n - 2):
        numbers.append(numbers[i] + numbers[i + 1])
    return numbers[:n]
