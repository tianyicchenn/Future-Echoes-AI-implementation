# -*- coding: utf-8 -*-
import speech_recognition as sr


def recognize_voice(wav_path):
    r = sr.Recognizer()
    with sr.WavFile(wav_path) as source:
        audio = r.listen(source)

    try:
        return r.recognize_google(audio, language='enl')
    except sr.UnknownValueError:
        print("Speech Recognition could not understand audio")
        return "error"
    except sr.RequestError as e:
        print("Could not request results from Speech Recognition service; {0}".format(e))
        return "error"


if __name__ == '__main__':
    print(recognize_voice(wav_path="test.wav"))
