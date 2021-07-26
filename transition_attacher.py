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

        in_1_len = get_packets(in_1)/frameRate
        # in_2_len = float(get_length(in_2))
        out_1_len = get_packets(out_1)/frameRate
        # out_2_len = float(get_length(out_2))

        first_clip_loc = f"{directory}{cam}{clips[0][0] - 1}{suffix}"
        first_clip_locTEMP = f"{directory}{cam}{clips[0][0] - 1}TEMP{suffix}"
        first_clip_len = get_packets(first_clip_loc)/frameRate
        cut_len = (in_1_len + out_1_len) / 2
        overalllen = first_clip_len - cut_len
        command = f"ffmpeg -ignore_chapters 1 -y -i {first_clip_loc} -vcodec qtrle -ss {cut_len} -t {overalllen} {first_clip_locTEMP} -hide_banner -loglevel error"
        subprocess.call(command, shell=True)

        deleteFile(first_clip_loc)
        renamefile(first_clip_locTEMP, first_clip_loc)


        for group in consecutive_clips:
            if group[0] == group[-1]:
                workingfiles = f"{cam}{group[0]}{suffix}"
            else:
                workingfiles = f"{cam}{group[0]}{suffix} to {cam}{group[-1]}{suffix}"

            print(f"Attaching transitions to {workingfiles}")

            # transition_in_1 = f"{cam_pre}{group[0]-1}{suffix}"
            transition_in_2 = f"{cam}{group[0]}{suffix}"
            # transition_out_1 = f"{cam_pre}{group[-1]}{suffix}"
            transition_out_2 = f"{cam}{group[-1] + 1}{suffix}"

            transition_in_11 = f"{cam}{group[0] - 1}.5{suffix}"
            # transition_in_22 = f"{cam_pre}{group[0]}_1{suffix}"
            transition_out_11 = f"{cam}{group[-1]}.5{suffix}"
            # transition_out_22 = f"{cam_pre}{group[-1]+1}_1{suffix}"

            # TRANSITION IN
            # if prior clip is a cover page, pass
            if clips_images[str(group[0]-1)] in clips_cover.values():
                pass
            else:
                # transition_in_1_loc = f"{directory}{transition_in_1}"
                # TEMP_transition_in_1_loc = f"{directory}TEMP{transition_in_1}"
                # transition_in_1_len = float(get_length(transition_in_1_loc))
                # difference = transition_in_1_len-in_1_len
                # command = f"ffmpeg -ignore_chapters 1 -y -i {transition_in_1_loc} -vcodec qtrle -ss 0 -t {difference} {TEMP_transition_in_1_loc} -hide_banner -loglevel error"
                # subprocess.call(command, shell=True)
                #
                # deleteFile(transition_in_1_loc)
                # renamefile(TEMP_transition_in_1_loc, transition_in_1_loc)
                #
                # transition_in_2_loc = f"{directory}{transition_in_2}"
                # TEMP_transition_in_2_loc = f"{directory}TEMP{transition_in_2}"
                # transition_in_2_len = float(get_length(transition_in_2_loc))
                # overalllen = transition_in_2_len-in_2_len
                # command = f"ffmpeg -ignore_chapters 1 -y -i {transition_in_2_loc} -vcodec qtrle -ss {in_2_len} -t {overalllen} {TEMP_transition_in_2_loc} -hide_banner -loglevel error"
                # subprocess.call(command, shell=True)
                #
                # deleteFile(transition_in_2_loc)
                # renamefile(TEMP_transition_in_2_loc, transition_in_2_loc)

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
            if clips_images[str(group[-1] + 1)] in clips_cover.values():
                pass
            else:
                # transition_out_1_loc = f"{directory}{transition_out_1}"
                # TEMP_transition_out_1_loc = f"{directory}TEMP{transition_out_1}"
                # transition_out_1_len = float(get_length(transition_out_1_loc))
                # difference = transition_out_1_len - out_1_len
                # command = f"ffmpeg -ignore_chapters 1 -y -i {transition_out_1_loc} -vcodec qtrle -ss 0 -t {difference} {TEMP_transition_out_1_loc} -hide_banner -loglevel error"
                # subprocess.call(command, shell=True)
                #
                # deleteFile(transition_out_1_loc)
                # renamefile(TEMP_transition_out_1_loc, transition_out_1_loc)

                # transition_out_2_loc = f"{directory}{transition_out_2}"
                # TEMP_transition_out_2_loc = f"{directory}TEMP{transition_out_2}"
                # transition_out_2_len = float(get_length(transition_out_2_loc))
                # overalllen = transition_out_2_len-out_2_len
                # command = f"ffmpeg -ignore_chapters 1 -y -i {transition_out_2_loc} -vcodec qtrle -ss {out_2_len} -t {overalllen} {TEMP_transition_out_2_loc} -hide_banner -loglevel error"
                # subprocess.call(command, shell=True)
                #
                # deleteFile(transition_out_2_loc)
                # renamefile(TEMP_transition_out_2_loc, transition_out_2_loc)
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

                # st()

if __name__ == '__main__':
    transitions(filesuffix, clips_background, layer1)