from parameters import *
import subprocess
from shutil import copyfile, rmtree, copytree
import os
from pdb import set_trace as st
import numpy as np
import shutil
import os.path

def frame_same(suffix, clips, directory):

    for k, v in dict(clips).items():

        INPUT = f"{directory}C0{k}{suffix}"
        FINAL_OUTPUT = f"{directory}C0{k}TEMP{suffix}"
        FINALFINAL_OUTPUT = f"{directory}C0{k}{suffix}"

        filelen = round(float(get_length(INPUT)), 2)

        # st()

        command = f"ffmpeg -ss -0 -i {INPUT} -t {filelen} -c copy {FINAL_OUTPUT} -hide_banner -loglevel error"
        subprocess.call(command, shell=True)

        os.remove(INPUT)

        command = f"ffmpeg -ss -0 -i {FINAL_OUTPUT} -t {filelen} -c copy {FINALFINAL_OUTPUT} -hide_banner -loglevel error"
        subprocess.call(command, shell=True)

        os.remove(FINAL_OUTPUT)


if __name__ == "__main__":
    frame_same("_TRIMMED", clips_all, OUTPUT_VIDEO_DIRECTORY)