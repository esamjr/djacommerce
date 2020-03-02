import hashlib
import random


def activation_code(key):
    salt = hashlib.sha256(str(random.random()).encode(
        'utf-8')).hexdigest()[:16].encode('utf-8')
    return hashlib.sha256(str(key+salt).encode('utf-8')).hexdigest()[18:50]

