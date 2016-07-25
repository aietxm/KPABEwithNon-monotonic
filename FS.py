
class RBAC_FileSystem():
    def __init__(self):
        global FS
        FS = {}

    def getResource(self,id_f):
        pass

    def getCT_f(self,id_f):
        return FS[id_f]

    def upDateR(self,id_f, new):
        FS[id_f]= new
    
    def isOneof(self,id_f):
        if id_f in FS:
            return True
        else:
            return False

