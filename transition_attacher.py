from parameters import *

#suffix of the top layer which is to be replaced
def transitions(suffix, clips_background, directory):

    for k, v in clips_background.items():
        if v == "toc":
            clips_background[k] = "100"
        if v == "v1":
            clips_background[k] = "101"
        if v == "v2":
            clips_background[k] = "102"
        if v == "v3":
            clips_background[k] = "103"
        if v == "v4":
            clips_background[k] = "104"
        if v == "v5":
            clips_background[k] = "105"
        if "," in v:
            clips_background[k] = "106"
    clips_background = {int(k):int(v) for k, v in clips_background.items()}

    # connect consecutive clips
    clips = list(clips_background.items())
    if bool(clips) == True:
        arr = np.array(clips)
        consecutive_clips = group_consecutives(arr[:, 0])

        for group in consecutive_clips:
            if str(group[0]).zfill(4) == str(group[-1]).zfill(4):
                workingfiles = f"{cam}{str(group[0]).zfill(4)}{suffix}"
            else:
                workingfiles = f"{cam}{str(group[0]).zfill(4)}{suffix} to {cam}{str(group[-1]).zfill(4)}{suffix}"
            print(f"Attaching transitions to {workingfiles}")

            transition_in_2 = f"{cam}{str(group[0]).zfill(4)}{suffix}"
            transition_out_2 = f"{cam}{str(group[-1] + 1).zfill(4)}{suffix}"
            transition_in_11 = f"{cam}{str(group[0] - 1).zfill(4)}.5{suffix}"
            transition_out_11 = f"{cam}{str(group[-1]).zfill(4)}.5{suffix}"

            if clips_images[str(group[0]-1).zfill(4)] in clips_cover.values():
                pass
            else:
                trans_in_len = get_packets(trans_in)/frameRate
                transition_in_2_loc = f"{directory}{transition_in_2}"
                TEMP_transition_in_2_loc = f"{directory}TEMP{transition_in_2}"
                transition_in_2_len = get_packets(transition_in_2_loc)/frameRate
                overalllen = transition_in_2_len-trans_in_len
                command = f"ffmpeg -ignore_chapters 1 -y -i {transition_in_2_loc} -vcodec qtrle -ss {trans_in_len} -t {overalllen} {TEMP_transition_in_2_loc} -hide_banner -loglevel error"
                subprocess.call(command, shell=True)

                deleteFile(transition_in_2_loc)
                renamefile(TEMP_transition_in_2_loc, transition_in_2_loc)

                copyfile(trans_in, f"{directory}{transition_in_11}")

            # TRANSITION OUT
            # if afterwards clip is a cover page, pass
            if clips_images[str(group[-1] + 1).zfill(4)] in clips_cover.values():
                pass
            else:
                trans_out_len = get_packets(trans_out)/frameRate

                transition_out_2_loc = f"{directory}{transition_out_2}"
                TEMP_transition_out_2_loc = f"{directory}TEMP{transition_out_2}"
                transition_out_2_len = get_packets(transition_out_2_loc)/frameRate
                overalllen = transition_out_2_len-trans_out_len
                command = f"ffmpeg -ignore_chapters 1 -y -i {transition_out_2_loc} -vcodec qtrle -ss {trans_out_len} -t {overalllen} {TEMP_transition_out_2_loc} -hide_banner -loglevel error"
                subprocess.call(command, shell=True)

                deleteFile(transition_out_2_loc)
                renamefile(TEMP_transition_out_2_loc, transition_out_2_loc)


                copyfile(trans_out, f"{directory}{transition_out_11}")

        list_clips = list(clips_all.items())
        first_clip_loc = f"{directory}{cam}{str(list_clips[0][0]).zfill(4)}{suffix}"
        firstclip_len = get_packets(first_clip_loc)/frameRate
        trans_in_len = get_packets(trans_in) / frameRate
        command = f"ffmpeg -ignore_chapters 1 -y -i {first_clip_loc} -vcodec qtrle -ss 0 -t {firstclip_len-(trans_in_len/2)} {tempclip(first_clip_loc)} -hide_banner -loglevel error"
        subprocess.call(command, shell=True)
        deleteFile(first_clip_loc)
        renamefile(tempclip(first_clip_loc), first_clip_loc)

if __name__ == '__main__':
    transitions(filesuffix, clips_background, layer1)