#!/bin/bash

def text_of(filename):
    with open(filename,'r') as fp:
        return fp.read()

def swap_letters(kl={})
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

######################################################

if __name__ == '__main__':
    pass