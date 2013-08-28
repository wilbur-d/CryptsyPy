#!/usr/bin/env python

import Cryptsy
import ciphile
import sys
import os
import getpass
from hashlib import md5, sha512

retries = 0
pw = getpass.getpass('Password: ')
print sha512(pw).hexdigest() 
while retries < 3:
	if sha512(pw).hexdigest() == '70bd6161ae1cdbd61857e2009e19d0e620452004037394c5340fdb3f158ae958384efeaa407e9f41df00191edec8b01ff675f1420d2194eb75fa4307e3c6ed3f':
		with open('crypt.conf', 'rb') as in_file, open('crypt.enc', 'wb') as out_file:
			ciphile.encrypt(in_file, out_file, pw)
			break
	else:
		pw = getpass.getpass('Incorrect Password, try again...')
		retries += 1


del pw

os.rename('crypt.enc', 'crypt.conf')

marketd = Cryptsy.Cryptsy(key, secret)
datum = marketd.getMarkets()
print datum['return'][0]['high_trade']
for x in datum['return']:
    print "%s Vol:  %s" %(x['primary_currency_code'], x['current_volume'])
