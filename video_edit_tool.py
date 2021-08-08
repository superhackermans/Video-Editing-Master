from parameters import *
from picture_attacher import *
from remove_audio import *
from trimmer import *
from cover_attacher import *
from transition_attacher import *
from slow_zoom_and_fade import *
from background_layer import *
from new_trimmer import *
from pop_ups import *
import time


def main():
  start_time = time.time()

  print("What would you like to run? \n"
        "For trimmer only type 't'. \n"
        "For everything else type 'e'.")
  x = input()

  make_folders()

  if x == "t":
      new_trimmer(filesuffix, vid_dir_in) # desired output, and directory

      dup_dir(layer2, backuplayer)
      # deletePath(layer2)
      # dup_dir(backuplayer, layer2)

      # altzoom(filesuffix, clips_ben, layer2)
      # slow_zoom(filesuffix, clips_ben, layer2)
      # fade_out(filesuffix, clips_ben, layer2)

  if x == "e":
      dup_dir(layer2, backuplayer)
      reset()

      splitcovers(cov_dir_in)

      if bool(clips_pop_up) == True:
          bottom_pop_ups(clips_pop_up, layer_popups)
          concat_and_replace(filesuffix, filesuffix, clips_except_popups, layer_popups, vid_transparency_smol)
      else:
          pass

      concat_and_replace(filesuffix, filesuffix, clips_all_except_pics_and_vid, layer2, vid_transparency_smol)
      concat_and_replace(filesuffix, filesuffix, clips_background, layer3, backgroundloc)
      concat_and_replace(filesuffix, filesuffix, clips_ben_and_cover, layer3, vid_transparency_smol)

      attach_pictures(filesuffix, clips_pictures, layer2)
      attach_multiple_pictures(filesuffix, clips_mult_pics, layer2)
      attach_videos(filesuffix, clips_video, layer2)

      dup_dir(backuplayer, layer1)
      add_transparency(filesuffix, filesuffix, clips_all, layer1)
      dup_dir(layer1, layer0)

      concat_and_replace(filesuffix, filesuffix, clips_all_except_cover_and_last, layer0, vid_transparency_smol)
      attach_covers(filesuffix, clips_cover, layer0)
      attach_side_covers(filesuffix, clips_cover, layer0)
      outro_attacher(filesuffix, clips_all, layer0)

      transitions(filesuffix, clips_background, layer1)
      concat_and_replace(filesuffix, filesuffix, clips_background, layer1, vid_transparency_smol)
      concat_and_replace(filesuffix, filesuffix, clips_ben, layer1, vid_transparency_smol)

      deletePath(wav_dir)
      deletePath(cover_cut)
      deletePath(wav_converting)

  else:
      pass
  print(f"Program took {round((time.time() - start_time) / 60, 2)} minutes to finish.")


if __name__ == '__main__':
    main()