from parameters import *
import subprocess
from pdb import set_trace as st

def inputToOutputMP4(filename):
    dotIndex = filename.rfind(".")
    return filename[:dotIndex]+".mp4"
def inputToOutputFilenameBEG(filename):
    dotIndex = filename.rfind(".")
    return "c"+filename[:dotIndex]+"_1"+filename[dotIndex:]
def inputToOutputFilenameMID(filename):
    dotIndex = filename.rfind(".")
    return "c"+filename[:dotIndex]+"_2"+filename[dotIndex:]
def inputToOutputFilenameEND(filename):
    dotIndex = filename.rfind(".")
    return "c"+filename[:dotIndex]+"_3"+filename[dotIndex:]

def splitcovers(directory):
    myCovers = []
    print("Spliting Cover Page: ")
    
    for file in os.listdir(directory):
        if file.endswith(".mov") or file.endswith(".MOV"):
            myCovers.append(file)
    if not myCovers:
        print("No input covers detected")
    myCovers = sorted(myCovers)

    for cover in myCovers:
        print(cover)
        INPUT_COVER = f"{directory}{cover}"
        assert INPUT_COVER != None , "No Input File Detected"
        OUTPUT_COVER1 = f"{OUTPUT_COVER_DIRECTORY}{inputToOutputFilenameBEG(cover)}"
        OUTPUT_COVER2 = f"{OUTPUT_COVER_DIRECTORY}{inputToOutputFilenameMID(cover)}"
        OUTPUT_COVER3 = f"{OUTPUT_COVER_DIRECTORY}{inputToOutputFilenameEND(cover)}"

        #-ss 0 -t 1 are start and length, respectively
        command = "ffmpeg -ignore_chapters 1 -i " + INPUT_COVER + " -vcodec qtrle -ss 0 -t 1 " + OUTPUT_COVER1 + " -hide_banner" + " -loglevel error"
        subprocess.call(command, shell=True)

        command = "ffmpeg -ignore_chapters 1 -i " + INPUT_COVER + " -vcodec qtrle -ss 1 -t 5.83 " + OUTPUT_COVER2 + " -hide_banner" + " -loglevel error"
        subprocess.call(command, shell=True)

        command = "ffmpeg -ignore_chapters 1 -i " + INPUT_COVER + " -vcodec qtrle -ss 6.83 -t 1 " + OUTPUT_COVER3 + " -hide_banner" + " -loglevel error"
        subprocess.call(command, shell=True)

if __name__ == '__main__':
    splitcovers(directory)