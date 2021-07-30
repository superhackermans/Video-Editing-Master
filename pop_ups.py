from parameters import *
from background_layer import add_transparency, concat_and_replace

def bottom_pop_ups(clips, directory):
    if bool(clips.items()) == True:
        deletePath(directory)
        dup_dir(backuplayer, directory)
        add_transparency(filesuffix, filesuffix, clips_pop_up, directory)
    for k, v in clips.items():
        print(f"Attaching pop up {v} to {cam}{k}{filesuffix}")

        pop_up_loc = f"{pop_up_dir}{v}.mov"
        video_loc = f"{directory}{cam}{k}{filesuffix}"

        pop_up_len = get_length(pop_up_loc)
        video_len = get_length(video_loc)

        cutamt = 0/frameRate
        # print(pop_up_len, video_len)
        if pop_up_len>video_len:
            ratio = ((video_len-1/frameRate) / pop_up_len)
            command = f'ffmpeg -y -i {pop_up_loc} -filter_complex "[0:v]setpts=PTS*{str(ratio)}[v]" -map "[v]" -vcodec qtrle -shortest {video_loc} -hide_banner -loglevel error'
            subprocess.call(command, shell=True)
            # cut 1 frame off forward clip
            forward_video_loc = f"{directory}{cam}{str(int(k)+1).zfill(4)}{filesuffix}"
            forward_video_len = get_length(forward_video_loc)
            command = f"ffmpeg -ignore_chapters 1 -y -i {forward_video_loc} -vcodec qtrle -ss 0 -t {forward_video_len-cutamt} {tempclip(forward_video_loc)} -hide_banner -loglevel error"
            subprocess.call(command, shell=True)
            deleteFile(forward_video_loc)
            renamefile(tempclip(forward_video_loc), forward_video_loc)
        elif pop_up_len<video_len:
            command = f"ffmpeg -ignore_chapters 1 -y -i {video_loc} -vcodec qtrle -ss 0 -t {video_len-pop_up_len-cutamt} {directory}{cam}{k}.5{filesuffix} -hide_banner -loglevel error"
            subprocess.call(command, shell=True)
            deleteFile(video_loc)
            copyfile(pop_up_loc, video_loc)
        elif video_len == pop_up_len:
            deleteFile(video_loc)
            copyfile(pop_up_loc, video_loc)
        else:
            print("Don't know what to do.")
            pass

if __name__ == "__main__":
    bottom_pop_ups(clips_pop_up, layer_popups)
    concat_and_replace(filesuffix, filesuffix, clips_except_popups, layer_popups, vid_transparency_smol)