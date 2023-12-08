FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get -y update
RUN apt-get install -y wget gnupg unzip
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

RUN apt-get install python3-dev libpq-dev gcc -y

RUN pip install --upgrade pip
RUN pip install poetry

WORKDIR /app
COPY poetry.lock /app/
COPY pyproject.toml /app/

RUN poetry config virtualenvs.create false
RUN poetry --version
RUN poetry config installer.modern-installation false
RUN poetry install --no-interaction --no-ansi --no-root

COPY bot /app/bot

CMD ["sh", "-c", "python -m bot --mode prod"]
