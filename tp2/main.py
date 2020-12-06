#!/bin/python3

# Convert Letter to value
def l2i(c):
    return ord(c)-65

# add_module('A',1) -> 'B'
def add_module(c,k):
    # 'c' is a chr in [65,90]
    # 'k' is a ord in [0,26[
    # returns chr in [65,90]
    return chr((ord(c)-65 + k) % 26 + 65)

# sub_module('A',1) -> 'Z'
def sub_module(c,k):
    # 'c' is a chr in [65,90]
    # 'k' is a ord in [0,26[
    # returns chr in [65,90]
    res = ord(c) - k
    if res < 65:
        res += 26
    return chr(res)


def str_sub_module(c1,c2,operation):
    SIZE = len(c1)
    res = ""
    for i in range(SIZE):
        res += operation(c1[i],l2i(c2[i]))
    return res

def aux(ciphertext1,ciphertext2):
    if len(ciphertext1) != len(ciphertext2):
        print("Strings must be of same size")
        exit(1)

    SIZE = len(ciphertext1)

    c1_c2 = str_sub_module(ciphertext1, ciphertext2, sub_module)

    res = c1_c2

    counter = 0
    for c in res:
        if c == 'A':
            counter += 1
    #print(counter)
    return counter


if __name__ == '__main__':
    ciphertexts = []
    
    with open("ciphertexts.txt", "r") as fp:
        while line := fp.readline():
            ciphertexts.append(line[:-1])
            fp.readline()

    reduced_ciphertexts = [ c[0:3] for c in ciphertexts ]

    list_to_use = ciphertexts

    i = 0
    highest = (-1,-1,0)
    while i < (len(list_to_use)-1):
        j = i+1
        while j < len(list_to_use):
            ciphertext1 = list_to_use[i]
            ciphertext2 = list_to_use[j]
            
            val = aux(ciphertext1, ciphertext2)
            print(val,"",end="")
            print("({},{}):".format(i+1,j+1))
            if val > highest[2]:
                highest = (i+1,j+1,val)
            j += 1
        i += 1
    print("Highest:",highest)