FROM python:3.10-slim
WORKDIR /project
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./app ./app
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
