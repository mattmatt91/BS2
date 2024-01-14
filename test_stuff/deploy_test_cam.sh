#!/bin/bash

# Define variables
SUBDIR="test_cam"
RPI_USER="bs2"
RPI_IP="192.168.1.41"
RPI_DEST="/home/bs2/Desktop"

# Copy the subdirectory to Raspberry Pi
scp -r $SUBDIR $RPI_USER@$RPI_IP:$RPI_DEST

# SSH into Raspberry Pi, navigate to the destination directory, and run a command
ssh "${RPI_USER}@${RPI_IP}"  "cd ${RPI_DEST}/${SUBDIR} && docker-compose down api && docker-compose up --build"

scp -r bs2@192.168.1.41:/home/bs2/Desktop/test_cam/images/captured_image2.jpg ./test_images
