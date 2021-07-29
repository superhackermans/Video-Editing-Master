from parameters import *

def concat_and_replace (suffix, new_suffix, clips, directory, replacement_footage):
    for k, v in clips.items():
        if v == "toc":
            clips[k] = "100"
    clips = {int(k):v for k, v in clips.items()}
    if bool(clips) == True:
        clips_list = list(clips.keys())
        consecutive_clips = group_consecutives(clips_list)
        for group in consecutive_clips:
            createPath(cover_cut)
            createPath(wav_dir)

            if group[0] == group[-1]:
                outputfilename = f"{cam}{group[0]}"
            else:
                outputfilename = f"{cam}{group[0]}-{cam}{group[-1]}"

            if replacement_footage == vid_transparency_smol:
                print(f"Adding transparency to {outputfilename}")
            elif replacement_footage == backgroundloc:
                print(f"Adding background to {outputfilename}")
            else:
                pass

            # lens = []
            frames = []
            for i in group:
                fileloc = f"{directory}{cam}{i}{suffix}"
                # filelen = float(get_length(fileloc))
                # lens.append(filelen)
                packets = float(get_packets(fileloc))
                frames.append(packets)
                # print(f"frames by length is {filelen*frameRate}")
                # print(f"frames by frame is {packets}")
                deleteFile(fileloc)

            # current_total_len = sum(lens)
            # print(f"Current total len is {current_total_len}")
            desired_frames = float(sum(frames))
            current_total_len = float(desired_frames/frameRate)
            # print(f"Current total len is {current_total_len}")

            if replacement_footage == vid_transparency_smol:
                output = f"{directory}{outputfilename}{new_suffix}"
                command = f"ffmpeg -ss -0 -i {replacement_footage} -t {current_total_len} -c copy {output} -hide_banner -loglevel error"
                subprocess.call(command, shell=True)
            else:
                output = f"{directory}{outputfilename}{new_suffix}"
                command = f"ffmpeg -ss -0 -i {replacement_footage} -t {current_total_len} {output} -hide_banner -loglevel error"
                subprocess.call(command, shell=True)

            # outputframes = float(get_packets(output))
            # framediscrepancy = float(outputframes-desired_frames)
            # if framediscrepancy == 0:
            #     pass
            # else:
            #     while framediscrepancy>.5:
            #         adjustment = .051
            #         current_total_len = float(outputframes/frameRate-(adjustment))
            #
            #         print(f"Total frames is now {outputframes}. Desired frames is {desired_frames}")
            #         print(f"There is a discrepancy of {framediscrepancy} frame(s). Trimming clip.")
            #         print(f"Adjustment is {adjustment}")
            #         print(f"Readjusting to {current_total_len * frameRate}.")
            #
            #         output = f"{directory}{outputfilename}{new_suffix}"
            #         command = f"ffmpeg -y -ss -0 -i {replacement_footage} -t {current_total_len} {output} -hide_banner -loglevel error"
            #         subprocess.call(command, shell=True)
            #
            #         outputframes = float(get_packets(output))
            #         framediscrepancy = float(outputframes-desired_frames)
            #     while framediscrepancy<-.5:
            #         adjustment = -.051
            #         current_total_len = float(outputframes/frameRate-(adjustment))
            #
            #         print(f"Total frames is now {outputframes}. Desired frames is {desired_frames}")
            #         print(f"There is a discrepancy of {framediscrepancy} frame(s). Extending clip.")
            #         print(f"Adjustment is {adjustment}")
            #         print(f"Readjusting to {current_total_len * frameRate}.")
            #
            #         output = f"{directory}{outputfilename}{new_suffix}"
            #         command = f"ffmpeg -y -ss -0 -i {replacement_footage} -t {current_total_len} {output} -hide_banner -loglevel error"
            #         subprocess.call(command, shell=True)
            #
            #         outputframes = float(get_packets(output))
            #         framediscrepancy = float(outputframes-desired_frames)
            #     print(f"The discrepancy is {framediscrepancy} frame(s).")

            # #from pic
            # output = f"{directory}{outputfilename}pic{new_suffix}"
            # command = f"ffmpeg -loop 1 -i {pic_transparency} -t {totallen} {output} -hide_banner -loglevel error "
            # subprocess.call(command, shell=True)


if __name__ == "__main__":
    dup_dir(layer3, layer2)
    concat_and_replace("_TRIMMED.MP4", clips_all_except_pics_and_vid, layer2, vid_transparency_smol)