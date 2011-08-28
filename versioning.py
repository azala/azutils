import os

vstring = 'version_'
lenvs = len(vstring)

class Version(object):
    def __init__(self, s):
        s = s.split('.')
        self.major = int(s[0])
        self.minor = int(s[1])
    def toStr(self):
        return str(self.major)+'.'+str(self.minor)

def increment():
    global vstring, lenvs
    l = os.listdir('.')
    l = list(filter(lambda x: x.startswith(vstring), l))
    if len(l) > 0:
        v = Version(l[0][lenvs:])
        v.minor += 1
        os.system('move "'+l[0]+'" "'+vstring+v.toStr()+'"')
    else:
        vs = '0.1'
        v = Version(vs)
        os.system('type nul > '+vstring+vs)
    return v.toStr()
