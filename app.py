import requests
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Masukkan API Key Bapak di sini
API_KEY = "AIzaSyA7OFq8GvEew2-5XwKv8k2UiD4V2DfZm88"

def tanya_ai(role, tugas):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
    
    # Format payload paling simpel
    payload = {
        "contents": [{"parts": [{"text": f"Anda adalah {role}. {tugas}. Jawab 1 kalimat."}]}]
    }
    
    try:
        # Langsung kirim JSON tanpa json.dumps agar Flask otomatis urus headers
        response = requests.post(url, json=payload, timeout=10)
        data = response.json()
        
        # Ambil teksnya
        return data['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        # Jika gagal, tampilkan pesan error aslinya agar kita tahu masalahnya
        return f"Manager sedang meeting. (Error: {str(e)})"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/jalankan_kantor')
def jalankan():
    res = tanya_ai("Manager Informa Bekasi", "Berikan 1 instruksi promo furniture hari ini")
    return jsonify({"role": "Manager Bekasi", "text": res})

@app.route('/staf_jawab/<path:instruksi>')
def staf_jawab(instruksi):
    res = tanya_ai("Staf Kreatif", f"Buat caption TikTok dari: {instruksi}")
    return jsonify({"role": "Staf Kreatif", "text": res})

app = app
