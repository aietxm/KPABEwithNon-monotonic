from charm.toolbox.pairinggroup import PairingGroup,GT
from charm.core.math.pairing import hashPair as sha1
from charm.schemes.abenc.abenc_waters09 import CPabe09
from charm.toolbox.symcrypto import SymmetricCryptoAbstraction,AuthenticatedCryptoAbstraction, MessageAuthenticator

groupObj = PairingGroup('SS512')
symKey = groupObj.random(GT)
a1 =  SymmetricCryptoAbstraction(sha1(symKey))
with open('/Users/cirnotxm/down/pk','rb') as f:
    msg1 = f.read() 
ct = a1.encrypt(msg1)
cpabe = CPabe09(groupObj)
(msk, pk) = cpabe.setup()
pol = '((ONE or THREE) and (TWO or FOUR))'

with open('/Users/cirnotxm/down/msk','wb') as fm:
    fm.write(str(msk))
    
with open('/Users/cirnotxm/down/mpk','wb') as fp:
    fp.write(str(pk))


with open('/Users/cirnotxm/down/info','wb') as fi:
    fi.write(ct)

print('Acces Policy: %s' % pol)
        
cipher = cpabe.encrypt(pk, symKey, pol)
print("\nCiphertext...")

print cipher

print type(cipher)

with open('/Users/cirnotxm/down/cipk','w') as re:
    re.write(str(cipher))

        
       
del groupObj

