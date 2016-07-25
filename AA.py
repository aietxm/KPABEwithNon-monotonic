from FS import RBAC_FileSystem

class AA():
    def __init__(self):
        global fs 
        fs= RBAC_FileSystem()

    def setCT_r(Self,id_r,CT_r):
        if fs.isOneof(id_r):
            flist = fs.getCT_r(id_r)
            flist.append(CT_r)
        else:
            flist = []
            flist.append(CT_r)
            fs.upDateR(id_r,flist)

    def getCT_r(self,id_r):
        return fs.getCT_f(id_r)

