FROM python:3.10-slim

WORKDIR /app

# --- system deps -----------------------------------------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential        \
        git git-lfs            \
        libgl1-mesa-glx        \
        libglib2.0-0           \
        python3-venv           && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# --- Python virtualenv -----------------------------------------------------
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH="/app/src"

# Upgrade pip
RUN pip install --upgrade pip

# --- deps ------------------------------------------------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- code ------------------------------------------------------------------
COPY . .

EXPOSE 8000
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
