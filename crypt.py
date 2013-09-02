#!/usr/bin/env python

import Cryptsy
from ciphvar import *
import os
import getpass
from hashlib import sha512
import ConfigParser

Config = ConfigParser.ConfigParser()
Config.read('./crypt.conf')
retries = 0
pw = getpass.getpass('Password: ')

pub = Config.get('Api-Key', 'pub')
key = Config.get('Api-Key', 'key').decode('string_escape')

#print sha512(pw).hexdigest() 

while retries < 3:
    # @TODO: Pull hash from Database
    if sha512(pw).hexdigest() == '70bd6161ae1cdbd61857e2009e19d0e620452004037394c5340fdb3f158ae958384efeaa407e9f41df00191edec8b01ff675f1420d2194eb75fa4307e3c6ed3f':
            key = decrypt(key, pw)
            print key
            break
    else:
        pw = getpass.getpass('Incorrect Password, try again...')
        retries += 1
del pw

#os.rename('crypt.enc', 'crypt.conf')
#print 'Key:\t:' + key
#print 'Priv:\t:' + key

marketd = Cryptsy.Cryptsy(pub, key)
datum = marketd.getMarkets()
print datum
for x in datum['return']:
    print "%s Vol:  %s" %(x['primary_currency_code'], x['current_volume'])