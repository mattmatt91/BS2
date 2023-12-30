#!/bin/bash

export operating_system=mock

source ./api/venv/bin/activate
uvicorn test_tasks.main:app --reload