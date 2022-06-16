from serial import Serial
import time
import random
import datetime
import speechRecognition as vR
import textToSpeech as tTS
import os
import pyaudio
import wave
import messageAnalysis as msgA
    
def record_audio(outputFileName):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    #RECORD_SECONDS = 5
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print("* start recording")
    frames = []
    while True:
        data = stream.read(CHUNK)
        frames.append(data)
        print("* recording...")
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            if line == "done":
                break
    print("* done recording")
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(outputFileName, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    return


def save_input(topicNumber, fileName):
    userInput = vR.recognize_voice(fileName)
    print(userInput)
    if (userInput != "error") and (len(userInput) > 20):
        # write to newMessages.txt
        with open('newMessages.txt', 'a') as f:
            f.write('topic' + str(topicNumber) + ';' + userInput + '\n')
            f.close()
        print("New message saved.")

        # analyse message & save to csv
        msgA.retract_credentials()
        entryTopic = topicNumber
        keywords = msgA.generate_keywords(userInput)
        sentiment = msgA.sentiment_analysis(userInput)
        print("keywords: " + keywords)
        print("Sentiment: " + sentiment)
        entryID = msgA.generate_id(topic)
        msgA.update_data(entryTopic, entryID, userInput, keywords, sentiment)
        # generatedAudioPath = "audio/topic" + str(topicNumber) + entryID
        # tTS.generate_audio(generatedAudioPath, userInput, "en")
        msgA.update_visualisation()

    else:
        print("Message ignored.")
    return
    
if __name__ == '__main__':
    ser = Serial('/dev/tty.usbmodem141401', 9600, timeout = 1)
    ser.flush()

    while True:

        # receive topic number
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                print(line)
                if line == 'Topic1':
                    topic = 1 
                    break
                elif line =='Topic2':
                    topic = 2
                    break
                elif line =='Topic3':
                    topic = 3
                    break


        # locate audio file paths
        audioDir = "audio/topic" + str(topic)
        fileNames = random.sample(os.listdir(audioDir), 4)
        lsVoiceDir = []
        for fname in fileNames:
            lsVoiceDir.append(audioDir + '/' + fname)

        # commands from arduino
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                print(line)
                if line == 'Ask question':
                    print("playing question...")
                    os.system("afplay " + "audio/q" + str(topic) + ".mp3")
                    time.sleep(2)
                    os.system("afplay " + "audio/instructions.mp3")
                    time.sleep(2)
                    os.system("afplay " + "audio/q" + str(topic) + ".mp3")

                    ser.write(b'question done\n')
                elif line == 'voice1':
                    print("select message 1")
                    os.system("afplay " + lsVoiceDir[0])
                    ser.write(b'done\n')
                elif line == 'voice2':
                    print("select message 2")
                    os.system("afplay " + lsVoiceDir[1])
                    ser.write(b'done\n')
                elif line == 'voice3':
                    print("select message 3")
                    os.system("afplay " + lsVoiceDir[2])
                    ser.write(b'done\n')
                elif line == 'voice4':
                    print("select message 4")
                    os.system("afplay " + lsVoiceDir[3])
                    ser.write(b'done\n')
                elif line == 'record':
                    userRecordingFileName = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S") + ".wav"
                    record_audio(userRecordingFileName)
                    time.sleep(0.5)
                    os.system("afplay " + "audio/recordFeedback.mp3")
                    save_input(topic, userRecordingFileName)


                elif line == 'endsession':
                    print("current session finished")
                    break
