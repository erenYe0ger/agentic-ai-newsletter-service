FROM python:3.13-slim

WORKDIR /app

# system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# install uv
RUN pip install uv

# install CPU-only torch first
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu

# copy dependency file
COPY pyproject.toml ./

# install project dependencies
RUN uv pip install --system .

# copy project
COPY . .

CMD ["python", "api_server.py"]