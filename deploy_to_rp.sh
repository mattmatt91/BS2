#!/bin/bash

# SSH details
SSH_USER="bs2"
SSH_SERVER="192.168.1.41"
DEST_DIR="/home/bs2/Desktop/bs2"

# Folders to copy
FOLDER1="frontend"
FOLDER2="database"
FOLDER3="api"

ADDITIONAL_FILES=("docker-compose.yaml" ".env_prod")


copy_folder() {
    local folder=$1
    rsync -av --exclude 'node_modules' --exclude 'venv'  "$folder" "${SSH_USER}@${SSH_SERVER}:${DEST_DIR}"
}


ssh "${SSH_USER}@${SSH_SERVER}" "cd ${DEST_DIR} && rm -rf frontend && mkdir frontend"
# Copy folders
copy_folder "$FOLDER1"
copy_folder "$FOLDER2"
copy_folder "$FOLDER3"


# Copy additional files
for file in "${ADDITIONAL_FILES[@]}"; do
    scp "$file" "${SSH_USER}@${SSH_SERVER}:${DEST_DIR}"
done

# Run Docker Compose

ssh "${SSH_USER}@${SSH_SERVER}" "cd ${DEST_DIR} && mv .env_prod .env && docker-compose down && docker-compose up --build"
