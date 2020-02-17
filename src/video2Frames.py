"""
Extract frames from a video signal
"""
import os 
import sys 
import subprocess

# get the current working directory
path = os.getcwd()
print("Current directory is:",path)
# go to the video files
# change tmp to whatever name used for the 
# directory that contains the .mp4 files 
tmp = ""+"videos" 
# create the path for the videos folder
path = os.path.join(path,tmp)
print("Entered dir:",path,"\n")

# create a directory named frames
if not os.path.exists(os.path.join(os.getcwd(),"frames")):
    tmp = os.getcwd()
    os.mkdir(os.path.join(tmp,"frames"))
    print("Created directory")

files = os.listdir(path)
# Getting the video names
video_names = [name for name in files if name.endswith('.mp4')]
[print(name) for name in video_names]
print()

folderPath = os.path.join(path,"frames")
print("Folder Path:",folderPath)

for video in video_names:
    # get the video name without the file extension 
    tmp = video.split('.')
    tmp = tmp[0]
    #print("Video Name Processing:",tmp)
    # for each video
    # make a new folder with the corresponding frames
    folderPath = os.path.join(folderPath,"frames={}".format(tmp))
    #print("folder path:",folderPath)
    if not os.path.exists(folderPath):
        tmp1 = os.getcwd()# get the current working dir 
        tmp2 = "frames"# concat the current dir with the /frames 
        tmp1 = os.path.join(tmp1,tmp2)
        tmp3 = "frames-{}".format(tmp) # concat the cur dir/frames 
        #print(tmp1)
        #print(tmp3)
        tmp2 = os.path.join(tmp1,tmp3)
        os.mkdir(os.path.join(tmp1,tmp3)) # create the new dir inside frames
        print("Created new folder",tmp2)
    
    #video folder input and frames folder output
    videoFile = os.path.join(path,video)
    print("Input:",videoFile)
    frameFile = os.path.join(tmp2,"frame-%05d.jpeg")
    print("Output:",frameFile)
    
    # Create video frames
    subprocess.run(['ffmpeg', '-i',videoFile, frameFile],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    