from parameters import *
import subprocess
from shutil import copyfile, rmtree
import os
import shutil

def attachpictures(clips_pictures):
    print("Beginning picture attaching")

    createPath(wav_dir)

    copy_directory(pic_dir_in, pic_dir_out)

    myTrimmedVideos = []
    for file in os.listdir(layer2):
        if file.endswith(".MP4"):
            myTrimmedVideos.append(file)
    if not myTrimmedVideos:
        print("No input trimmed videos detected")
    myTrimmedVideos = sorted(myTrimmedVideos)

    clips_pictures_list = list(clips_pictures.keys())

    #check which trimmed videos to extract WAV audio from and move them into convert_to_wav folder
    source_dir = layer2
    target_dir= wav_converting

    for clip in clips_pictures_list:
        # print(f"Converting clip {clip} to WAV format")
        filename = f"C0{clip}_TRIMMED.MP4"
        try:
            shutil.move(os.path.join(source_dir, filename), target_dir)
        except:
            pass

    #extract WAV audio from trimmed videos
    for trimmed_video in clips_pictures_list:
        INPUT_TRIMMED_FILE = f"{wav_converting}{inputToOutputNewTrimmed(trimmed_video)}"
        OUTPUT_WAV = f"{wav_dir}{inputToOutputNewWAV(trimmed_video)}"
        #convert trimmed mp4 into WAV
        command = "ffmpeg -i " + INPUT_TRIMMED_FILE + " -hide_banner " + OUTPUT_WAV + " -loglevel error"
        subprocess.call(command, shell=True)



    myJPEG = []
    for file in os.listdir(pic_dir_in):
        if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".JPG") or file.endswith(".JPEG"):
            myJPEG.append(file)
    myJPEG = sorted(myJPEG)

    #convert jpg and jpeg to png files
    for jpg in myJPEG:
        # print(f"Converting {jpg} to PNG format")
        INPUT_JPG = f"{pic_dir_in}{jpg}"
        OUTPUT_PNG = f"{pic_dir_in}{inputToOutputPNG(jpg)}"
        #convert JPG to PNG
        command = "ffmpeg -i " + INPUT_JPG + " -hide_banner " + OUTPUT_PNG + " -loglevel error"
        subprocess.call(command, shell=True)



    myPictures = []
    for file in os.listdir(pic_dir_in):
        if file.endswith(".png"):
            myPictures.append(file)
    if not myPictures:
        print("No input pictures detected")
    myPictures = sorted(myPictures)

    #rename pictures to matching video
    def NOPNG(filename):
        dotIndex = filename.rfind(".")
        return filename[:dotIndex]
    images_clips = {y:x for x,y in clips_pictures.items()}
    for key, value in clips_pictures.items():
        if value.isdigit:
            INPUT_PICTURE = f"{pic_dir_in}{value}.png"
            OUTPUT_PICTURE = f"{pic_dir_in}C0{key}.png"
            copyfile(INPUT_PICTURE, OUTPUT_PICTURE)
        else:
            pass

    myWAVFiles = []
    for file in os.listdir(wav_dir):
        if file.endswith(".wav") or file.endswith(".WAV"):
            myWAVFiles.append(file)
    if not myWAVFiles:
        print("No input WAVs detected")
    myWAVFiles = sorted(myWAVFiles)

    # print(myWAVFiles)R

    #attach trimmed_wav_file with PNG picture
    for file in myWAVFiles:
        print(f"Attaching picture to {file}")
        INPUT_WAV = f"{wav_dir}{file}"
        INPUT_IMAGE = f"{pic_dir_in}{inputToOutputPNG(file)}"
        OUTPUT_MOV = f"{layer2}{inputToOutputMOV(file)}"
        #combine wav and png to mp4
        command = "ffmpeg -loop 1 -y -i " + INPUT_IMAGE + " -i " + INPUT_WAV + " -shortest -acodec copy -vcodec png " + " -hide_banner -loglevel error " + OUTPUT_MOV
        subprocess.call(command, shell=True)

    deletePath(wav_dir)
    deletePath(vid_processed)
    deletePath(wav_converting)

if __name__ == "__main__":
    attachpictures()