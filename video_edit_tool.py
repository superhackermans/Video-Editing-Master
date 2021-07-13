from cover_splitter import *
from cover_attacher import *
from alternate_zoom import *
from picture_attacher import *
from trimmer import *
from remove_audio import *
from transition_attacher import *
from background_layer import *

# frame_same("_TRIMMED.MP4", clips_all, OUTPUT_VIDEO_DIRECTORY)

if __name__ == '__main__':
    make_folders()
    trimmer()
    attachpictures(clips_pictures)
    splitcovers(cov_dir_in)
    dup_dir(layer2, backuplayer)
    dup_dir(layer2, layer3)
    add_transparency("_TRIMMED.MP4","_TRIMMEDEMPTY.MOV", clips_bentoc, layer2)
    dup_dir(layer2, layer1)
    add_transparency("_TRIMMED.MOV", "_TRIMMEDEMPTY.MOV", clips_pictures, layer1)
    attachcovers("_TRIMMED.MP4", clips_cover, layer1)
    add_transparency("_TRIMMED.MP4","_TRIMMEDEMPTY.MOV", clips_cover, layer2)
    if bool(clips_toc) == True: # if TOC clip exists, convert to MOV transparency
        add_transparency("_TRIMMED.MP4", "_TRIMMED.MOV", clips_toc, layer3)
    else:
        pass
    replace_footage("_TRIMMED.MOV", clips_background, layer3, backgroundloc)
    attachsidecovers("_TRIMMEDEMPTY.MOV", clips_cover, layer1)
    remove_audio(layer1)
    remove_audio(layer2)
    transitions("_TRIMMEDEMPTY.MOV", clips_background, layer1)
    altzoom("_TRIMMED.MP4", clips_ben, layer3)