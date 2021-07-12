from parameters import *
import numpy as np
from backgroundattacher import *
import os.path

#duplicate file
def dup_dir(directory, directory2):
    try:
        shutil.copytree(directory, directory2)
    except:
        FileExistsError
def group_consecutives(vals, step=1):
    """Return list of consecutive lists of numbers from vals (number list)."""
    run = []
    result = [run]
    expect = None
    for v in vals:
        if (v == expect) or (expect is None):
            run.append(v)
        else:
            run = [v]
            result.append(run)
        expect = v + step
    return result

def add_transparency(suffix, clips, directory):
    # print("Adding transparency to top layer files (OUTPUT/trimmed_files/)")
    createPath(wav_dir)

    # TOP LAYER (trimmed_files)
    # ben clips and TOC become transparent
    for k, v in dict(clips).items():
        filename = f"C0{k}{suffix}"
        print(f"Adding transparency to {filename}")
        INPUT_TRIMMED_FILE = f"{directory}{filename}"
        OUTPUT_WAV = f"{wav_dir}{inputToOutputNewWAV(k)}"
        FINAL_OUTPUT = f"{directory}C0{k}_TRIMMEDEMPTY.MOV"
        # FINALFINAL_OUTPUT = f"{directory}C0{k}_TRIMMEDEMPTY.MOV"
        # command = f'ffmpeg -i {INPUT_TRIMMED_FILE} -i {TRANSPARENCY} -c:a copy {FINAL_OUTPUT}'
        # subprocess.call(command, shell=True)

        # extract audio
        command = "ffmpeg -i " + INPUT_TRIMMED_FILE + " -hide_banner " + OUTPUT_WAV + " -loglevel error"
        subprocess.call(command, shell=True)

        # attach audio wav to transparent image
        command = "ffmpeg -loop 1 -y -i " + pic_transparency + " -i " + OUTPUT_WAV + " -shortest -acodec copy -vcodec png " + " -hide_banner -loglevel error " + FINAL_OUTPUT
        subprocess.call(command, shell=True)

        # filelength = float(get_length(FINAL_OUTPUT))

        layer3 = f"{layer3}{filename}"
        layer3len = round(float(get_length(layer3)), decimals)
        # print(f"Layer 3 filelength is {filelength2}")

        # command = f"ffmpeg -ss -0 -i {FINAL_OUTPUT} -t {filelength2} -c copy {FINALFINAL_OUTPUT} -hide_banner -loglevel error"
        # subprocess.call(command, shell=True)

        filelength = float(get_length(FINAL_OUTPUT))
        discrepancy = (filelength - layer3len) * discrepancy_multiplier

        # if discrepancy >= 0:
        #     print(f"Trimming by {discrepancy}")
        #     command = f"ffmpeg -ss -0 -i {FINAL_OUTPUT} -t {layer3len-(discrepancy)}" \
        #               f" -c:v libx264 -strict -2 " \
        #               f" {FINALFINAL_OUTPUT} -hide_banner -loglevel error"
        #     subprocess.call(command, shell=True)
        # else:
        #     print("nothing cut")
        #     command = f"ffmpeg -ss -0 -i {FINAL_OUTPUT} -t {layer3len} " \
        #               f" -c:v libx264 -strict -2 " \
        #               f" {FINALFINAL_OUTPUT} -hide_banner -loglevel error"
        #     subprocess.call(command, shell=True)

        # renamefile(FINAL_OUTPUT, FINALFINAL_OUTPUT)

        filelength = float(get_length(FINAL_OUTPUT))

        if filelength-layer3len == 0:
            print("There is no discrepancy between lengths of original clip and new clip.")
        else:
            print(f"filelength of C0{k}_TRIMMEDEMPTY.MOV is {filelength}")
            print(f"filelength of C0{k}_TRIMMED.MP4 layer 3 clip is {layer3len}")
            print(f"The discrepancy is {filelength - layer3len}")

        #remove old file
        deleteFile(INPUT_TRIMMED_FILE)
        # deleteFile(FINAL_OUTPUT)

    # deletePath(WAV_DIRECTORY)

        #resize video clips by .88 with alpha border

def replace_footage(suffix, clips_background, directory):

    # turning toc string into random integer... code doesnt work with strings so this is a simple workaround bc values dont even matter here
    for k, v in clips_background.items():
        if v == "toc":
            clips_background[k] = "100"
    clips_background = {int(k):int(v) for k, v in clips_background.items()}

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
                TRIMMED_LOC = f"{directory}C0{j}{suffix}"

                #write it into the text file

                with open("concat_clips.txt", "a") as file:
                    file.write(f"file '{TRIMMED_LOC}'\n")

            if group[0] == group[-1]:
                outputfilename = f"C0{group[0]}"
            else:
                outputfilename = f"C0{group[0]}-C0{group[-1]}"
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
            command = f"ffmpeg -ss -0 -i {backgroundloc} -t {filelength} " \
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
                TRIMMED_LOC = f"{directory}C0{j}{suffix}"
                # WAV_LOC = f"{directory}C0{j}_TRIMMED.WAV"
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
    replace_footage("_TRIMMED.MOV", clips_background, layer3)