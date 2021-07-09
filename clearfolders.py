from parameters import *

import os, shutil


def deletecontents(directory):
    folder = directory
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def erasetextfile(directory):
    open(directory, 'w').close()

if __name__ == '__main__':
    print("Are you sure you want to erase all files in folders? Type 'o' for only output deletion")
    x = input()

    input_directories = [INPUT_VIDEO_DIRECTORY, PICTURE_DIRECTORY, INPUT_COVER_DIRECTORY, DATA_FILE]
    output_directories = [OUTPUT_VIDEO_DIRECTORY, WAV_CONVERSION_FILES, OUTPUT_COVER_DIRECTORY, PICTURE_OUTPUT_DIRECTORY,]
    delete_directories = [WAV_DIRECTORY, PICTURE_OUTPUT_DIRECTORY, OUTPUT_VIDEO_DIRECTORY3, WAV_CONVERSION_FILES, "./TEMP", OUTPUT_VIDEO_DIRECTORY2, OUTPUT_COVER_DIRECTORY, OUTPUT_VIDEO_DIRECTORY]

    if x == "yes" or x == "y":
        for file in input_directories:
            try:
                deletecontents(file)
            except:
                pass

        for file in output_directories:
            try:
                deletecontents(file)
            except:
                pass

        for directory in delete_directories:
            try:
                shutil.rmtree(directory)
            except:
                pass

    elif x == "o":
        for file in output_directories:
            try:
                deletecontents(file)
            except:
                pass

        for directory in delete_directories:
            try:
                shutil.rmtree(directory)
            except:
                pass

    else:
        print("Nothing deleted")