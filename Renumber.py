from parameters import *

def renumber(directory, suffix, original_number, first_replace, last_replace):
    myVideos = []
    for file in os.listdir(directory):
        if file.endswith(".MP4") or file.endswith(".mp4"):
            myVideos.append(file)


    def clip(number):
        clip_loc = f"{directory}{cam}{str(number).zfill(4)}{suffix}"
        return clip_loc

    original_clip = clip(original_number)
    temp_clip =  clip(0000)

    os.rename(original_clip, temp_clip)

    while clip(first_replace) != clip(last_replace):
        os.rename(clip(last_replace), clip(last_replace+1))
        last_replace -= 1

    os.rename(clip(first_replace), clip(first_replace+1))
    os.rename(temp_clip, clip(first_replace))


if __name__ == '__main__':
    renumber(vid_dir_in, ".MP4", 717, 706, 715)
    # 717 -> 706 and 706 -> 707 and so forth