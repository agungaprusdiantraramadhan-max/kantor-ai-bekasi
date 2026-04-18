from flask import Flask, render_template, jsonify
import requests
import os

app = Flask(__name__)
app.debug = True  # Tambahkan ini untuk melihat error jika ada
app = app         # Pastikan ini ada agar Vercel mengenalnya

# Mengambil API Key dari sistem (nanti kita setting di Render agar aman)
API_KEY = "AQ.Ab8RN6LEnSn4eq5IcY8uXx1Ex6GyAmSw2Eb_SdiBSKInjCDUhg"

def tanya_ai(role, tugas):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    data = {"contents": [{"parts": [{"text": f"Anda adalah {role}. {tugas}. Jawab maksimal 1 kalimat singkat."}]}]}
    try:
        response = requests.post(url, json=data)
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "Gagal terhubung ke AI"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/jalankan_kantor')
def jalankan():
    instruksi = tanya_ai("Manager Informa MM Bekasi", "Berikan 1 instruksi promo sofa bed hari ini")
    return jsonify({"role": "Manager Bekasi", "text": instruksi})

@app.route('/staf_jawab/<path:instruksi>')
def staf_jawab(instruksi):
    caption = tanya_ai("Staf Kreatif", f"Buat caption TikTok singkat dari instruksi ini: {instruksi}")
    return jsonify({"role": "Staf Kreatif", "text": caption})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
