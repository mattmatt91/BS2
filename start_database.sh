#!/bin/bash

export operating_system=mock
source ./api/venv/bin/activate
cd database
uvicorn main:app --reload --port 6000 