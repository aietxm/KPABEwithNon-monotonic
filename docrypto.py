__author__ = 'cirnotxm'
from charm.toolbox.pairinggroup import PairingGroup,GT
from charm.core.math.pairing import hashPair as sha1
from charm.schemes.abenc.abenc_waters09 import CPabe09
from charm.toolbox.symcrypto import SymmetricCryptoAbstraction
from charm.core.engine.util import objectToBytes,bytesToObject
import os
debug = True
tempUrl = '/Users/cirnotxm/down/temp/'
configUrl = '/Users/cirnotxm/down/config/up_config'

with open(configUrl,"rb") as f:
    ss = f.read()

s = eval(ss)

fileUrl= s[0]
fileName= s[1]
pol = s[2]

if debug :
    print fileName
    print fileUrl
    print pol

groupObj = PairingGroup('SS512')

AES_pk = groupObj.random(GT)

if debug: print AES_pk

a = SymmetricCryptoAbstraction(sha1(AES_pk))
try:
    f = open(fileUrl, "rb")
    ptext = f.read()
    ct = a.encrypt(ptext)
    ctf = tempUrl + fileName;
    if debug: print  ctf
    fr = open(ctf, "wb")
    fr.write(ct)
except:
    print "Error"
finally:
    f.close()
    fr.close()

cpabe = CPabe09(groupObj)

(mk, pk) = cpabe.setup()


cipher = cpabe.encrypt(pk, AES_pk, pol)


mkBytes = objectToBytes(mk,groupObj)

pkBytes = objectToBytes(pk,groupObj)

cipher = objectToBytes(cipher,groupObj)




with open(ctf+".mk","wb") as fmk:
    fmk.write(mkBytes)

with open(ctf+".pk","wb") as fpk:
    fpk.write(pkBytes)

with open(ctf+".ci","wb") as fci:
    fci.write(cipher)


# if os.path.exists(configUrl):
#     os.remove(configUrl)

del groupObj





