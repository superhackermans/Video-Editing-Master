from parameters import *
from cover_splitter import *
from concat_and_replace import *
from picture_attacher import *
from remove_audio import *
from trimmer import *
from cover_attacher import *
from transition_attacher import *
from alternate_zoom import *


if __name__ == '__main__':
    make_folders()
    trimmer(filesuffix, vid_dir_in) # desired output, and directory
    attachpictures(filesuffix, clips_pictures)
    splitcovers(cov_dir_in)

    # dup_dir(layer2, backuplayer)
    # sec_to_frames(filesuffix, clips_all, layer2)
    # dup_dir(layer2, layer3)
    # dup_dir(layer2, layer4)

    # reset()

    # concat_and_replace(filesuffix, filesuffix, clips_all_except_pics, layer2, vid_transparency_smol)
    # concat_and_replace(filesuffix, filesuffix, clips_background, layer3, backgroundloc)
    # concat_and_replace(filesuffix, filesuffix, clips_ben_and_cover, layer3, vid_transparency_smol)
    # remove_audio(layer2)
    # remove_audio(layer3)

    # attachcovers(filesuffix, clips_cover, layer4)

    # dup_dir(layer4, layer1)
    # dup_dir(layer4, layer0)
    # add_transparency(filesuffix, filesuffix, clips_all, layer1)
    # add_transparency(filesuffix, filesuffix, clips_all, layer0)
    # attachcovers(filesuffix, clips_cover, layer0)
    # attachsidecovers(filesuffix, clips_cover, layer0)
    # transitions(filesuffix, clips_background, layer1)

    altzoom(filesuffix, clips_ben, layer4)
    # slow_zoom("_TRIMMED.MP4", clips_ben, layer4)

