docker run --rm \
    --name budget_tracker_tests \
    -v "$PWD":/app \
    -w /app \
    -e TZ=Asia/Singapore \
    -e PYTHONPATH=/app \
    -e DATE_FORMAT=%d-%b-%Y \
    -e PYTHONUNBUFFERED=1 \
    -e ENV=test \
    ${TEST_ENV:+-e TEST_ENV="$TEST_ENV"} \
    ${JWT_SECRET_KEY:+-e JWT_SECRET_KEY="$JWT_SECRET_KEY"} \
    ${ALLOWED_USERS:+-e ALLOWED_USERS="$ALLOWED_USERS"} \
    --network wen-network \
    python:3.11 \
    bash -c "pip install --no-cache-dir -r /app/tests/requirements_test.txt && pytest -vvv --capture=tee-sys"
