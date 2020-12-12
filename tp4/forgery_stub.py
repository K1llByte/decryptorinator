#!/usr/bin/python

import os
# import relevant cryptographic primitives

AES_BLOCK_LENGTH = 16 # bytes
AES_KEY_LENGTH = 32 # bytes

# Insecure CBCMAC.
def cbcmac(key, msg):
  if not _validate_key_and_msg(key, msg): return False

  # Implement CBCMAC with either a random IV, or with a tag consisting of all
  # ciphertext blocks.

  # return tag

def verify(key, msg, tag):
  if not _validate_key_and_msg(key, msg): return False

  # If parameters are valid, then recalculate the mac.
  # Implement this recalculation.

  # return True/False


# Receives a pair consisting of a message, and a valid tag.
# Outputs a forged pair (message, tag), where message must be different from the
# received message (msg).
# ---> Note that the key CANNOT be used here! <---
def produce_forgery(msg, tag):
  # Implement a forgery, that is, produce a new pair (m, t) that fools the
  # verifier.

  # return (new_msg, new_tag)

def check_forgery(key, new_msg, new_tag, original_msg):
  if new_msg == original_msg:
    print("Having the \"forged\" message equal to the original " +
        "one is not allowed...")
    return False

  if verify(key, new_msg, new_tag) == True:
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
  key = os.urandom(32)
  msg = os.urandom(32)

  tag = cbcmac(key, msg)

  # Should print "True".
  print(verify(key, msg, tag))

  (mprime, tprime) = produce_forgery(msg, tag)

  # GOAL: produce a (message, tag) that fools the verifier.
  check_forgery(key, mprime, tprime, msg)

if __name__ == '__main__':
  main()
