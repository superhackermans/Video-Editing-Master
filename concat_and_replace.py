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

            if str(group[0]).zfill(4) == str(group[-1]).zfill(4):
                outputfilename = f"{cam}{str(str(group[0]).zfill(4))}"
            else:
                outputfilename = f"{cam}{str(str(group[0]).zfill(4))}-{cam}{str(str(group[-1]).zfill(4))}"

            if replacement_footage == vid_transparency_smol:
                print(f"Adding transparency to {outputfilename}")
            elif replacement_footage == backgroundloc:
                print(f"Adding background to {outputfilename}")
            else:
                pass
            # lens = []
            frames = []
            for i in group:
                fileloc = f"{directory}{cam}{str(i).zfill(4)}{suffix}"
                packets = float(get_packets(fileloc))
                frames.append(packets)
                deleteFile(fileloc)

            desired_frames = float(sum(frames))
            current_total_len = float(desired_frames/frameRate)

            if replacement_footage == vid_transparency_smol:
                output = f"{directory}{outputfilename}{new_suffix}"
                command = f"ffmpeg -ss -0 -i {replacement_footage} -t {current_total_len} -c copy {output} -hide_banner -loglevel error"
                subprocess.call(command, shell=True)
            else:
                output = f"{directory}{outputfilename}{new_suffix}"
                command = f"ffmpeg -ss -0 -i {replacement_footage} -t {current_total_len} {output} -hide_banner -loglevel error"
                subprocess.call(command, shell=True)



if __name__ == "__main__":
    # dup_dir(layer3, layer2)
    concat_and_replace(filesuffix, filesuffix, clips_except_popups, layer_popups, vid_transparency_smol)
