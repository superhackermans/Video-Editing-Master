from parameters import *
import subprocess
from shutil import copyfile, rmtree, copytree
import os
from pdb import set_trace as st
import numpy as np
import shutil
from backgroundattacher import *
import os.path


clips_images = readfile(DATA_FILE)
clips_ben = {k: v for k, v in clips_images.items() if v == "--"}
clips_cover = {k: v for k, v in clips_images.items() if v == "c1" or v == "c2" or v == "c3"
               or v == "c4" or v == "c5" or v == "c6"
               or v == "c7" or v == "c8" or v == "c9"}
clips_background = {k: v for k, v in clips_images.items() if v.isdigit()}
clips_toc = {k: v for k, v in clips_images.items() if v == "toc"}

#duplicate file
def dup_dir(directory, directory2):
    try:
        shutil.copytree(directory, directory2)
    except:
        FileExistsError
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
def add_transparency(suffix, clips, directory):
    # print("Adding transparency to top layer files (OUTPUT/trimmed_files/)")
    try:
        os.mkdir(WAV_DIRECTORY)
    except FileExistsError:
        pass

    # TOP LAYER (trimmed_files)
    # ben clips and TOC become transparent
    for k, v in dict(clips).items():
        filename = f"C0{k}{suffix}"
        print(f"Adding transparency to {filename}")
        INPUT_TRIMMED_FILE = f"{directory}{filename}"
        OUTPUT_WAV = f"{WAV_DIRECTORY}{inputToOutputNewWAV(k)}"
        FINAL_OUTPUT = f"{directory}C0{k}_TRIMMEDEMPTY0.MOV"
        FINALFINAL_OUTPUT = f"{directory}C0{k}_TRIMMEDEMPTY.MOV"
        # command = f'ffmpeg -i {INPUT_TRIMMED_FILE} -i {TRANSPARENCY} -c:a copy {FINAL_OUTPUT}'
        # subprocess.call(command, shell=True)

        # extract audio
        command = "ffmpeg -i " + INPUT_TRIMMED_FILE + " -hide_banner " + OUTPUT_WAV + " -loglevel error"
        subprocess.call(command, shell=True)

        # attach audio wav to transparent image
        command = "ffmpeg -loop 1 -y -i " + TRANSPARENCY + " -i " + OUTPUT_WAV + " -shortest -acodec copy -vcodec png " + " -hide_banner -loglevel error " + FINAL_OUTPUT
        subprocess.call(command, shell=True)

        filelength = float(get_length(FINAL_OUTPUT))

        # Cut last frame of video (audio is a little longer so ffmpeg adds a frame to the end of the snippet)
        command = f"ffmpeg -ss -0 -i {FINAL_OUTPUT} -t {filelength - 1/24} -c copy {FINALFINAL_OUTPUT} -hide_banner -loglevel error"
        subprocess.call(command, shell=True)

        #remove old file
        try:
            os.remove(INPUT_TRIMMED_FILE)
        except FileNotFoundError:
            pass
        try:
            os.remove(FINAL_OUTPUT)
        except FileNotFoundError:
            pass

    shutil.rmtree(WAV_DIRECTORY)

        #resize video clips by .88 with alpha border

def replace_footage(suffix, clips_background, directory):

    # BOTTOM LAYER (trimmed_files_dup)

    #find consecutive clips
    clips_background = {int(k):v for k, v in clips_background.items()}
    clips_concat = {}
    clips_solo = {}
    for k, v in clips_background.items():
        if k - 1 in clips_background:
            clips_concat.update({k:int(v)})
        elif k + 1 in clips_background:
            clips_concat.update({k:int(v)})
        else:
            clips_solo.update({str(k):v})

    # st()
    # attach solo clips
    # if bool(clips_solo) == True:
    #     try: backgroundattacher("_TRIMMED.MOV", directory, clips_solo)
    #     except: pass
    # else:
    #     pass
    #
    # if bool(clips_toc) == True:
    #     try: backgroundattacher("_TRIMMED.MP4", directory, clips_toc)
    #     except: pass
    # else:
    #     pass

    clips_background = {int(k):int(v) for k, v in clips_background.items()}

    # connect consecutive clips
    cc = list(clips_background.items())
    if bool(cc) == True:
        arr = np.array(cc)
        consecutive_clips = group_consecutives(arr[:, 0])

        for i in consecutive_clips:
            text_file = 'concat_clips.txt'
            with open(text_file, 'w') as fp:
                pass
            for j in i:
                TRIMMED_LOC = f"{directory}C0{j}{suffix}"

                #write it into the text file

                with open("concat_clips.txt", "a") as file:
                    file.write(f"file '{TRIMMED_LOC}'\n")

            if i[0] == i [-1]:
                outputfilename = f"C0{i[0]}"
            else:
                outputfilename = f"C0{i[0]}-C0{i[-1]}"
            outputnobgloc = f"{directory}{outputfilename}.MOV"
            outputbgloc =  f"{directory}{outputfilename}_bg.MOV"
            outputbglocfinal = f"{directory}{outputfilename}bg.MOV"
            command = f"ffmpeg -f concat -safe 0 -i {text_file} -c copy {outputnobgloc} -hide_banner -loglevel error"
            subprocess.call(command, shell=True)

            # attach background
            CUTCOVER = "./files/OUTPUT/cutcover/"
            try:
                os.mkdir(CUTCOVER)
            except FileExistsError:
                pass
            WAV_DIRECTORY = "./files/OUTPUT/wav_files/"
            try:
                os.mkdir(WAV_DIRECTORY)
            except FileExistsError:
                pass

            print(f"Attaching background to {outputfilename}.MP4")

            filelength = float(get_length(outputnobgloc))
            # Cut cover to match audio duration
            output_cover = f"{CUTCOVER}{outputfilename}.MP4"
            command = f"ffmpeg -ss -0 -i {backgroundloc} -t {filelength} -c copy {output_cover} -hide_banner -loglevel error"
            subprocess.call(command, shell=True)

            # # overlay cut cover onto video
            # command = f'ffmpeg -i {outputnobgloc} -i {output_cover} -c:a copy -filter_complex "[0:v] overlay" {outputbg} -hide_banner -loglevel error'
            # subprocess.call(command, shell=True)

            OUTPUT_WAV = f"{WAV_DIRECTORY}{outputfilename}.WAV"
            # st()
            # convert no bg to WAV
            command = f"ffmpeg -i {outputnobgloc} -vn -acodec copy {OUTPUT_WAV} -hide_banner -loglevel error"
            subprocess.call(command, shell=True)

            # attach audio to video
            command = f"ffmpeg -i {output_cover} -i {OUTPUT_WAV} {outputbgloc} -hide_banner -loglevel error"
            subprocess.call(command, shell=True)

            # Cut last frame of video (audio is a little longer so ffmpeg adds a frame to the end of the snippet)
            # st()
            filelength = float(get_length(outputbgloc))
            cutlength = (filelength - (1 / 24)) #0.042
            command = f"ffmpeg -ss -0 -i {outputbgloc} -t {cutlength} -c copy {outputbglocfinal} -hide_banner -loglevel error"
            subprocess.call(command, shell=True)

            os.remove(outputnobgloc)
            os.remove(outputbgloc)

            for j in i:
                TRIMMED_LOC = f"{directory}C0{j}{suffix}"
                # WAV_LOC = f"{directory}C0{j}_TRIMMED.WAV"
                os.remove(TRIMMED_LOC)

            os.remove(text_file)

        # add blue background to concatenated files

    else:
        pass

    try:
        shutil.rmtree(CUTCOVER)
    except FileNotFoundError:
        pass
    try:
        shutil.rmtree(WAV_DIRECTORY)
    except FileNotFoundError:
        pass

if __name__ == "__main__":
    # dup_dir(OUTPUT_VIDEO_DIRECTORY, directory)
    # add_transparency("_TRIMMED.MP4", clips_ben)
    # add_transparency("_TRIMMEDCOVER.MP4", clips_cover)
    replace_footage(clips_background)