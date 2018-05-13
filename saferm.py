#!/usr/bin/python3
import time ,os , sys
import psutil , datetime  , argparse , urllib3 , shutil
import glob , re

if(os.name=='nt'):
    exit(10) ; 

commandstring = '' ;  

for arg in sys.argv:
    if ' ' in arg:
        commandstring+= '"{}" '.format(arg) ;
    else:
        commandstring+="{} ".format(arg) ; 

if(os.getpid()!=os.getpgid(0)):
    print('passing it to system rm') ; 
    os.system('rm ' + commandstring) ; 
    exit(0) ; 



def argument_parser():
    parser = argparse.ArgumentParser() ; 

    parser.add_argument('files' , nargs='+' ,  help="The files which need to be removed ")  ; 

    parser.add_argument('-f' , '--force' ,action="store_true" , required=False ,help="ignore nonexistent files and arguments, never prompt")

    parser.add_argument('-i' , action="store_true" , help="prompt before every removal " , required=False) ; 
    
    parser.add_argument('-I' , action="store_true" , help="prompt once before removing more than three files, or when  removing  recursively;  less intrusive than -i, while still giving protection against most mistakes" , required=False)

    parser.add_argument('--interactive' , action="store_true" , help="prompt according to WHEN: never, once (-I), or always (-i); without WHEN, prompt always" , required=False) 

    parser.add_argument('-r' ,'-R', '--recursive' ,  action="store_true" ,help="remove directories and their contents recursively" , required=False)

    parser.add_argument('-d' , help='remove empty directories',  action="store_true" ,required=False) ; 

    parser.add_argument('-v' , help="explain what is being done" ,  action="store_true" ,required=False) ; 

    
    args = parser.parse_args() ; 
    return args ; 


    

args = argument_parser() ;

trashfilespath = "~/.local/share/Trash/files" ; 
trashinfopath= "~/.local/share/Trash/info"

t = time.localtime() ; 
timeString = "{}-{:0>2}-{:0>2}T{:0>2}:{:0>2}:{:0>2}".format(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)


#Uncomment if glob patterns don't resolve in args.files

#>>>>>>>>>>>>>>>>>>>>.

# fileslist = [] ; #Final list after resolving patterns 

# for i in range(len(args.files)):
#     fileslist.extend(glob.glob(args.files[i])) ; 

# print(">>>>>" , fileslist) ;

#<<<<<<<<<<<<<<<<<<<<<
    
fullpaths = {os.path.abspath(path) for path in args.files}

for path in fullpaths:
    if not os.path.exists(path):
        print("rm: cannot remove '{}': No such file or directory".format(path)) ; 
        exit(10) ; 


for path in fullpaths:

    #handle duplicates already present in the trash 
    newpath = os.path.join(trashfilespath , os.path.basename(path)) ; 

    trashfiles = os.listdir(trashfilespath) ; 
    for file in trashfiles:
        filename_no_extention , extention  = os.path.splitext(file)
        match = re.match('{}\.(\d+)$'.format(path) , filename_no_extention )

        if(match):
            duplicate_number = int(match.groups()[0])+1 ; 
            newpath = os.path.join(os.path.split(path)[0] , filename_no_extention+'.'+str(duplicate_number)+extention) ; 
            print(newpath) ; 

        print(newpath) ; 


        # Copy the file to the trashfilespath before removing it
        # shutil.copy2(path , newpath ) ; 

            

    trashinfoString = '''
    [Trash Info]
    Path={0}/home/natesh/Documents/Smart%20India%20Hackathon.docx
    DeletionDate={1}
    '''.format(path.replace(' ' , '%20') , timeString)


print(fullpaths) ;

pathString = ''''''

