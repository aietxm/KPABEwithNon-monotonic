from charm.toolbox.pairinggroup import PairingGroup,GT
from charm.core.math.pairing import hashPair as sha1
from charm.schemes.abenc.abenc_waters09 import CPabe09
from charm.toolbox.symcrypto import SymmetricCryptoAbstraction,AuthenticatedCryptoAbstraction, MessageAuthenticator

asl= ['ONE','TWO']
groupObj = PairingGroup('SS512')
cpabe = CPabe09(groupObj)


with open('/Users/cirnotxm/down/info','rb') as f:
    info = f.read()


cpkey = cpabe.keygen(pk,msk,asl)

with open('/Users/cirnotxm/down/cipk','r') as f2:
    ciphertext = f2.read()


ciphertext = eval(ciphertext)

print ciphertext

prig_msg = cpabe.decrypt(pk,cpkey,ciphertext)

a2 =  SymmetricCryptoAbstraction(sha1(orig_symKey))

plaintext = a2.decrypt(info)

print plaintext
