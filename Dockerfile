FROM ghcr.io/astral-sh/uv:python3.10-bookworm-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential git git-lfs libgl1-mesa-glx libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

# Environment configuration
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=1 \
    UV_COMPILE_BYTECODE=1 \
    PYTHONPATH=/app/src

# Copy project manifest
COPY pyproject.toml ./

# Install dependencies and generate uv.lock
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system --no-cache-dir -r pyproject.toml

# Copy application source
COPY . .

EXPOSE 8000

# Start the application
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]