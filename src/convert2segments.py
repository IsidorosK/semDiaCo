import os 
import csv
import sys 

# get the current working directory
path = os.getcwd()
print("Current path is:",path)
# go to annotation files
tmp = ""+"annotation"
# create the path to annotation folder
path = os.path.join(path,tmp)
print("\nEntered path:",path)

files = os.listdir(path)
for f in files:
    if f.endswith('.txt'):
        print(f)
        # get file name 
        name = f.split('.') # throw the file extension
        name = name[0]+'.segments'
        print(name)
        # Concat path to files
        f = os.path.join(path,f)
        name = os.path.join(path,name)
        with open(f,'r') as inp, open(name,'w') as out:
            w = csv.writer(out, delimiter=',')
            w.writerows(x for x in csv.reader(inp, delimiter='\t'))
        #inp.close()
        #out.close()

# Remove .txt files
files = ""
files = os.listdir(path)
for f in files:
    if f.endswith('.txt'):
        # path to file
        f = os.path.join(path,f) 
        os.remove(f)

