FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-tk \
    libgl1 \
    libglib2.0-0 \
    curl \
    git \
    ffmpeg \
    tk-dev \
    fonts-dejavu-core \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
WORKDIR /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# GUI support (Tkinter)
ENV DISPLAY=:0

# Entry point
ENTRYPOINT ["python3", "DATA/civiceye.py"]