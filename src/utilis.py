import random
import string

charSet = string.digits + string.ascii_letters

def generate_short_code(length = 6):
    generated_code = ''.join(random.choices(charSet, k=length))
    return generated_code

if __name__ == '__main__':
    print('--- Testing generate_short_code ---')

    for _ in range(5):
        print(generate_short_code())
    print('-' * 25)

    print('Generating a code with 10 characters')
    print(generate_short_code(10))
    print('--- Test complete ---')
