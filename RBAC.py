from __future__ import print_function
from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
from mysecretutil import SecretUtil
from charm.toolbox.ABEnc import ABEnc
from AES import AESEnCrypt,AESDecrypt
from AA import AA
from FS import RBAC_FileSystem


__author__ = 'CirnoTxm'


class RBAC_scheme():

    U0 = 'AdminUsers'

    def __init__(self,groupObj):
        global group,util,RURL,RFL,RUL,URL,FRL,aa,fs
        group = groupObj
        aa = AA()
        fs = RBAC_FileSystem()
        util = SecretUtil(group)
        RURL = {}
        RFL,FRL,RUL,URL = {},{},{},{}

    def add2List(self,key,value,list):
        instance = list.get(key)
        if instance == None:
            temp =[value]
            list[key] = temp
        else:
            instance.append(value)
            list[key] = instance

    def del4List(self,key,value,list):
        instance = list.get(key)
        if instance == None:
            return False
        for index in range(len(instance)):
            if instance[index] == value:
                del(instance[index])
        return True

    # checked
    def setup(self):
        g1 = group.random(G1)
        g2 = group.random(G2)
        alpha = group.random()
        beta = group.random()
        h = group.random(G1)
        e_gg_alpha = pair(g1,g1) ** alpha
        pk = {'g':g1, 'g_beta':g1**beta , 'g_beta_2':(g1**beta)**beta, 'h_beta':h**beta, 'e_gg_alpha':e_gg_alpha}
        mk = {'alpha':alpha, 'beta':beta, 'g_alpha':g1**alpha, 'h':h}
        return (pk,mk)

    # checked
    def AddRole(self,pk,id_r):
        if id_r not in RURL:
            RURL[id_r]=[]
            RURL[id_r].append("r0")
        id_u0 = RURL[id_r][0]
        v,K_r = group.random(ZR), group.random(ZR)
        C1 = pk['g'] **(1/K_r)
        C2 = group.hash(unicode(id_r),G1) ** (1/K_r)
        C = K_r * (pk['e_gg_alpha']** v)
        C0 = pk['g'] ** v
        C0_1 = pk['g_beta'] ** v
        C0_2 = (pk['g_beta_2'] **(v * group.hash(id_u0))) * (pk['h_beta']**v )
        CT_r = {'C1':C1, 'C2':C2, 'C':C, 'C0':C0,'C0_1':C0_1, 'C0_2':C0_2 ,'VER':0, 'v':v}
        aa.setCT_r(id_r,CT_r)
        return CT_r
    # generate a key to use AES encrypt the Resourse whose ID is id_r, judge the flag 'isNew',if it is true, init FRL[id_f]
    def addPermission(self,id_f,isNew):
        k_f = group.random(ZR)
        CT_sf = AESEnCrypt(k_f,fs.getResource(id_f))
        fs.upDateR(id_f,CT_sf)
        if isNew:
            FRL[id_f] = []
        return k_f
    # checked
    def AddUser(self,pk,mk,id_u):
        t = group.random(ZR)
        D0 = mk['g_alpha']*(pk['g_beta_2'] ** t)
        D1 = ((pk['g_beta']**group.hash(id_u))*mk['h']) ** t
        D2 = pk['g'] ** -t
        SK_u = {'D0':D0, 'D1':D1, 'D2':D2}
        return SK_u
    # checked
    def AssignUser(self,id_u,id_r,CT_r,mk):
        self.add2List(id_r,id_u,RUL)
        self.add2List(id_u,id_r,URL)
        r,w = group.random(ZR), group.random(ZR)
        D3 = pk['g'] ** ((mk['alpha'] + w)/mk['beta'])
        D_r = (CT_r['C1'] ** w) * (CT_r['C2'] ** r)
        D_r_2 = CT_r['C1'] ** r
        SK_r_u = {'D3':D3, 'D_r':D_r ,'D_r_2':D_r_2}
        return SK_r_u

     # checked
    def DeassignUser(self,pk,id_u,id_r,CT_r):
        self.del4List(id_r,id_u,RUL)
        self.del4List(id_u,id_r,URL)
        u_list  = RURL[id_r]
        id_u0 = u_list[0]
        u_list.append(id_u)
        n = len(u_list)
        v = CT_r['v']
        Ver = CT_r['VER']
        v_1,K_r_1 = group.random(ZR), group.random(ZR)
        v += v_1
        C1 = pk['g'] ** (1 / K_r_1)
        C2 = group.hash(unicode(id_r), G1) ** (1 / K_r_1)
        C = K_r_1 * (pk['e_gg_alpha'] ** v)
        C0 = pk['g'] ** v
        C0_1 = pk['g_beta'] ** v_1
        C0_2 = (pk['g_beta_2'] ** (v_1 * group.hash(id_u0))) * (pk['h_beta'] ** v_1)
        CT_r_1 = {'C1': C1, 'C2': C2, 'C': C, 'C0': C0, 'C'+str(n-1)+'_1': C0_1, 'C'+str(n-1)+'_2': C0_2, 'VER': Ver+1, 'v':v}
        aa.setCT_r(id_r,CT_r_1)
        return CT_r_1

    # checked
    def Encrypt(self,id_r,S_f,K_f,isNew,pk):
        CT_r_f = group.hash(unicode(id_r),G1) ** S_f
        CT_f_l = {}
        if isNew:
            C3 = pk['g'] ** S_f
            C4 = K_f * (pk['e_gg_alpha'] ** S_f )
            C5 = pk['g_beta'] ** S_f
            CT_f_l[id_r] = CT_r_f
            return {'C3':C3, 'C4':C4 ,'C5':C5, 'CT_r_f':CT_f_l}
        return CT_r_f

    def isNewResource(self,id_r):
        return True

    def getkey(self,id_r):
        return group.random(ZR)

    def getPermission(self,id_f):
        S_f = group.random(ZR)
        CT_f = {}

        return S_f,CT_f

    # cheked
    def GrantPermission(self,id_r,id_f):
        if self.isNewResource(id_f):
            K_f= self.addPermission(id_f,True)
        else:
            K_f = self.getKey(id_f)
        list = FRL.get(id_f)
        if len(list) == 0:
            S_f = group.random(ZR)
            CT_f = self.Encrypt(id_r,S_f,K_f,True,pk)
        else:
            (S_f , CT_f) = self.getPermission(id_f)
            CT_f_1 = self.Encrypt(id_r,S_f,K_f,False,pk)
            CT_f['CT_r_f'][id_r] = CT_f_1
        self.add2List(id_r,id_f,RFL)
        self.add2List(id_f,id_r,FRL)
        return CT_f
    # checked
    def RevokePermission(self,id_r,id_f,pk):
        self.del4List(id_f,id_r,FRL)
        self.del4List(id_r,id_f,RFL)
        K_f_1 = self.addPermission(id_f,False)
        S_f_1 = group.random(ZR)
        #upDateR(id_f,AESEnCrypt(K_f_1,getResource(id_f)))
        if len(FRL[id_f])>1 :
            IDList = FRL[id_f]
            CT_f_1 = {}
            for i in range(len(IDList)):
                if i == 1 and IDList[i]!="#" :
                    CT_f_1 =self.Encrypt(IDList[i],S_f_1,K_f_1,True,pk)
                elif i!=0:
                    CT_f_1['CT_r_f'][IDList[i]] = self.Encrypt(IDList[i],S_f_1,K_f_1,False,pk)
        return CT_f_1

    def CheckAccess(self,id_u,id_f,SK_u,SK_r_u):
        a = URL[id_u]
        b = FRL[id_f]
        CT_f = fs.getCT_f(id_f)
        inter = list(set(a).intersection(set(b)))
        if len(inter) == 0:
            return
        id_r = inter[0]
        CT_r = aa.getCT_r(id_r)
        print (CT_r)
        CT_r_0 = CT_r[0] # the current CT_r
        u_list = RURL[id_r]
        E1 = 1
        E2 = 1
        for i in range(len(u_list)):
            u_i = u_list[i]
            index = 'C'+str(i)
            E1 *=CT_r[i][index+'_1'] ** (1/(group.hash(id_u) - group.hash(u_i)))
            E2 *=CT_r[i][index+'_2'] ** (1/(group.hash(id_u) - group.hash(u_i)))
        D = pair(CT_r_0['C0'],SK_u['D0']) / (pair(SK_u['D1'],E1) * pair(SK_u['D2'],E2))
        K_r = CT_r_0['C'] / D
        A = pair(SK_r_u['D_r'] ** K_r,CT_f['C3']) / pair(SK_r_u['D_r_2'] ** K_r, CT_f['CT_r_f'][id_r])
        K_f = CT_f['C4'] / (pair(CT_f['C5'],SK_r_u['D3']) / A)

        #TODO if there is a Revoke happening,how does it works

        return AESDecrypt(K_f,getResource(id_f))



if __name__ == '__main__':
    group = PairingGroup('SS512')
    test = RBAC_scheme(group)
    (pk,mk) = test.setup()
    print (pk)
    print (mk)

    #addRoleTest
    CT = test.AddRole(pk,'r1')
    print (CT)

    #addUserTest
    SK_u = test.AddUser(pk,mk,'u1')
    print (SK_u)

    #AssignUserTest
    SK_r_u = test.AssignUser('u1','r1',CT,mk)
    print (SK_r_u)

    #GrantPermisionTest
    CT_f = test.GrantPermission('r1','f1')
    print (CT_f)

    #CheckAccessTest
    test.CheckAccess('u1','f1',SK_u,SK_r_u)

    #CT_1 = test.DeassignUser(pk,'u1','r1',CT)

    #print (SK)
    #print (SK_r_u)
    #print (CT_1)
