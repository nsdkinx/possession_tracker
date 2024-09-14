import random


def generate_random_int_id() -> int:
    """Generates a random 10 numbers long int ID"""
    return int(
        ''.join([str(random.randint(0, 9)) for _ in range(10)])
    )
