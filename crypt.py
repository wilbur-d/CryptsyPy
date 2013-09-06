#!/usr/bin/env python

import Cryptsy
from ciphvar import *
import os
import getpass
from hashlib import sha512
from passlib import hash
import ConfigParser
import sqlite3

db = 'cobot.db'
def getCreds(dbname, uname):
    conn = sqlite3.connect(dbname)
    cont = conn.cursor()
    cont.execute('SELECT hash FROM users WHERE user=?', uname)
    return cont.fetchone()[0].split('$')[3]

hashCheck = getCreds(db, ('geod',))
print hashCheck



Config = ConfigParser.ConfigParser()
Config.read('./crypt.conf')
retries = 0
pw = getpass.getpass('Password: ')

pub = Config.get('Api-Key', 'pub')
key = Config.get('Api-Key', 'key').decode('string_escape') # decode() is necesary to strip
														   # extra escape chars

#print sha512(pw).hexdigest() 

while retries < 3:
    # @TODO: Pull hash from Database
    if hash.sha512_crypt.encrypt(pw, salt='HX', rounds=5000) == hashCheck:
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