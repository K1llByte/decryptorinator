#!/usr/bin/python

import socket
import threading
import signal, sys
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

# An useful function to open files in the same dir as script...
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
def path(fname):
  return os.path.join(__location__, fname)

host = "localhost"
port = 8080
connections = []
total_connections = 0

# RFC 3526's parameters. Easier to hardcode...
p = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF
g = 2
params_numbers = dh.DHParameterNumbers(p,g)
parameters = params_numbers.parameters()

AES_BLOCK_LEN = 16 # bytes
AES_KEY_LEN = 32 # bytes
PKCS7_BIT_LEN = 128 # bits
SOCKET_READ_BLOCK_LEN = 4096 # bytes


def signal_handler(sig, frame):
    print('You pressed Ctrl+C; bye...')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


class Client(threading.Thread):
    def __init__(self, socket, address, id, name):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.name = name

        # Don't wait for child threads (client connections) to finish.
        self.daemon = True

        self.dh_y = None
        self.dh_g_y = None
        self.dh_g_y_as_bytes = None
        self.dh_g_x_as_bytes = None
        self.dh_g_x = None
  
        # Symmetric (shared) key
        self.key = None
  
        # Private key from the server's certificate
        self.private_key = None
        with open(path("TC_Server.key.pem"), "rb") as key_file:
            self.private_key = load_pem_private_key(key_file.read(), password=None)
  
        # Certificate and public key from the server's certificate
        self.public_key = None
        self.certificate_as_bytes = None
        with open(path("TC_Server.cert.pem"), "rb") as cert_file:
            self.certificate_as_bytes = cert_file.read()
            cert = load_pem_x509_certificate(self.certificate_as_bytes)
            self.public_key = cert.public_key()
            print("self.public_key:",self.public_key)
  
        self.client_certificate = None
        self.client_public_key = None


    def __str__(self):
        return str(self.id) + " " + str(self.address)


    # Receives and returns bytes.
    def encrypt(self, m):
        padder = padding.PKCS7(PKCS7_BIT_LEN).padder()
        padded_data = padder.update(m) + padder.finalize()
        iv = os.urandom(AES_BLOCK_LEN)
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv))
        encryptor = cipher.encryptor()

        ct = encryptor.update(padded_data) + encryptor.finalize()
        return iv+ct


    # Receives and returns bytes.
    def decrypt(self, c):
        #return c # delete this...

        iv, ct = c[:AES_BLOCK_LEN], c[AES_BLOCK_LEN:]
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        pt = decryptor.update(ct) + decryptor.finalize()
        unpadder = padding.PKCS7(PKCS7_BIT_LEN).unpadder()
        pt = unpadder.update(pt) + unpadder.finalize()
        return pt


    def handshake(self, debug = False):
        # ============== Handshake Description ============== #
        # (1) Client -> Server : gx.                          #
        #    (1.1) Set DH parameters and generate private (y) #
        #          and exponential (gy).                      #
        #    (1.2) Receive Client's exponential (gx)          #
        #          also generated like the server.            #
        #                                                     #
        # (2) Client <- Server : gy, CertB, EK(SB(gy, gx)).   #
        #    (2.1) Compute shared secret key.                 #
        #    (2.2) Make encrypted signature EK(SB(gy, gx)).   #
        #        (2.2.1) Concatenate gy and gx (server's      #
        #                exponential and client's             #
        #                exponential).                        #
        #        (2.2.2) Sign gy_gx using server's asymmetric #
        #                private key B.                       #
        #        (2.2.3) Encrypt gy_gx using shared key.      #
        #    (2.3) Concatenate gy, CertB, EK(SB(gy, gx)) and  # 
        #          send to client.                            #
        #                                                     #
        # (3) Client -> Server : CertA, EK(SA(gx, gy)).       #
        #    (3.1) Receive Client's certificate and encrypted #
        #          signature.                                 #
        #    (3.2) Verify certificate validation              #
        #    (3.3) Verify encrypted signature                 #
        # =================================================== #

        # (1)
        # (1.1)
        self.dh_y = parameters.generate_private_key()
        self.dh_g_y = self.dh_y.public_key()
        self.dh_g_y_as_bytes = self.dh_g_y.public_bytes( \
            Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)

        # (1.2)
        try:
            self.dh_g_x_as_bytes = self.socket.recv(SOCKET_READ_BLOCK_LEN)
            self.dh_g_x = load_pem_public_key(self.dh_g_x_as_bytes)
        except Exception as e:
            #print(e)
            print("Something went wrong during handshake ...")
            return False

        # (2.1)
        shared_key = self.dh_y.exchange(self.dh_g_x)
        self.key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=None,
        ).derive(shared_key)

        # (2.2)
        # (2.2.1)
        SEPARATOR = b"\r\n\r\n"
        gy_gx = self.dh_g_y_as_bytes + SEPARATOR + self.dh_g_x_as_bytes

        # (2.2.2) and (2.2.3)
        signed_and_encrypted = self.encrypt(gy_gx + SEPARATOR + self.sign(gy_gx))

        # (2.3)
        gy_cert_sae = self.dh_g_y_as_bytes + SEPARATOR + self.certificate_as_bytes + SEPARATOR + signed_and_encrypted
        self.socket.sendall(gy_cert_sae)

        # (3.1)
        try:
            cert_sae = self.socket.recv(SOCKET_READ_BLOCK_LEN)
        except Exception as e:
            #print(e)
            print("Something went wrong during handshake ...")
            return False

        tmp = cert_sae.split(SEPARATOR)
        self.client_certificate = load_pem_x509_certificate(tmp[0])
        self.client_public_key = self.client_certificate.public_key()
        
        # (3.2)
        if not self.validate_certificate():
            print("Invalid Certificate")
            return False
        sae = tmp[1]
        signed_msg = self.decrypt(sae)
        tmp = signed_msg.split(SEPARATOR)
        gx_gy = tmp[0]
        signature = tmp[1]

        # (3.3)
        try:
            self.verify(gx_gy,signature)
        except:
            print("Invalid Signature")
            return False

        print("> Finished")
        return True


    def run(self):
        print("Going to do handshake for client " + str(self.address) + "... ")
        hs = self.handshake()
        
        if hs is None or self.key is None:
            print("FAILED.")
            print("Client " + str(self.address) + ": closing connection.")
            self.socket.close()
            connections.remove(self)
            return False
        print("done.")

        data = ""
        while True:
            try:
                data = self.socket.recv(SOCKET_READ_BLOCK_LEN)
            except:
                pass
            if len(data) > 0:
                pt = self.decrypt(data)
                print("ID " + str(self.id) + ": " + pt.decode("utf-8"))
    
                self.socket.sendall(self.encrypt("Server received: ".encode("utf-8") + pt))
            else:
                print("Client " + str(self.address) + " has disconnected")
                self.socket.close()
                connections.remove(self)
                break


    # Message is bytes.
    def sign(self, message):
        signature = self.private_key.sign(
        message,
        PSS(mgf=MGF1(hashes.SHA256()),
                salt_length=PSS.MAX_LENGTH),
        hashes.SHA256())
        return signature


    # Message and signature bytes.
    def verify(self, message, signature):
        self.client_public_key.verify(
            signature,
            message,
            PSS(mgf=MGF1(hashes.SHA256()),
                    salt_length=PSS.MAX_LENGTH),
                    hashes.SHA256())


    # Receives the certificate object (not the bytes).
    def validate_certificate(self, debug = False):
        certificate = self.client_certificate

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

        if certificate.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value != "TC Client":
            debug and print("Wrong field (server cert): %s" % NameOID.COMMON_NAME)
            return False

        ca_public_key.verify(
            certificate.signature,
            certificate.tbs_certificate_bytes,
            PKCS1v15(),
            certificate.signature_hash_algorithm)

        return True


def main():
    # Create new server socket. Set SO_REUSEADDR to avoid annoying "address
    # already in use" errors, when doing Ctrl-C plus rerunning the server.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(5)

    # Create new thread to wait for connections.
    while True:
        client_socket, address = sock.accept()
        global total_connections
        connections.append(Client(client_socket, address, total_connections, "Name"))
        connections[len(connections) - 1].start()
        total_connections += 1
    for t in connections:
        t.join()


if __name__ == '__main__':
  main()
