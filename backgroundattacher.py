import subprocess
from parameters import *
from pdb import set_trace as st
import shutil
import os


def backgroundattacher(suffix, directory, bg_to_attach):
    # check if dictionary is empty
    for key, value in bg_to_attach.items():
        filename = f"C0{key}{suffix}"
        backgroundloc = "./assets/BORDER.mp4"
        FINAL_OUTPUT = f"{directory}C0{key}_TRIMMED_bg.MP4"
        FINALFINAL_OUTPUT = f"{directory}C0{key}_TRIMMEDBG.MP4"

        INPUT_TRIMMED_FILE = f"{directory}{filename}"
        if os.path.isfile(INPUT_TRIMMED_FILE) == True:

            # WAV_DIRECTORY = "./files/OUTPUT/wav_files/"
            # try:
            #     os.mkdir(WAV_DIRECTORY)
            # except FileExistsError:
            #     pass
            CUTCOVER = "./files/OUTPUT/cutcover/"
            try:
                os.mkdir(CUTCOVER)
            except FileExistsError:
                pass
            print(f"Attaching background to {filename}")
            # OUTPUT_WAV = f"{WAV_DIRECTORY}{inputToOutputNewWAV(key)}"

            # #convert trimmed mp4 into WAV in wav_files folder
            # command = "ffmpeg -i " + INPUT_TRIMMED_FILE + " -hide_banner " + OUTPUT_WAV + " -loglevel error"
            # subprocess.call(command, shell=True)

            # Get the duration of the audio file
            # command = "ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 " + OUTPUT_WAV + " -hide_banner -loglevel error"
            # proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            # wavlen = proc.communicate()[0].decode('utf-8').strip('\n')

            filelength = float(get_length(INPUT_TRIMMED_FILE))-2/24

            # Cut video to match audio duration
            output_cover = f"{CUTCOVER}{key}.MP4"
            command = f"ffmpeg -ss -0 -i {backgroundloc} -t {filelength} -c copy {output_cover} -hide_banner -loglevel error"
            subprocess.call(command, shell=True)

            # overlay cut cover onto video
            command = f'ffmpeg -i {INPUT_TRIMMED_FILE} -i {output_cover} -c:a copy -filter_complex "[0:v] overlay" {FINAL_OUTPUT} -hide_banner -loglevel error'
            subprocess.call(command, shell=True)

            # # cut 1 frame off the end
            # cutframe = (filelength - (1.1 / 24))
            # print(filelength)
            # print(cutframe)
            # command = f"ffmpeg -ss -0 -i {FINAL_OUTPUT} -t {cutframe} -c copy {FINALFINAL_OUTPUT} -hide_banner -loglevel error"
            # subprocess.call(command, shell=True)
            #delete old file
            # try:
            #     os.remove(f"{FINAL_OUTPUT}")
            # except:
            #     FileNotFoundError
            try:
                os.remove(f"{directory}C0{key}_TRIMMED.MP4")
            except:
                FileNotFoundError
            try:
                os.remove(f"{directory}C0{key}_TRIMMED.MOV")
            except:
                FileNotFoundError

            # overlay background on video


            # # attach audio to video
            # command = f"ffmpeg -i {CUTCOVER}{key}.mp4 -i {OUTPUT_WAV} {FINAL_OUTPUT} -hide_banner -loglevel error"
            # subprocess.call(command, shell=True)
            #
            # # Cut last frame of video (audio is a little longer so ffmpeg adds a frame to the end of the snippet)
            # filelength = float(get_length(FINAL_OUTPUT))
            # command = f"ffmpeg -ss -0 -i {FINAL_OUTPUT} -t {filelength - 1 / 24} -c copy {FINALFINAL_OUTPUT} -hide_banner -loglevel error"
            # subprocess.call(command, shell=True)

            # try:
            #     os.remove(FINAL_OUTPUT)
            # except FileNotFoundError:
            #     pass
        else:
            pass
    try:
        shutil.rmtree(CUTCOVER)
    except FileNotFoundError:
        pass
    try:
        shutil.rmtree(wav_dir)
    except FileNotFoundError:
        pass












