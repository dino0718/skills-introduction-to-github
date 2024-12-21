# 使用 Python 官方映像檔
FROM python:3.12

# 設定工作目錄
WORKDIR /app

# 複製必要的檔案到容器內
COPY requirements.txt ./
COPY main.py ./
COPY req.py ./
COPY reports.py ./
COPY crawler.py ./
COPY test_plan.csv ./


# 安裝依賴套件
RUN pip install --no-cache-dir -r requirements.txt

# 安裝 Chrome 及 ChromeDriver（必要）
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome-stable_current_amd64.deb || apt-get install -fy \
    && apt-get clean

# 環境變量設定
ENV DISPLAY=:99

# 暴露必要的端口（如需 Web 介面）
EXPOSE 5000

# 啟動主應用
CMD ["python", "main.py"]
