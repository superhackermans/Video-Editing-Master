import os
from shutil import copyfile, rmtree
import subprocess
import shutil
import subprocess
from shutil import copyfile, rmtree, copytree
import os
import os.path
from pdb import set_trace as st
import numpy as np
import subprocess
from audiotsm import phasevocoder
from audiotsm.io.wav import WavReader, WavWriter
from scipy.io import wavfile
import math
from shutil import copyfile, rmtree
from pdb import set_trace as st

# camera prefix
cam = "C"
filesuffix = "_TRIMMED.MOV"

# File locations
data_file = "./files/data.txt"
vid_dir_in = "./files/INPUT/unprocessed_raw_files/"
cov_dir_in = "./files/INPUT/covers/"
vid_processed = "./files/OUTPUT/processed_raw_files/"
pop_up_dir = "./files/INPUT/pop_ups/"
backuplayer = "./files/OUTPUT/backup_layer/"
layer0 = "./files/OUTPUT/0_layer_covers/"
layer1 = "./files/OUTPUT/1_layer_transitions/"
layer_popups = "./files/OUTPUT/2.5_layer_pop_ups/"
layer2 = "./files/OUTPUT/2_layer_pics/"
layer_toc = "./files/OUTPUT/3.5_toc/"
layer3 = "./files/OUTPUT/3_layer_background/"
layer4 = "./files/OUTPUT/4_layer_ben/"
pic_dir_in = "./files/INPUT/pictures/"
wav_converting = "./files/OUTPUT/convert_to_wav/"  # files with pictures to extract audio from
cover_dir_out = "./files/OUTPUT/coverssplit/"
wav_dir = "./files/OUTPUT/wav_files/"
pic_dir_out = "./files/OUTPUT/pictures/"
cover_cut = "./files/OUTPUT/cutcover/"
output_main = "./files/OUTPUT/"

TEMP_FOLDER = "TEMP"

# asset file locations
in_1 = "./assets/in_1.mov"
in_2 = "./assets/in_2.mov"
out_1 = "./assets/out_1.mov"
out_2 = "./assets/out_2.mov"
trans_in = "./assets/in.MOV"
trans_out = "./assets/out.MOV"
backgroundloc = "./assets/BORDER.MOV"
pic_transparency = "./assets/transparency.png"
# vid_transparency = "./assets/transparency.mov"
vid_transparency_smol = "./assets/transparency_smol.mov"
outro = "./assets/outro.mov"
toc_loc = "{pop_up_dir}toc.mov"

# parameters
frameRate = 24
SAMPLE_RATE = 44100
SILENT_THRESHOLD = 0.07  # 0-1. 1 is max volume
FRAME_SPILL_FRONT = 0  # frames on front side of speech to be included
FRAME_SPILL_BACK = 2  # frames on back side of speech to be included
FRAME_SPILL_BACK_FINAL = 5  # frames to include at the very end of the clip
silent_speed = 99999999999999
sounded_speed = 1
NEW_SPEED = [silent_speed, sounded_speed]
FRAME_QUALITY = 3  # 1 is highest, 31 is lowest
AUDIO_FADE_ENVELOPE_SIZE = 400  # smooth out transition's audio by quickly fading in/out (arbitrary magic number whatever)
MAX_SILENCE_PERMITTED = 36  # length of frames permitted to not count as silence
mistake_threshold = 2/3 # if there a mistake past this point, it will not remove

original_dimensions = 3840, 2160
scale_factor = .85
raise_up = 0


def group_consecutives(vals, step=1):
    """Return list of consecutive lists of numbers from vals (number list)."""
    run = []
    result = [run]
    expect = None
    for v in vals:
        if (v == expect) or (expect is None):
            run.append(v)
        else:
            run = [v]
            result.append(run)
        expect = v + step
    return result

def jpg_to_png(directory):
    myJPEG = []
    for file in os.listdir(directory):
        if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".JPG") or file.endswith(".JPEG"):
            myJPEG.append(file)
    myJPEG = sorted(myJPEG)
    for jpg in myJPEG:
        # print(f"Converting {jpg} to PNG format")
        INPUT_JPG = f"{directory}{jpg}"
        OUTPUT_PNG = f"{directory}{inputToOutputPNG(jpg)}"
        # convert JPG to PNG
        command = "ffmpeg -y -i " + INPUT_JPG + " -hide_banner " + OUTPUT_PNG + " -loglevel error"
        subprocess.call(command, shell=True)

def dup_dir(directory, directory2):
    try:
        shutil.copytree(directory, directory2)
        print(f"Duplicating {directory}")
    except (FileExistsError, OSError) as e:
        pass

def reset():
    deletePath(layer1)
    deletePath(layer2)
    deletePath(layer3)
    deletePath(layer4)
    deletePath(layer0)
    deletePath(layer_popups)
    deletePath(layer_toc)
    dup_dir(backuplayer, layer2)
    # sec_to_frames(filesuffix, clips_all, layer2)
    dup_dir(layer2, layer3)
    dup_dir(layer3, layer4)


def createPath(s):
    try:
        os.mkdir(s)
    except (FileExistsError, OSError) as e:
        pass


def deletePath(s):
    try:
        rmtree(s, ignore_errors=False)
    except OSError:
        print("Deletion of the directory %s failed" % s)
        # print(OSError)


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


def move_file(src, filename, dest):
    try:
        shutil.move(os.path.join(src, filename), dest)
    except:
        pass


def nosuffix(filename):
    dotIndex = filename.rfind(".")
    return filename[:dotIndex]


def tempclip(filename):
    dotIndex = filename.rfind(".")
    return filename[:dotIndex] + "TEMP" + filename[dotIndex:]


def basesuffix(suffix):
    dotIndex = suffix.rfind(".")
    return suffix[dotIndex:]


def inputToOutputFilename(filename):
    dotIndex = filename.rfind(".")
    return filename[:dotIndex] + filesuffix


def inputToOutputWAV(filename):
    dotIndex = filename.rfind(".")
    return filename[:dotIndex] + ".WAV"


def inputToOutputMOV(filename):
    dotIndex = filename.rfind(".")
    return filename[:dotIndex] + filesuffix


def inputToOutputPNG(filename):
    dotIndex = filename.rfind(".")
    return filename[:dotIndex] + ".png"


def inputToOutputNewTrimmed(filename):
    return cam + filename + filesuffix


def inputToOutputNewWAV(filename):
    return cam + filename + ".WAV"


def altElement(a):
    return a[::2]


def inputToOutputNewTrimmedAndZoomed(filename):
    return cam + filename + "_TRIMMED.MOV"


def convert(suffix, filetype, newfiletype, clips, directory):
    for k, v in clips.items():
        input = f"{directory}{cam}{k}{suffix}{filetype}"
        output = f"{directory}{cam}{k}{suffix}{newfiletype}"
        command = f"ffmpeg -i {input} -hide_banner {output} -loglevel error"
        subprocess.call(command, shell=True)
        deleteFile(input)


def sec_to_frames(suffix, clips, directory):
    print("Making things frame perfect...")
    for k, v in dict(clips).items():
        INPUTCLIP = f"{directory}{cam}{k}{suffix}"
        TEMP_OUTPUT = f"{directory}{cam}{k}TEMP{suffix}"
        print(f"working on clip {cam}{k}...")
        filelen = float(get_packets(INPUTCLIP)) / frameRate
        command = f"ffmpeg -ss -0 -i {INPUTCLIP} -t {filelen}  -c copy  " \
                  f" {TEMP_OUTPUT} -hide_banner -loglevel error"
        subprocess.call(command, shell=True)

        print(f"The length is {float(get_length(TEMP_OUTPUT))}")
        print(f"The desired length is {filelen}")

        deleteFile(INPUTCLIP)
        renamefile(TEMP_OUTPUT, INPUTCLIP)


def readfile(file):
    file = open(file)
    clips = []
    images = []

    for line in file:
        splitLine = line.split("\t")
        clips.append(splitLine[0].zfill(4))
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
    return float(filelength)


def get_packets(fileloc):
    # get number of frames in a file
    command = "ffprobe -v error -select_streams v:0 -count_packets -show_entries stream=nb_read_packets -of csv=p=0 " + fileloc + " -hide_banner -loglevel error"
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, )
    packets = proc.communicate()[0].decode('utf-8').strip('\n')
    return float(packets)


def get_frames(fileloc):
    # get number of frames in a file
    command = "ffprobe -v error -select_streams v:0 -count_frames -show_entries stream=nb_read_frames -of csv=p=0 " + fileloc + " -hide_banner -loglevel error"
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, )
    frames = proc.communicate()[0].decode('utf-8').strip('\n')
    return float(frames)


# make directories if not there
def make_folders():
    directories = [output_main, vid_dir_in, pic_dir_in, cov_dir_in, pop_up_dir, data_file, wav_converting,
                   cover_dir_out, layer2]
    for directory in directories:
        try:
            os.mkdir(directory)
        except FileExistsError:
            pass
    deletePath(TEMP_FOLDER)


clips_images = readfile(data_file)
clips_pop_up = {k: v for k, v in clips_images.items() if v == "b1" or v == "b2" or v == "b3"
                or v == "b4" or v == "b5" or v == "b6"
                or v == "b7" or v == "b8" or v == "b9"
                or v == "b10" or v == "b11" or v == "b12"}
clips_cover = {k: v for k, v in clips_images.items() if v == "c1" or v == "c2" or v == "c3"
               or v == "c4" or v == "c5" or v == "c6"
               or v == "c7" or v == "c8" or v == "c9"
               or v == "c10" or v == "c11" or v == "c12"}
clips_video = {k: v for k, v in clips_images.items() if
               v == "v1" or v == "v2" or v == "v3" or v == "v4" or v == "v5"}
clips_all = {k: v for k, v in clips_images.items()}
clips_pictures = {k: v for k, v in clips_images.items() if v.isdigit()}
clips_mult_pics = {k: v for k, v in clips_images.items() if "," in v}
clips_ben = {k: v for k, v in clips_images.items() if v == "--" or v in clips_pop_up.values()}
clips_bentoc = {k: v for k, v in clips_images.items() if v in clips_ben.values() or v == "toc"}
clips_background = {k: v for k, v in clips_images.items() if v == "toc"
                    or v in clips_video.values() or v in clips_pictures.values() or v in clips_mult_pics.values()}
clips_toc = {k: v for k, v in clips_images.items() if v == "toc"}
clips_all_except_pics_and_vid = {k: v for k, v in clips_images.items() if
                                 v not in clips_pictures.values() and v not in clips_video.values() and v not in clips_mult_pics.values()}
clips_ben_and_cover = {k: v for k, v in clips_images.items() if
                       v in clips_cover.values() or v in clips_ben.values()}
clips_all_except_cover = {k: v for k, v in clips_images.items() if v not in clips_cover.values()}
clips_except_popups = {k: v for k, v in clips_images.items() if v not in clips_pop_up.values()}
clips_all_except_cover_and_last = {k: v for k, v in clips_images.items() if v in clips_all_except_cover.values() and k not in [*clips_images.keys()][-1]}


if __name__ == "__main__":
    st()
    make_folders()
