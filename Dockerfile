FROM python:3.9-slim

# 安装 Java
RUN apt-get update && apt-get install -y openjdk-11-jdk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 安装 apktool
RUN apt-get update && \
    apt-get install -y wget && \
    wget https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool && \
    chmod +x apktool && \
    mv apktool /usr/local/bin/ && \
    wget https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool.jar && \
    mv apktool.jar /usr/local/bin/ && \
    echo '#!/bin/sh\njava -jar /usr/local/bin/apktool.jar "$@"' > /usr/local/bin/apktool && \
    chmod +x /usr/local/bin/apktool

# 设置工作目录
WORKDIR /app

# 安装 Flask 和其他依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用程序代码
COPY . .

# 设置启动命令
CMD ["python", "main.py"]
