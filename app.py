from flask import Flask, render_template, jsonify
import requests
import json

app = Flask(__name__)

# Kunci langsung tanpa os.environ agar pasti terbaca
API_KEY = "AQ.Ab8RN6LEnSn4eq5IcY8uXx1Ex6GyAmSw2Eb_SdiBSKInjCDUhg"

def tanya_ai(role, tugas):
    # Kita gunakan model gemini-1.5-flash yang paling stabil untuk Vercel
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [{
            "parts": [{"text": f"Anda adalah {role}. {tugas}. Jawab maksimal 1 kalimat singkat."}]
        }]
    }
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
        response_data = response.json()
        
        # Mengambil teks jawaban
        return response_data['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        print(f"Error: {e}")
        return "Manager sedang sibuk, silakan coba lagi."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/jalankan_kantor')
def jalankan():
    instruksi = tanya_ai("Manager Informa Bekasi", "Berikan 1 instruksi promo sofa atau furniture hari ini")
    return jsonify({"role": "Manager Bekasi", "text": instruksi})

@app.route('/staf_jawab/<path:instruksi>')
def staf_jawab(instruksi):
    caption = tanya_ai("Staf Kreatif", f"Buat caption TikTok singkat dari instruksi ini: {instruksi}")
    return jsonify({"role": "Staf Kreatif", "text": caption})

# Penting untuk Vercel
app = app
