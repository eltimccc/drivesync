FROM python:3.11.5
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5001

CMD ["flask", "run", "--reload"]
