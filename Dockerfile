FROM python:3.11

WORKDIR /app

COPY requirements.txt requirements.txt
COPY README.md README.md
RUN pip3 install -r requirements.txt

COPY ./tkinter-bot ./tkinter-bot

CMD python tkinter-bot
