import glob
import ntpath
import os
import pathlib
import sys

#path = 'D:\\translated novels\\'

#path = 'E:\\novels_jkc\\'
path = 'D:\\Novels\\'
names=''

path_back=path
def walkdirs(path):
    loc=path.replace(path_back,'')
    loc='\\'+loc
    global names
    names+="\n\nFolder : "+loc+"\n"
    #print(loc)
    rename(path)
    for root, dirs, files in os.walk(path, topdown=True):
        for dir in dirs:
            dir_path = path + dir + "\\"
            print("Moving to dir " + dir_path)
            sys.stdout.flush()
            walkdirs(dir_path)

i=0
def rename(path):
    fg = glob.glob(path + "*")
    for file in fg:
        if(pathlib.Path(file).is_file()):
            global i
            i = i + 1
            file_base = ntpath.basename(file)
            file_arr = os.path.splitext(file_base)
            file_name = file_arr[0]
            global names
            names+="\n"+file_name+"  ---  "+str(os.path.getsize(file)/1000)+" KB"
            # file_ext = file_arr[1]
            # temp=file_name
            #print(str(i) + "  :  " + file_name)


try:
    filew=open('D:/Novels/catalogue.txt', mode='r', encoding='utf-8')
    txt=filew.read()
    filew.close()
    names+=txt
except:
    print('no old file')
#print(names)
walkdirs(path)
#print(names)
file = open('D:/Novels/catalogue.txt', mode='w', encoding='utf-8')
file.write(names)
file.close()