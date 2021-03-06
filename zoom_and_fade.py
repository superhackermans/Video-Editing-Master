from parameters import *

def altzoom(suffix, clips, directory):
    #zoom in alternating

    clips = list(clips.keys())
    alterClips = altElement(clips)
    alterClips = sorted(alterClips[1:-1])

    TEMP_FOLDER = "./files/OUTPUT/alterClips/"
    createPath(TEMP_FOLDER)

    zoomdimension = original_dimensions[0]*scale_factor, original_dimensions[1]*scale_factor

    scale_x = int((original_dimensions[0]-zoomdimension[0])/2)
    scale_y = int((original_dimensions[1]-zoomdimension[1])/2 + raise_up)

    zoomcommand = f'"crop={zoomdimension[0]}:{zoomdimension[1]}:{scale_x}:{scale_y}"' #no idea why it works with the z. cant figure it out otherwise

    for clip in alterClips:
        filename = f"{cam}{clip}{suffix}"
        move_file(directory, filename, TEMP_FOLDER)
        print(f"Preparing to zoom in {filename}")
    for clip in alterClips:
        filename = f"{cam}{clip}{suffix}"
        print(f"Zooming in {filename}")
        INPUT_TRIMMED_FILE = f"{TEMP_FOLDER}{inputToOutputNewTrimmed(clip)}"
        OUTPUT_ZOOMED = f"{directory}{inputToOutputNewTrimmedAndZoomed(clip)}"
        #convert trimmed mp4 into WAV
        command = f'ffmpeg -y -i {INPUT_TRIMMED_FILE} -filter:v {zoomcommand} -c:a copy {OUTPUT_ZOOMED} -hide_banner -loglevel error'
        # st()
        subprocess.call(command, shell=True)

    shutil.rmtree(TEMP_FOLDER)

def slow_zoom(suffix, clips, directory):
    saturation = 1.00
    brightness = 0
    gamma = .98
    gamma_r = 1
    gamma_g = 0.99
    zoom_in = 1.2
    zoom_out = 1.3

    clips = list(clips.items())

    first_clip_loc = f"{directory}{cam}{str(clips[0][0]).zfill(4)}{suffix}"
    last_clip_loc = f"{directory}{cam}{str(clips[-1][0]).zfill(4)}{suffix}"

    def zoom(inorout, clip_loc):
        print(f"Implementing slow zoom {inorout} on {clip_loc}")
        tempfile = tempclip(clip_loc)
        total_frames = get_packets(clip_loc)
        if inorout == "in":
            zoom_cmd = (
                f"""-vf "scale=w=({original_dimensions[0]}*4):h=({original_dimensions[1]}*4), 
                zoompan=z='min(pzoom+({zoom_in}-1)/{total_frames},{zoom_in})':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':
                s={original_dimensions[0]}x{original_dimensions[1]}:fps={frameRate}" """
            )
        if inorout == "out":
            num = (zoom_out - 1) / total_frames
            zoom_cmd = (
                f"""-vf "scale=w=({original_dimensions[0]}*4):h=({original_dimensions[1]}*4), 
                zoompan=z='if(lte(pzoom,1.0),{zoom_out},max(1.001,pzoom-{num}))':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':
                s={original_dimensions[0]}x{original_dimensions[1]}:fps={frameRate}" """
            )
        command = f"""ffmpeg -y -i {clip_loc} {zoom_cmd} {tempfile} -hide_banner -loglevel error"""
        subprocess.call(command, shell=True)
        #
        # readjust colors
        command = (
            f"ffmpeg -y -i {tempfile} -vf eq=gamma={gamma}:brightness={brightness}:saturation={saturation}:gamma_r={gamma_r}:gamma_g={gamma_g} "
            f"{clip_loc} -hide_banner -loglevel error"
        )
        subprocess.call(command, shell=True)
        deleteFile(tempfile)

    zoom("in", first_clip_loc)
    zoom("out", last_clip_loc)

def fade_out(suffix, clips, directory):
    clips = list(clips.items())

    last_clip_loc = f"{directory}{cam}{str(clips[-1][0]).zfill(4)}{suffix}"
    tempfile = tempclip(last_clip_loc)
    print(f"Fading out {last_clip_loc}")
    fadeduration = 1
    startfade = get_length(last_clip_loc)-fadeduration

    command = f"""ffmpeg -i {last_clip_loc} -vf "fade=t=out:st={startfade}:d={fadeduration}" -c:a copy {tempfile}  -hide_banner -loglevel error"""
    subprocess.call(command, shell=True)
    deleteFile(last_clip_loc)
    renamefile(tempfile, last_clip_loc)

if __name__ == "__main__":
    altzoom(filesuffix, clips_ben, layer4)
    slow_zoom(filesuffix, clips_ben, layer4)
    fade_out(filesuffix, clips_ben, layer4)
