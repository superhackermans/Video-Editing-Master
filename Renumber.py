from parameters import *

def renumber(directory, suffix, replacement_clip, clip_to_replace, last_clip):
    myVideos = []
    for file in os.listdir(directory):
        if file.endswith(".MP4") or file.endswith(".mp4"):
            myVideos.append(file)

    def clip(number):
        clip_loc = f"{directory}{cam}{str(number).zfill(4)}{suffix}"
        return clip_loc

    original_clip = clip(replacement_clip)
    temp_clip =  clip(0000)

    os.rename(original_clip, temp_clip)

    while clip(clip_to_replace) != clip(last_clip):
        os.rename(clip(last_clip), clip(last_clip + 1))
        last_clip -= 1

    os.rename(clip(clip_to_replace), clip(clip_to_replace + 1))
    os.rename(temp_clip, clip(clip_to_replace))

def deleteclip(directory, suffix, clip_to_delete, last_clip):
    myVideos = []
    for file in os.listdir(directory):
        if file.endswith(".MP4") or file.endswith(".mp4"):
            myVideos.append(file)

    def clip(number):
        clip_loc = f"{directory}{cam}{str(number).zfill(4)}{suffix}"
        return clip_loc

    os.remove(clip(clip_to_delete))

    while clip(clip_to_delete) != clip(last_clip):
        os.rename(clip(clip_to_delete+1), clip(clip_to_delete))
        clip_to_delete += 1


if __name__ == '__main__':
    # renumber(vid_dir_in, ".MP4", 717, 706, 715) (directory, suffix, replacement_clip, clip_to_replace, last_clip)
    # deleteclip(vid_dir_in, ".MP4", 706, 715) #(directory, suffix, clip_to_delete, last_clip)
    print("nothing")
