FROM python:3.11-alpine

WORKDIR /telegram_bot

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# CMD ["python", "main.py"]
CMD alembic upgrade head && python main.py