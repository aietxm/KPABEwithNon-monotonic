from charm.toolbox.symcrypto import SymmetricCryptoAbstraction,AuthenticatedCryptoAbstraction, MessageAuthenticator
from charm.toolbox.pairinggroup import PairingGroup,GT
from charm.core.math.pairing import hashPair as sha1

debug = 0

groupObj = PairingGroup('SS512')



try:
    f = open('/Users/cirnotxm/down/pk','rb')
    pk = f.read()
    
    a = SymmetricCryptoAbstraction(sha1(groupObj.deserialize(pk)))

    ffe = open('/Users/cirnotxm/down/jiami','rb')

    ct = ffe.read()
    
    de = a.decrypt(ct)
    
    fpk = open('/Users/cirnotxm/down/jiemi.dmg','wb')
    
    fpk.write(de)

finally:
    
    ffe.close()
    f.close()
    fpk.close()