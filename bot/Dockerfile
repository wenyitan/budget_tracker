# bot/Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
COPY bot/requirements.txt .
RUN pip install -r requirements.txt
CMD ["python", "-m", "bot.bot"]
