#!/bin/python

# Compute prime factorization
def prime_factorization(n):
    i = 2
    res = []
    while i*i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            res.append(i)
    if n > 1:
        res.append(n)
    return res

# Greatest common divisor
def gcd(a,b):
    r = a % b
    return b if r == 0 else gcd(b, r)

# Least Common Multiple
def lcm(a,b):
    return (a*b) // gcd(a,b)

# Encoding accordingly to specified scheme
def encode(l1,l2,l3):
    return 729*l1 + 27*l2 + l3

# Decoding accordingly to specified scheme
def decode(n):
    l3 = n % 27
    v1 = n - l3
    l1 = v1 // 729
    v2 = v1 - l1*729
    l2 = v2 // 27
    return (l1,l2,l3)

# Convert numeric values 0-26 to uppercase
# characters [A-Z] or a whitespace 
def num_to_char(n):
    # 26 is whitespace
    if n == 26:
        return ' '
    elif n < 0 or n > 25:
        raise Exception()
    else:
        return chr(n+65)

# Convert a valid chatacter to the corresponding number 0-26
def char_to_num(c):
    if c == ' ':
        # whitespace is 26
        return 26
    else:
        tmp = ord(c)
        if tmp < 65 or tmp > 90:
            raise Exception()
        else:
            return tmp-65


# Decrypt ciphertext with key 'd' and 'n'
# and decode the resulting integer in the specified scheme
# returns the result plaintext string
def rsa_dec(cipher,d,n):
    res = ""
    for c in cipher:
        l1,l2,l3 = decode((c**d) % n)
        res += num_to_char(l1)
        res += num_to_char(l2)
        res += num_to_char(l3)
    return res


if __name__ == '__main__':
    arr = []
    # Open ciphertext file and fill the array with its integers 
    with open('ciphertext.txt') as f:
        while line := f.readline():
            tmp = int(line)
            arr.append(tmp)

    e = 17
    n = 213271

    # Prime factorization    
    factors = prime_factorization(n)
    p = factors[0]
    q = factors[1]

    # Compute 'd'
    d = pow(e, -1,lcm(p-1,q-1))
    # Decrypt everithing
    res = rsa_dec(arr,d,n)
    print(res)
    