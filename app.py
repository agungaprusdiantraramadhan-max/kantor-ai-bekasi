import os
import requests
import json
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Mengambil kunci dari Environment Variable Vercel
API_KEY = os.environ.get("GEMINI_API_KEY")

def tanya_ai(role, tugas):
    if not API_KEY:
        return "API Key belum terpasang di Vercel."
    
    # MENGGUNAKAN MODEL TERBARU SESUAI DAFTAR BAPAK
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [{
            "parts": [{"text": f"Anda adalah {role}. {tugas}. Jawab maksimal 1 kalimat singkat dan tegas."}]
        }]
    }
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
        data = response.json()
        
        # Mengambil teks dari struktur respons Gemini terbaru
        if 'candidates' in data:
            return data['candidates'][0]['content']['parts'][0]['text']
        else:
            return "Manager sedang memantau floor, coba lagi!"
    except:
        return "Koneksi ke server AI terputus."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/jalankan_kantor')
def jalankan():
    txt = tanya_ai("Manager Informa Bekasi", "Berikan 1 instruksi promo furniture unggulan hari ini")
    return jsonify({"role": "Manager Bekasi", "text": txt})

@app.route('/staf_jawab/<path:instruksi>')
def staf_jawab(instruksi):
    txt = tanya_ai("Staf Kreatif", f"Buat caption TikTok viral dari instruksi: {instruksi}")
    return jsonify({"role": "Staf Kreatif", "text": txt})

app = app
