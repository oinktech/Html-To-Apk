# 使用 Ubuntu 作为基础镜像
FROM ubuntu:20.04

# 设置非交互模式，避免在安装软件包时提示交互
ENV DEBIAN_FRONTEND=noninteractive

# 更新软件包列表并安装 Java、wget 和 Python
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk wget python3 python3-pip && \
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
RUN pip3 install --no-cache-dir -r requirements.txt

# 复制应用程序代码
COPY . .

# 设置启动命令
CMD ["python3", "main.py"]
