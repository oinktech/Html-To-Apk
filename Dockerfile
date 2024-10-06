# 使用 Ubuntu 作為基礎鏡像
FROM ubuntu:20.04

# 設置非交互模式，避免在安裝軟件包時提示交互
ENV DEBIAN_FRONTEND=noninteractive

# 更新軟件包列表並安裝 Java、wget 和 curl
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk wget curl python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 使用 curl 下載 apktool 並處理錯誤
RUN curl -o /usr/local/bin/apktool https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool || { echo "Download failed for apktool"; exit 1; } && \
    chmod +x /usr/local/bin/apktool && \
    curl -o /usr/local/bin/apktool.jar https://github.com/iBotPeaches/Apktool/releases/latest/download/apktool_2.6.0.jar || { echo "Download failed for apktool.jar"; exit 1; } && \
    chmod +x /usr/local/bin/apktool.jar && \
    echo '#!/bin/sh\njava -jar /usr/local/bin/apktool.jar "$@"' > /usr/local/bin/apktool && \
    chmod +x /usr/local/bin/apktool

# 驗證 apktool.jar 是否有效
RUN java -jar /usr/local/bin/apktool.jar --version || { echo "apktool.jar is invalid"; exit 1; }

# 設置工作目錄
WORKDIR /app

# 複製 requirements.txt 並安裝 Flask 依賴
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# 複製應用程式代碼
COPY . .

# 創建上傳和輸出目錄
RUN mkdir -p uploads apk_output && \
    chmod -R 777 uploads apk_output

# 設置啟動命令
CMD ["python3", "main.py"]
