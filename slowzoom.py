from parameters import *


def slow_zoom(suffix, clips, directory):
    saturation = 1.06
    brightness = -.025
    zoom_in = 1.2

    clips = list(clips.items())

    first_clip_loc = f"{directory}{cam}{clips[0][0]}{suffix}"
    last_clip_loc = f"{directory}{cam}{clips[-1][0]}{suffix}"

    tempfile = f"{directory}{cam}{clips[0][0]}TEMP{suffix}"
    total_frames = get_packets(first_clip_loc)
    zoom_in_cmd = f"""-vf "scale=w=(3840*4):h=(2160*4), zoompan=z='min(pzoom+({zoom_in}-1)/{total_frames},{zoom_in})':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=3840x2160" """
    command = f"""ffmpeg -y -i {first_clip_loc} {zoom_in_cmd} -an {tempfile} -hide_banner -loglevel error"""
    subprocess.call(command, shell=True)

    # extract audio from original
    command = f"ffmpeg -i {first_clip_loc} -hide_banner {directory}{cam}{clips[0][0]}.wav -loglevel error"
    subprocess.call(command, shell=True)
    deleteFile(first_clip_loc)
    # attach audio to video
    command = f"ffmpeg -i {tempfile} -i {directory}{cam}{clips[0][0]}.wav -vf eq=brightness={brightness}:saturation={saturation} -c:v libx264 -strict -2  {first_clip_loc} -hide_banner -loglevel error"
    subprocess.call(command, shell=True)
    deleteFile(f"{directory}{cam}{clips[0][0]}.wav")
    deleteFile(tempfile)



    tempfile = f"{directory}{cam}{clips[-1][0]}TEMP{suffix}"
    total_frames = get_packets(last_clip_loc)
    zoom_in_cmd = f"""-vf "scale=w=(3840*4):h=(2160*4), zoompan=z='min(pzoom+({zoom_in}-1)/{total_frames},{zoom_in})':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=3840x2160" """
    command = f"""ffmpeg -y -i {last_clip_loc} {zoom_in_cmd} -an {tempfile} -hide_banner -loglevel error"""
    subprocess.call(command, shell=True)

    # extract audio from original
    command = f"ffmpeg -i {last_clip_loc} -hide_banner {directory}{cam}{clips[-1][0]}.wav -loglevel error"
    subprocess.call(command, shell=True)
    deleteFile(last_clip_loc)
    # attach audio to video
    command = f"ffmpeg -i {tempfile} -i {directory}{cam}{clips[-1][0]}.wav -vf eq=brightness={brightness}:saturation={saturation} -c:v libx264 -strict -2  {last_clip_loc} -hide_banner -loglevel error"
    subprocess.call(command, shell=True)
    deleteFile(f"{directory}{cam}{clips[-1][0]}.wav")
    deleteFile(tempfile)


def fade_out(suffix, clips, directory):
    pass


if __name__ == "__main__":
    slow_zoom("_TRIMMED.MP4", clips_ben, layer3)
