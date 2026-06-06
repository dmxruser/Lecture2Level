import os
from flask import Flask, flash, redirect, render_template, request, session, jsonify, send_file
from werkzeug.utils import secure_filename
import random


from shelp import convert, load_song, calc_average, get_lenghts, speed_up
from lhelp import make_data
from fhelp import encrypt_file, output_file

app = Flask(__name__)
app.secret_key = 'dev-secret-key-12345'
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

LEVELS = [
    "leveldata/head.txt",
    "leveldata/0.txt",
]

PATHS = [
    "leveldata/1",
    "leveldata/2",
    "leveldata/3",
]

@app.route('/')
def index():
    return render_template('index.html')

def get_upload_from_request():
    file = request.files.get('file')
    if file is None or not file.filename:
        return None
    return file

def prepare_upload(file):
    filename = secure_filename(file.filename or "")
    folder_name = os.path.splitext(filename)[0]
    file_dir = os.path.join(UPLOAD_FOLDER, folder_name)
    os.makedirs(file_dir, exist_ok=True)
    filepath = os.path.join(file_dir, filename)
    file.save(filepath)
    return filename, folder_name, file_dir, filepath

def convert_uploaded_file(filename, filepath):
    if filename.endswith('.mp4'):
        audio_filepath = convert(filepath)
        os.remove(filepath)
        return audio_filepath
    return filepath

def apply_speed_change(audio_filepath, file_dir, folder_name, speed):
    if speed != 1.0:
        sped_up_path = os.path.join(file_dir, f"{folder_name}_sped_up.mp3")
        speed_up(audio_filepath, sped_up_path, speed)
        os.remove(audio_filepath)
        return sped_up_path
    return audio_filepath

def analyze_audio(audio_filepath):
    y, sr = load_song(audio_filepath)
    avg = calc_average(y, sr)
    return get_lenghts(y, sr, avg)

def build_level_data(lengths, distance=0):
    text = []
    with open(LEVELS[0], 'r') as f:
        text.append(f.read())
    text.append(make_data(LEVELS[1], distance))
    distance += 270

    for level in lengths[1:]:
        ran_folder = random.randint(0, 2)
        ran_file = random.randint(1, 3)
        file_path = f"{PATHS[ran_folder]}/{ran_file}.txt"

        text.append(make_data(file_path, distance))
        distance += 270

    return "".join(text)

def write_gmd_file(file_dir, folder_name, level_data):
    gmd_filename = f"{folder_name}.gmd"
    output_file(os.path.join(file_dir, gmd_filename), level_data)
    return gmd_filename

@app.route('/analyze', methods=['POST', 'GET'])
def analyze():
    if request.method == 'POST':
        file = get_upload_from_request()
        if file is None:
            return redirect('/')

        speed = request.form.get('speed', type=float, default=1.0)
        filename, folder_name, file_dir, filepath = prepare_upload(file)
        audio_filepath = convert_uploaded_file(filename, filepath)
        audio_filepath = apply_speed_change(audio_filepath, file_dir, folder_name, speed)
        session['audio_path'] = audio_filepath

        lengths = analyze_audio(audio_filepath)
        level_data = build_level_data(lengths)
        gmd_filename = write_gmd_file(file_dir, folder_name, level_data)

        return render_template('info.html', filename=gmd_filename, audio_filename=os.path.basename(audio_filepath))
    else:
        return redirect('/')

@app.route('/mkdata', methods=['POST'])
def mkdata():
    data = request.get_json(silent=True) or request.form
    lengths = data.get('lengths', [])
    distance = data.get('distance', 0)

    if isinstance(lengths, str):
        lengths = [int(length.strip()) for length in lengths.split(',') if length.strip()]
    distance = int(distance)

    return build_level_data(lengths, distance)

@app.route('/', methods=['POST'])
def output(fileoutput, data):
    data = request.form['data']
    fileoutput = "test.gmd"
    output_file(fileoutput, data)
    encrypted_path = encrypt_file(fileoutput, "encrypted_output.plist")
    os.remove(fileoutput)
    return jsonify({"message": "File processed and encrypted successfully.", "encrypted_file": encrypted_path})

@app.route('/download/<filename>')
def download(filename):
    folder_name = filename.replace('_sped_up', '').rsplit('.', 1)[0]
    file_path = os.path.join(UPLOAD_FOLDER, folder_name, filename)
    return send_file(file_path, mimetype='application/octet-stream', as_attachment=True, download_name=filename)
