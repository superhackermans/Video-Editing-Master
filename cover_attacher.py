from parameters import *


def inputToOutputWAV(filename):
    dotIndex = filename.rfind(".")
    return filename[:dotIndex]+".WAV"
def inputToOutputNewWAV(filename):
    return cam+filename+".WAV"
def inputToOutputFilenameTRANSITION(filename):
    return cam+filename+"_transition.MOV"

def attach_covers(suffix, clips, directory):
    # find which clips have cover pages

    for key, value in clips.items():

        filename = f"{cam}{key}{suffix}"
        originalfile = f"{layer4}{filename}"
        cover = f"{value}_2"
        coverloc = f"{cover_dir_out}{cover}.mov"
        final_output = f"{directory}{cam}{key}{suffix}"

        print(f"Attaching cover {value} to {filename}")

        original_len = get_length(originalfile)
        coverlen = get_length(coverloc)

        #ADDED BUFFER OF HALF A FRAME!!!
        ratio = ((original_len-.5/frameRate)/coverlen)

        command = f'ffmpeg -y -i {coverloc} -filter_complex "[0:v]setpts=PTS*{str(ratio)}[v]" -map "[v]" -shortest {final_output} -hide_banner -loglevel error'
        subprocess.call(command, shell=True)

        frame_len = get_packets(final_output)
        original_frames = get_packets(originalfile)

        if original_frames-frame_len == 0:
            print("There was no discrepancy between lengths.")
        else:
            print(f"filelength of cover {value} is {frame_len} frames")
            print(f"filelength of layer 3 clip is {original_frames} frames")
            print(f"The discrepancy is {frame_len - original_frames} frames")

def attach_side_covers(suffix, clips, directory):

    buffer = 1/frameRate

    print("Attaching sides of covers")
    #make wav directory

    for key, value in clips.items():
        # brightness = "0.00"
        # saturation = "0.03"
        #name everything
        behindfilenum = str(int(key)-1)
        forwardfilenum = str(int(key)+1)
        behindfile = f"{cam}{behindfilenum}{suffix}"
        forwardfile = f"{cam}{forwardfilenum}{suffix}"
        behindfileloc = f"{directory}{behindfile}"
        forwardfileloc = f"{directory}{forwardfile}"

        coverbehind = f"{value}_1"
        coverforward = f"{value}_3"
        coverbehindloc = f"{cover_dir_out}{coverbehind}{basesuffix(filesuffix)}"
        coverforwardloc = f"{cover_dir_out}{coverforward}{basesuffix(filesuffix)}"

        final_output_b2 = f"{directory}{cam}{behindfilenum}.5{suffix}"
        final_output_f2 = f"{directory}{cam}{forwardfilenum}_1{suffix}"

        newbehindfileloc = f"{directory}TEMP{behindfile}"
        newfowardfileloc = f"{directory}TEMP{forwardfile}"

        #cut off 1 s section at the very end of behind clip
        if os.path.isfile(behindfileloc) == True:
            transition1frames = get_packets(coverbehindloc)
            cut_point = str(float(get_length(behindfileloc))-transition1frames/frameRate+buffer)
            command = f"ffmpeg -ignore_chapters 1 -i {behindfileloc} -vcodec qtrle -ss 0 -t {cut_point} {newbehindfileloc} -hide_banner -loglevel error"
                      # f" -c:v libx264 -strict -2 " \
            subprocess.call(command, shell=True)
        if os.path.isfile(forwardfileloc) == True:
            transition2frames = get_packets(coverforwardloc)
            cut_point = str(float(get_length(forwardfileloc))-transition2frames/frameRate)
            command = f"ffmpeg -ignore_chapters 1 -i {forwardfileloc} -vcodec qtrle -ss {transition2frames/frameRate} -t {cut_point} {newfowardfileloc} -hide_banner -loglevel error"
                      # f" -c:v libx264 -strict -2 " \
            subprocess.call(command, shell=True)

        # fwd clip

        # command = "ffmpeg -ignore_chapters 1 -i " + behindfileloc + " -vcodec qtrle -ss " + cut_point + " " + " -t 1 " + newbehindtransitionloc + " -hide_banner" + " -loglevel error"
        # subprocess.call(command, shell=True)
        deleteFile(behindfileloc)
        deleteFile(forwardfileloc)
        renamefile(newbehindfileloc, behindfileloc)
        renamefile(newfowardfileloc, forwardfileloc)
        copyfile(coverbehindloc, final_output_b2)
        copyfile(coverforwardloc, final_output_f2)

def outro_attacher(suffix, clips, directory):
    clips = list(clips.items())
    last_clip_loc = f"{directory}{cam}{clips[-1][0]}{suffix}"
    last_clip_len = get_length(last_clip_loc)
    cutamt = .5
    command = f"ffmpeg -ignore_chapters 1 -y -i {last_clip_loc} -vcodec qtrle -ss 0 -t {last_clip_len-cutamt} {tempclip(last_clip_loc)} -hide_banner -loglevel error"
    subprocess.call(command, shell=True)
    deleteFile(last_clip_loc)
    renamefile(tempclip(last_clip_loc), last_clip_loc)

    outro_clip = f"{directory}{cam}{clips([-1]+1)[0]}{suffix}"
    copyfile(outro, outro_clip)

if __name__ == '__main__':

    # attachcovers(clips)
    attach_side_covers("_TRIMMEDEMPTY.MOV", clips, layer1)






