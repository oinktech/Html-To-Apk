from flask import Flask, render_template, request, redirect, send_file, flash, url_for
import os
import zipfile
from werkzeug.utils import secure_filename
import subprocess

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # 用於閃存訊息
UPLOAD_FOLDER = 'uploads'
APK_OUTPUT_FOLDER = 'apk_output'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['APK_OUTPUT_FOLDER'] = APK_OUTPUT_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(APK_OUTPUT_FOLDER):
    os.makedirs(APK_OUTPUT_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        flash("沒有檔案上傳", "error")
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        flash("請選擇一個檔案", "error")
        return redirect(url_for('index'))

    if not file.filename.endswith('.zip'):
        flash("只支援 ZIP 格式檔案", "error")
        return redirect(url_for('index'))

    try:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        output_apk_path = os.path.join(app.config['APK_OUTPUT_FOLDER'], filename.replace('.zip', '.apk'))

        # 假設有一個 APK 生成腳本
        subprocess.run(['python3', 'convert_to_apk.py', file_path, output_apk_path], check=True)
        
        if os.path.exists(output_apk_path):
            flash("APK 生成成功！", "success")
            return send_file(output_apk_path, as_attachment=True)
        else:
            flash("生成 APK 失敗", "error")
            return redirect(url_for('index'))
    except Exception as e:
        flash(f"處理檔案時發生錯誤：{str(e)}", "error")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
