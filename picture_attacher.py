from parameters import *
from background_layer import concat_and_replace



def jpg_to_png(directory):
    myJPEG = []
    for file in os.listdir(directory):
        if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".JPG") or file.endswith(".JPEG"):
            myJPEG.append(file)
    myJPEG = sorted(myJPEG)
    for jpg in myJPEG:
        # print(f"Converting {jpg} to PNG format")
        INPUT_JPG = f"{directory}{jpg}"
        OUTPUT_PNG = f"{directory}{inputToOutputPNG(jpg)}"
        # convert JPG to PNG
        command = "ffmpeg -y -i " + INPUT_JPG + " -hide_banner " + OUTPUT_PNG + " -loglevel error"
        subprocess.call(command, shell=True)

def attach_pictures(suffix, clips, directory):
    print("Attaching pictures")

    copy_directory(pic_dir_in, pic_dir_out)

    jpg_to_png(pic_dir_in)

    for key, value in clips.items():
        if value.isdigit:
            INPUT_PICTURE = f"{pic_dir_in}{value}.png"
            OUTPUT_PICTURE = f"{pic_dir_in}{cam}{key}.png"
            copyfile(INPUT_PICTURE, OUTPUT_PICTURE)
        else:
            pass

        print(f"Attaching {value}.png to {cam}{key}{suffix}")
        INPUT_IMAGE = f"{pic_dir_in}{cam}{key}.png"
        OUTPUT_MOV = f"{directory}{cam}{key}{suffix}"
        filelen = float(get_packets(OUTPUT_MOV))/frameRate + magicnumber
        command = f"ffmpeg -loop 1 -y -i {INPUT_IMAGE} -vcodec qtrle -t {filelen} {OUTPUT_MOV} -hide_banner -loglevel error "
        subprocess.call(command, shell=True)

        deleteFile(OUTPUT_PICTURE)

def attach_multiple_pictures(suffix, clips, directory):
    for key, value in clips.items():
        pics = value.split(",")
        # print(pics)
        original_mov = f"{directory}{cam}{key}{suffix}"
        n = 1
        pic_lens = []
        for pic in pics:
            pic = pic.strip()
            picture = f"{pic_dir_in}{pic}.png"
            # print(picture)
            output_mov = f"{directory}{cam}{key}_{n}{suffix}"
            filelen = (get_packets(original_mov)/len(pics))/frameRate + magicnumber
            # print(filelen*24)
            print(f"Attaching picture to {cam}{key}{suffix} (pic {pic}.png)")
            command = f"ffmpeg -loop 1 -y -i {picture} -vcodec qtrle -t {filelen} {output_mov} -hide_banner -loglevel error "
            subprocess.call(command, shell=True)
            n = n+1
            # print(get_packets(output_mov))
            pic_lens.append(get_packets(output_mov))
        # print(pic_lens)
        # total_len = float(sum(pic_lens))
        # original_len = get_packets(original_mov)
        # print(original_len)
        # framediscrepancy = total_len - original_len
        # print(framediscrepancy)
        deleteFile(original_mov)

def attach_videos(suffix, clips, directory):
    for k, v in clips.items():
        if os.path.isfile(f"{pic_dir_in}{v}.mov") == True:
            input = f"{pic_dir_in}{v}.mov"
            output = f"{pic_dir_in}{v}.mp4"
            command = f"ffmpeg -i -y {input} -hide_banner {output} -loglevel error"
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
    # deletePath(layer2)
    # dup_dir(layer4, layer2)
    # concat_and_replace(filesuffix, filesuffix, clips_all_except_pics_and_vid, layer2, vid_transparency_smol)
    # concat_and_replace(filesuffix, filesuffix, clips_background, layer3, backgroundloc)
    # concat_and_replace(filesuffix, filesuffix, clips_ben_and_cover, layer3, vid_transparency_smol)

    # attach_pictures(filesuffix, clips_pictures, layer2)
    # attach_multiple_pictures(filesuffix, clips_mult_pics, layer2)
    attach_videos(filesuffix, clips_video, layer2)