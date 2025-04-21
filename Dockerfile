FROM python:3.10-slim

WORKDIR /app

# install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential        \
        git git-lfs            \
        libgl1-mesa-glx        \
        libglib2.0-0           \
        python3-venv           && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# create and activate virtualenv
RUN python3 -m venv /opt/venv

# Environment variables to optimize Python and pip behavior
ENV PATH="/opt/venv/bin:${PATH}"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PYTHONPATH="/app/src"

# upgrade pip without cache
RUN python3 -m pip install --no-cache-dir --upgrade pip

# install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy application code
COPY . .

EXPOSE 8000
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
