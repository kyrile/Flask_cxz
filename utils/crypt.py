import hashlib


def pwd(text):
    md5_crypt = hashlib.md5()
    md5_crypt.update(text.encode('utf-8'))
    md5_crypt.update('cxz'.encode('utf-8'))
    return md5_crypt.hexdigest()
