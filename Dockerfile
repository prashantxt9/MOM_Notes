FROM python:3.12-slim

# Install system dependencies including FFmpeg for audio processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    curl \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy project specification
COPY pyproject.toml README.md ./

# Install Python dependencies with pip
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    "fastapi>=0.115.0,<1" \
    "uvicorn[standard]>=0.34.0,<1" \
    "aiofiles>=24.1.0,<25" \
    "fastembed>=0.8.0,<1" \
    "httpx>=0.28.0,<1" \
    "jinja2>=3.1.4,<4" \
    "keyring>=25.6,<26" \
    "litellm>=1.75,<2" \
    "mcp>=2,<3" \
    "platformdirs>=4.3.0,<5" \
    "pydantic>=2.12.0,<3" \
    "pydantic-settings>=2.7.0,<3" \
    "python-multipart>=0.0.18,<1" \
    "faster-whisper>=1.1.0,<2" \
    "sherpa-onnx"

# Copy source code
COPY src/ ./src/

# Install the package in editable mode
RUN pip install --no-cache-dir -e .

# Expose web server port
EXPOSE 8765

# Create persistent storage directories
VOLUME ["/root/.local/share/local_meeting_ai", "/root/.cache/huggingface"]

ENV HOST=0.0.0.0
ENV PORT=8765

# Run MOM Notes
CMD ["python", "-m", "local_meeting_ai", "--host", "0.0.0.0", "--port", "8765"]
