#!/bin/bash

docker build -t test_task . 
docker run  -p 8000:8000 test_task