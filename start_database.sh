#!/bin/bash

export operating_system=mock
source ./api/venv/bin/activate
uvicorn database.main:app --reload --port 6000 