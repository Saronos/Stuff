import string
import random

def generate_short_code(length=6):
    """Genera un código corto aleatorio."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))