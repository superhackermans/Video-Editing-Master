import os
import numpy as np
import math
from shutil import copyfile, rmtree
import subprocess


def inputToOutputFilename(filename, suffix):
    dotIndex = filename.rfind(".")
    return filename[:dotIndex]+suffix+filename[dotIndex:]
def inputToOutputFilename(filename):
    dotIndex = filename.rfind(".")
    return filename[:dotIndex]+"_TRIMMED"+filename[dotIndex:]
def createPath(s):
    try:
        os.mkdir(s)
    except OSError:
        pass
def deletePath(s): # Dangerous! Watch out!
    try:
        rmtree(s,ignore_errors=False)
    except OSError:
        print ("Deletion of the directory %s failed" % s)
        print(OSError)
def inputToOutputWAV(filename):
    dotIndex = filename.rfind(".")
    return filename[:dotIndex]+".WAV"
def inputToOutputMOV(filename):
    dotIndex = filename.rfind(".")
    return filename[:dotIndex]+"_TRIMMED.MOV"
def inputToOutputPNG(filename):
    dotIndex = filename.rfind(".")
    return filename[:dotIndex]+".png"
def inputToOutputNewTrimmed(filename):
    return "C0"+filename+"_TRIMMED.MP4"
def inputToOutputNewWAV(filename):
    return "C0"+filename+".WAV"
def altElement(a):
    return a[::2]
def inputToOutputNewTrimmedAndZoomed(filename):
    return "C0"+filename+"_TRIMMEDZOOMED.MP4"

def readfile(file):
    file = open(DATA_FILE)

    clips = []
    images = []
    clips_images = {}

    for line in file:
        splitLine = line.split("\t")
        clips.append(splitLine[0])
        if len(splitLine[1]) > 9:
            splitLine[1] = "--"
        images.append(splitLine[1].strip())
        images = [i.replace('Photo ', '') for i in images]
    clips_images = dict(zip(clips, images))

    file.close()

    return clips_images

def get_length(fileloc):
    # filelength = float(get_length(fileloc))
    # get length of a file
    command = "ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 " + fileloc + " -hide_banner -loglevel error"
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, )
    filelength = proc.communicate()[0].decode('utf-8').strip('\n')
    return filelength

#File locations
DATA_FILE = "./files/data.txt"
INPUT_VIDEO_DIRECTORY = "./files/INPUT/unprocessed_raw_files/"
INPUT_COVER_DIRECTORY = "./files/INPUT/covers/"
# INPUT_VIDEO_DIRECTORY = "/Users/danielko/Dropbox/YouTube/"
PROCESSED_FILES_DIRECTORY = "./files/OUTPUT/processed_raw_files/"
OUTPUT_VIDEO_DIRECTORY = "./files/OUTPUT/trimmed_files_2nd_layer/"
OUTPUT_VIDEO_DIRECTORY2 = "./files/OUTPUT/trimmed_files_3rd_layer/"
OUTPUT_VIDEO_DIRECTORY3 = "./files/OUTPUT/trimmed_files_1st_layer/"
PICTURE_DIRECTORY = "./files/INPUT/pictures/"
WAV_CONVERSION_FILES = "./files/OUTPUT/convert_to_wav/" #files with pictures to extract audio from
OUTPUT_COVER_DIRECTORY = "./files/OUTPUT/coverssplit/"
WAV_DIRECTORY = "./files/OUTPUT/wav_files/"
PICTURE_OUTPUT_DIRECTORY = "./files/OUTPUT/pictures/"

backgroundloc = "./assets/BORDER.mp4"
TRANSPARENCY = "./assets/transparency.png"

#parameters
frameRate = 24
SAMPLE_RATE = 44100
SILENT_THRESHOLD = 0.07 #0-1. 1 is max volume
FRAME_SPILL_FRONT = 1 #frames on front side of speech to be included
FRAME_SPILL_BACK = 2 #frames on back side of speech to be included
FRAME_SPILL_BACK_FINAL = 6 #frames to include at the very end of the clip
silent_speed = 99999999999999
sounded_speed = 1
NEW_SPEED = [silent_speed, sounded_speed]
FRAME_QUALITY = 3 #1 is highest, 31 is lowest
AUDIO_FADE_ENVELOPE_SIZE = 400 # smooth out transition's audio by quickly fading in/out (arbitrary magic number whatever)
MAX_SILENCE_PERMITTED = 36 #length of frames permitted to not count as silence

original_dimensions = 3840, 2160
scale_factor = .80
raise_up = 500

#make directories if not there
def make_folders():
    directories = [INPUT_VIDEO_DIRECTORY, PICTURE_DIRECTORY, INPUT_COVER_DIRECTORY, DATA_FILE, OUTPUT_VIDEO_DIRECTORY, WAV_CONVERSION_FILES, OUTPUT_COVER_DIRECTORY, OUTPUT_VIDEO_DIRECTORY]
    for directory in directories:
        try:
            os.mkdir(directory)
        except FileExistsError:
            pass

clips_images = readfile(DATA_FILE)
clips_pictures = {k: v for k, v in clips_images.items() if v.isdigit()}
clips_ben = {k: v for k, v in clips_images.items() if v == "--"}
clips_bentoc = {k: v for k, v in clips_images.items() if v == "--" or v == "toc"}
clips_cover = {k: v for k, v in clips_images.items() if v == "c1" or v == "c2" or v == "c3"
               or v == "c4" or v == "c5" or v == "c6"
               or v == "c7" or v == "c8" or v == "c9"}
clips_background = {k: v for k, v in clips_images.items() if v.isdigit()}
clips_toc = {k: v for k, v in clips_images.items() if v == "toc"}

if __name__ == "__main__":
    make_folders()