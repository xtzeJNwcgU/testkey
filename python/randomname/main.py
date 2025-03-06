import random
import string

def generate_random_string(length=8):
    if length < 1:
        raise ValueError("Panjang string harus minimal 1.")
    
    letters = string.ascii_letters + string.digits
    random_string = 'xbb' + ''.join(random.choices(letters, k=length-1))
    
    return random_string

# Contoh penggunaan
print(generate_random_string(10))
