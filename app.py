from flask import Flask, request, send_file, render_template
import os
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return "Nenhum arquivo enviado.", 400

    file = request.files['file']
    if file.filename == '':
        return "Nome de arquivo inválido.", 400

    # Salva o arquivo MP4
    mp4_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(mp4_path)

    # Converte o arquivo para MP3
    mp3_filename = file.filename.replace('.mp4', '.mp3')
    mp3_path = os.path.join(OUTPUT_FOLDER, mp3_filename)
    subprocess.run(['ffmpeg', '-i', mp4_path, mp3_path])

    # Remove o arquivo MP4 após a conversão
    os.remove(mp4_path)

    return {'download_url': f'/download/{mp3_filename}'}

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    mp3_path = os.path.join(OUTPUT_FOLDER, filename)
    return send_file(mp3_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)