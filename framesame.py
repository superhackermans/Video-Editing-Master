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

        INPUTCLIP = f"{directory}C0{k}{suffix}"
        MIDDLE_OUTPUT = f"{directory}C0{k}TEMP{suffix}"
        FINAL_OUTPUT = f"{directory}C0{k}{suffix}"

        filelen = round(float(get_length(INPUTCLIP)), decimals)

        # st()

        renamefile(INPUTCLIP, MIDDLE_OUTPUT)
        deleteFile(INPUTCLIP)

        command = f"ffmpeg -ss -0 -i {MIDDLE_OUTPUT} -t {filelen}" \
                  f" -c:v libx264 -strict -2 " \
                  f" {FINAL_OUTPUT} -hide_banner -loglevel error"
        subprocess.call(command, shell=True)

        deleteFile(MIDDLE_OUTPUT)


if __name__ == "__main__":
    frame_same("_TRIMMED", clips_all, layer2)