from parameters import *
from background_layer import add_transparency

def bottom_pop_ups(clips, directory):
    for k, v in clips.items():
        print(f"Attaching pop up {v} to {cam}{k}")
        createPath(directory)
        dup_dir(backuplayer, directory)
        add_transparency(filesuffix, filesuffix, clips_all, directory)

        pop_up_loc = f"{pop_up_dir}{v}.mov"
        video_loc = f"{directory}{cam}{k}{filesuffix}"

        pop_up_len = get_length(pop_up_loc)
        video_len = get_length(video_loc)

        if pop_up_len>video_len:
            ratio = (video_len / pop_up_len)
            command = f'ffmpeg -y -i {pop_up_loc} -filter_complex "[0:v]setpts=PTS*{str(ratio)}[v]" -map "[v]" -shortest {video_loc} -hide_banner -loglevel error'
            subprocess.call(command, shell=True)
        elif video_len<pop_up_len:
            command = f"ffmpeg -ignore_chapters 1 -y -i {video_loc} -vcodec qtrle -ss 0 -t {video_len-pop_up_len} {tempclip(video_loc)} -hide_banner -loglevel error"
            subprocess.call(command, shell=True)
            deleteFile(video_loc)
            renamefile(tempclip(video_loc), video_loc)
            copyfile(pop_up_loc, f"{directory}{cam}{k}.5{filesuffix}")
        elif video_len == pop_up_len:
            deleteFile(video_loc)
            copyfile(pop_up_loc, video_loc)
        else:
            print("Don't know what to do.")
            pass

if __name__ == "__main__":
    bottom_pop_ups(clips_pop_up, layer00)