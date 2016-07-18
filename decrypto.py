__author__ = 'CirnoTxm'
from charm.toolbox.pairinggroup import PairingGroup,GT,pair
from charm.core.math.pairing import hashPair as sha1
from charm.schemes.abenc.abenc_waters09 import CPabe09
from charm.toolbox.symcrypto import SymmetricCryptoAbstraction
from charm.core.engine.util import objectToBytes,bytesToObject
import json
import os
debug = True
keyUrl = '/Users/cirnotxm/down/key/'
configUrl = '/Users/cirnotxm/down/config/down_config'

with open(configUrl,"rb") as f:
    ss = f.read()

s = eval(ss)

fileUrl= s[0]
fileName = s[1]
asl = s[2]

asl = eval(asl)

if debug :
    print fileUrl
    print fileName
    print type(asl)

groupObj = PairingGroup('SS512')
cpabe = CPabe09(groupObj)

keyFile = keyUrl+fileName

with open(keyFile+'.mk',"rb") as fmk:
    mk = fmk.read()


with open(keyFile+".pk","rb") as fpk:
    pk = fpk.read()

with open(keyFile+".ci","rb") as fci:
    cipher = fci.read()

# print mk+"\n"
# print pk+"\n"
# print cipher+"\n"

mk = bytesToObject(mk,groupObj)
pk = bytesToObject(pk,groupObj)
cipher = bytesToObject(cipher,groupObj)

sk = cpabe.keygen(pk,mk,asl)

print sk

try:
    plaintext = cpabe.decrypt(pk,sk,cipher)
except:
    print "Error"

if plaintext!=False :
    a = SymmetricCryptoAbstraction(sha1(plaintext))

    with open(fileUrl,"rb") as f:
        cloudfile = f.read()
    file = a.decrypt(cloudfile)

    with open(fileUrl,"wb") as re:
        re.write(file)
else:
    print "Dcrypto Fail!"

del groupObj

#os.remove(configUrl)