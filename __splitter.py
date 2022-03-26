
import os
import sys
import glob
import shutil
import ntpath
import time


def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True



path = 'C:\\Users\\Smile\\Downloads\\new\\'

def walkdirs(path):
    rename(path)
    for root, dirs, files in os.walk(path, topdown=True):
        for dir in dirs:
            dir_path = path + dir + "\\"
            print("Moving to dir " + dir_path)
            sys.stdout.flush()
            walkdirs(dir_path)


def rename(path):
    files = glob.glob(path + "*")
    i = 0
    for file in files:
        if isEnglish(file):
            print(file)
        else:
            i = i + 1
            old_name = file
            try:
                file_base = ntpath.basename(file)
                file_arr = os.path.splitext(file_base)
                file_name = file_arr[0]
                file_ext = file_arr[1]
                temp=file_name
                #file_name=file_name.replace('[','(')
                #file_name = file_name.replace(']', ')')
                temp=str(temp)
                temp=temp.split('__')
                temp=temp.pop()
                #print(temp)
                #translated= translated.replace(':','-')
                #new_name = ntpath.dirname(file) + "\\" + translated
                new_name = ntpath.dirname(file)+"\\"+temp+file_ext
            except:
                print("Translating error")
                sys.stdout.flush()
                i = i - 1
                pass
                continue
            try:
                print(str(i)+"  :renaming " + str(old_name) + " to " + str(new_name))
                new_name=new_name.replace('"','')
                new_name = new_name.replace('?', '7')
                sys.stdout.flush()
            except:
                try:
                    print("renaming XXX to " + str(new_name))
                    sys.stdout.flush()
                except:
                    print("renaming XXX to YYY")
                    sys.stdout.flush()
                    pass
            shutil.move(old_name, new_name)
            time.sleep(.300)


    print(str(i) + " files translated")

walkdirs(path)



