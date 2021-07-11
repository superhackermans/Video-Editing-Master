from cover_splitter import *
from cover_attacher import *
from alternate_zoom import *
from picture_attacher import *
from trimmer import *
from backgroundattacher import *
from background_layer import *
from framesame import *

clips_images = readfile(DATA_FILE)
clips_all =  {k: v for k, v in clips_images.items()}
clips_pictures = {k: v for k, v in clips_images.items() if v.isdigit()}
clips_ben = {k: v for k, v in clips_images.items() if v == "--"}
clips_bentoc = {k: v for k, v in clips_images.items() if v == "--" or v == "toc"}
clips_cover = {k: v for k, v in clips_images.items() if v == "c1" or v == "c2" or v == "c3"
               or v == "c4" or v == "c5" or v == "c6"
               or v == "c7" or v == "c8" or v == "c9"}
clips_background = {k: v for k, v in clips_images.items() if v.isdigit()}
clips_toc = {k: v for k, v in clips_images.items() if v == "toc"}

if __name__ == '__main__':
    # make_folders()
    # trimmer()
    frame_same("_TRIMMED.MP4", clips_all, OUTPUT_VIDEO_DIRECTORY)
    attachpictures(clips_pictures)
    splitcovers(INPUT_COVER_DIRECTORY)
    dup_dir(OUTPUT_VIDEO_DIRECTORY, OUTPUT_VIDEO_DIRECTORY2)
    add_transparency("_TRIMMED.MP4", clips_bentoc, OUTPUT_VIDEO_DIRECTORY)
    dup_dir(OUTPUT_VIDEO_DIRECTORY, OUTPUT_VIDEO_DIRECTORY3)
    add_transparency("_TRIMMED.MOV", clips_pictures, OUTPUT_VIDEO_DIRECTORY3)
    attachcovers("_TRIMMED.MP4", clips_cover, OUTPUT_VIDEO_DIRECTORY3)
    add_transparency("_TRIMMED.MP4", clips_cover, OUTPUT_VIDEO_DIRECTORY)
    replace_footage("_TRIMMED.MOV", clips_background, OUTPUT_VIDEO_DIRECTORY2)
    # attachsidecovers("_TRIMMEDEMPTY.MOV", clips_cover)
    # altzoom("_TRIMMED.MP4", clips_ben)