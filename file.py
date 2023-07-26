import os
import azure.cognitiveservices.speech as speechsdk
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

# Replace these with your Azure Speech Service credentials
SUBSCRIPTION_KEY = "b771e7fc717c426d87afa4391f0e691d"
REGION = "eastus"

@app.route('/synthesize', methods=['POST'])
def synthesize():
    data = request.get_json()
    text = data['text']

    print("Received text:", text)
    # Initialize the Speech Synthesizer
    speech_config = speechsdk.SpeechConfig(subscription=SUBSCRIPTION_KEY, region=REGION)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    # Synthesize speech from the provided text
    result = speech_synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        # Save the synthesized audio to a file (optional)
        wav_path = "example.wav"
        with open(wav_path, "wb") as f:
            f.write(result.audio_data)

        # Return the audio data as a response
        return send_file(result.audio_data, mimetype="audio/wav")
    else:
        return jsonify({'error': 'Speech synthesis failed'}), 500

if __name__ == '__main__':
    app.run(port=8000)
