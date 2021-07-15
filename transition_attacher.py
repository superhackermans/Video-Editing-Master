from parameters import *
from background_layer import *
import subprocess

#suffix of the top layer which is to be replaced
def transitions(suffix, clips_background, directory):

    for k, v in clips_background.items():
        if v == "toc":
            clips_background[k] = "100"
    clips_background = {int(k):int(v) for k, v in clips_background.items()}

    # connect consecutive clips
    clips = list(clips_background.items())
    if bool(clips) == True:
        arr = np.array(clips)
        consecutive_clips = group_consecutives(arr[:, 0])

        for group in consecutive_clips:
            if group[0] == group[-1]:
                workingfiles = f"{cam_pre}{group[0]}{suffix}"
            else:
                workingfiles = f"{cam_pre}{group[0]}{suffix} to {cam_pre}{group[-1]}{suffix}"

            print(f"Attaching transitions to {workingfiles}")

            transition_in_1 = f"{cam_pre}{group[0]-1}{suffix}"
            transition_in_2 = f"{cam_pre}{group[0]}{suffix}"
            transition_out_1 = f"{cam_pre}{group[-1]}{suffix}"
            transition_out_2 = f"{cam_pre}{group[-1] + 1}{suffix}"

            transition_in_11 = f"{cam_pre}{group[0]-1}.5{suffix}"
            transition_in_22 = f"{cam_pre}{group[0]}_1{suffix}"
            transition_out_11 = f"{cam_pre}{group[-1]}.5{suffix}"
            transition_out_22 = f"{cam_pre}{group[-1]+1}_1{suffix}"

            in_1_len = float(get_length(in_1))
            in_2_len = float(get_length(in_2))
            out_1_len = float(get_length(out_1))
            out_2_len = float(get_length(out_2))

            # TRANSITION IN
            # if prior clip is a cover page, pass
            if clips_images[str(group[0]-1)] in clips_cover.values():
                pass
            else:

                transition_in_1_loc = f"{directory}{transition_in_1}"
                TEMP_transition_in_1_loc = f"{directory}TEMP{transition_in_1}"
                transition_in_1_len = float(get_length(transition_in_1_loc))
                difference = transition_in_1_len-in_1_len
                command = f"ffmpeg -ignore_chapters 1 -y -i {transition_in_1_loc} -vcodec qtrle -ss 0 -t {difference} {TEMP_transition_in_1_loc} -hide_banner -loglevel error"
                subprocess.call(command, shell=True)

                deleteFile(transition_in_1_loc)
                renamefile(TEMP_transition_in_1_loc, transition_in_1_loc)

                transition_in_2_loc = f"{directory}{transition_in_2}"
                TEMP_transition_in_2_loc = f"{directory}TEMP{transition_in_2}"
                transition_in_2_len = float(get_length(transition_in_2_loc))
                overalllen = transition_in_2_len-in_2_len
                command = f"ffmpeg -ignore_chapters 1 -y -i {transition_in_2_loc} -vcodec qtrle -ss {in_2_len} -t {overalllen} {TEMP_transition_in_2_loc} -hide_banner -loglevel error"
                subprocess.call(command, shell=True)

                deleteFile(transition_in_2_loc)
                renamefile(TEMP_transition_in_2_loc, transition_in_2_loc)

                copyfile(trans_in, f"{directory}{transition_in_11}")

            # TRANSITION OUT
            # if afterwards clip is a cover page, pass
            if clips_images[str(group[-1] + 1)] in clips_cover.values():
                pass
            else:
                transition_out_1_loc = f"{directory}{transition_out_1}"
                TEMP_transition_out_1_loc = f"{directory}TEMP{transition_out_1}"
                transition_out_1_len = float(get_length(transition_out_1_loc))
                difference = transition_out_1_len - out_1_len
                command = f"ffmpeg -ignore_chapters 1 -y -i {transition_out_1_loc} -vcodec qtrle -ss 0 -t {difference} {TEMP_transition_out_1_loc} -hide_banner -loglevel error"
                subprocess.call(command, shell=True)

                deleteFile(transition_out_1_loc)
                renamefile(TEMP_transition_out_1_loc, transition_out_1_loc)

                transition_out_2_loc = f"{directory}{transition_out_2}"
                TEMP_transition_out_2_loc = f"{directory}TEMP{transition_out_2}"
                transition_out_2_len = float(get_length(transition_out_2_loc))
                overalllen = transition_out_2_len-out_2_len
                command = f"ffmpeg -ignore_chapters 1 -y -i {transition_out_2_loc} -vcodec qtrle -ss {out_2_len} -t {overalllen} {TEMP_transition_out_2_loc} -hide_banner -loglevel error"
                subprocess.call(command, shell=True)

                deleteFile(transition_out_2_loc)
                renamefile(TEMP_transition_out_2_loc, transition_out_2_loc)

                copyfile(trans_out, f"{directory}{transition_out_11}")

                # st()

if __name__ == '__main__':
    transitions("_TRIMMEDEMPTY.MOV", clips_background, layer1)