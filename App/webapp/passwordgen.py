from hashlib import sha3_256
from werkzeug.security import  generate_password_hash,check_password_hash
def encode(s):
    return generate_password_hash(s)

def decode(gen,password):
    return check_password_hash(gen,password)


if __name__ == '__main__':
    s='qqqq'
    gen=encode(s)
    print(gen)
    original=decode(gen,s)
    print(original)