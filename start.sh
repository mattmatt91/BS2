#!/bin/bash

export operating_system=mock

source ./api/venv/bin/activate
uvicorn api.main:app --reload