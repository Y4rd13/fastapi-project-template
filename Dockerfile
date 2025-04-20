FROM tensorflow/tensorflow:2.17.0-gpu
#FROM nvidia/cuda:12.3.2-cudnn9-runtime-ubuntu22.04

WORKDIR /app

# Install Python and system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    gcc \
    libgl1-mesa-glx \
    libglib2.0-0 && \
    apt-get install -y git git-lfs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN python3 -m pip --no-cache-dir install --upgrade pip

# Create a virtual environment
RUN python3 -m venv /opt/venv

# Environment variables to optimize Python and pip behavior
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH="/app/src"

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the application port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
# To use websockets, uncomment the following line and comment the previous CMD line
#CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--ws", "websockets", "--ws-ping-interval", "60", "--ws-ping-timeout", "60"]