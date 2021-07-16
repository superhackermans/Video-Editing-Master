from parameters import *
import subprocess
import shutil

def altzoom(suffix, clips, directory):
    #zoom in alternating

    clips = list(clips.keys())

    alterClips = altElement(clips)
    alterClips = sorted(alterClips[1:-2])

    TEMP_FOLDER = "./files/OUTPUT/alterClips/"
    createPath(TEMP_FOLDER)

    zoomdimension = original_dimensions[0]*scale_factor, original_dimensions[1]*scale_factor

    scale_x = (original_dimensions[0]-zoomdimension[0])/2
    scale_y = (original_dimensions[1]-zoomdimension[1])/2 + raise_up

    zoomcommand = f'"crop={zoomdimension[0]}:{zoomdimension[1]}:{scale_x}:{scale_y}z"' #no idea why it works with the z. cant figure it out otherwise


    source_dir = directory
    target_dir = TEMP_FOLDER

    for clip in alterClips:
        filename = f"{cam}{clip}{suffix}"
        try:
            shutil.move(os.path.join(source_dir, filename), target_dir)
        except:
            pass

    #extract WAV audio from trimmed videos
    for clip in alterClips:
        filename = f"{cam}{clip}{suffix}"
        print(f"Zooming in {filename}")
        INPUT_TRIMMED_FILE = f"{TEMP_FOLDER}{inputToOutputNewTrimmed(clip)}"
        OUTPUT_ZOOMED = f"{directory}{inputToOutputNewTrimmedAndZoomed(clip)}"
        #convert trimmed mp4 into WAV
        command = f'ffmpeg -i {INPUT_TRIMMED_FILE} -filter:v {zoomcommand} -c:a copy {OUTPUT_ZOOMED} -hide_banner -loglevel error'
        subprocess.call(command, shell=True)

    shutil.rmtree(TEMP_FOLDER)

if __name__ == "__main__":
    altzoom("_TRIMMED.MP4", clips_ben)