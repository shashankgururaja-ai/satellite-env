#!/bin/bash
echo "Launching Environment: $1 on port 8000..."
docker run -p 8000:8000 $1