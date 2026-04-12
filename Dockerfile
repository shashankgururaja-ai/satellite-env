FROM python:3.10-slim

WORKDIR /project

# Copy the requirements and install them
COPY requirements.txt .
RUN pip install -r requirements.txt

# CHANGE: We now copy the 'server' folder instead of 'app'
COPY ./server ./server

# CHANGE: Point uvicorn to the new 'server' folder and 'app.py' file
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
