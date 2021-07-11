from parameters import *
from background_layer import *
import subprocess

#suffix of the top layer which is to be replaced
def transitions(suffix, clips_background, directory):

    clips_background = {int(k):int(v) for k, v in clips_background.items()}

    # connect consecutive clips
    cc = list(clips_background.items())
    if bool(cc) == True:
        arr = np.array(cc)
        consecutive_clips = group_consecutives(arr[:, 0])

    for group in consecutive_clips:
        if group[0] == group[-1]:
            workingfiles = f"C0{group[0]}"
        else:
            workingfiles = f"C0{group[0]}-C0{group[-1]}"
        print(f"Attaching transitions to {workingfiles}")

        transition_in = f"C0{group[0]}{suffix}"
        transition_out = f"C0{group[-1]}{suffix}"

        #need toc here as well

        # if prior clip is a cover page, pass
        if clips_images[str(i[0]-1)] in clips_cover.values():
            pass
        else:
            prior_clip = f"C0{clips_images[str(i[0]-1)]}{suffix}"
            prior_clip_loc = f"{directory}{prior_clip}"
            prior_clip_len = float(get_length(prior_clip_loc))

            cut_point = 1 # len of transition
            command = f"ffmpeg -ignore_chapters 1 -y -i {prior_clip_loc} -vcodec qtrle -ss 0 -t {prior_clip_len}-{cut_point} {forwardfileloc} -hide_banner -loglevel error"
            subprocess.call(command, shell=True)
            # command = f"ffmpeg -ignore_chapters 1 -i {forwardfileloc} -vcodec qtrle -ss {cut_point} -t {fwdfilelen} {newforwardfileloc} -hide_banner -loglevel error"
            # subprocess.call(command, shell=True)
            # attach transition
        # transition in

        # if afterwards clip is a cover page, pass
        if clips_images[str(i[-1] + 1)] in clips_cover.values():
            pass
        else:
            print("code")
            #add transition
        # transition out

        st()

if __name__ == '__main__':
    transitions(".MOV", clips_background)