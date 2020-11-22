#!/bin/python3

from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers.modes import CBC, ECB
from os import urandom

# File / Image encryption
def enc_image(filename, dest_file, key, mode):
    KEY_SIZE = len(key)
    # AES Object to encrypt
    aes_instance = Cipher(AES(key), mode)
    encryptor = aes_instance.encryptor()

    bytes = None
    # Open target file in binary mode only for read
    with open(filename,'rb') as img:
        bytes = img.read()
        bytes += (KEY_SIZE - (len(bytes) % KEY_SIZE))*b'\x00'
        enc = encryptor.update(bytes) + encryptor.finalize()

    # Create a new file with the encrypted content
    with open(dest_file,'wb+') as dest:
        dest.write(enc)

# File / Image decryption
def dec_image(filename, dest_file, key, mode):
    aes_instance = Cipher(AES(key), mode)
    decryptor = aes_instance.decryptor()

    bytes = None
    # Open target file in binary mode only for read
    with open(filename,'rb') as img:
        bytes = img.read()
        dec = decryptor.update(bytes) + decryptor.finalize()

    # Create a new file with the decrypted content
    with open(dest_file,'wb+') as dest:
        # Write the decrypted bytes to file
        dest.write(dec)


if __name__ == '__main__':
    # Generate a random initialization vector
    #iv = urandom(16)
    # Generate a random key
    #key = urandom(32)
    # Encrypt image to a new file with CBC mode
    #enc_image('ex1.bmp', 'ex1.enc.bmp', key, CBC(iv))
    # Decrypt image to a new file with CBC mode
    #dec_image('ex1.enc.bmp', 'ex1.dec.bmp', key, CBC(iv))

    # Generate a random key
    key = urandom(32)
    # Encrypt image to a new file with ECB mode
    enc_image('ex1.bmp', 'ex1.enc.bmp', key, ECB())
    # Encrypt image to a new file with ECB mode
    dec_image('ex1.enc.bmp', 'ex1.dec.bmp', key, ECB())