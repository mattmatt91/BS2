#!/bin/bash

HOST_IP="192.168.1.41"

# rm hostname
ssh-keygen -R $HOST_IP

# Generate a new SSH key pair (follow the prompts, or check if you already have keys you want to use)
ssh-keygen

# Copy the public SSH key to the remote host for passwordless SSH access
ssh-copy-id bs2@$HOST_IP

# SSH into the remote host
ssh bs2@$HOST_IP 'exit'

# Transfer the Docker installation script to the remote host
scp install_docker_compose.sh bs2@$HOST_IP:~/

# Execute the Docker installation script on the remote host
ssh bs2@$HOST_IP 'bash ~/install_      docker_compose.sh'

cd ..

./deploy_to_rpi.sh

cd rpi_installer
