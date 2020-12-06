#!/bin/python3


# add_module('A',1) -> 'B'

def l2i(c):
    return ord(c)-65

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


def sub_mod(c,k):
    return chr( (ord(c)-65 - k) % 26 + 65)

# def aux(ciphertext1, ciphertext2):
#     for i in range(26):
#         for j in range(26):
#             t1 = i#chr(65+i)
#             t2 = j#chr(65+j)

#             c1 = ord(ciphertext1[0])
#             k1 = c1 - t1
#             if k1 < 65:
#                 k1 += 26

#             c2 = ord(ciphertext2[0])
#             k2 = c2 - t2
#             if k2 < 65:
#                 k2 += 26

#             if k1 == k2:
#                 print(chr(c1),chr(c2))

def operacao(c1,c2,operation):
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

    c1_c2 = operacao(ciphertext1, ciphertext2, sub_module)
    #print("c1_c2:",c1_c2)
    
    #c2_c1 = operacao(ciphertext2, ciphertext1)
    #print("c2_c1:",c2_c1)

    #res = operacao(c1_c2, c2_c1)

    res = c1_c2


    counter = 0
    for c in res:
        if c == 'A':
            counter += 1
    #print(counter)
    return counter

    # if res == 'A'*SIZE:
    #     print("WE HAVE A MATCH")
    # else:
    #     print("nothing")



def aux2(c1,c2,c3):
    if len(c1) != len(c2) or len(c1) != len(c2):
        print("Strings must be of same size")
        exit(1)

    SIZE = len(ciphertext1)

    key2 = operacao(c2, c1, sub_module)
    ''



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


    # highest = (-1,-1,0)
    # for i in range(len(list_to_use)):
    #     for j in range(len(list_to_use)):
    #         if i != j:
    #             ciphertext1 = list_to_use[i]
    #             ciphertext2 = list_to_use[j]

                
    #             val = aux(ciphertext1, ciphertext2)
    #             print(val,"",end="")
    #             print("({},{}):".format(i+1,j+1))
    #             if val > highest[2]:
    #                 highest = (i,j,val)
    # print("Highest:",highest)


    # for i in range(len(list_to_use)):
    #     for j in range(len(list_to_use)):
    #         for k in range(len(list_to_use)):
    #             if k != j or j != i:
    #                 ciphertext1 = list_to_use[i]
    #                 ciphertext2 = list_to_use[j]
    #                 ciphertext3 = list_to_use[k]

    #                 aux2(ciphertext1, ciphertext2, ciphertext3)

    #print(add_module('G', l2i('Z')))
    #print(add_module('C', 26-l2i('I')))

    #print(operacao("MWI","MCJ",add_module))

    #print(sub_mod('T',l2i('K')))