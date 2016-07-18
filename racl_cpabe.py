from charm.schemes.abenc.abenc_bsw07 import CPabe_BSW07
from myKp import KPabe
from charm.toolbox.pairinggroup import PairingGroup,GT
from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
from charm.toolbox.secretutil import SecretUtil


def tes():
    group = PairingGroup('SS512')
    g, gp = group.random(G1), group.random(G2)
    alpha, beta = group.random(ZR), group.random(ZR)
    # initialize pre-processing for generators
    print g,gp
    g.initPP()
    gp.initPP()

    print gp
    print g

    e_gg_alpha = pair(g, gp ** alpha)
    e_gg_alpha2 = pair(g,gp) ** alpha
    if e_gg_alpha == e_gg_alpha2:
        print 'true'
    else:
        print 'false'





def CPABE():
    group = PairingGroup('SS512')
    cpabe = CPabe_BSW07(group)
    (pk,mk) = cpabe.setup()
    policy = 'ID1 or ID2 or ID3'
    asl =['ID1']
    msg = group.random(GT)
    ct = cpabe.encrypt(pk,msg,policy)
    sk = cpabe.keygen(pk,mk,asl)
    plaintext = cpabe.decrypt(pk,sk,ct)
    print plaintext
    print msg


if __name__== '__main__':
    tes()



