import os
from shutil import copyfile, rmtree
import subprocess
import shutil
import subprocess
from shutil import copyfile, rmtree, copytree
import os
import os.path
from pdb import set_trace as st

cutamttransparency = 0
discrepancy_multiplier = 1
cutamtbg = 0
cutamtcover = 0
decimals = 3

#File locations
data_file = "./files/data.txt"
vid_dir_in = "./files/INPUT/unprocessed_raw_files/"
cov_dir_in = "./files/INPUT/covers/"
vid_processed = "./files/OUTPUT/processed_raw_files/"
layer1 = "./files/OUTPUT/trimmed_files_1st_layer/"
layer2 = "./files/OUTPUT/trimmed_files_2nd_layer/"
layer3 = "./files/OUTPUT/trimmed_files_3rd_layer/"
pic_dir_in = "./files/INPUT/pictures/"
wav_converting = "./files/OUTPUT/convert_to_wav/" #files with pictures to extract audio from
cover_dir_out = "./files/OUTPUT/coverssplit/"
wav_dir = "./files/OUTPUT/wav_files/"
pic_dir_out = "./files/OUTPUT/pictures/"
backgroundloc = "./assets/BORDER.mp4"
pic_transparency = "./assets/transparency.png"
cover_cut = "./files/OUTPUT/cutcover/"

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

def createPath(s):
    try:
        os.mkdir(s)
    except (FileExistsError, OSError) as e:
        pass
def deletePath(s):
    try:
        rmtree(s,ignore_errors=False)
    except OSError:
        print ("Deletion of the directory %s failed" % s)
        print(OSError)
def deleteFile(s):
    try:
        os.remove(s)
    except FileNotFoundError:
        pass
def copy_directory(directory, newdirectory):
    try:
        shutil.copytree(directory, newdirectory)
    except FileExistsError:
        pass
def renamefile(src, dest):
    try:
        os.rename(src, dest)
    except OSError:
        pass
def inputToOutputFilename(filename, suffix):
    dotIndex = filename.rfind(".")
    return filename[:dotIndex]+suffix+filename[dotIndex:]
def inputToOutputFilename(filename):
    dotIndex = filename.rfind(".")
    return filename[:dotIndex]+"_TRIMMED"+filename[dotIndex:]
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
    file = open(data_file)
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

#make directories if not there
def make_folders():
    directories = [vid_dir_in, pic_dir_in, cov_dir_in, data_file, layer2, wav_converting, cover_dir_out, layer2]
    for directory in directories:
        try:
            os.mkdir(directory)
        except FileExistsError:
            pass

clips_images = readfile(data_file)
clips_all = {k: v for k, v in clips_images.items()}
clips_pictures = {k: v for k, v in clips_images.items() if v.isdigit()}
clips_ben = {k: v for k, v in clips_images.items() if v == "--"}
clips_bentoc = {k: v for k, v in clips_images.items() if v == "--" or v == "toc"}
clips_cover = {k: v for k, v in clips_images.items() if v == "c1" or v == "c2" or v == "c3"
               or v == "c4" or v == "c5" or v == "c6"
               or v == "c7" or v == "c8" or v == "c9"}
clips_background = {k: v for k, v in clips_images.items() if v.isdigit() or v == "toc"} # includes table of contents
clips_toc = {k: v for k, v in clips_images.items() if v == "toc"}

if __name__ == "__main__":
    make_folders()