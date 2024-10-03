# Bonus
import os, sys

base_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(base_dir, "output")

def fizzbuzz(n: int, divisors: dict) -> list:
    result = []
    for i in range(1, n+1):
        res = ""
        for divisor, word in divisors.items():
            if i % divisor == 0:
                res += word
        result.append(res or str(i))
    return result

def write_to_file(n: int, results: list):
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"{n}.txt")
    with open(file_path, 'w') as f:
        f.write("\n".join(results))

def process_number(n: int, divisors: dict) -> list | ValueError:
    try:
        n = int(n)
        if n < 1:
            raise ValueError("Number must be greater than 0")
        results = fizzbuzz(n, divisors)
        write_to_file(n, results)
        print(f"> Results for {n} exported in Algo/output/{n}.txt")
        print("\n".join(results), "\n")
        return results
    except ValueError as ve:
        print(f"> ValueError({n}): {ve}")
        return ve

def parse_divisors(input_string: str) -> dict | None:
    divisors = {}
    rules = input_string.split(' ')
    for rule in rules:
        try:
            divisor, word = rule.split(':')
            divisors[int(divisor)] = word
        except ValueError:
            print(f"Skipping invalid rule: {rule}")
    return divisors

if "-h" in sys.argv or "--help" in sys.argv or len(sys.argv) > 1:
    help_message = """Usage: python fizzbuzz.py

    Example:
    python3 Algo/fizzbuzz.py
    > Enter divisor rules (by default: 3:Fizz 5:Buzz): 3:Fizz 5:Buzz 7:Woof
    > Enter a number: 15
    """
    print(help_message)
    exit(0)

divisor_inputs = input("Enter divisor rules (by default: 3:Fizz 5:Buzz): ")
if not divisor_inputs:
    divisors = {3: "Fizz", 5: "Buzz"}
else:
    divisors = parse_divisors(divisor_inputs)
    if not divisors:
        exit(ValueError("No valid divisor rule found"))

while True:
    number = input("Enter a number: ")
    if not number:
        print("Please enter a valid number")
        continue

    process_number(number, divisors)
