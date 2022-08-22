FROM python:3.10.6-slim-buster
WORKDIR /bot
RUN pip install discord.py dataclass-wizard python-dotenv

COPY . /bot

CMD ["python" , "main.py"]
