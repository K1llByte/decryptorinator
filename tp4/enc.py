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
data["nonce"] = os.urandom(16)

# This message is considered to be always with utf-8 encoding
msg = "Isto é uma mensagem não muito secreta!"

# Encrypt using ChaCha20 the text
def enc_bytes(plaintext_bytes,key,nonce):
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None)
    ciphertext = cipher.encryptor().update(plaintext_bytes)
    return ciphertext
    
# Get the HMAC of the bytes
def get_mac(text_bytes, key):
    h = hmac.HMAC(key, hashes.SHA256())
    h.update(text_bytes)
    return h.finalize()

######## Excryption Schemes ########

# Encrypt Then MAC
def etm():
    ciphertext = enc_bytes(msg.encode("utf-8"), KEY, data["nonce"])
    mac = get_mac(ciphertext,HMAC_KEY)
    data["encrypted"] = ciphertext + mac

    w2f("dados-etm.dat", data)

# Encrypt And MAC
def eam():
    ciphertext = enc_bytes(msg.encode("utf-8"), KEY, data["nonce"])
    mac = get_mac(msg.encode("utf-8"), HMAC_KEY)
    data["encrypted"] = ciphertext + mac

    w2f("dados-eam.dat", data)

# MAC Then Encrypt 
def mte():
    mac = get_mac(msg.encode('utf-8'), HMAC_KEY)
    data["encrypted"] = enc_bytes(msg.encode('utf-8')+mac, KEY, data["nonce"])
    
    w2f("dados-mte.dat", data)

####################################

def w2f(file_name, data):
    # File structure:
    # NONCE{16b}:ENCRYPTED:EOF
    with open(file_name, 'wb') as f:
        f.write(data["nonce"])
        f.write(data["encrypted"])

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
