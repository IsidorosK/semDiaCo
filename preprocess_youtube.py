#!/usr/bin/env python3

"""
    Program Usage: python3 youtube.py <Youtube URL> <Absolute path to save the videos>
    Example: python3 youtube.py 'https://www.youtube.com/playlist?list=PLP28C3ZgpKBy8G5UqubZgDEI6-vx4LGWH' '/mnt/c/Users/Alex/Desktop/videos'
"""

import os
import sys
import shutil
import argparse
import subprocess
from pytube import Playlist
from natsort import natsorted
from pydub import AudioSegment
from pydub.utils import make_chunks


def runBash(command):
    os.system(command)

def DownloadVideo(URL,path):

    playlist = Playlist(URL)
    print('Number of videos in playlist: %s' % len(playlist.video_urls))
    
    #Saving Video URLs to txt file
    with open("video_URLs.txt", "w") as output:
        for e in playlist.video_urls:
            output.write("%s\n" % e)

    if not os.path.exists(path):
        # Create the folder into the chosen path
        os.mkdir(path)

    #Download a playlist from YouTube
    playlist.download_all(path)
    print("Successfully downloaded the YouTube playlist...")
    
    #Rename files
    [os.rename(os.path.join(path, f), os.path.join(path, f).replace(' ', '_')) for f in os.listdir(path)]
    [os.rename(os.path.join(path, f), os.path.join(path, f).replace('-', '_')) for f in os.listdir(path)]
    [os.rename(os.path.join(path, f), os.path.join(path, f).replace('&', '_')) for f in os.listdir(path)]
    print("Seccussfully renamed the files...")
    print("Press a key or ctrl+c in order to continue the process","\n")

def getWAV(path):
    VIDEOS_EXTENSION = '.mp4'
    AUDIO_EXTENSION = 'wav'

    EXTRACT_VIDEO_COMMAND = ('ffmpeg -i "{from_video_path}" '
                             '-f {audio_ext} -ab 192000 '
                             '-vn "{to_audio_path}"')

    os.chdir(path)
    files = os.listdir(path)
    #print("\nEntering into the chosen path",path)
    #print("YouTube video titles...\n")
    [print(f) for f in files]

    #print("\n Creating the .WAV file for every .mp4 Video")
    #print(".WAV files are saved into the same directory with the Video files\n")
    for f in files:
        if not f.endswith(VIDEOS_EXTENSION):
            continue
        f_name = '{}.{}'.format(f[:-4], AUDIO_EXTENSION)
        command = EXTRACT_VIDEO_COMMAND.format(from_video_path=f, audio_ext=AUDIO_EXTENSION, to_audio_path=f_name,)
        os.system(command)

def cropAudio(path):
    #Create 1sec .wav segments
    os.chdir(path)

    #get the current working dir and cd..
    tmp1 = os.path.normpath(os.getcwd() + os.sep + os.pardir)
    #folder to save the audio segments
    fname = 'audio_segments'
    #creating the new path
    newFolder = os.path.join(tmp1,fname)
    if not os.path.exists(newFolder):
        os.mkdir(newFolder)
        print("New Folder:",newFolder,"\n")
    else:
        pass
    
    files = os.listdir(path) #listing the files in  the downloaded videos dir
    files=natsorted(files)
    [print(fName) for fName in files]
    print()

    """
    rename the list names in the following format: 
    video1,video2,....,...,video(len(list))
    where the name order is the same as the name order 
    contained into the files list, that is declared above
    """
    i = 1
    for fName in files:
        if fName.endswith('.wav'):
            #print(fName)
            newName = 'video'+'_'+str(i)+'.'+'wav'
            os.rename(fName,newName)
            i+=1
        else:
            pass
        
    print("\nNew file names...")
    files = os.listdir(path) #listing the files in  the downloaded videos dir
    files=natsorted(files)
    [print(fName) for fName in files if fName.endswith('.wav') ]
    print()
    
    #Create chunks 
    chunk_length_ms = 60000 # pydub calculates in millisec
    
    for fName in os.listdir(path):
        if fName.endswith('.wav'):
            frm = fName.split(".") #frm[0]
            
            #Create the segments into the new directory
            myaudio = AudioSegment.from_file(fName)
            chunks = make_chunks(myaudio, chunk_length_ms) #Make chunks of one sec
            
            for i, chunk in enumerate(chunks):
                tmpName = frm[0]+'_'+str(i)+'.wav'
                chunk_name = newFolder+'/'+tmpName
                print("exporting", chunk_name)
                chunk.export(chunk_name, format="wav")
    
def cropVideo(path):

    #Create 1sec .mp4 segments
    os.chdir(path)

    #get the current working dir and cd..
    tmp1 = os.path.normpath(os.getcwd() + os.sep + os.pardir)
    #folder to save the audio segments
    fname = 'video_segments'
    #creating the new path
    newFolder = os.path.join(tmp1,fname)
    if not os.path.exists(newFolder):
        os.mkdir(newFolder)
        print("New Folder:",newFolder,"\n")
    
    
    f = 'ffmpeg-split.py'
    src = tmp1+'/'+f
    dst = newFolder+'/'+f
    shutil.move(src,dst)
    dst = newFolder
    
    #Copy the .mp4 files into a new directory in order to create segments of K-seconds
    path2YouTubeVideos = os.path.join(tmp1,'youtube_videos')
    for f in os.listdir(path2YouTubeVideos):
        if f.endswith('.mp4'):
            shutil.copy(f,dst)

    #Rename the videos in the new directory
    files = os.listdir(dst) #listing the files in  the downloaded videos dir
    files=natsorted(files)
    print("\n")
    [print(fName) for fName in files]
    print()
    
    i = 1
    for fName in files:
        if fName.endswith('.mp4'):
            #print(fName)
            newName = 'video'+'_'+str(i)+'.'+'mp4'
            #print(newName)
            os.rename(os.path.join(dst,fName),os.path.join(dst,newName))
            i+=1
        else:
            pass
    

    '''
    Crop videos into 1 Sec segments 
    In order to achive this we should call the script
    Named ffmpeg-split.py
    '''

    cd_video_segments = newFolder
    #The command to execute 
    #Enter your directory do not forget to include this part:
    #/video_segments/ffmpeg-split.py -f  -s 10
    tmp = 'python2 /mnt/c/Users/Alekos/Desktop/video_segments/ffmpeg-split.py -f  -s 60'
    files = os.listdir(newFolder)
    for fName in files:
        if fName.endswith('.mp4'):
            #Setting the path to each file we want to crop    
            abs_path2_video_file = cd_video_segments+'/'+fName #pairei lathos onoma 
            #print(abs_path2_video_file)
            
            # Add substring at specific index
            N = 70 #the index to enter the substring
            python3_command = list(tmp)
            python3_command.insert(N, abs_path2_video_file)
            python3_command = ''.join(python3_command)
            #print(python3_command)

            # launch your python2 script using bash
            process = subprocess.Popen(python3_command.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()  # receive output from the python2 script

            abs_path_2_video_file = ""
        else:
            pass
        


def main():
    #Sevice Arguments
    #save the command line arguments into temp variables
    URL = str(sys.argv[1])
    p = str(sys.argv[2])
    print("\nTypeof playlistURL:",type(URL))
    print("Playlist URL:",URL)
    print("Typeof folder path:",type(p))
    print("Folder to save videos",p)
    path = p

    #1.Download Videos from YouTube
    DownloadVideo(URL,p)

    #2. Extract the .wav files from the .mp4 videos
    getWAV(p)

    #3. Create the Segments for the audio files 
    cropAudio(p)
    
    #4.Create the segments for the video files 
    #cropVideo(p)



if __name__ == "__main__": 
    main()
else: 
    pass

