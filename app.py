import requests
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Masukkan API Key terbaru Bapak di sini
API_KEY = "AIzaSyA7OFq8GvEew2-5XwKv8k2UiD4V2DfZm88"

def tanya_ai(role, tugas):
    # Menggunakan URL paling standar
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
    
    # Format data yang paling ringkas
    data_input = {
        "contents": [{"parts": [{"text": f"Anda adalah {role}. {tugas}. Jawab 1 kalimat singkat."}]}]
    }
    
    try:
        response = requests.post(url, json=data_input, timeout=10)
        hasil = response.json()
        
        # Ambil teks dengan cara yang paling aman
        teks = hasil['candidates'][0]['content']['parts'][0]['text']
        return teks
    except Exception as e:
        # Jika gagal, tampilkan pesan error aslinya agar kita tahu 100% masalahnya
        return f"Sistem Google merespon: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/jalankan_kantor')
def jalankan():
    pesan = tanya_ai("Manager Informa Bekasi", "Berikan 1 instruksi promo furniture")
    return jsonify({"role": "Manager Bekasi", "text": pesan})

@app.route('/staf_jawab/<path:instruksi>')
def staf_jawab(instruksi):
    pesan = tanya_ai("Staf Kreatif", f"Buat caption TikTok dari: {instruksi}")
    return jsonify({"role": "Staf Kreatif", "text": pesan})

# Penting agar Vercel mengenalnya
app = app
