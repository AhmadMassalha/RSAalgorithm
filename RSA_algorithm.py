import random
import sympy
import re

# euclids gcd algorithm
def euclid(a,b):
    if b == 0:
        return a
    else:
        r = a % b
        a = b
        b = r
        return euclid(a,b)
    
    
# modular power algorithm
def mod_pow(a,b,n):
    if b == 0:
        return 1
    if b % 2 == 0:
        return mod_pow(a,b/2,n)*mod_pow(a,b/2,n) % n
    else:
        return a*mod_pow(a,b-1,n) % n
    
# generate two primes in a tuple using sympy.randprime 
def gen_two_prime():
    return (sympy.randprime(100,1000),sympy.randprime(100,1000))
    
# make private key and public key
def make_private_and_public():
    (q,p) = gen_two_prime()
    #print(q,'|',p)    
    n = q*p
    euler = (p-1)*(q-1)
    while True:
        e = random.randint(1,euler)
        if euclid(e,euler) == 1:
            break
    while True:
        d = random.randint(0,euler)
        if e*d%euler == 1:
            break
    print('private:{',d,',',n,'}')
    print('public:{',e,',',n,'}')
    return {'private': (d,n) , 'public' : (e,n) }


# convert str into int using alphabitical values
# devided by 0
def my_convert_str_int(s):
    def alph_ord(c):
        return ord(c.lower()) - ord('a') + 1
    out = ''
    for x,c in enumerate(s):
        out+= str(alph_ord(c))
        if x != len(s)-1:
            out+= '0'
    return int(out)

# convert back to str
def my_convert_int_str(num):
    def get_alphabetic_character(order):
        return chr(ord('A') + order - 1)
    
    num_str = str(num)
    pattern = r'0(?=[1-9])'
    final = ''
    result = re.split(pattern, num_str)
    for i in result:
        final += get_alphabetic_character(int(i)).lower()
    return final


# RSA encrypt
def encrypt(M, public_tuple):
    if my_convert_str_int(M) > public_tuple[1]:
        return None
    
    return pow(my_convert_str_int(M),public_tuple[0]) % public_tuple[1]

# RSA dycrypt
def decrypt(C, private_tuple):
    return pow(C,private_tuple[0]) % private_tuple[1]

# encrypt big message using RSA
def encrypt_big_message(s,public_tuple):
    if len(s) % 2 != 0:
        s += '#'
    s_list = [s[i:i+2] for i in range(0, len(s), 2)]
    returned = ''
    for x,i in enumerate(s):
        returned += str(encrypt(i,public_tuple))
        if x != len(s) - 1:
            returned += '|'
    return returned

# decrypt big message using RSA
def decrypt_big_message(C, private_tuple):
    c_list = C.split('|')
    message = ''
    for n in c_list:
        message += my_convert_int_str(decrypt(int(n), private_tuple))
    return message


# tests
"""converted = my_convert_str_int('amh')
print('ConvertedInt:',converted)
print('ConvertedStr:',my_convert_int_str(converted))"""


keys = make_private_and_public()
print('Keys:' , keys)

encrypted_message = encrypt_big_message('hihowareyoumynameisahmad',keys['public'])
print('EYNC: ', encrypted_message)
print('DYC:',decrypt_big_message(encrypted_message, keys['private']))


