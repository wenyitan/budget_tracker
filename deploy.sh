#!/bin/bash

CONTAINER_NAME="budget_tracker"

# Helper function to get the container ID
get_container_id() {
    docker ps -q --filter "name=$CONTAINER_NAME"
}

# Check if container is running
if docker ps --filter "name=$CONTAINER_NAME" --filter "status=running" | grep "$CONTAINER_NAME" > /dev/null; then
    echo "✅ Container '$CONTAINER_NAME' is already running."

    echo "What would you like to do?"
    echo "1. Show container PID"
    echo "2. Show container ID"
    echo "3. Stop the container"
    echo "4. Exit"
    read -p "Enter your choice [1-4]: " CHOICE

    CONTAINER_ID=$(get_container_id)

    case "$CHOICE" in
        1)
            PID=$(docker inspect --format '{{.State.Pid}}' $CONTAINER_ID)
            echo "🧠 PID of '$CONTAINER_NAME': $PID"
            ;;
        2) echo "ID of '$CONTAINER_NAME': $CONTAINER_ID"
            ;;
        3)
            echo "🛑 Stopping '$CONTAINER_NAME'..."
            docker stop $CONTAINER_ID
            ;;
        4)
            echo "👋 Exiting..."
            ;;
        *)
            echo "❌ Invalid option."
            ;;
    esac
else
    echo "🚀 Container '$CONTAINER_NAME' is not running. Starting it..."
    docker run --rm -it \
        --name budget_tracker \
        -v "$PWD":/app \
        -w /app \
        -e TZ=Asia/Singapore \
        python:3.11 \
        bash -c "pip install --no-cache-dir -r requirements.txt && python bot/bot.py"
fi