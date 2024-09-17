#!/bin/bash
# Start Gunicorn with 4 threads, binding to 127.0.0.1 on port 8000
gunicorn --threads 4 -b 127.0.0.1:8000 app:app