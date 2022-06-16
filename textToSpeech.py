from gtts import gTTS
import os

def generate_audio(filename, dataText, outputLanguage):
    # Passing the text and language to the engine,
    myobj = gTTS(text=dataText, lang=outputLanguage, slow=True)
    # Saving the converted audio in a mp3 file
    myobj.save(filename)

# Playing the converted file


if __name__ == "__main__":
    generate_audio('testoutput.mp3', 'this is a demo for future echoes', 'en')
    #Mac OS
    os.system("afplay " + "testoutput.mp3")
    #Linux - first 'sudo apt install mpg123'
    #os.system("mpg123 " + "testoutput.mp3")
