from parameters import *
from cover_splitter import *
from concat_and_replace import *
from picture_attacher import *
from remove_audio import *
from trimmer import *
from cover_attacher import *
from transition_attacher import *
from alternate_zoom import *
from slow_zoom_and_fade import slow_zoom, fade_out
from background_layer import *
from pop_ups import *
import time

if __name__ == '__main__':
    start_time = time.time()

    # make_folders()
    # trimmer(filesuffix, vid_dir_in) # desired output, and directory
    #
    # splitcovers(cov_dir_in)
    #
    # dup_dir(layer2, backuplayer)
    # dup_dir(layer2, layer3)
    # dup_dir(layer2, layer4)

    reset()

    if bool(clips_pop_up) == True:
        bottom_pop_ups(clips_pop_up, layer_popups)
        concat_and_replace(filesuffix, filesuffix, clips_except_popups, layer_popups, vid_transparency_smol)
    else:
        pass

    concat_and_replace(filesuffix, filesuffix, clips_all_except_pics_and_vid, layer2, vid_transparency_smol)
    concat_and_replace(filesuffix, filesuffix, clips_background, layer3, backgroundloc)
    concat_and_replace(filesuffix, filesuffix, clips_ben_and_cover, layer3, vid_transparency_smol)

    attach_pictures(filesuffix, clips_pictures, layer2)
    attach_videos(filesuffix, clips_video, layer2)

    dup_dir(backuplayer, layer1)
    add_transparency(filesuffix, filesuffix, clips_all, layer1)
    dup_dir(layer1, layer0)

    attachcovers(filesuffix, clips_cover, layer0)
    attachsidecovers(filesuffix, clips_cover, layer0)
    concat_and_replace(filesuffix, filesuffix, clips_all_except_cover, layer0, vid_transparency_smol)

    transitions(filesuffix, clips_background, layer1)
    concat_and_replace(filesuffix, filesuffix, clips_background, layer1, vid_transparency_smol)
    concat_and_replace(filesuffix, filesuffix, clips_ben, layer1, vid_transparency_smol)

    altzoom(filesuffix, clips_ben, layer4)
    slow_zoom(filesuffix, clips_ben, layer4)
    fade_out(filesuffix, clips_ben, layer4)

    deletePath(wav_dir)
    deletePath(cover_cut)
    deletePath(wav_converting)

    print(f"Program took {round((time.time() - start_time)/60, 2)} minutes to finish.")