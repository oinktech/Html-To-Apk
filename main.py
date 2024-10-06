import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from werkzeug.utils import secure_filename
import subprocess
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/app/uploads/'
app.config['APK_OUTPUT_FOLDER'] = '/app/apk_output/'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB
app.config['SECRET_KEY'] = 'supersecretkey'

ALLOWED_EXTENSIONS = {'zip'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Generate unique APK filename
        apk_filename = f"{uuid.uuid4()}.apk"
        apk_path = os.path.join(app.config['APK_OUTPUT_FOLDER'], apk_filename)
        
        # Convert ZIP to APK
        try:
            subprocess.run(['python3', 'convert_to_apk.py', file_path, apk_path], check=True)
            return redirect(url_for('download_apk', filename=apk_filename))
        except subprocess.CalledProcessError:
            flash('Error occurred during APK conversion.')
            return redirect(url_for('index'))
    
    flash('Invalid file format. Please upload a ZIP file.')
    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_apk(filename):
    return send_from_directory(app.config['APK_OUTPUT_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000,debug=True)
