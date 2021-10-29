from parameters import *

def renumber(suffix, original_number, replacement_number):
    myVideos = []
    for file in os.listdir(directory):
        if file.endswith(".MP4") or file.endswith(".mp4"):
            myVideos.append(file)

    os.rename(src, dst)


first_clip_loc = f"{directory}{cam}{str(clips[0][0]).zfill(4)}{suffix}"


if __name__ == '__main__':
    renumber(".MP4", 100, 50)
    # 100 -> 50 and 50 -> 51 and so forth