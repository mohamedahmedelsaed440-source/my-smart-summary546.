import streamlit as st
import google.generativeai as genai
import pdfplumber
from PIL import Image
import pytesseract
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
from arabic_reshaper import reshape
from bidi.algorithm import get_display

# إعداد الـ API
API_KEY = "AIzaSyDso4OPFXij1guGTSX6gN2zwSaXDix-c1o"
genai.configure(api_key=API_KEY)

@st.cache_resource
def load_model():
    return genai.GenerativeModel("gemini-1.5-flash")

model = load_model()

def fix_arabic(text):
    try: return get_display(reshape(text))
    except: return text

def extract_content(file):
    if file.type.startswith("image/"):
        return pytesseract.image_to_string(Image.open(file), lang="ara+eng")
    elif file.type == "application/pdf":
        with pdfplumber.open(file) as pdf:
            return "\n".join([p.extract_text() or "" for p in pdf.pages])
    elif file.type in ["audio/mpeg", "audio/wav", "audio/mp3"]:
        audio = AudioSegment.from_file(file)
        wav_io = BytesIO(); audio.export(wav_io, format="wav"); wav_io.seek(0)
        r = sr.Recognizer()
        with sr.AudioFile(wav_io) as src: return r.recognize_google(r.record(src), language="ar-SA")
    return file.read().decode(errors="ignore")

# تصميم الواجهة الملكية
st.set_page_config(page_title="Royal AI Platform", layout="wide")
st.markdown("<style>html, body, * { font-family: 'Cairo', sans-serif; text-align: right; } .card { padding: 20px; background: white; border-radius: 1
