import os, time, sys, ConfigParser, shutil, datetime, traceback

def backup(src, bkdirpath=os.path.abspath('backups'), t=time.gmtime(), oneDir=False, srcIsDir=False):
    '''
    standardized backup procedure
    default: make folder 'backups' under current dir
             then make dated subfolder of backups (like '2010-01-01-070000')
             then copy src to that folder
    '''
    if srcIsDir:
        dirs = src.split('\\')
        if dirs[-1] == '':
            srctail = dirs[-2]
        else:
            srctail = dirs[-1]
    else:
        srctail = os.path.split(src)[1]
    
    if not oneDir:
        bkdirpath = os.path.join(bkdirpath, dateTimeStr(t))
        dst = srctail
    else:
        dst = datedFileName(srctail, t)
        
    try:
        os.makedirs(bkdirpath)
    except os.error as e:
        pass
    
    bkdirpath = os.path.join(bkdirpath, dst)
    try:
        if srcIsDir:
            shutil.copytree(src, bkdirpath)
        else:
            shutil.copy(src, bkdirpath)
        return True
    except IOError as e:
        return False

def datedFileName(fn, st):
    parts = list(fn.rpartition('.'))
    parts[0] += '-' + dateTimeStr(st)
    return ''.join(parts)

def fwrite(l, fn, mode='wb'):
    #short for writing a list of encoded strings to a file
    outfile = open(fn, mode)
    outfile.writelines(l)
    outfile.close()

def fread(fn):
    #complement to fwrite
    infile = open(fn, 'rb')
    l = infile.readlines()
    infile.close()
    return l

def clean(l):
    #decode and clear \r\n from a list of bytestrings
    return list(map(lambda x: x.decode('utf').rstrip(), l))

def unclean(l):
    #inverse clean
    return list(map(lambda x: (x+'\r\n').encode('utf'), l))

def readToSplitList(fn, sep = '\t'):
    return map(lambda x: x.split(sep), clean(fread(fn)))

def dateTimeStr(st):
    #my string representation of a struct_time
    return time.strftime('%Y-%m-%d-%H%M%S', st)

def doubleSlash(s):
    #doubles every backslash in a string
    return s.replace('\\', '\\\\')

def invDateTimeStr(s):
    #inverse dateTimeStr (string to struct_time)
    return time.strptime(s, '%Y-%m-%d-%H%M%S')

def invTimetuple(st):
    #inverse of datetime.timetuple()
    return datetime.datetime(*st[:6])

def listdir(d):
    #os.listdir, preserving unicode strings
    return os.listdir(unicode(d))

def opj(*args):
    #short for os.path.join. I hate writing that
    return os.path.join(*args)

def readStrip(f):
    return [x.strip() for x in f.readlines()]

def tryCfg(cp, f, kill = False):
    try:
        cp.read(f)
    except:
        print "Failed to parse config file '"+f+"."
        if kill:
            sys.exit(1)
        return False

def tryOpen(f, mode, kill = False):
    try:
        return open(f, mode)
    except IOError:
        print "Could not open '"+f+"' in mode '"+mode+"'."
        if kill:
            sys.exit(1)
        return False
    
def tryRemoveFile(f, printExc=True):
    try:
        os.remove(f)
    except Exception as e:
        if printExc:
            traceback.print_exc(e)
        else:
            print 'Could not remove file: '+f
        return
    print 'Removed file: '+f
    
def tryRemoveDir(d, printExc=True):
    try:
        shutil.rmtree(d)
    except Exception as e:
        if printExc:
            traceback.print_exc(e)
        else:
            print 'Could not remove dir: '+d
        return
    print 'Removed dir: '+d
    
def killAppleFiles(path, printExc):
    #safety
    print 'Killing apple files in: '+path
    print 'Get out now if you don\'t want this.'
    raw_input()
    tryRemoveFile(opj(path, '._.Trashes'), printExc)
    tryRemoveDir(opj(path, '.Spotlight-V100'), printExc)
    tryRemoveDir(opj(path, '.Trashes'), printExc)
    tryRemoveDir(opj(path, '.fseventsd'), printExc)
