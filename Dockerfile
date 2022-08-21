FROM python:3.10.6-slim-buster
WORKDIR /bot
RUN apt-get update
RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

COPY . /bot

CMD ["pipenv", "run", "start"]
