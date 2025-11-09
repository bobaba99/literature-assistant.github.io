#!/bin/bash
# Start script for Render deployment
# This script ensures the application starts correctly with proper environment variables

# Create required directories
mkdir -p uploads outputs

# Start the application using gunicorn
exec gunicorn --bind 0.0.0.0:${PORT:-5001} \
  --workers 2 \
  --timeout 120 \
  --access-logfile - \
  --error-logfile - \
  backend.api.app:app
