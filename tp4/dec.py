#!/usr/bin/python

import os, sys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, hmac
# Gerar dois arrays (diferentes!!) de bytes de tamanhos adequados, a utilizar
# como chave para a cifra e para o mac. Estes valores deverão estar hardcoded em
# ambos ficheiros enc.py e dec.py.
KEY = b'\xa7\xdcrc6o\t\xcf\x0co\xbe}Sb\xc3\xcf\xe5\x88\xa8\xb6H\xcfry1\xdfQ\x85K"\xf5|' # 32 bytes
HMAC_KEY = b'\x94\x0e\x9d[R\\\xfb\xf5\x9aU\xeeb\xf6!s\xd7\xd4\xfb\xfeL\x02s\xc6\xdb\xeb\xf6r\xff1\xa9\xf8\xfc' # 32 bytes

data = {}

def rff(file_name):
    # File structure:
    # NONCE{16b}:ENCRYPTED:EOF
    with open(file_name, 'rb') as f:
        data["nonce"] = f.read(16)
        data["encrypted"] = f.read()
        return data

# Decrypt bytes using ChaCha20
def dec_bytes(ciphertext, key, nonce):
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None)
    plaintext = cipher.decryptor().update(ciphertext)
    return plaintext

# Verify the validation of the mac to the text
def verify_mac(msg_bytes, mac_bytes, key):
    h = hmac.HMAC(key, hashes.SHA256())
    h.update(msg_bytes)
    h.verify(mac_bytes)

######## Decryption Schemes ########
# Encrypt Then MAC
def etm():
    data = rff("dados-etm.dat")
    mac = data["encrypted"][-32:]
    ciphertext = data["encrypted"][:-32]
    try:
        verify_mac(ciphertext, mac, HMAC_KEY)
        plaintext = dec_bytes(ciphertext, KEY, data["nonce"])
        print(plaintext.decode('utf-8'))
    except:
        print('Could not verify data integrity')

# Encrypt And MAC
def eam():
    data = rff("dados-eam.dat")
    mac = data["encrypted"][-32:]
    ciphertext = data["encrypted"][:-32]
    plaintext = dec_bytes(ciphertext, KEY, data["nonce"])
    try:
        verify_mac(plaintext, mac, HMAC_KEY)
        print(plaintext.decode('utf-8'))
    except:
        print('Could not verify data integrity')

# MAC Then Encrypt 
def mte():
    data = rff("dados-mte.dat")
    plaintext_mac = dec_bytes(data["encrypted"], KEY, data["nonce"])
    mac = plaintext_mac[-32:]
    plaintext = plaintext_mac[:-32]
    try:
        verify_mac(plaintext, mac, HMAC_KEY)
        print(plaintext.decode('utf-8'))
    except:
        print('Could not verify data integrity')

####################################

def main():

    if len(sys.argv) != 2:
      print("Please provide one of: eam, etm, mte")
    elif sys.argv[1] == "eam":
      eam()
    elif sys.argv[1] == "etm":
      etm()
    elif sys.argv[1] == "mte":
      mte()
    else:
      print("Please provide one of: eam, etm, mte")

if __name__ == '__main__':
    main()
