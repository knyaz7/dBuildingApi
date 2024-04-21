from flask import jsonify, request, send_file
from gtts import gTTS

def text_to_audio(text, path):
    tts = gTTS(text=text, lang='ru')
    tts.save(path)

def convert_text_to_audio():
    if 'text' not in request.form:
        return jsonify({'error': 'Text parameter is missing'}), 400

    text = request.form['text']

    # Уникальное имя для аудиофайла
    audio_file_path = 'output_audio.wav'

    # Преобразование текста в аудиофайл
    text_to_audio(text, audio_file_path)

    # Посылаем аудиофайл обратно в ответе
    return send_file(audio_file_path, as_attachment=True)