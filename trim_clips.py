from parameters import *
import time



def getMaxVolume(s):
    maxv = float(np.max(s))
    minv = float(np.min(s))
    return max(maxv, -minv)


def unpack(chunks):
    audio_array = []
    for chunk in chunks:
        frames = chunk[1]-chunk[0]
        for i in range(int(frames)):
            audio_array.append(chunk[2])
    new_array = np.asarray(audio_array)
    return new_array

def pack(array):
    chunks = [[0,0,0]]
    audioFrameCount = len(array)
    shouldIncludeFrame = np.zeros(audioFrameCount)
    for i in range(audioFrameCount):
        start = int(max(0,i))
        end = int(min(audioFrameCount,i+1))
        shouldIncludeFrame[i] = np.max(array[start:end])
        if (i >= 1 and shouldIncludeFrame[i] != shouldIncludeFrame[i-1]): # Did we flip?
            chunks.append([chunks[-1][1],i,shouldIncludeFrame[i-1]])
        try:
            shouldIncludeFrame[i+1]
        except IndexError:
            chunks.append([chunks[-1][1],i+1,shouldIncludeFrame[i-1]])
    chunks = np.asarray(chunks[1:])
    return chunks

def repack(chunks):
    arr = unpack(chunks)
    return pack(arr)

def copyFrame(inputFrame, outputFrame):
    TEMP_FOLDER = "TEMP"
    src = TEMP_FOLDER + "/frame{:06d}".format(inputFrame + 1) + ".jpg"
    dst = TEMP_FOLDER + "/newFrame{:06d}".format(outputFrame + 1) + ".jpg"
    if not os.path.isfile(src):
        return False
    copyfile(src, dst)
    # if outputFrame%20 == 19:
    #     print(str(outputFrame+1)+" time-altered frames saved.")
    return True


def trimmer(output_suffix, directory, output_dir):
    deletePath(TEMP_FOLDER)
    start_time = time.time()
    # turn filenames in list
    myVideos = []

    for file in os.listdir(directory):
        if file.endswith(".MP4") or file.endswith(".mp4"):
            myVideos.append(file)
    if not myVideos:
        print("No input videos detected")
        # quit()
    myVideos = sorted(myVideos)
    print(f"Processing: {myVideos[0]} to {myVideos[-1]}")
    # for video in myVideos:
    #     print(video)
    # print(myVideos)

    createPath(wav_dir)

    # Trim and delete mistakes
    for video_name in myVideos:
        INPUT_FILE = f"{directory}{video_name}"
        assert INPUT_FILE != None, "No Input File Detected"
        OUTPUT_FILE = f"{output_dir}{nosuffix(video_name)}{output_suffix}"

        createPath(TEMP_FOLDER)

        command = "ffmpeg -y -i " + INPUT_FILE + " -qscale:v " + str(
            FRAME_QUALITY) + " " + TEMP_FOLDER + "/frame%06d.jpg -hide_banner -loglevel error"
        subprocess.call(command, shell=True)
        # get audio
        command = "ffmpeg -y -i " + INPUT_FILE + " -ab 160k -ac 2 -ar " + str(
            SAMPLE_RATE) + " -vn " + TEMP_FOLDER + "/audio.wav -loglevel error"
        subprocess.call(command, shell=True)

        # read extracted audio file
        sampleRate, audioData = wavfile.read(TEMP_FOLDER + "/audio.wav")
        audioSampleCount = audioData.shape[0]
        maxAudioVolume = getMaxVolume(audioData)
        if maxAudioVolume <= min_volume_threshold:
            print(f"{video_name} has no significant sound.")
            continue

        # define parameters
        samplesPerFrame = sampleRate / frameRate
        audioFrameCount = int(math.ceil(audioSampleCount / samplesPerFrame))
        hasLoudAudio = np.zeros((audioFrameCount))
        volumeInformation = np.empty(1)


        for i in range(audioFrameCount):
            start = int(i * samplesPerFrame)
            end = min(int((i + 1) * samplesPerFrame), audioSampleCount)
            audiochunks = audioData[start:end]
            maxchunksVolume = float(getMaxVolume(audiochunks))/maxAudioVolume
            volumeInformation = np.append(volumeInformation, maxchunksVolume)
            if maxchunksVolume >= SILENT_THRESHOLD:
                hasLoudAudio[i] = 1

        volumeInformation = volumeInformation[1:]

        audioarray = np.asarray(hasLoudAudio)
        chunks = pack(audioarray)
        if chunks.shape == (1,3):
            print(f"Please check audio for {video_name}. Shape is {chunks.shape}")
            continue
        # # if no audio, continue to next iteration
        # is_all_zero = np.all((audioarray == 0))
        # if is_all_zero:
        #     continue

        # if there are small isolated elements of noise, remove them
        tiny_noise_idxs = np.where((chunks[:, 1] - chunks[:, 0] <= TINY_MISTAKE_THRESHOLD) & (chunks[:, 2] == 1))
        if tiny_noise_idxs[0].shape >= (1, 0):
            chunks[[tiny_noise_idxs], 2] = 0
        chunks = repack(chunks)
        tiny_silence_idxs = np.where((chunks[:, 1] - chunks[:, 0] <= TINY_MISTAKE_THRESHOLD) & (chunks[:, 2] == 0))
        if tiny_silence_idxs[0].shape >= (1, 0):
            chunks[[tiny_silence_idxs], 2] = 1
        chunks = repack(chunks)


        # if there is a long mistake, turn all noise prior mistake into 0
        midpointframe = chunks[-1, 1] * (cutoff_point)
        if chunks[-1][1] < 250:
            midpointframe = chunks[-1, 1] * (cutoff_point*1.1)
        long_zero_idxs = np.where((chunks[:, 1] - chunks[:, 0] > MAX_SILENCE_PERMITTED) & (chunks[:, 2] == 0) & (
                    chunks[:, 1] < midpointframe))
        if chunks.shape != (3,3):
            if long_zero_idxs[0].shape >= (1,):
                chunks[:long_zero_idxs[0][-1], 2] = 0
        chunks = repack(chunks)

        # is_all_zero = np.all((audioarray == 0))
        # if is_all_zero:
        #     continue
        # st()

        # if there is noise at the end after silence, erase end
        # if chunks[-1][-1] == 1 and chunks[-2][-1] == 0:
        #     chunks[-1][-1] = 0
        # if there is a long silence after the midpoint frame, turn all noise after silence into silence


        post_long_zero_idxs = np.where((chunks[:, 1] - chunks[:, 0] > MAX_SILENCE_PERMITTED) & (chunks[:, 2] == 0) & (
                chunks[:, 0] > midpointframe))
        if post_long_zero_idxs[0].shape >= (1,):
            chunks[post_long_zero_idxs[0][-1]:, 2] = 0

        chunks = repack(chunks)

        clip_len = round((audioFrameCount) / 24, 2)
        intro_cut = round((chunks[1][0]) / 24, 2)
        end_cut = round((chunks[-1][1] - chunks[-1][0]) / 24, 2)

        if intro_cut != 0 and end_cut != 0:
            print(f'{video_name}: Trimming {intro_cut} seconds/{round(intro_cut / clip_len * 100, 2)}% from front and {end_cut} seconds/{round(end_cut / clip_len * 100, 2)}% from back.')
        if intro_cut != 0 and end_cut == 0:
            print(f"{video_name}: Trimming {intro_cut} seconds/{round(intro_cut / clip_len * 100, 2)}% from front.")
        if intro_cut == 0 and end_cut != 0:
            print(f"{video_name}: Trimming {end_cut} seconds/{round(end_cut / clip_len * 100, 2)}% from back")
        if intro_cut == 0 and end_cut == 0:
            print("Nothing trimmed.")

        # make all correct frames present
        one_idx = np.asarray(np.where(chunks[:, 2] == 1))
        first = one_idx[0][0]
        last = one_idx[0][-1]
        chunks[first:last, 2] = 1

        chunks = repack(chunks)


        FRAME_SPILL_BACK_FINAL = 5  # frames to include at the very end of the clip
        s_number = 0.013
        s_number2 = 0.012
        s_number3 = 0.011
        s_number4 = 0.01
        # crude s finder
        if chunks.shape == (3,3):
            if volumeInformation[int(chunks[1,1])] >= s_number:
                FRAME_SPILL_BACK_FINAL = FRAME_SPILL_BACK_FINAL + 2
            if (volumeInformation[int(chunks[1,1])+1] >= s_number2) & (volumeInformation[int(chunks[1,1])] >= s_number):
                FRAME_SPILL_BACK_FINAL = FRAME_SPILL_BACK_FINAL + 1
            if (volumeInformation[int(chunks[1, 1]) + 2] >= s_number3) & (volumeInformation[int(chunks[1, 1]) + 1] >= s_number2) & (volumeInformation[int(chunks[1, 1])] >= s_number):
                FRAME_SPILL_BACK_FINAL = FRAME_SPILL_BACK_FINAL + 1
                if (volumeInformation[int(chunks[1, 1]) + 3] >= s_number4) & (volumeInformation[int(chunks[1, 1]) + 2] >= s_number3) & (
                        volumeInformation[int(chunks[1, 1]) + 1] >= s_number2) & (
                        volumeInformation[int(chunks[1, 1])] >= s_number):
                    FRAME_SPILL_BACK_FINAL = FRAME_SPILL_BACK_FINAL + 1
        if FRAME_SPILL_BACK_FINAL > 4:
            print(f"     Adding {FRAME_SPILL_BACK_FINAL} total spill frames")

        # add spill where necessary
        if chunks.shape == (3, 3):
            chunks[1][0] = chunks[1][0] - FRAME_SPILL_FRONT_FINAL
            chunks[1][1] = chunks[1][1] + FRAME_SPILL_BACK_FINAL

            chunks[0][1] = chunks[0][1] - FRAME_SPILL_FRONT_FINAL
            chunks[2][0] = chunks[2][0] + FRAME_SPILL_BACK_FINAL
        elif (chunks.shape == (2, 3)) & (chunks[0][2] == 0):
            chunks[1][0] = chunks[1][0] - FRAME_SPILL_FRONT_FINAL
            chunks[1][1] = chunks[1][1] + FRAME_SPILL_BACK_FINAL

            chunks[0][1] = chunks[0][1] - FRAME_SPILL_FRONT_FINAL
        elif (chunks.shape == (2, 3)) & (chunks[0][2] == 1):
            chunks[0][1] = chunks[0][1] + FRAME_SPILL_BACK_FINAL
            chunks[1][0] = chunks[1][0] - FRAME_SPILL_BACK_FINAL
        else:
            print(f"     2 or 3 dimensional array not detected. Shape is {chunks.shape}, please review.")

        # print(chunks)
        # create new Audio data array
        outputAudioData = np.zeros((0, audioData.shape[1]))
        outputPointer = 0








        lastExistingFrame = None
        for chunk in chunks:
            audioChunk = audioData[int(chunk[0] * samplesPerFrame):int(chunk[1] * samplesPerFrame)]

            sFile = TEMP_FOLDER + "/tempStart.wav"
            eFile = TEMP_FOLDER + "/tempEnd.wav"
            wavfile.write(sFile, SAMPLE_RATE, audioChunk)
            with WavReader(sFile) as reader:
                with WavWriter(eFile, reader.channels, reader.samplerate) as writer:
                    tsm = phasevocoder(reader.channels, speed=NEW_SPEED[int(chunk[2])])
                    tsm.run(reader, writer)
            _, alteredAudioData = wavfile.read(eFile)
            leng = alteredAudioData.shape[0]
            endPointer = outputPointer + leng
            outputAudioData = np.concatenate((outputAudioData, alteredAudioData / maxAudioVolume))

            if leng < AUDIO_FADE_ENVELOPE_SIZE:
                outputAudioData[outputPointer:endPointer] = 0  # audio is less than 0.01 sec, let's just remove it.
            else:
                premask = np.arange(AUDIO_FADE_ENVELOPE_SIZE) / AUDIO_FADE_ENVELOPE_SIZE
                mask = np.repeat(premask[:, np.newaxis], 2, axis=1)  # make the fade-envelope mask stereo
                outputAudioData[outputPointer:outputPointer + AUDIO_FADE_ENVELOPE_SIZE] *= mask
                outputAudioData[endPointer - AUDIO_FADE_ENVELOPE_SIZE:endPointer] *= 1 - mask

            startOutputFrame = int(math.ceil(outputPointer / samplesPerFrame))
            endOutputFrame = int(math.ceil(endPointer / samplesPerFrame))
            for outputFrame in range(startOutputFrame, endOutputFrame):
                inputFrame = int(chunk[0] + NEW_SPEED[int(chunk[2])] * (outputFrame - startOutputFrame))
                didItWork = copyFrame(inputFrame, outputFrame)
                if didItWork:
                    lastExistingFrame = inputFrame
                else:
                    copyFrame(lastExistingFrame, outputFrame)

            outputPointer = endPointer

        wavfile.write(TEMP_FOLDER + "/audioNew.wav", SAMPLE_RATE, outputAudioData)

        command = "ffmpeg -framerate " + str(
            frameRate) + " -y -i " + TEMP_FOLDER + "/newFrame%06d.jpg -i " + TEMP_FOLDER + "/audioNew.wav -strict -2 " + OUTPUT_FILE + " -loglevel error"
        subprocess.call(command, shell=True)

        deletePath(TEMP_FOLDER)


    print(f"Finished trimming in {round((time.time() - start_time) / 60, 2)} minutes. "
          f"Avg {round(round((time.time() - start_time) / 60, 2) / (len(myVideos)), 2)} minutes per clip.")


def retrim(output_suffix, directory, output_dir, additional_spill, silentthresh):

    print("Which clips would you like to retrim?")
    x = input()
    x_list = x.split(",")
    x_list = [x.strip(' ') for x in x_list]
    # x_list = [x.strip('C0') for x in x_list]

    myVideos = []

    for x in x_list:
        myVideos.append(f"C{x.zfill(4)}.mp4")

    deletePath(TEMP_FOLDER)
    start_time = time.time()
    # turn filenames in list

    myVideos = sorted(myVideos)
    # for video in myVideos:
    #     print(video)
    # print(myVideos)

    createPath(wav_dir)

    # Trim and delete mistakes
    for video_name in myVideos:
        INPUT_FILE = f"{directory}{video_name}"
        assert INPUT_FILE != None, "No Input File Detected"
        OUTPUT_FILE = f"{output_dir}{nosuffix(video_name)}{output_suffix}"

        createPath(TEMP_FOLDER)

        command = "ffmpeg -y -i " + INPUT_FILE + " -qscale:v " + str(
            FRAME_QUALITY) + " " + TEMP_FOLDER + "/frame%06d.jpg -hide_banner -loglevel error"
        subprocess.call(command, shell=True)
        # get audio
        command = "ffmpeg -y -i " + INPUT_FILE + " -ab 160k -ac 2 -ar " + str(
            SAMPLE_RATE) + " -vn " + TEMP_FOLDER + "/audio.wav -loglevel error"
        subprocess.call(command, shell=True)

        # read extracted audio file
        sampleRate, audioData = wavfile.read(TEMP_FOLDER + "/audio.wav")
        audioSampleCount = audioData.shape[0]
        maxAudioVolume = getMaxVolume(audioData)
        if maxAudioVolume <= min_volume_threshold:
            print(f"{video_name} has no significant sound.")
            continue

        # define parameters
        samplesPerFrame = sampleRate / frameRate
        audioFrameCount = int(math.ceil(audioSampleCount / samplesPerFrame))
        hasLoudAudio = np.zeros((audioFrameCount))
        volumeInformation = np.empty(1)

        for i in range(audioFrameCount):
            start = int(i * samplesPerFrame)
            end = min(int((i + 1) * samplesPerFrame), audioSampleCount)
            audiochunks = audioData[start:end]
            maxchunksVolume = float(getMaxVolume(audiochunks)) / maxAudioVolume
            volumeInformation = np.append(volumeInformation, maxchunksVolume)
            if maxchunksVolume >= silentthresh:
                hasLoudAudio[i] = 1

        volumeInformation = volumeInformation[1:]

        audioarray = np.asarray(hasLoudAudio)
        chunks = pack(audioarray)
        if chunks.shape == (1, 3):
            print(f"Please check audio for {video_name}. Shape is {chunks.shape}")
            continue
        # # if no audio, continue to next iteration
        # is_all_zero = np.all((audioarray == 0))
        # if is_all_zero:
        #     continue

        # if there are small isolated elements of noise, remove them
        tiny_noise_idxs = np.where((chunks[:, 1] - chunks[:, 0] <= TINY_MISTAKE_THRESHOLD) & (chunks[:, 2] == 1))
        if tiny_noise_idxs[0].shape >= (1, 0):
            chunks[[tiny_noise_idxs], 2] = 0
        chunks = repack(chunks)
        tiny_silence_idxs = np.where((chunks[:, 1] - chunks[:, 0] <= TINY_MISTAKE_THRESHOLD) & (chunks[:, 2] == 0))
        if tiny_silence_idxs[0].shape >= (1, 0):
            chunks[[tiny_silence_idxs], 2] = 1
        chunks = repack(chunks)

        # if there is a long mistake, turn all noise prior mistake into 0
        midpointframe = chunks[-1, 1] * (cutoff_point)
        if chunks[-1][1] < 250:
            midpointframe = chunks[-1, 1] * (cutoff_point * 1.1)
        long_zero_idxs = np.where((chunks[:, 1] - chunks[:, 0] > MAX_SILENCE_PERMITTED) & (chunks[:, 2] == 0) & (
                chunks[:, 1] < midpointframe))
        if chunks.shape != (3, 3):
            if long_zero_idxs[0].shape >= (1,):
                chunks[:long_zero_idxs[0][-1], 2] = 0
        chunks = repack(chunks)

        # is_all_zero = np.all((audioarray == 0))
        # if is_all_zero:
        #     continue
        # st()

        # if there is noise at the end after silence, erase end
        # if chunks[-1][-1] == 1 and chunks[-2][-1] == 0:
        #     chunks[-1][-1] = 0
        # if there is a long silence after the midpoint frame, turn all noise after silence into silence

        post_long_zero_idxs = np.where(
            (chunks[:, 1] - chunks[:, 0] > MAX_SILENCE_PERMITTED) & (chunks[:, 2] == 0) & (
                    chunks[:, 0] > midpointframe))
        if post_long_zero_idxs[0].shape >= (1,):
            chunks[post_long_zero_idxs[0][-1]:, 2] = 0

        chunks = repack(chunks)

        clip_len = round((audioFrameCount) / 24, 2)
        intro_cut = round((chunks[1][0]) / 24, 2)
        end_cut = round((chunks[-1][1] - chunks[-1][0]) / 24, 2)

        if intro_cut != 0 and end_cut != 0:
            print(
                f'{video_name}: Trimming {intro_cut} seconds/{round(intro_cut / clip_len * 100, 2)}% from front and {end_cut} seconds/{round(end_cut / clip_len * 100, 2)}% from back.')
        if intro_cut != 0 and end_cut == 0:
            print(f"{video_name}: Trimming {intro_cut} seconds/{round(intro_cut / clip_len * 100, 2)}% from front.")
        if intro_cut == 0 and end_cut != 0:
            print(f"{video_name}: Trimming {end_cut} seconds/{round(end_cut / clip_len * 100, 2)}% from back")
        if intro_cut == 0 and end_cut == 0:
            print("Nothing trimmed.")

        # make all correct frames present
        one_idx = np.asarray(np.where(chunks[:, 2] == 1))
        first = one_idx[0][0]
        last = one_idx[0][-1]
        chunks[first:last, 2] = 1

        chunks = repack(chunks)
        # print(chunks)
        FRAME_SPILL_BACK_FINAL = 2  # frames to include at the very end of the clip
        s_number = 0.02
        s_number2 = 0.017
        s_number3 = 0.015
        s_number4 = 0.01
        # crude s finder
        if chunks.shape == (3, 3):
            if volumeInformation[int(chunks[1, 1])] >= s_number:
                FRAME_SPILL_BACK_FINAL = FRAME_SPILL_BACK_FINAL + 2
            if (volumeInformation[int(chunks[1, 1]) + 1] >= s_number2) & (
                    volumeInformation[int(chunks[1, 1])] >= s_number):
                FRAME_SPILL_BACK_FINAL = FRAME_SPILL_BACK_FINAL + 1
            if (volumeInformation[int(chunks[1, 1]) + 2] >= s_number3) & (
                    volumeInformation[int(chunks[1, 1]) + 1] >= s_number2) & (
                    volumeInformation[int(chunks[1, 1])] >= s_number):
                FRAME_SPILL_BACK_FINAL = FRAME_SPILL_BACK_FINAL + 1
                if (volumeInformation[int(chunks[1, 1]) + 3] >= s_number4) & (
                        volumeInformation[int(chunks[1, 1]) + 2] >= s_number3) & (
                        volumeInformation[int(chunks[1, 1]) + 1] >= s_number2) & (
                        volumeInformation[int(chunks[1, 1])] >= s_number):
                    FRAME_SPILL_BACK_FINAL = FRAME_SPILL_BACK_FINAL + 1

        FRAME_SPILL_BACK_FINAL = FRAME_SPILL_BACK_FINAL + additional_spill

        if FRAME_SPILL_BACK_FINAL > 4:
            print(f"     Adding {FRAME_SPILL_BACK_FINAL} total spill frames")


        # add spill where necessary
        if chunks.shape == (3, 3):
            chunks[1][0] = chunks[1][0] - FRAME_SPILL_FRONT_FINAL
            chunks[1][1] = chunks[1][1] + FRAME_SPILL_BACK_FINAL

            chunks[0][1] = chunks[0][1] - FRAME_SPILL_FRONT_FINAL
            chunks[2][0] = chunks[2][0] + FRAME_SPILL_BACK_FINAL
        elif (chunks.shape == (2, 3)) & (chunks[0][2] == 0):
            chunks[1][0] = chunks[1][0] - FRAME_SPILL_FRONT_FINAL
            chunks[1][1] = chunks[1][1] + FRAME_SPILL_BACK_FINAL

            chunks[0][1] = chunks[0][1] - FRAME_SPILL_FRONT_FINAL
        elif (chunks.shape == (2,3)) & (chunks[0][2]==1):
            chunks[0][1] = chunks[0][1] + FRAME_SPILL_BACK_FINAL
            chunks[1][0] = chunks[1][0] - FRAME_SPILL_BACK_FINAL

        else:
            print(f"     2 or 3 dimensional array not detected. Shape is {chunks.shape}, please review.")

        # print(chunks)
        # create new Audio data array
        outputAudioData = np.zeros((0, audioData.shape[1]))
        outputPointer = 0

        lastExistingFrame = None
        for chunk in chunks:
            audioChunk = audioData[int(chunk[0] * samplesPerFrame):int(chunk[1] * samplesPerFrame)]

            sFile = TEMP_FOLDER + "/tempStart.wav"
            eFile = TEMP_FOLDER + "/tempEnd.wav"
            wavfile.write(sFile, SAMPLE_RATE, audioChunk)
            with WavReader(sFile) as reader:
                with WavWriter(eFile, reader.channels, reader.samplerate) as writer:
                    tsm = phasevocoder(reader.channels, speed=NEW_SPEED[int(chunk[2])])
                    tsm.run(reader, writer)
            _, alteredAudioData = wavfile.read(eFile)
            leng = alteredAudioData.shape[0]
            endPointer = outputPointer + leng
            outputAudioData = np.concatenate((outputAudioData, alteredAudioData / maxAudioVolume))

            if leng < AUDIO_FADE_ENVELOPE_SIZE:
                outputAudioData[outputPointer:endPointer] = 0  # audio is less than 0.01 sec, let's just remove it.
            else:
                premask = np.arange(AUDIO_FADE_ENVELOPE_SIZE) / AUDIO_FADE_ENVELOPE_SIZE
                mask = np.repeat(premask[:, np.newaxis], 2, axis=1)  # make the fade-envelope mask stereo
                outputAudioData[outputPointer:outputPointer + AUDIO_FADE_ENVELOPE_SIZE] *= mask
                outputAudioData[endPointer - AUDIO_FADE_ENVELOPE_SIZE:endPointer] *= 1 - mask

            startOutputFrame = int(math.ceil(outputPointer / samplesPerFrame))
            endOutputFrame = int(math.ceil(endPointer / samplesPerFrame))
            for outputFrame in range(startOutputFrame, endOutputFrame):
                inputFrame = int(chunk[0] + NEW_SPEED[int(chunk[2])] * (outputFrame - startOutputFrame))
                didItWork = copyFrame(inputFrame, outputFrame)
                if didItWork:
                    lastExistingFrame = inputFrame
                else:
                    copyFrame(lastExistingFrame, outputFrame)

            outputPointer = endPointer

        wavfile.write(TEMP_FOLDER + "/audioNew.wav", SAMPLE_RATE, outputAudioData)

        command = "ffmpeg -framerate " + str(
            frameRate) + " -y -i " + TEMP_FOLDER + "/newFrame%06d.jpg -i " + TEMP_FOLDER + "/audioNew.wav -strict -2 " + OUTPUT_FILE + " -loglevel error"
        subprocess.call(command, shell=True)

        deletePath(TEMP_FOLDER)

    print(f"Finished trimming in {round((time.time() - start_time) / 60, 2)} minutes. "
          f"Avg {round(round((time.time() - start_time) / 60, 2) / (len(myVideos)), 2)} minutes per clip.")


if __name__ == "__main__":
    retrim(filesuffix, vid_dir_in, layer2)  # desired output, and directory