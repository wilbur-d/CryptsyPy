#!/usr/bin/env python

from hashlib import sha512
from passlib import hash
from ciphvar import *
import ConfigParser
import getpass
import sqlite3
import Cryptsy

db = 'cobot.db'
Config = ConfigParser.ConfigParser()
Config.read('./crypt.conf')
cryptsyPub = Config.get('Api-Key', 'pub')
cryptsyKey = Config.get('Api-Key', 'key').decode('string_escape')   # decode() is necesary to strip
                                                                    # extra escape chars
def getCreds(dbname, uname):
    conn = sqlite3.connect(dbname)
    cont = conn.cursor()
    cont.execute('SELECT hash FROM users WHERE user=?', uname)
    hashSplice = cont.fetchone()[0]
    return (hashSplice.split('$')[2], hashSplice.split('$')[3])
    conn.close()


def logIn():
    hashsalt, hashdb = getCreds(db, ('geod',))

    pw = getpass.getpass('Password: ')

    hashCheck = hash.sha512_crypt.encrypt(pw, salt=hashsalt, rounds=5000).split('$')[3]

    retries = 3
    for retry in range(0,retries):
        if hashCheck == hashdb:
                global cryptsyKey 
                cryptsyKey = decrypt(cryptsyKey, pw)
                print cryptsyKey
                return True
        else:
            print 'Incorrect Password, Try Again.'
            pw = getpass.getpass('Password: ')
    del pw
    return False
    

if logIn():
    marketd = Cryptsy.Cryptsy(cryptsyPub, cryptsyKey)
    datum = marketd.getMarkets()
    print datum
    for x in datum['return']:
        print "%s Vol:  %s" %(x['primary_currency_code'], x['current_volume'])