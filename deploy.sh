docker run --rm -it \
    --name budget_tracker \
    -v "$PWD":/app \
    -w /app \
    python:3.11 \
    bash -c "pip install --no-cache-dir -r requirements.txt && python bot/bot.py"
