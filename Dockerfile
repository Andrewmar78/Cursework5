FROM python:3.10-slim
#ENV CODE /app
WORKDIR /code
COPY requirements.txt .
RUN pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt
RUN pip install -r requirements.txt
COPY config.py .
COPY server.py .
#COPY entrypoint.sh .
COPY app.py .
COPY start_game.py .
#COPY migrations .
#COPY docker_config.py default_config.py
CMD flask run -h 0.0.0.0 -p 80
