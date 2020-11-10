#!/bin/bash

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

import re

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

def mono_decoder(txt):

    words_list = re.split('[ \n().,]',txt)
    
    # Remove all occurrences of the empty
    # element '' from the split 
    words_set = set(filter(lambda e : '' != e and not e.islower(), words_list))
    
    matches_by_confidence = []
    max_tuple = None
    for word in words_set:
        #print(word)
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
        selected_match = matches[0]
        for c in word:
            tmp = ord(c)
            # Check if is Uppercase letter
            if tmp >= 65 and tmp <= 90:
                res[c] = selected_match[i]
            i += 1

        return res
        
    for c,l,w in matches_by_confidence:
        if(max_tuple[0] == c):
            print('Confidence:',max_tuple[0])
            return __extract_letter_translation(max_tuple[1],max_tuple[2])


######################################################

if __name__ == '__main__':
    known_letters = {
        'G':'t',
        'Q':'h',
        'X':'e',
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

    ciphertext = text_of('cryptogram3.txt')
    mixtext = swap_letters(ciphertext,kl=known_letters)
    plaintext = mono_decoder(mixtext)
    print(plaintext)