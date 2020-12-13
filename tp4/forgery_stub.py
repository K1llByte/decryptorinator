#!/usr/bin/python

import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

AES_BLOCK_LENGTH = 16 # bytes
AES_KEY_LENGTH = 32 # bytes

# Insecure CBCMAC
def cbcmac(key, msg, iv):
    if not _validate_key_and_msg(key, msg):
        return False
    
    #iv = b'\x00' * 16
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    tag = encryptor.update(msg) + encryptor.finalize()
    
    return tag[-5:]

def verify(key, msg, tag, iv):
    if not _validate_key_and_msg(key, msg):
        return False

    new_tag = cbcmac(key, msg, iv)
    return new_tag == tag
    # If parameters are valid, then recalculate the mac.
    # Implement this recalculation.

    # return True/False


# Forges a new message with the same tag for the given iv
# The new message's first block is xor'd with the iv used 
# to calculate the tag, and the new iv is going to be zeros 
def produce_forgery(msg, iv, tag):
    new_msg = bytes([_a ^ _b for _a, _b in zip(iv, msg[:AES_BLOCK_LENGTH])]) + msg[AES_BLOCK_LENGTH:]
    new_tag = tag
    new_iv = b'\x00' * 16
    return (new_msg, new_iv, new_tag)

def check_forgery(key, new_msg, new_iv, new_tag, original_msg):
    if new_msg == original_msg:
        print("Having the \"forged\" message equal to the original " +
            "one is not allowed...")
        return False

    if verify(key, new_msg, new_tag, new_iv) == True:
        print("MAC successfully forged!")
        return True
    else:
        print("MAC forgery attempt failed!")
        return False

def _validate_key_and_msg(key, msg):
    if type(key) is not bytes:
        print("Key must be array of bytes!")
        return False
    elif len(key) != AES_KEY_LENGTH:
        print("Key must be have %d bytes!" % AES_KEY_LENGTH)
        return False
    if type(msg) is not bytes:
        print("Msg must be array of bytes!")
        return False
    elif len(msg) != 2*AES_BLOCK_LENGTH:
        print("Msg must be have %d bytes!" % (2*AES_BLOCK_LENGTH))
        return False
    return True

def main():
    key = os.urandom(AES_KEY_LENGTH)
    msg = os.urandom(32)
    iv = os.urandom(16)

    tag = cbcmac(key, msg, iv)

    # Should print "True".
    print(verify(key, msg, tag, iv))

    (mprime, ivprime, tprime) = produce_forgery(msg, iv, tag)

    # GOAL: produce a (message, tag) that fools the verifier.
    check_forgery(key, mprime, ivprime, tprime, msg)

if __name__ == '__main__':
    main()