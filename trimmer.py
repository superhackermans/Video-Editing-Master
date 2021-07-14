import subprocess
from audiotsm import phasevocoder
from audiotsm.io.wav import WavReader, WavWriter
from scipy.io import wavfile
import numpy as np
import math
from shutil import copyfile, rmtree
import os
import shutil
from parameters import *

def getMaxVolume(s):
    maxv = float(np.max(s))
    minv = float(np.min(s))
    return max(maxv,-minv)
def copyFrame(inputFrame,outputFrame):
    TEMP_FOLDER = "TEMP"
    src = TEMP_FOLDER+"/frame{:06d}".format(inputFrame+1)+".jpg"
    dst = TEMP_FOLDER+"/newFrame{:06d}".format(outputFrame+1)+".jpg"
    if not os.path.isfile(src):
        return False
    copyfile(src, dst)
    # if outputFrame%20 == 19:
    #     print(str(outputFrame+1)+" time-altered frames saved.")
    return True

def trimmer():
    # turn filenames in list
    myVideos = []
    print("Processing: ")
    for file in os.listdir(vid_dir_in):
        if file.endswith(".MP4") or file.endswith(".mp4"):
            myVideos.append(file)
    if not myVideos:
        print("No input videos detected")
        # quit()
    myVideos = sorted(myVideos)
    for video in myVideos:
        print(video)
    # print(myVideos)

    createPath(vid_processed)
    createPath(wav_dir)

    #Trim and delete mistakes
    for video_name in myVideos:
        print(f'Beginning Trimming for {video_name}')
        INPUT_FILE = f"{vid_dir_in}{video_name}"
        assert INPUT_FILE != None , "No Input File Detected"
        OUTPUT_FILE = f"{layer2}{inputToOutputFilename(video_name)}"

        TEMP_FOLDER = "TEMP"
        createPath(TEMP_FOLDER)

        command = "ffmpeg -i " + INPUT_FILE + " -qscale:v " + str(
            FRAME_QUALITY) + " " + TEMP_FOLDER + "/frame%06d.jpg -hide_banner" + " -loglevel error"
        subprocess.call(command, shell=True)
        # get audio
        command = "ffmpeg -i " + INPUT_FILE + " -ab 160k -ac 2 -ar " + str(
            SAMPLE_RATE) + " -vn " + TEMP_FOLDER + "/audio.wav" + " -loglevel error"
        subprocess.call(command, shell=True)

        #read extracted audio file
        sampleRate, audioData = wavfile.read(TEMP_FOLDER+"/audio.wav")
        audioSampleCount = audioData.shape[0]
        maxAudioVolume = getMaxVolume(audioData)

        #define parameters
        samplesPerFrame = sampleRate/frameRate
        audioFrameCount = int(math.ceil(audioSampleCount/samplesPerFrame))
        hasLoudAudio = np.zeros((audioFrameCount))
        volumeInformation = np.zeros((audioFrameCount))


        #split audio into frames and turn the volume info into an array
        for i in range(audioFrameCount):
            start = int(i * samplesPerFrame)
            end = min(int((i + 1) * samplesPerFrame), audioSampleCount)
            audiochunks = audioData[start:end]
            maxchunksVolume = float(getMaxVolume(audiochunks))/maxAudioVolume
            volumeInformation = np.append(volumeInformation, maxchunksVolume)
            # print(maxchunksVolume)
            if maxchunksVolume >= SILENT_THRESHOLD:
                hasLoudAudio[i] = 1

        #remove small smack instances
        loud_instance = np.where(hasLoudAudio == 1)[0]
        if hasLoudAudio[loud_instance[0] + 1] == 0:
            hasLoudAudio[loud_instance[0]] = 0
        if hasLoudAudio[loud_instance[0] + 2] == 0:
            hasLoudAudio[loud_instance[0]] = 0

        #add frame spill to the end
        hasLoudAudio[loud_instance[-1]:(loud_instance[-1])] = 1

        #combine into list of chunks
        chunks = [[0,0,0]]
        shouldIncludeFrame = np.zeros(audioFrameCount)

        #concatenate and add buffers
        for i in range(audioFrameCount):
            start = int(max(0,i-FRAME_SPILL_FRONT))
            end = int(min(audioFrameCount,i+1+FRAME_SPILL_BACK))
            shouldIncludeFrame[i] = np.max(hasLoudAudio[start:end])
            if (i >= 1 and shouldIncludeFrame[i] != shouldIncludeFrame[i-1]): # Did we flip?
                chunks.append([chunks[-1][1],i,shouldIncludeFrame[i-1]])

        #Eliminate small middle chunks
        for chunk in chunks[1:-1]:
            if chunk[1] - chunk[0] < MAX_SILENCE_PERMITTED:
                chunk[2] = 1.0
        # print(f'middle chunks are {chunks}')
        #If long pause, delete all footage prior
        arr = np.asarray(chunks)

        zero_idxs = np.where(arr[1:-1, 2] == 0)[0] + 1      # + 1 to compensate for indexing from 1:

        #find midpoint and the frame where silence was found, if there are multiple instances
        midpointframe = arr[-1, 1]*(2/3)
        if zero_idxs.shape >= (1,):
            framepointofsilence = arr[zero_idxs[-1], 1]

        #ignore if silence gap was due to noise at the end of the clip. else, delete everything in front
        if zero_idxs.shape == (0,):
            break_point = 0
        elif zero_idxs.shape != (0,) and framepointofsilence > midpointframe:
            arr[zero_idxs[-1]:, 2] = 0
        else:
            break_point = zero_idxs[-1]
            arr[:break_point, 2] = 0

        #add a frame spill to the end
        one_idxs = np.where(arr[:, 2] == 1)[0]
        arr[one_idxs[-1], 1] = arr[one_idxs[-1], 1] + FRAME_SPILL_BACK_FINAL

        chunks = arr.tolist()
        """
        shouldincludeFrames ie. 1 reaches above threshold and 0 does not per frame
        [0. 0. 0. 0. 0. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1.
         1. 0. 0. 0. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1.
         1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 0. 0. 0. 0. 1. 1. 1. 1. 1. 1. 1. 1.
         1. 1. 1. 1. 0. 0. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 0. 0. 0.
         0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.
         0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
    
        appended chunks is [[0, 25, 1.0], [25, 28, 0.0], [28, 93, 1.0], [93, 96, 0.0], [96, 118, 1.0], [118, 126, 0.0],
        [126, 157, 1.0], [157, 175, 0.0], [175, 304, 1.0], [304, 309, 0.0], [309, 371, 1.0], [371, 374, 0.0],[374, 418, 1.0],
        [418, 421, 0.0], [421, 478, 1.0], [478, 517, 0.0]]
        """
        #append last chunk
        # print(f'chunks[-1][1] is {chunks[-1][1]}')
        chunks.append([chunks[-1][1],audioFrameCount,shouldIncludeFrame[i-1]])
        if chunks[-1][2] == 1 and chunks[-2][2] == 0:
            chunks[-1][2] = 0
        chunks = chunks[1:]
        # st()
        print(f'Chunked audio: {chunks}')
        # print(f'Mistakes detected and removing: {mistakes}')

        #create new Audio data array
        outputAudioData = np.zeros((0,audioData.shape[1]))
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

        command = "ffmpeg -framerate "+str(frameRate)+" -i "+TEMP_FOLDER+"/newFrame%06d.jpg -i "+TEMP_FOLDER+"/audioNew.wav -strict -2 "+OUTPUT_FILE + " -loglevel error"
        subprocess.call(command, shell=True)

        shutil.rmtree(TEMP_FOLDER)

        #move file to processed_raw_files folder
        source_dir = vid_dir_in
        target_dir = vid_processed

        shutil.move(os.path.join(source_dir, video_name), target_dir)

        print(f'Finished Trimming for {video_name}')

    for video_name in myVideos:

        target_dir = vid_dir_in
        source_dir = vid_processed

        shutil.move(os.path.join(source_dir, video_name), target_dir)

    print("Finished trimming all files bitch")

# trimmer()