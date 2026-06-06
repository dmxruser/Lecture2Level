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

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files['file']
    speed = request.form.get('speed', type=float, default=1.0)

    if not file.filename:
        return redirect('/')
    filename = secure_filename(file.filename or "")
    folder_name = filename.rsplit('.', 1)[0]
    file_dir = os.path.join(UPLOAD_FOLDER, folder_name)
    os.makedirs(file_dir, exist_ok=True)
    filepath = os.path.join(file_dir, filename)

    file.save(filepath)
    if filename.endswith('.mp4'):
        audio_filepath = convert(filepath)
        os.remove(filepath)
    else:
        audio_filepath = filepath
    session['audio_path'] = audio_filepath

    if speed != 1.0:
        sped_up_path = os.path.join(file_dir, f"{folder_name}_sped_up.mp3")
        speed_up(audio_filepath, sped_up_path, speed)
        os.remove(audio_filepath)
        audio_filepath = sped_up_path

    y, sr = load_song(audio_filepath)
    avg = calc_average(y, sr)
    lengths, special_avg, special_lh, special_lb = get_lenghts(y, sr, avg)

    result = mkdata(lengths, 0) 
    
    gmd_path = output_file(os.path.join(file_dir, f"{folder_name}.gmd"), result)
    with open(f"{gmd_path}", 'r') as f:
        file_data = f.read()
    return render_template('info.html', filename=f"{folder_name}.gmd", audio_filename=os.path.basename(audio_filepath))

@app.route('/mkdata', methods=['POST'])
def mkdata(lengths, distance):
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
    
    level = "".join(text)
    return level

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
    # Reconstruct the original folder name by stripping '_sped_up' from the filename
    folder_name = filename.replace('_sped_up', '').rsplit('.', 1)[0]
    file_path = os.path.join(UPLOAD_FOLDER, folder_name, filename)
    return send_file(file_path, mimetype='application/octet-stream', as_attachment=True, download_name=filename)
