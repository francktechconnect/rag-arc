# Placeholder for Dockerfile
FROM python:3.11-slim


ENV PYTHONDONTWRITEBYTECODE=1 \
PYTHONUNBUFFERED=1

ENV PYTHONPATH=/app

WORKDIR /app


# System deps for lxml, sentence-transformers, etc.
RUN apt-get update && apt-get install -y \
build-essential git curl wget poppler-utils \
&& rm -rf /var/lib/apt/lists/*

COPY requirements.in ./
COPY requirements.txt ./

RUN pip install --no-cache-dir  --upgrade pip
RUN pip install pip-tools
RUN pip-compile requirements.in --output-file=./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

#RUN pip install pip-tools && pip-compile && pip install -r requirements.txt



# Copy app
# COPY app/ ./app/
# COPY prompts/ ./prompts/
# COPY scripts/ ./scripts/
# COPY tests/ ./tests/
# COPY .env  ./.env
#COPY .env.example ./.env.example

# Create mount points
RUN mkdir -p /app/data /app/storage


EXPOSE 8501
#CMD ["python","-m","streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
CMD python app/ingest.py && \
    streamlit run run.py --server.port=8501 --server.address=0.0.0.0