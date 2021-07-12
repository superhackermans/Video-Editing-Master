import subprocess
from parameters import *


def remove_audio(directory):
    print(f"Removing audio from all videos in {directory}")
    clips = [] # clip is file name
    for file in os.listdir(directory):
        if file.endswith(".MP4") or file.endswith(".mp4") or file.endswith(".MOV") or file.endswith(".mov"):
            clips.append(file)
    if not clips:
        print("No input videos detected")
    clips = sorted(clips)
    for clip in clips:
        in_vid = f"{directory}{clip}"
        out_vid = f"{directory}temp{clip}"
        command = f"ffmpeg -y -i {in_vid} -c copy -an {out_vid} -hide_banner -loglevel error"
        subprocess.call(command, shell=True)

        deleteFile(in_vid)
        renamefile(out_vid, in_vid)

if __name__ == "__main__":
    remove_audio(layer1)
    remove_audio(layer2)