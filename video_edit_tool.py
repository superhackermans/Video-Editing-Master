from cover_splitter import *
from get_len_and_concat import *
from picture_attacher import *
from remove_audio import *
from trimmer import *
from cover_attacher import *
from transition_attacher import *
from alternate_zoom import *

# frame_same("_TRIMMED.MP4", clips_all, OUTPUT_VIDEO_DIRECTORY)
filesuffix = "_TRIMMED.MOV"

if __name__ == '__main__':
    make_folders()
    trimmer(filesuffix, vid_dir_in) # desired output, and directory
    attachpictures(filesuffix, clips_pictures)
    splitcovers(cov_dir_in)
    dup_dir(layer2, backuplayer)
    dup_dir(layer2, layer3)
    dup_dir(layer2, layer4)

    # reset()

    concat_and_replace(filesuffix, filesuffix, clips_all_except_pics, layer2, vid_transparency_smol)
    concat_and_replace(filesuffix, filesuffix, clips_background, layer3, backgroundloc)
    concat_and_replace(filesuffix, filesuffix, clips_ben, layer3, vid_transparency_smol)
    concat_and_replace(filesuffix, filesuffix, clips_cover, layer3, vid_transparency_smol)
    remove_audio(layer2)
    remove_audio(layer3)
    dup_dir(layer4, layer1)
    add_transparency(filesuffix, filesuffix, clips_all, layer1)
    attachcovers(filesuffix, clips_cover, layer1)
    attachsidecovers(filesuffix, clips_cover, layer1)
    transitions(filesuffix, clips_background, layer1)

    # altzoom(filesuffix, clips_ben, layer4)
    # slow_zoom("_TRIMMED.MP4", clips_ben, layer4)

