from flask import Flask, render_template, jsonify
import requests
import json

app = Flask(__name__)

# Menggunakan API Key baru Bapak
API_KEY = "AIzaSyA7OFq8GvEew2-5XwKv8k2UiD4V2DfZm88"

def tanya_ai(role, tugas):
    # Menggunakan model Gemini 1.5 Flash yang tersedia saat ini
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [{
            "parts": [{"text": f"Anda adalah {role}. {tugas}. Jawab maksimal 1 kalimat singkat."}]
        }]
    }
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=15)
        response_data = response.json()
        
        # Mengambil teks jawaban dari struktur Gemini
        if 'candidates' in response_data:
            return response_data['candidates'][0]['content']['parts'][0]['text']
        else:
            return "Koneksi stabil, tapi Manager sedang berpikir keras. Coba lagi ya!"
    except Exception as e:
        return "Gagal terhubung ke server AI. Cek koneksi internet."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/jalankan_kantor')
def jalankan():
    instruksi = tanya_ai("Manager Informa MM Bekasi", "Berikan 1 instruksi promo furniture hari ini")
    return jsonify({"role": "Manager Bekasi", "text": instruksi})

@app.route('/staf_jawab/<path:instruksi>')
def staf_jawab(instruksi):
    caption = tanya_ai("Staf Kreatif", f"Buat caption TikTok singkat dari instruksi ini: {instruksi}")
    return jsonify({"role": "Staf Kreatif", "text": caption})

# PENTING: Untuk Vercel
app = app
