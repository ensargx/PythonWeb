#!/bin/bash

# This script will be executed inside the container

pip3 install -r requirements.txt

python3 upload_video.py
