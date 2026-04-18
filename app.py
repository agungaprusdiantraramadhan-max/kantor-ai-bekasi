import os
import requests
import json
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Mengambil kunci dari brankas Vercel (Environment Variable)
API_KEY = os.environ.get("GEMINI_API_KEY")

def tanya_ai(role, tugas):
    if not API_KEY:
        return "API Key belum terpasang di Settings Vercel."
        
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    payload = {"contents": [{"parts": [{"text": f"Anda adalah {role}. {tugas}. Jawab maksimal 1 kalimat."}]}]}
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
        data = response.json()
        return data['candidates'][0]['content']['parts'][0]['text']
    except:
        return "Manager sedang meeting offline, coba klik lagi!"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/jalankan_kantor')
def jalankan():
    txt = tanya_ai("Manager Informa Bekasi", "Berikan 1 instruksi promo sofa bed hari ini")
    return jsonify({"role": "Manager Bekasi", "text": txt})

@app.route('/staf_jawab/<path:instruksi>')
def staf_jawab(instruksi):
    txt = tanya_ai("Staf Kreatif", f"Buat caption TikTok dari: {instruksi}")
    return jsonify({"role": "Staf Kreatif", "text": txt})
    
