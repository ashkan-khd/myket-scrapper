import random
import string


def rand_slug(length: int) -> str:
    letters = string.digits + string.ascii_lowercase + string.ascii_uppercase
    result_str = "".join(random.choice(letters) for _ in range(length))
    return result_str
