# Cyphertext #2

The letter frequency table generated was:

|J|A|I|V|S|G|H|Y|Z|N|P|E|U|L|K|Q|T|R|W|M|F|O|C|D|B|X|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|12.2034| 11.6102| 8.5593| 7.7119| 7.6271| 7.4576| 6.2712| 5.5085| 4.0678| 3.8136| 3.6441| 3.1356| 3.1356| 2.4576| 2.4576| 2.2034| 1.6949| 1.6949| 1.4407| 1.3559| 1.2712| 0.339| 0.1695| 0.0847| 0.0847| 0.0|

The letter frequency table created for this text doesn't match any special word easy to deduce (it only helped find the letter I that was the S).

So the next step is to manually find some absolute letters translations to try find some words.

The hint word i'll find now is a 3 letter word with 2 equal letters at the end `JGG`

This ciphered word could be '_too_' or '_all_', The word i think it represents is the first one because i suspect the word `JHA` is '_the_'

One letter is not present in this cryptogram, the letter: _X_

. . .

# Cyphertext #3

This text seems easier because the letter frequency swap showed some complete words such as `THE`, `AT`, `THEM`

This words found could obviously wrong and be just a coincidence but for a start we'll assume

GQX -> THE

Exacly the same strategy of the Cyphertext #2

Three letters are not present in this cryptogram, the letter: `D`, `E` and `W`

# Cyphertext #1

The Vigenere cipher was a little harder a lucky to decipher manually, the inicial take for the cipher was to assume that 
the inicial `WMP` was a `THE`, this was just a hint because it could be other words.

To make the `WMP` become a `THE` we subtractred the characters to obtain the key for that substitution that was `DFL`

Decrypting the text with vigénere with only the key `DFL`,
at first sight we can capture the presence of the word `our` in the first sentence, this could be a coincidence, but we assumed not.

The next step we thought was to extend the key with `A`'s to see if any word could be deduced, with 2 `A`'s the result wasn't clear 
but we could defenitly have hints of what words could be in the text, such as `oribgn` for `origin`, `whei` for `when`, `of` ...

'n' + {value} = 'i'

i = 8

n = 13

value = 13-8 = -5

The positive of -5 is 26-5 = 21

21 is the letter `V`

With this information we tried the key `DFLVA`

At this point our suspects were right and the `origgn` word matched almost perfectly so we did one more subtitution of the `g` for `i` obtaining `Y`.

The key now was `DFLVY` and we could defenitly see the plain text declaring this as completed

<!-- All the cipher texts were decrypted with help of a `match` function and the words.txt file -->

___
# Monoalphabetic decryptor

Reference for the 3000 most used words in english:

https://www.ef.com/wwen/english-resources/english-vocabulary/top-3000-words/

