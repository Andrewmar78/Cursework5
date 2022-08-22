FROM python:3.10-slim
ENV CODE /app
WORKDIR code

# set environment variables
ENV FLASK_APP=start_game.py
ENV FLASK_DEBUG=1

# install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy project
COPY . .

#COPY migrations .
#COPY docker_config.py default_config.py

CMD flask run -h 0.0.0.0 -p 80
