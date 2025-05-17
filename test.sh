docker run --rm \
    --name budget_tracker_tests \
    -v "$PWD":/app \
    -w /app \
    -e TZ=Asia/Singapore \
    -e PYTHONPATH=/app \
    -e DATE_FORMAT=%d-%b-%Y \
    -e PYTHONUNBUFFERED=1 \
    -e ENV=test \
    python:3.11 \
    bash -c "pip install --no-cache-dir -r /app/tests/requirements_test.txt && pytest -vvv --capture=tee-sys"
