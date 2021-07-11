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
    print("Attaching Covers")

    WAV_DIRECTORY = "./files/OUTPUT/wav_files/"
    try:
        os.mkdir(WAV_DIRECTORY)
    except FileExistsError:
        pass

    cutamt = (1/36)

    for key, value in clips_cover.items():
        filename = f"C0{key}{suffix}"
        cover = f"{value}_2"
        coverloc = f"{OUTPUT_COVER_DIRECTORY}{cover}.mov"
        final_output = f"{directory}C0{key}_TRIMMEDCOVER.MOV"

        INPUT_TRIMMED_FILE = f"{directory}{filename}"
        OUTPUT_WAV = f"{WAV_DIRECTORY}{inputToOutputNewWAV(key)}"

        #convert trimmed mp4 into WAV in wav_files folder
        command = "ffmpeg -i " + INPUT_TRIMMED_FILE + " -hide_banner " + OUTPUT_WAV + " -loglevel error"
        subprocess.call(command, shell=True)

        # Matching video to audio duration and attach

        layer3 = f"{OUTPUT_VIDEO_DIRECTORY2}{filename}"
        wavlen = round(float(get_length(layer3))-(cutamt), 2)

        # wavlen = float(get_length(OUTPUT_WAV))
        coverlen = float(get_length(coverloc))

        ratio = (wavlen/coverlen)
        command = f'ffmpeg -i {coverloc} -i {OUTPUT_WAV} -filter_complex "[0:v]setpts=PTS*{str(ratio)}[v]" -map "[v]" -map 1:a -shortest {final_output} -hide_banner -loglevel error'
        subprocess.call(command, shell=True)

        #delete old file
        try:
            os.remove(f"{OUTPUT_VIDEO_DIRECTORY3}C0{key}{suffix}")
        except:
            FileNotFoundError

    shutil.rmtree(WAV_DIRECTORY)

def attachsidecovers(suffix, clips_cover):
    print("Attaching sides of covers")
    #make wav directory
    WAV_DIRECTORY = "./files/OUTPUT/wav_files/"
    try:
        os.mkdir(WAV_DIRECTORY)
    except FileExistsError:
        pass

    for key, value in clips_cover.items():
        brightness = "0.00"
        # saturation = "0.03"
        #name everything
        behindfilenum = str(int(key)-1)
        forwardfilenum = str(int(key)+1)
        behindfile = f"C0{behindfilenum}{suffix}"
        forwardfile = f"C0{forwardfilenum}{suffix}"
        behindfileloc = f"{OUTPUT_VIDEO_DIRECTORY3}{behindfile}"
        forwardfileloc = f"{OUTPUT_VIDEO_DIRECTORY3}{forwardfile}"

        coverbehind = f"{value}_1"
        coverforward = f"{value}_3"
        coverbehindloc = f"{OUTPUT_COVER_DIRECTORY}{coverbehind}.MOV"
        coverforwardloc = f"{OUTPUT_COVER_DIRECTORY}{coverforward}.MOV"

        middle_output_b2 = f"{OUTPUT_VIDEO_DIRECTORY3}C0{behindfilenum}_TRIMMED_1mid.MOV"
        middle_output_f2 = f"{OUTPUT_VIDEO_DIRECTORY3}C0{forwardfilenum}_TRIMMED_1mid.MOV"

        final_output_b2 = f"{OUTPUT_VIDEO_DIRECTORY3}C0{behindfilenum}_TRIMMEDEMPTY_2.MOV"
        final_output_f2 = f"{OUTPUT_VIDEO_DIRECTORY3}C0{forwardfilenum}_TRIMMEDEMPTY_1.MOV"

        #behind file
        #get length of the behind file
        coverbehindlen = float(get_length(behindfileloc))

        def inputToOutputFilenameCUTCLIPB(filename):
            return "C0" + filename + "_TRIMMEDEMPTY_1.MOV"
        newbehindfileloc = f"{OUTPUT_VIDEO_DIRECTORY3}{inputToOutputFilenameCUTCLIPB(str(int(key)-1))}"
        newbehindtransitionloc = f"{OUTPUT_VIDEO_DIRECTORY3}{inputToOutputFilenameTRANSITION(str(int(key)-1))}"

        #cut off 1 s section at the very end of behind clip
        cut_point = str(float(coverbehindlen)-1)
        command = "ffmpeg -ignore_chapters 1 -i " + behindfileloc + " -vcodec qtrle -ss 0 -t " + cut_point + " " + newbehindfileloc + " -hide_banner" + " -loglevel error"
        subprocess.call(command, shell=True)
        command = "ffmpeg -ignore_chapters 1 -i " + behindfileloc + " -vcodec qtrle -ss " + cut_point + " " + " -t 1 " + newbehindtransitionloc + " -hide_banner" + " -loglevel error"
        subprocess.call(command, shell=True)


        overlaycmd = \
            ' -filter_complex "overlay=100:-1:format=auto" -c:v prores_ks -c:a copy '\
            # " -filter_complex '[0]split[m][a];[m][a]alphamerge[keyed]; [1][keyed]overlay=eof_action=endall' "
            # '-c:a copy -filter_complex "[0:v] overlay"'


        #make new transition with overlay
        command = f'ffmpeg -y -i {newbehindtransitionloc} -i {coverbehindloc} \
        {overlaycmd} \
        {middle_output_b2} -hide_banner -loglevel error'
        subprocess.call(command, shell=True)

        command = f'ffmpeg -y -i {middle_output_b2} \
        -vf eq=brightness={brightness}  -c:a copy  \
        {final_output_b2} -hide_banner -loglevel error'
        subprocess.call(command, shell=True)

        # delete unuused files
        try:
            os.remove(newbehindtransitionloc)
            # os.remove(coverbehindloc)
            os.remove(middle_output_b2)
            os.remove(behindfileloc)
        except:
            FileNotFoundError



        #forward file
        command = f'ffmpeg -y -i {forwardfileloc}  -i {coverforwardloc} \
        {overlaycmd} \
        {middle_output_f2} -hide_banner -loglevel error'
        subprocess.call(command, shell=True)

        command = f'ffmpeg -y -i {middle_output_f2} \
        -vf eq=brightness={brightness} -c:a copy  \
        {final_output_f2} -hide_banner -loglevel error'
        subprocess.call(command, shell=True)

        #delete unused files
        try:
            os.remove(forwardfileloc)
            os.remove(middle_output_f2)
        except:
            FileNotFoundError


        # #convert mp4 into mov
        # command = f'ffmpeg -i {behindfileloc} \
        #         {movfileb} -hide_banner -loglevel error'
        # subprocess.call(command, shell=True)

        # make new transition with overlay
        # command = f'''
        # ffmpeg -y -ss 00:00:01 -i {movfileb}  -i {coverbehindloc} \
        # -filter_complex "[0:0][1:0]overlay=enable='between(t,{str(float(coverbehindlen)-1)},{coverbehindlen})'[out]" -shortest -map [out] -map 0:1 -pix_fmt yuv420p -c:a copy -c:v libx264 -crf 18 \
        # {final_output_b2} -hide_banner -loglevel error'''
        # subprocess.call(command, shell=True)

        # overlay = enable = 'between(t\,45,50)'[out]

        # overlay:enable = "between(t, {str(float(coverbehindlen)-1)}, {coverbehindlen})"

    shutil.rmtree(WAV_DIRECTORY)

if __name__ == '__main__':
    # attachcovers(clips_cover)
    attachsidecovers("_TRIMMEDEMPTY.MOV", clips_cover)






