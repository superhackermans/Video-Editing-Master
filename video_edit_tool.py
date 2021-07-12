from cover_splitter import *
from cover_attacher import *
from alternate_zoom import *
from picture_attacher import *
from trimmer import *
from backgroundattacher import *
from background_layer import *
from framesame import *
from remove_audio import *

if __name__ == '__main__':
    make_folders()
    trimmer()
    # frame_same("_TRIMMED.MP4", clips_all, OUTPUT_VIDEO_DIRECTORY)
    attachpictures(clips_pictures)
    splitcovers(cov_dir_in)
    # dup_dir(layer2, layer3)
    # add_transparency("_TRIMMED.MP4", clips_bentoc, layer2)
    # dup_dir(layer2, layer1)
    # add_transparency("_TRIMMED.MOV", clips_pictures, layer1)
    # attachcovers("_TRIMMED.MP4", clips_cover, layer1)
    # add_transparency("_TRIMMED.MP4", clips_cover, layer2)
    # replace_footage("_TRIMMED.MOV", clips_background, layer3)
    # attachsidecovers("_TRIMMEDEMPTY.MOV", clips_cover, layer1)
    # remove_audio(layer1)
    # remove_audio(layer3)
    # altzoom("_TRIMMED.MP4", clips_ben)