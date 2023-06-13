# @iconic
# 08-06-21
# @ㇼㇼ
#==
# Generate icons from a random image in a DIR
# intended for large image sets with multiple catagory folders
# args: branch, regen -- go through all child folders from cwd | remove old INI and ICO and generate new ones
#==
import sys
from configparser import RawConfigParser
import ctypes
import os
import random
from wand.image import Image
from wand.exceptions import BlobError
import filetype
generated = []

def start(branch,regen):
    if not branch:
        if iniExists(os.getcwd()) and not regen:
            return
        icoName=convertICO(getFile(os.getcwd()),os.getcwd())
        generateINI(icoName,os.getcwd())
        return
    for root, dirs, files in os.walk(os.getcwd()):
        for _dir in dirs:
            d = os.path.join(root,_dir)
            if iniExists(d):
                print(d+' >> INI FOUND...')
                if not regen:
                    print(d+' >> NO REGEN...')
                    continue
            clearINI(d)
            fileName=getFile(d)
            if fileName is None:    
                continue
            icoName=convertICO(fileName,d)
            generateINI(icoName,d)


def iniExists(dir):
    return os.path.exists(os.path.join(dir,"desktop.ini"))
    
def clearINI(dir):
    print(dir+" >> CLEARING INI")
    con = RawConfigParser()
    con.read(os.path.join(dir,"desktop.ini"))
    IconName = con['.ShellClassInfo']['IconResource'].replace(',0','')
    os.remove(os.path.join(dir,"desktop.ini"))
    os.remove(os.path.join(dir,IconName))
       
def containsICO(dir):
    for f in os.listdir(dir):
        if f.endswith('ico'):
            return True
    return False
                
def getFile(dir):
    try:
        fileName = random.choice(os.listdir(dir))
        file = os.path.join(dir,fileName)
        if file.endswith(tuple(['.jpg','.jpeg','.png','.gif'])):
            return(fileName)
        getFile(dir)
            
    except RecursionError:
        pass
        
def generateINI(fileName,dir):
    print(dir+ " >> Generating INI...")
    os.system('attrib -R "' +dir+'"')
    config = RawConfigParser()
    config.optionxform=str
    cfFile = open(os.path.join(dir,'desktop.ini'),'w')
    config.add_section('.ShellClassInfo')
    config.add_section('ViewState')
    config.set('.ShellClassInfo','IconResource','FOLDERICO.ico,0')
    config.set('ViewState','Mode','')
    config.set('ViewState','Vid','')
    config.set('ViewState','FolderType','Pictures')

    config.write(cfFile)
    cfFile.close()
    os.system('attrib +S +H "'+os.path.join(dir,'desktop.ini')+'"')
    os.system('attrib +R "' +dir+'"')
    print(dir+" >> GENERATION COMPLETE")
    
def convertICO(fileName,dir):
    print(fileName+ " >> Generating icon... ")
    icoName = 'FOLDERICO.ico'
    im = Image(filename=os.path.join(dir,fileName))
    im.resize(256,256)
    im.convert('ico').save(filename=os.path.join(dir,icoName))

os.chdir(os.getcwd())
args = sys.argv
if len(args) !=3:
    args.append(0)
    args.append(0)
arg = [0,0]
if args[2] in ['regen','true','1']:
    arg[1] = 1
if args[1] in ['branch','true','1']:
    arg[0] = 1
print(arg)
start(arg[0],arg[1])