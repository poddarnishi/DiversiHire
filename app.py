from flask import Flask, render_template, request
import PyPDF2
import speech_recognition as sr
import os
from gtts import gTTS 

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/upload', methods=['POST'])
# def upload():
#     if 'file' not in request.files:
#         return 'No file part'
    
#     file = request.files['file']
    
#     if file.filename == '':
#         return 'No selected file'
    
#     if file:
#         pdf_reader = PyPDF2.PdfFileReader(file)
#         text = ''
#         for page_num in range(pdf_reader.numPages):
#             page = pdf_reader.getPage(page_num)
#             text += page.extractText()
#         return text
    
@app.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.2)
        print("Speak something...")
        audio = recognizer.listen(source, timeout=10)
    try:
        text = recognizer.recognize_google(audio)
        gTTS(text=text, lang='en', slow=False).save("Answer1.mp3")
        os.system("Answer1.mp3") 
        print(text)
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"Error: {str(e)}"
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
