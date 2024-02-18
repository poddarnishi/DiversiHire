from flask import Flask, render_template, request, jsonify, url_for
import PyPDF2
import speech_recognition as sr
import os
from gtts import gTTS 
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
from spacy.matcher import PhraseMatcher
from PyPDF2 import PdfWriter, PdfFileReader, PageObject
import spacy
import re
import fitz
from flask import redirect, url_for
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/interview')
def interview():
    return render_template('interview.html')

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

    if request.method=='GET':
        return render_template('mic.html')
    else:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.2)
            print("Speak something...")
            audio = recognizer.listen(source, timeout=10)
        try:
            text = recognizer.recognize_google(audio)
            gTTS(text=text, lang='en', slow=False).save("static/Answer1.mp3")
            audio_url = url_for('static', filename='Answer1.mp3')
            print(text)
            return text

        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return f"Error: {str(e)}"
def save_text_to_file(text, filename):
    with open(filename, 'w') as file:
        file.write(text)


UPLOAD_FOLDER = 'uploads'
SANTIZED_FOLDER = 'sanitized'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SANTIZED_FOLDER'] = SANTIZED_FOLDER

nlp = spacy.load('en_core_web_sm')

PHRASES = [
    "male", "female", "non-binary", "transgender",
    "United States", "USA", "America", "China", "India",  # Add more countries as needed
    "New York", "California", "Texas", "London", "Paris", "Mumbai"  # Add more cities or regions as needed
    "Mr.", "Ms.", "Mrs.", "Miss", "Dr.",  # Honorific titles
    "male", "female", "other", "prefer not to say",  # Gender identities
    "African", "Asian", "Caucasian", "Hispanic", "Latino", "Middle Eastern", "Native American", "Pacific Islander",  # Ethnicities
    "Christian", "Muslim", "Jewish", "Buddhist", "Hindu", "Atheist", "Agnostic", "other religion",  # Religious affiliations
    "married", "single", "divorced", "widowed", "separated", "partnered",  # Marital status
    "heterosexual", "homosexual", "bisexual", "pansexual", "asexual",  # Sexual orientations
    "USA", "UK", "United Kingdom", "Australia", "Canada", "Germany", "France", "Italy", "Spain", "Japan", "Brazil",  # Additional countries
    "NY", "LA", "SF", "UK", "JP", "CA", "TX", "FL", "WA",  # Abbreviations for states, cities, and countries
    "North", "South", "East", "West", "Northeast", "Northwest", "Southeast", "Southwest",  # Directions
    "the United States", "the USA", "the UK", "the United Kingdom",  # Country prefixes
    "Europe", "Asia", "Africa", "North America", "South America", "Australia", "Antarctica",  # Continents
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", "Australia", "Austria",  # Countries
    "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan",
    "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde",
    "Cambodia", "Cameroon", "Canada", "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo, Democratic Republic of the",
    "Congo, Republic of the", "Costa Rica", "Cote d'Ivoire", "Croatia", "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti",
    "Dominica", "Dominican Republic", "East Timor (Timor-Leste)", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia",
    "Eswatini", "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada",
    "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq",
    "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea, North", "Korea, South",
    "Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania",
]

matcher = PhraseMatcher(nlp.vocab)
matcher.add("PHRASES", None, *[nlp(text) for text in PHRASES])


PROPER_NOUNS = ["PROPN"]

def sanitize_text(text):
    doc = nlp(text)
    spans = []
    for match_id, start, end in matcher(doc):
        span = doc[start:end]
        spans.append(span)
    for span in spans:
        text = text.replace(span.text, "REDACTED")
    return text


def remove_propn(text):
     # Remove email addresses
    text = re.sub(r'\S+@\S+', 'REDACTED_EMAIL', text)
    
    # Remove phone numbers (supports common formats)
    text = re.sub(r'(\+?(\d{1,2})?[ -]?\(?\d{3}\)?[ -]?\d{3}[ -]?\d{4}\b)', 'REDACTED_PHONE', text)
    
    # Remove URLs
    text = re.sub(r'https?://(?:www\.)?linkedin\.com/(?:in|pub|profile)/\S+', 'REDACTED_URL', text)
    
    # remove .com
    text = re.sub(r'\b\S*\.com\S*\b', 'REDACTED', text)
    
    doc = nlp(text)
    sanitized_text = []
    for token in doc:
        if token.ent_type_ == 'PERSON':
            sanitized_text.append("REDACTED_NAME")
        else:
            sanitized_text.append(token.text)
    return ' '.join(sanitized_text)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login form submission
        # Validate credentials (you will implement this)
        # Redirect to appropriate page
        return render_template('index.html')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle register form submission
        # Register user (you will implement this)
        # Redirect to appropriate page
        return render_template('index.html')
    return render_template('register.html')

@app.route('/form')
def upload_form():
    return render_template('apply.html')

@app.route('/job_details.html')
def job_details():
    return render_template('job-detail.html')

@app.route('/display_text')
def display_text():
    sanitized_file_path = os.path.join(app.config['SANTIZED_FOLDER'], 'sanitized_resume.txt')
    with open(sanitized_file_path, 'r', encoding='utf-8') as f:
        sanitized_resume_content = f.read()
    #print(sanitized_resume_content)
    return render_template('display.html', resume_content=sanitized_resume_content)


def sanitize(text):
    sanitized_text = sanitize_text(text)
    clean_txt = remove_propn(sanitized_text)
    return clean_txt

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file and file.filename.endswith('.pdf'):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        pdf_text = extract_text_from_pdf(file_path)
        clean_txt = sanitize(pdf_text)
        sanitized_file_path = os.path.join(app.config['SANTIZED_FOLDER'], 'sanitized_' + 'resume.txt')
        with open(sanitized_file_path, 'w', encoding='utf-8') as f:
            f.write(clean_txt)
        
        #txt_to_pdf('sanitized/sanitized_resume.txt', 'sanitized/sanitized_resume.pdf')
        return redirect(url_for('display_text'))
    else:
        return 'Invalid file type'

def extract_text_from_pdf(pdf_path):
    text = ''
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text




def txt_to_pdf(input_txt, output_pdf):
    c = canvas.Canvas(output_pdf, pagesize=letter)
    
    with open(input_txt, 'r') as f:
        text = f.read()

    c.setFont("Helvetica", 12)
    
  
    lines = text.split('\t')
    for line in lines:
        c.drawString(50, 750, line)  
        c.showPage() 
    c.save()

def display_pdf_text(pdf_text):
    return render_template('display.html', pdf_text=pdf_text)
  
if __name__ == '__main__':
    app.run(debug=True)
