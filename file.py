from flask import Flask, request, send_file, jsonify, send_from_directory
from ttsmms import TTS, download

app = Flask(__name__)

@app.route('/synthesize', methods=['POST'])
def synthesize():
    data = request.get_json()
    text = data['text']
    
    dir_path = download("eng", "./data")
    tts = TTS(dir_path)
    wav = tts.synthesis(text)
    wav_path = "example.wav"
    tts.synthesis(text, wav_path=wav_path)
    
#    return send_file(wav_path, mimetype="audio/wav", as_attachment=True)

# Generate URL for the WAV file
    base_url = request.host_url.rstrip('/')
    wav_url = f"{base_url}/{wav_path}"

    return jsonify({'wav_url': wav_url})

@app.route('/<path:filename>')
def serve_static_file(filename):
    return send_from_directory('.', filename)
    
if __name__ == '__main__':
    app.run()
