#!/usr/bin/env python
from hashlib import md5
from Crypto.Cipher import AES
from Crypto import Random

def derive_key_and_iv(password, salt, key_length, iv_length):
    d = d_i = ''
    while len(d) < key_length + iv_length:
        d_i = md5(d_i + password + salt).digest()
        d += d_i
    return d[:key_length], d[key_length:key_length+iv_length]

def encrypt(invar, password, key_length=32):
    bs = AES.block_size
    salt = Random.new().read(bs)
    print salt
    key, iv = derive_key_and_iv(password, salt, key_length, bs)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    return salt + cipher.encrypt(invar)

def decrypt(invar, password, key_length=32):
    bs = AES.block_size
    salt = invar[:bs]
    #print salt
    key, iv = derive_key_and_iv(password, salt, key_length, bs)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    return cipher.decrypt(invar[16:])

"""
msg = 'Tootsy rollzaaaaaaPOLZANYUKUH TOOGE12312938a;sldkfj'
msg = encrypt(msg, 'toot')

print msg

msg = decrypt(msg, 'toot')

print msg"""