from parameters import *

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

    input_directories = [vid_dir_in, pic_dir_in,
                         cov_dir_in, data_file, pop_up_dir]
    output_directories = [layer2, wav_converting,
                          cover_dir_out, pic_dir_out, vid_processed, cover_cut]
    delete_directories = [wav_dir, pic_dir_out, layer1,
                          wav_converting, "./TEMP", layer3,
                          cover_dir_out, layer2, layer4, backuplayer, layer0, layer_popups]

    if x == "yes" or x == "y":
        deletecontents(output_main)
        deletecontents("./files/INPUT/")
        erasetextfile(data_file)
        make_folders()
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