
from charm.toolbox.symcrypto import SymmetricCryptoAbstraction,AuthenticatedCryptoAbstraction, MessageAuthenticator
from charm.toolbox.pairinggroup import PairingGroup,GT
from charm.core.math.pairing import hashPair as sha1

debug = 0

groupObj = PairingGroup('SS512')

pk = groupObj.random(GT)

if debug :print pk

a = SymmetricCryptoAbstraction(sha1(pk))

try:
    

    f = open('/Users/cirnotxm/down/charm.dmg','rb')
    ff = f.read()
    ct = a.encrypt(ff)

    if debug :print ct

    ffe = open('/Users/cirnotxm/down/jiami','wb')

    ffe.write(ct)
    
    fpk = open('/Users/cirnotxm/down/pk','wb')
    
    fpk.write(groupObj.serialize(pk))

finally:
    
    ffe.close()
    f.close()
    fpk.close()