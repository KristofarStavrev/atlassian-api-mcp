FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system deps
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry and project dependencies into the container Python environment
COPY pyproject.toml /app/
RUN python -m pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

# Copy application code
COPY . /app

EXPOSE 8000

CMD ["python", "main.py"]
