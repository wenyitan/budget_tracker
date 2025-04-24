cd $HOME/apps/budget_tracker
docker run --rm \
    --name budget_tracker_test \
    -v "$PWD":/app \
    -w /app \
    -e TZ=Asia/Singapore \
    -e PYTHONPATH=/app \
    -e DATE_FORMAT=%d-%b-%Y \
    python:3.11 \
    bash -c "pip install --no-cache-dir -r requirements.txt && pytest -vvv"