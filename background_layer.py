from parameters import *

def convertfile(suffix, newsuffix, clips, directory):
    if bool(clips.items) == True:
        for key, value in clips.items():
            print(f"Converting {cam}{key}{suffix} to {cam}{key}{newsuffix}...")
            filename = f"{directory}{cam}{key}{suffix}"
            newfilename = f"{directory}{cam}{key}{newsuffix}"

            command = f"ffmpeg -i {filename} -hide_banner {newfilename} -loglevel error"
            subprocess.call(command, shell=True)

            deleteFile(filename)

def concat_and_replace (suffix, new_suffix, clips, directory, replacement_footage):
    for k, v in clips.items():
        if v == "toc":
            clips[k] = "100"
    clips = {int(k):v for k, v in clips.items()}
    if bool(clips) == True:
        if replacement_footage == vid_transparency_smol:
            print(f"Adding transparency to {str(clips)} in {directory}")
        elif replacement_footage == backgroundloc:
            print(f"Adding background to {str(clips)} in {directory}")
        else:
            pass
        clips_list = list(clips.keys())
        consecutive_clips = group_consecutives(clips_list)
        for group in consecutive_clips:
            createPath(cover_cut)
            createPath(wav_dir)

            if str(group[0]).zfill(4) == str(group[-1]).zfill(4):
                outputfilename = f"{cam}{str(str(group[0]).zfill(4))}"
            else:
                outputfilename = f"{cam}{str(str(group[0]).zfill(4))}-{cam}{str(str(group[-1]).zfill(4))}"

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

def add_transparency(suffix, newsuffix, clips, directory):
    # print("Adding transparency to top layer files (OUTPUT/trimmed_files/)")
    print(f"Adding transparency to {clips} in {directory}")
    for k, v in dict(clips).items():
        filename = f"{cam}{k}{suffix}"
        INPUT_TRIMMED_FILE = f"{directory}{filename}"
        FINAL_OUTPUT = f"{directory}{cam}TEMP{k}{newsuffix}"
        totallen = float(get_packets(INPUT_TRIMMED_FILE))/frameRate

        command = f"ffmpeg -ss -0 -i {vid_transparency_smol} -t {totallen} -c copy " \
                  f" {FINAL_OUTPUT} -hide_banner -loglevel error"
        subprocess.call(command, shell=True)

        deleteFile(INPUT_TRIMMED_FILE)
        renamefile(FINAL_OUTPUT, INPUT_TRIMMED_FILE)


def replace_footage(suffix, clips_background, directory, replacement_footage):

    # turning toc string into random integer... code doesnt work with strings so this is a simple workaround bc values dont even matter here
    for k, v in clips_background.items():
        if v == "toc":
            clips_background[k] = "100"
    clips_background = {int(k):int(v) for k, v in clips_background.items()}

    deletePath(wav_dir)
    deletePath(cover_cut)

    # connect consecutive clips
    cc = list(clips_background.items())
    if bool(cc) == True:
        arr = np.array(cc)
        consecutive_clips = group_consecutives(arr[:, 0])

        for group in consecutive_clips:
            createPath(cover_cut)
            createPath(wav_dir)

            text_file = 'concat_clips.txt'
            with open(text_file, 'w') as fp:
                pass
            for j in group:
                TRIMMED_LOC = f"{directory}{cam}{j}{suffix}"

                #write it into the text file

                with open("concat_clips.txt", "a") as file:
                    file.write(f"file '{TRIMMED_LOC}'\n")

            if group[0] == group[-1]:
                outputfilename = f"{cam}{group[0]}"
            else:
                outputfilename = f"{cam}{group[0]}-{cam}{group[-1]}"
            outputnobgloc = f"{directory}{outputfilename}.MOV"
            outputbgloc =  f"{directory}{outputfilename}_bg.MOV"
            outputbglocfinal = f"{directory}{outputfilename}bg.MOV"
            command = f"ffmpeg -f concat -safe 0 -i {text_file} -c copy {outputnobgloc} -hide_banner -loglevel error"
            subprocess.call(command, shell=True)

            # attach background
            print(f"Attaching background to {outputfilename}.MP4")

            filelength = float(get_length(outputnobgloc))
            # Cut cover to match audio duration
            output_cover = f"{cover_cut}{outputfilename}.MP4"
            command = f"ffmpeg -ss -0 -i {replacement_footage} -t {filelength} " \
                      f" -c:v libx264 -strict -2 " \
                      f" {output_cover} -hide_banner -loglevel error"
            subprocess.call(command, shell=True)

            # # overlay cut cover onto video
            # command = f'ffmpeg -i {outputnobgloc} -i {output_cover} -c:a copy -filter_complex "[0:v] overlay" {outputbg} -hide_banner -loglevel error'
            # subprocess.call(command, shell=True)

            OUTPUT_WAV = f"{wav_dir}{outputfilename}.WAV"

            # convert no bg to WAV
            command = f"ffmpeg -i {outputnobgloc} -vn -acodec copy {OUTPUT_WAV} -hide_banner -loglevel error"
            subprocess.call(command, shell=True)

            # attach audio to video
            command = f"ffmpeg -i {output_cover} -i {OUTPUT_WAV} {outputbgloc} -hide_banner -loglevel error"
            subprocess.call(command, shell=True)

            # Cut last frame of video (audio is a little longer so ffmpeg adds a frame to the end of the snippet)
            # st()
            # filelength = float(get_length(outputbgloc))
            # cutlength = (filelength - (cutamtbg))
            # command = f"ffmpeg -ss -0 -i {outputbgloc} -t {cutlength}" \
            #           f" -c:v libx264 -strict -2 " \
            #           f"{outputbglocfinal} -hide_banner -loglevel error"
            # subprocess.call(command, shell=True)

            renamefile(outputbgloc, outputbglocfinal)

            deleteFile(outputnobgloc)

            for j in group:
                TRIMMED_LOC = f"{directory}{cam}{j}{suffix}"
                deleteFile(TRIMMED_LOC)

            deleteFile(text_file)

        # add blue background to concatenated files

    else:
        pass

    deletePath(cover_cut)
    deletePath(wav_dir)

if __name__ == "__main__":
    # dup_dir(OUTPUT_VIDEO_DIRECTORY, directory)
    # add_transparency("_TRIMMED.MP4", clips_ben)
    # add_transparency("_TRIMMEDCOVER.MP4", clips_cover)
    replace_footage("_TRIMMED.MOV", clips_background, layer3, backgroundloc)