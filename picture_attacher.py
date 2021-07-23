from parameters import *

def attach_pictures(suffix, clips, directory):
    print("Beginning picture attaching")

    copy_directory(pic_dir_in, pic_dir_out)

    jpg_to_png(pic_dir_in)

    for key, value in clips.items():
        if value.isdigit:
            INPUT_PICTURE = f"{pic_dir_in}{value}.png"
            OUTPUT_PICTURE = f"{pic_dir_in}{cam}{key}.png"
            copyfile(INPUT_PICTURE, OUTPUT_PICTURE)
        else:
            pass

        print(f"Attaching picture to {cam}{key}{suffix}")
        INPUT_IMAGE = f"{pic_dir_in}{cam}{key}.png"
        OUTPUT_MOV = f"{directory}{cam}{key}{suffix}"
        filelen = float(get_length(OUTPUT_MOV))
        command = f"ffmpeg -loop 1 -y -i {INPUT_IMAGE} -c copy -t {filelen} {OUTPUT_MOV} -hide_banner -loglevel error "
        subprocess.call(command, shell=True)

        deleteFile(OUTPUT_PICTURE)

def attach_videos(suffix, clips, directory):
    for k, v in clips.items():
        if os.path.isfile(f"{pic_dir_in}{v}.mov") == True:
            input = f"{pic_dir_in}{v}.mov"
            output = f"{pic_dir_in}{v}.mp4"
            command = f"ffmpeg -i {input} -hide_banner {output} -loglevel error"
            subprocess.call(command, shell=True)

        in_vid = f"{pic_dir_in}{v}.mp4"
        out_vid = f"{directory}{cam}{k}.mp4"
        original_vid = f"{directory}{cam}{k}{suffix}"

        original_len = get_length(original_vid)
        vid_len = get_length(in_vid)
        ratio = (original_len / vid_len)

        command = f'ffmpeg -y -i {in_vid} -filter_complex "[0:v]setpts=PTS*{str(ratio)}[v]" -map "[v]" -shortest {out_vid} -hide_banner -loglevel error'
        subprocess.call(command, shell=True)

        deleteFile(original_vid)


if __name__ == "__main__":
    # attach_pictures(filesuffix, clips_pictures, layer2)
    attach_videos(filesuffix, clips_video, layer2)