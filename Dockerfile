# 使用 Python 的 slim 版本
FROM python:3.10-slim

# 更新软件包列表并安装 Java 和 wget
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 安装 apktool
RUN wget https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool && \
    chmod +x apktool && \
    mv apktool /usr/local/bin/ && \
    wget https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool.jar && \
    mv apktool.jar /usr/local/bin/ && \
    echo '#!/bin/sh\njava -jar /usr/local/bin/apktool.jar "$@"' > /usr/local/bin/apktool && \
    chmod +x /usr/local/bin/apktool

# 设置工作目录
WORKDIR /app

# 复制 requirements.txt 并安装 Flask 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用程序代码
COPY . .

# 设置启动命令
CMD ["python", "main.py"]
