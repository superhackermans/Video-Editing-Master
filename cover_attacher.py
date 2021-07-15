import subprocess
from parameters import *
from pdb import set_trace as st
import shutil
import os

def inputToOutputWAV(filename):
    dotIndex = filename.rfind(".")
    return filename[:dotIndex]+".WAV"
def inputToOutputNewWAV(filename):
    return "C0"+filename+".WAV"
def inputToOutputFilenameTRANSITION(filename):
    return "C0"+filename+"_transition.MOV"

def attachcovers(suffix, clips_cover, directory):
    # find which clips have cover pages

    createPath(wav_dir)

    for key, value in clips_cover.items():

        filename = f"C0{key}{suffix}"
        originalfile = f"{layer1}{filename}"
        cover = f"{value}_2"
        coverloc = f"{cover_dir_out}{cover}.mov"
        final_output = f"{directory}C0{key}_TRIMMEDCOVER.MOV"

        print(f"Attaching cover {value} to {filename}")

        INPUT_TRIMMED_FILE = f"{directory}{filename}"
        # OUTPUT_WAV = f"{wav_dir}{inputToOutputNewWAV(key)}"
        #
        # #convert trimmed mp4 into WAV in wav_files folder
        # command = "ffmpeg -i " + INPUT_TRIMMED_FILE + " -hide_banner " + OUTPUT_WAV + " -loglevel error"
        # subprocess.call(command, shell=True)

        # Matching video to audio duration and attach

        # layer3 = f"{layer3}{filename}"
        # wavlen = round(float(get_length(layer3))-(cutamtcover), decimals)
        wavlen = float(get_length(originalfile)) + addamtcover
        coverlen = float(get_length(coverloc))

        ratio = (wavlen/coverlen)

        command = f'ffmpeg -i {coverloc} -filter_complex "[0:v]setpts=PTS*{str(ratio)}[v]" -map "[v]" -shortest {final_output} -hide_banner -loglevel error'
        subprocess.call(command, shell=True)

        filelength = float(get_length(final_output))

        if wavlen-filelength == 0:
            print("There was no discrepancy between lengths.")
        else:
            print(f"filelength of cover {value} is {filelength}")
            print(f"filelength of layer 3 clip is {wavlen}")
            print(f"The discrepancy is {filelength - wavlen}")

        #delete old file
        try:
            os.remove(f"{directory}C0{key}{suffix}")
        except:
            FileNotFoundError

    deletePath(wav_dir)

def attachsidecovers(suffix, clips_cover, directory):
    print("Attaching sides of covers")
    #make wav directory

    for key, value in clips_cover.items():
        # brightness = "0.00"
        # saturation = "0.03"
        #name everything
        behindfilenum = str(int(key)-1)
        forwardfilenum = str(int(key)+1)
        behindfile = f"C0{behindfilenum}{suffix}"
        forwardfile = f"C0{forwardfilenum}{suffix}"
        behindfileloc = f"{directory}{behindfile}"
        forwardfileloc = f"{directory}{forwardfile}"

        coverbehind = f"{value}_1"
        coverforward = f"{value}_3"
        coverbehindloc = f"{cover_dir_out}{coverbehind}.MOV"
        coverforwardloc = f"{cover_dir_out}{coverforward}.MOV"

        final_output_b2 = f"{directory}C0{behindfilenum}.5_TRIMMED.MOV"
        final_output_f2 = f"{directory}C0{forwardfilenum}_1_TRIMMED.MOV"

        newbehindfileloc = f"{directory}TEMP{behindfile}"
        newfowardfileloc = f"{directory}TEMP{forwardfile}"

        #cut off 1 s section at the very end of behind clip
        if os.path.isfile(behindfileloc) == True:
            cut_point = str(float(get_length(behindfileloc))-1)
            command = f"ffmpeg -ignore_chapters 1 -i {behindfileloc} -vcodec qtrle -ss 0 -t {cut_point} {newbehindfileloc} -hide_banner -loglevel error"
                      # f" -c:v libx264 -strict -2 " \
            subprocess.call(command, shell=True)
        if os.path.isfile(forwardfileloc) == True:
            cut_point = str(float(get_length(forwardfileloc))-1)
            command = f"ffmpeg -ignore_chapters 1 -i {forwardfileloc} -vcodec qtrle -ss 1 -t {cut_point} {newfowardfileloc} -hide_banner -loglevel error"
                      # f" -c:v libx264 -strict -2 " \
            subprocess.call(command, shell=True)

        # fwd clip

        # command = "ffmpeg -ignore_chapters 1 -i " + behindfileloc + " -vcodec qtrle -ss " + cut_point + " " + " -t 1 " + newbehindtransitionloc + " -hide_banner" + " -loglevel error"
        # subprocess.call(command, shell=True)
        deleteFile(behindfileloc)
        deleteFile(forwardfileloc)
        renamefile(newbehindfileloc, behindfileloc)
        renamefile(newfowardfileloc, forwardfileloc)
        copyfile(coverbehindloc, final_output_b2)
        copyfile(coverforwardloc, final_output_f2)




if __name__ == '__main__':
    # attachcovers(clips_cover)
    attachsidecovers("_TRIMMEDEMPTY.MOV", clips_cover, layer1)






