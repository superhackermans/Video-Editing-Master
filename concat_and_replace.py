from parameters import *
from background_layer import *

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
                outputfilename = f"{cam}{group[0]}-C0{group[-1]}"

            if replacement_footage == vid_transparency_smol:
                print(f"Adding transparency to {outputfilename}{new_suffix}")
            elif replacement_footage == backgroundloc:
                print(f"Adding background to {outputfilename}{new_suffix}")
            else:
                pass

            lens = []
            total_packets = []
            for i in group:
                fileloc = f"{directory}{cam}{i}{suffix}"
                filelen = float(get_length(fileloc))
                lens.append(filelen)
                packets = float(get_packets(fileloc))
                total_packets.append(packets)

                deleteFile(fileloc)

            if replacement_footage == backgroundloc:
                cutamt = cutamtbg
            else:
                cutamt = 0

            totallen = sum(lens)-cutamt
            totalpackets = float(sum(total_packets)/frameRate)

            output = f"{directory}{outputfilename}{new_suffix}"
            command = f"ffmpeg -ss -0 -i {replacement_footage} -t {totallen} -c copy " \
                      f" {output} -hide_banner -loglevel error"
            subprocess.call(command, shell=True)
            # st()
            # outputlen = float(get_length(output))
            outputframes = float(get_packets(output))/frameRate
            if totallen-outputframes == 0:
                print("There is no discrepancy")
            else:
                print(f"There is a discrepancy of {totallen-outputframes}")
            # #from pic
            # output = f"{directory}{outputfilename}pic{new_suffix}"
            # command = f"ffmpeg -loop 1 -i {pic_transparency} -t {totallen} {output} -hide_banner -loglevel error "
            # subprocess.call(command, shell=True)


if __name__ == "__main__":
    dup_dir(layer3, layer2)
    concat_and_replace("_TRIMMED.MP4", clips_all_except_pics, layer2, vid_transparency_smol)