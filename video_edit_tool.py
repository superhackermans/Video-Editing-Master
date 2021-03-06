from parameters import *
from picture_attacher import *
from remove_audio import *
from cover_attacher import *
from transition_attacher import *
from zoom_and_fade import *
from background_layer import *
from trim_clips import *
from pop_ups import *
import time
from trim_clips import *
from Renumber import *


def everythingelse():
    if bool(clips_pop_up):
        bottom_pop_ups(clips_pop_up, layer_popups)
        concat_and_replace(filesuffix, filesuffix, clips_except_popups, layer_popups, vid_transparency_smol)
    else:
        pass

    dup_dir(layer2, layer3)
    # add_transparency(filesuffix, filesuffix, clips_all, layer3)
    concat_and_replace(filesuffix, filesuffix, clips_background, layer3, backgroundloc)
    concat_and_replace(filesuffix, filesuffix, clips_ben_and_cover, layer3, vid_transparency_smol)

    concat_and_replace(filesuffix, filesuffix, clips_all_except_pics_and_vid, layer2, vid_transparency_smol)
    attach_pictures(filesuffix, clips_pictures, layer2)
    attach_multiple_pictures(filesuffix, clips_mult_pics, layer2)
    attach_videos(filesuffix, clips_video, layer2)

    deletePath(layer1)
    dup_dir(backuplayer, layer1)
    add_transparency(filesuffix, filesuffix, clips_all, layer1)
    dup_dir(layer1, layer0)

    dup_dir(backuplayer, layer4)

    attach_covers(filesuffix, clips_cover, layer0)
    attach_side_covers(filesuffix, clips_cover, layer0)
    outro_attacher(filesuffix, clips_all, layer0)
    concat_and_replace(filesuffix, filesuffix, clips_all_except_cover_and_last, layer0, vid_transparency_smol)

    transitions(filesuffix, clips_background, layer1)
    concat_and_replace(filesuffix, filesuffix, clips_background, layer1, vid_transparency_smol)
    concat_and_replace(filesuffix, filesuffix, clips_ben, layer1, vid_transparency_smol)
    #
    deletePath(wav_dir)
    deletePath(cover_cut)
    deletePath(wav_converting)

def zooms():
    altzoom(filesuffix, clips_benALT, layer2)
    slow_zoom(filesuffix, clips_ben, layer2)
    fade_out(filesuffix, clips_ben, layer2)

def main():
    start_time = time.time()

    print("What would you like to run? \n"
          "For trimmer only type 't'. \n"
          "To retrim type 'rt'. \n"
          "For zooms only type 'z'. \n"
          "For everything besides trimmer type 'e'. \n"
          "To reset and rerun, type 'r') \n"
          "To delete a clip, type 'd') \n"
          "To renumber a clip, type 'rn') \n")

    x = input()

    make_folders()

    if x == "t":
        trimmer(filesuffix, vid_dir_in, layer2)  # desired output, and directory

    if x == "rt":
        retrim(filesuffix, vid_dir_in, layer2, 12,
               0.03)  # desired output, and directory and additional frame spill/threshold for silence

    if x == "z":
        zooms()

    if x == "e":
        zooms()
        dup_dir(layer2, backuplayer)
        splitcovers(cov_dir_in)

        everythingelse()
    if x == "r":
        def reset():
            deletePath(layer1)
            deletePath(layer2)
            deletePath(layer3)
            deletePath(layer4)
            deletePath(layer0)
            deletePath(layer_popups)
            deletePath(layer_toc)
            dup_dir(backuplayer, layer2)
            # dup_dir(layer2, backuplayer)

        reset()

        everythingelse()

    if x == "d":
        print("Which clip would you like to delete?")
        y = input()
        print("What is the last clip?")
        z = input()
        try:
            deleteclip(layer2, "_TRIMMED.MOV", int(y), int(z))
            print("Clip deleted from video directory out")
        except:
            pass
        try:
            deleteclip(vid_dir_in, ".MP4", int(y), int(z))  # (directory, suffix, clip_to_delete, last_clip)
            print("Clip deleted from video directory in")
        except:
            pass
    if x == "rn":
        print("Which clip would you like to insert?")
        y = input()
        print("Which clip will this replace?")
        z = input()
        print("What is the last clip?")
        zz = input()
        try:
            renumber(layer2, "_TRIMMED.MOV", int(y), int(z), int(zz))
            print("Clip renumbered from video directory out")
        except:
            pass
        try:
            renumber(vid_dir_in, ".MP4", int(y), int(z),int(zz))
            # renumber(vid_dir_in, ".MP4", 717, 706, 715) (directory, suffix, replacement_clip, clip_to_replace, last_clip)
            print("Clip renumbered from video directory in")
        except:
            pass

    else:
        pass
    print(f"Program took {round((time.time() - start_time) / 60, 2)} minutes to finish.")


if __name__ == '__main__':
    main()
