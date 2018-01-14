import base64

from M2Crypto import RSA, BIO, Rand, m2, EVP, X509

from aadhaar_demo_auth.exceptions import InvalidConfiguration


class DemoAuthEncryptor:
    """
    Encryption for various data elements like session key, pid xml etc
    """

    def __init__(self, cfg, pub_key=None):
        self._cfg = cfg
        self._public_key = pub_key
        self._algo = cfg.common.encryption_algorithm

    def x509_get_cert_expiry(self):
        """
        UIDAI certificate expiry date
        """
        if not self._public_key:
            raise InvalidConfiguration("Public Key missing")
        x509 = X509.load_cert(self._public_key)
        return x509.get_not_after().__str__()

    def x509_encrypt(self, data):
        """
        Encrypt using x509 public key of UIDAI
        """
        x509 = X509.load_cert(self._public_key)
        rsa = x509.get_pubkey().get_rsa()
        return rsa.public_encrypt(data, RSA.pkcs1_padding)

    # Reference: http://stackoverflow.com/questions/5003626/problem-with-m2cryptos-aes
    def aes_encrypt(self, key, msg, iv=None):
        """
        Encrypt a msg using a plain string as key
        """
        iv = '\0' * 16 if iv is None else base64.b64decode(iv)
        # op 1 is for encryption
        cipher = EVP.Cipher(alg=self._algo, key=key, iv=iv, op=1)
        message = cipher.update(msg)
        return message + cipher.final()
