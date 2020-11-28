#!/bin/python

import re
import random

def text_of(filename):
    with open(filename,'r') as fp:
        return fp.read()

def swap_letters(txt,kl={}):
    res = ""
    for c in txt:
        if c in kl.keys():
            res += kl[c]
        else:
            res += c
    return res


def match(arg,wordsfile='words.txt'):
    arg = '^{}$'.format(arg.lower().replace('.','[a-zA-Z]'))
    res = []
    with open(wordsfile,'r') as ws:
        for line in ws:
            res.extend(re.findall(arg,line))
    return res


def confidence(matches):
    return 1 / len(matches)

def mk_dot(txt):
    i = 0
    res = ''
    for c in txt:
        res += '.' if c.isupper() else c
    return res

def mono_decoder_aux(txt):

    words_list = re.split('[ \n().,]',txt)
    
    # Remove all occurrences of the empty
    # element '' from the split 
    words_set = set(filter(lambda e : '' != e and not e.islower(), words_list))
    
    matches_by_confidence = []
    max_tuple = None
    for word in words_set:
        matched = match(mk_dot(word))
        if len(matched):
            tmp = (confidence(matched),matched,word)
            matches_by_confidence.append(tmp)
            if max_tuple == None or max_tuple[0] < tmp[0]:
                max_tuple = tmp
    
    if max_tuple == None:
        return

    def __extract_letter_translation(matches,word):
        res = {}
        i = 0
        selected_match = random.choice(matches)
        for c in word:
            tmp = ord(c)
            # Check if is Uppercase letter
            if tmp >= 65 and tmp <= 90:
                res[c] = selected_match[i]
            i += 1

        return res
        
    for c,l,w in matches_by_confidence:
        if(max_tuple[0] == c):
            print('Confidence:',max_tuple[0],'| Word:',max_tuple[2],'Matched as:',max_tuple[1])
            return __extract_letter_translation(max_tuple[1],max_tuple[2])

def mono_decoder(txt,kl={}):
    known_letters = kl

    def is_decrypted(txt):
        for c in txt:
            c = ord(c)
            if c >= 65 and c <= 90:
                return False
        return True


    txt = swap_letters(txt,kl=known_letters)
    while not is_decrypted(txt):
        tmp = mono_decoder_aux(txt)
        if tmp == None:
            raise Exception('This decryption iteration is unviable')
        known_letters.update(tmp)
        txt = swap_letters(txt,kl=known_letters)
    return txt

###################### Vigenère ######################



def rot_char(char,key_char,inverse=False):
    key = ord(key_char) - 65
    c = ord(char)
    if c >= 65 and c <= 90:
        c += -key if inverse else key
        if c > 90: # Overflow
            c -= 26
        elif c < 65: # Underflow
            c += 26
    return chr(c+32)

def vigenere_decode(txt):
    # def rot_by_key(word,key):
    #     res = ''
    #     for i in range(len(key)):
    #         if len(word) > i:
    #             res += rot_char(word[i],key[i],True)
    #         else:
    #             return res
    #     return res + word[i+1:]

    def rot_by_key_all(txt,key):
        i = 0
        res = ''
        for c in txt:
            tmp = ord(c)
            if tmp >= 65 and tmp <= 90:
                res += rot_char(c,key[i],True)
            else:
                res += c
            
            i += 1
            if len(key) <= i:
                i = 0
        return res

    key = 'DFLVY'
    # DFLVY
    #key = 'AOD'
    #key = 'DFL'
    #key = 'AFB'

    # DFL       | the wgezbdly es thw gtoqdl wv our
    # DFLBBB    | the aqezbfpi es xrw gvsadl yz our
    # DFLCCCCCC | the zpfckdly hb wqw gurzeo wv pxa

    return rot_by_key_all(txt,key)

    """ selected_word = words_list[0]
    must_match = ['the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'any', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use']
    for a in range(26):
        for b in range(26):
            for c in range(26):
                key = chr(a+65) + chr(b+65) + chr(c+65)
                #print(key)
                if swap_by_key(selected_word,key) in must_match:
                    print(key)
                    print(swap_by_key(selected_word,key))
                    return key
    return None """

######################################################

if __name__ == '__main__':
    c2_kl={
        'J':'t', # Assuming: JHA -> the, JGG -> too
        'G':'o', # Assuming: JHA -> the, JGG -> too
        'A':'e', # Assuming: JHA -> the, JGG -> too
        'H':'h', # Assuming: JHA -> the, JGG -> too
        'S':'i', # Hinted by the letter frequency swap
        #'Y':'s',
        #'V':'n',
        #'L':'f',
        #'W':'g',
        #'E':'c',
        #'I':'a', 
        #'Q':'w', # Qhat -> what
        #'N':'r', # waNNant -> warrant
        #'U':'u',
        #'Z':'l', 
        #'C':'q', # reCuire -> require
        #'P':'d', # entitleP -> entitled
        #'M':'y', # necessarM -> necessary
        #'F':'v', # indiFiduals -> individuals
        #'K':'m', # Kiscellaneous -> miscellaneous
        #'R':'p', # RhilosoRhy -> philosophy
        #'T':'b', # Tut -> but
        #'D':'j', # Dudgment -> judgment
        #'B':'x', # eBisting -> existing
        #'O':'k' # manOind -> mankind
    }

    known_letters = {
        #'G':'t',
        #'U':'a', # thUt -> that
        #'V':'s', # haV -> has
        #'I':'o', # tI -> to
        #'T':'r', # tToRNOe -> trouble
        #'R':'u', # tToRNOe -> trouble
        #'N':'b', # tToRNOe -> trouble
        #'O':'l', # tToRNOe -> trouble
        #'S':'w', # Sho -> who
        #'H':'i', # Hts -> its
        #'J':'p', # oJJose -> oppose
        #'C':'n', # Ceither -> neither
        #'B':'m', # eBpire -> empire (EXTRACTED OUT OF THE DECODED CONTEXT)
        #'M':'c', # whiMh -> which
        #'A':'y', # capacitA -> capacity
        #'K':'g', # lonK -> long
        #'F':'v', # ciFilisation -> civilisation
        #'Z':'f', # Zrom -> from
        #'L':'d', # LestroyeL -> destroyed
        #'L':'d', # taPe -> take (EXTRACTED OUT OF THE DECODED CONTEXT)
        #'Y':'q', # vanYuished -> vanquished
        #'P':'k', # liPe -> like
    }

    # ciphertext = text_of('cryptogram2.txt')
    # #mixtext = swap_letters(ciphertext,kl=known_letters)
    # plaintext = ""
    # try:
    #     plaintext = mono_decoder(ciphertext,kl=c2_kl)
    # except Exception as e:
    #     print(e)

    # TODO: Decryption Accuracy rate value with
    # matching the words in plaintext with the 
    # words in the words file 

    # print(plaintext)

    # Vigenere (AOD)
    print(vigenere_decode(text_of('cryptogram1.txt')))

    

# W=22
# M=12
# P=15

# T=19
# H=7
# E=4

# 22-19=3
# 12-7=5
# 15-4=11

# D
# F
# L