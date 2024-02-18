import speech_recognition as sr
from gtts import gTTS 
import os

# Initialize the recognizer 
r = sr.Recognizer() 
 
# Function to convert text to
# speech    
     
# Loop infinitely for user to
# speak
 
while(1):    
     
    # Exception handling to handle
    # exceptions at the runtime
    try:
         
        # use the microphone as source for input.
        with sr.Microphone() as source2:
             
            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level 
            r.adjust_for_ambient_noise(source2, duration=0.2)
            #listens for the user's input 
            audio2 = r.listen(source2) 
            # Using google to recognize audio
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()
            print("Did you say ",MyText)
            gTTS(text=MyText, lang='en', slow=False).save("Test.mp3")
            os.system("Test.mp3") 
             
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
         
    except sr.UnknownValueError:
        print("unknown error occurred")