from OpenSSL import crypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
import base64

class cert_key(object):

    def __init__(self,cert,private_key):
        self.cert=cert
        self.private_key=private_key
        self.cert_obj = crypto.load_certificate(crypto.FILETYPE_PEM,self.cert)
        self.public_key=self.get_public_key()

    def get_public_key(self):
        public_key = crypto.dump_publickey(crypto.FILETYPE_PEM, self.cert_obj.get_pubkey()).decode("utf-8")
        return public_key

    def get_expired_time(self):
        return self.cert_obj.get_notAfter().decode()

    def get_subject_domain(self):
        domain=""
        for name,subdomain in self.cert_obj.get_subject().get_components():
            if not domain:
                domain = subdomain.decode()
            else:
                domain = domain+','+subdomain.decode()
        return domain

    # 获取额外的域名，不稳定，有时候得到的扩展不是域名，推荐用上面那个
    def get_extension_domain(self):
        index=self.cert_obj.get_extension_count()-1
        extension_domain=str(self.cert_obj.get_extension(index)).replace("DNS:","")
        return extension_domain


    def rsa_encrypt(self,message):
        """校验RSA加密 使用公钥进行加密"""
        cipher = Cipher_pkcs1_v1_5.new(RSA.importKey(self.public_key))
        cipher_text = base64.b64encode(cipher.encrypt(message.encode())).decode()
        return cipher_text


    def rsa_decrypt(self,text):
        """校验RSA加密 使用私钥进行解密"""
        cipher = Cipher_pkcs1_v1_5.new(RSA.importKey(self.private_key))
        retval = cipher.decrypt(base64.b64decode(text), 'ERROR').decode('utf-8')
        return retval

    def verify(self):
        try:
            cipher_text=self.rsa_encrypt("ok")
            result=self.rsa_decrypt(cipher_text)
            return result
        except Exception as e:
            result='fail'
            return  result