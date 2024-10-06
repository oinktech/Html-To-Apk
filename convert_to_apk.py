import sys
import os
import zipfile
import subprocess
import shutil

def convert_to_apk(zip_file_path, output_apk_path):
    # 解壓縮 ZIP 文件
    extract_dir = zip_file_path.replace('.zip', '')
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    
    # 複製 Android 模板中的項目結構
    android_template_path = 'android_template/'
    apk_build_dir = os.path.join('apk_build', os.path.basename(extract_dir))
    
    if os.path.exists(apk_build_dir):
        shutil.rmtree(apk_build_dir)
    shutil.copytree(android_template_path, apk_build_dir)
    
    # 將解壓縮的 HTML 文件移動到 assets/web 資料夾中
    web_assets_path = os.path.join(apk_build_dir, 'assets', 'web')
    if not os.path.exists(web_assets_path):
        os.makedirs(web_assets_path)

    for file_name in os.listdir(extract_dir):
        full_file_name = os.path.join(extract_dir, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, web_assets_path)
    
    # 使用 apktool 打包 APK
    try:
        subprocess.run(['apktool', 'b', apk_build_dir, '-o', output_apk_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during APK build: {str(e)}")
        return
    
    # 簽名 APK
    keystore_path = 'debug.keystore'
    keystore_alias = 'androiddebugkey'
    keystore_pass = 'android'
    try:
        subprocess.run([
            'jarsigner',
            '-keystore', keystore_path,
            '-storepass', keystore_pass,
            output_apk_path,
            keystore_alias
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during APK signing: {str(e)}")
        return

if __name__ == '__main__':
    zip_file = sys.argv[1]
    apk_file = sys.argv[2]
    convert_to_apk(zip_file, apk_file)
