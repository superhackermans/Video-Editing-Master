from parameters import *

all_layers = [layer0, layer1, layer2, layer3, layer4]

def count_frames(directory):
    clips = [] # clip is file name
    for file in os.listdir(directory):
        if file.endswith(".MP4") or file.endswith(".mp4") or file.endswith(".MOV") or file.endswith(".mov"):
            clips.append(file)
    if not clips:
        print("No input videos detected")
    clips = sorted(clips)
    frames = []
    lens = []
    for clip in clips:
        fileloc = f"{directory}{clip}"
        packets = float(get_packets(fileloc))
        frames.append(packets)
        len = float(get_length(fileloc))
        lens.append(len)
    # print(frames)
    total_frames = sum(frames)
    total_len = sum(lens)
    print(f"total_frames for {directory} is {total_frames}")
    print(f"total_len for {directory} is {round(total_len, 3)}")



if __name__ == '__main__':
    for layer in all_layers:
        count_frames(layer)