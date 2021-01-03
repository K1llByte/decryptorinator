#!/usr/bin/python

import socket
import threading
import sys, signal
import os
import random

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

from cryptography.x509 import load_pem_x509_certificate
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.asymmetric.padding import PSS, MGF1, PKCS1v15

from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.serialization import load_pem_private_key

AES_BLOCK_LEN = 16 # bytes
AES_KEY_LEN = 32 # bytes
PKCS7_BIT_LEN = 128 # bits
SOCKET_READ_BLOCK_LEN = 6144 # bytes


def signal_handler(sig, frame):
    print('You pressed Ctrl+C; bye...')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


# An useful function to open files in the same dir as script...
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
def path(fname):
    return os.path.join(__location__, fname)

host = "localhost"
port = 8080

# RFC 3526's parameters. Easier to hardcode...
p = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF
g = 2
params_numbers = dh.DHParameterNumbers(p,g)
parameters = params_numbers.parameters()


# Load Client's Private Key
private_key = None
with open(path("TC_Client.key.pem"), "rb") as key_file:
    private_key = load_pem_private_key(key_file.read(), password=None)
  
# Load Client's x509 Certificate, Public Key
public_key = None
certificate_as_bytes = None
with open(path("TC_Client.cert.pem"), "rb") as cert_file:
    certificate_as_bytes = cert_file.read()
    cert = load_pem_x509_certificate(certificate_as_bytes)
    public_key = cert.public_key()
    #print("public_key:",public_key)


def connect():
    #Attempt connection to server
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        return sock
    except Exception as e:
        print("Could not make a connection to the server: %s" % e)
        input("Press enter to quit")
        sys.exit(0)


# Receives and returns bytes.
def encrypt(k, m):
    padder = padding.PKCS7(PKCS7_BIT_LEN).padder()
    padded_data = padder.update(m) + padder.finalize()
    iv = os.urandom(AES_BLOCK_LEN)
    cipher = Cipher(algorithms.AES(k), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ct = encryptor.update(padded_data) + encryptor.finalize()
    return iv+ct


# Receives and returns bytes.
def decrypt(k, c):
    iv, ct = c[:AES_BLOCK_LEN], c[AES_BLOCK_LEN:]
    cipher = Cipher(algorithms.AES(k), modes.CBC(iv))
    decryptor = cipher.decryptor()
    pt = decryptor.update(ct) + decryptor.finalize()
    unpadder = padding.PKCS7(PKCS7_BIT_LEN).unpadder()
    pt = unpadder.update(pt) + unpadder.finalize()
    return pt


def handshake(socket):
    # ========== Client: Handshake Description ========== #
    # (1) Client -> Server : gx.                          #
    #    (1.1) Set DH parameters and generate private (x) #
    #          and exponential (gx).                      #
    #    (1.2) Send exponential (gx)                      #
    #                                                     #
    # (2) Client <- Server : gy, CertB, EK(SB(gy, gx)).   #
    #    (2.1) Receive server's exponential, certificate  #
    #          and encrypted signature                    #
    #    (2.2) Compute shared secret key.                 #
    #    (2.3) Verify certificate validation              #
    #    (2.4) Verify encrypted signature                 #
    #                                                     #
    # (3) Client -> Server : CertA, EK(SA(gx, gy)).       #
    #    (3.1) Make encrypted signature EK(SA(gx, gy)).   #
    #        (3.1.1) Concatenate gx and gy (client's      #
    #                exponential and server's             #
    #                exponential).                        #
    #        (3.1.2) Sign gx_gy using client's asymmetric #
    #                private key A.                       #
    #        (3.1.3) Encrypt gx_gy using shared key.      #
    #    (3.2) Concatenate CertA, EK(SA(gx, gy)) and      #
    #          send to server.                            #
    # =================================================== #

    # (1)
    # (1.1)
    dh_x = parameters.generate_private_key()
    dh_g_x = dh_x.public_key()
    dh_g_x_as_bytes = dh_g_x.public_bytes( \
        Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)

    # (1.2)
    socket.sendall(dh_g_x_as_bytes)

   

    # (2.1)
    SEPARATOR = b"\r\n\r\n"
    try:
        gy_cert_sae = socket.recv(SOCKET_READ_BLOCK_LEN)
    except:
        print("Something went wrong during handshake ...")
        return None
    
    tmp = gy_cert_sae.split(SEPARATOR)
    dh_g_y_as_bytes = tmp[0]
    dh_g_y = load_pem_public_key(dh_g_y_as_bytes)
    server_certificate = load_pem_x509_certificate(tmp[1])
    server_public_key = server_certificate.public_key()
    sae = tmp[2]
    
    # (2.2)
    shared_key = dh_x.exchange(dh_g_y)
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=None,
    ).derive(shared_key)
    
    
    # (2.3)
    if not validate_certificate(server_certificate):
        print("Invalid Certificate")
        return None

    # (2.4)
    message_and_signature = decrypt(derived_key,sae)
    tmp2 = message_and_signature.split(SEPARATOR)
    gy_gx = tmp2[0] + SEPARATOR + tmp2[1]
    signature = tmp2[2]

    try:
        verify(server_public_key,gy_gx,signature)
    except Exception as e:
        print(e)
        print("Invalid Signature")
        return None

    
    # (3)
    # (3.1)
    # (3.1.1)
    SEPARATOR = b"\r\n\r\n"
    gx_gy = dh_g_x_as_bytes + SEPARATOR + dh_g_y_as_bytes

    # (3.1.2) and (3.1.2)
    signed_and_encrypted = encrypt(derived_key, gx_gy + SEPARATOR + sign(private_key,gx_gy))

    # (3.2)
    cert_sae = certificate_as_bytes + SEPARATOR + signed_and_encrypted
    socket.sendall(cert_sae)

    return derived_key


def process(socket):
    print("Going to do handshake... ")
    k = handshake(socket)
    if k is None:
        print("FAILED.")
        return False
    print("done.")

    while True:
        pt = input("Client message: ")
        if len(pt) > 0:
            msg_to_send = encrypt(k, pt.encode("utf-8"))
            print("encrypted msg:",msg_to_send)
            socket.sendall(msg_to_send)
        else:
            socket.close()
            break
        try:
            data = socket.recv(SOCKET_READ_BLOCK_LEN)
            pt = decrypt(k, data)
            print(pt.decode("utf-8"))
        except:
            print("You have been disconnected from the server")
            break


# Sign message using private assymetric key 
# to ensure data entegrity
def sign(private_key, message):
    signature = private_key.sign(
        message,
        PSS(mgf=MGF1(hashes.SHA256()),
                salt_length=PSS.MAX_LENGTH),
        hashes.SHA256())
    return signature


# Verify messages signature using corresponding 
# public assymetric key to ensure data entegrity
def verify(server_public_key, message, signature):
    server_public_key.verify(
        signature,
        message,
        PSS(mgf=MGF1(hashes.SHA256()),
                salt_length=PSS.MAX_LENGTH),
                hashes.SHA256())


# Receives the certificate object (not the bytes).
def validate_certificate(certificate, debug = False):
    ca_public_key = None
    ca_cert = None
    with open(path("TC_CA.cert.pem"), "rb") as cert_file:
        ca_cert = load_pem_x509_certificate(cert_file.read())
        ca_public_key = ca_cert.public_key()

    if ca_cert.subject.get_attributes_for_oid(NameOID.COUNTRY_NAME)[0].value != \
            certificate.issuer.get_attributes_for_oid(NameOID.COUNTRY_NAME)[0].value:
        debug and print("Mismatched field: %s" % NameOID.COUNTRY_NAME)
        return False

    if ca_cert.subject.get_attributes_for_oid(NameOID.STATE_OR_PROVINCE_NAME)[0].value != \
            certificate.issuer.get_attributes_for_oid(NameOID.STATE_OR_PROVINCE_NAME)[0].value:
        debug and print("Mismatched field: %s" % NameOID.STATE_OR_PROVINCE_NAME)
        return False

    if ca_cert.subject.get_attributes_for_oid(NameOID.LOCALITY_NAME)[0].value != \
            certificate.issuer.get_attributes_for_oid(NameOID.LOCALITY_NAME)[0].value:
        debug and print("Mismatched field: %s" % NameOID.LOCALITY_NAME)
        return False

    if ca_cert.subject.get_attributes_for_oid(NameOID.ORGANIZATION_NAME)[0].value != \
            certificate.issuer.get_attributes_for_oid(NameOID.ORGANIZATION_NAME)[0].value:
        debug and print("Mismatched field: %s" % NameOID.ORGANIZATION_NAME)
        return False

    if ca_cert.subject.get_attributes_for_oid(NameOID.ORGANIZATIONAL_UNIT_NAME)[0].value != \
            certificate.issuer.get_attributes_for_oid(NameOID.ORGANIZATIONAL_UNIT_NAME)[0].value:
        debug and print("Mismatched field: %s" %
            NameOID.ORGANIZATIONAL_UNIT_NAME)
        return False

    if ca_cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value != \
            certificate.issuer.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value:
        debug and print("Mismatched field: %s" % NameOID.COMMON_NAME)
        return False

    if certificate.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value != "TC Server":
        debug and print("Wrong field (server cert): %s" % NameOID.COMMON_NAME)
        return False

    ca_public_key.verify(
        certificate.signature,
        certificate.tbs_certificate_bytes,
        PKCS1v15(),
        certificate.signature_hash_algorithm)
    return True


def main():
    s = connect()
    process(s)


if __name__ == '__main__':
  main()
