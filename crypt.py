#!/usr/bin/env python

from hashlib import sha512
from passlib import hash
from ciphvar import *
import ConfigParser
import getpass
import sqlite3
import Cryptsy

global db = 'cobot.db'

def getCreds(dbname, uname):
    conn = sqlite3.connect(dbname)
    cont = conn.cursor()
    cont.execute('SELECT hash FROM users WHERE user=?', uname)
    hashSplice = cont.fetchone()[0]
    return (hashSplice.split('$')[2], hashSplice.split('$')[3])


Config = ConfigParser.ConfigParser()
Config.read('./crypt.conf')

cryptsyPub = Config.get('Api-Key', 'pub')
cryptsyKey = Config.get('Api-Key', 'key').decode('string_escape')   # decode() is necesary to strip
                                                                    # extra escape chars


hashsalt, hashdb = getCreds(db, ('geod',))

pw = getpass.getpass('Password: ')

hashCheck = hash.sha512_crypt.encrypt(pw, salt=hashsalt, rounds=5000).split('$')[3]

retries = 0
while retries < 3:
    if hashCheck == hashdb:
            cryptsyKey = decrypt(cryptsyKey, pw)
            print cryptsyKey
            break
    else:
        pw = getpass.getpass('Incorrect Password, try again...')
        retries += 1
del pw

marketd = Cryptsy.Cryptsy(cryptsyPub, cryptsyKey)
datum = marketd.getMarkets()
print datum
for x in datum['return']:
    print "%s Vol:  %s" %(x['primary_currency_code'], x['current_volume'])