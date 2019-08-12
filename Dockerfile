FROM python:3.7.4-stretch
RUN pip install python-telegram-bot==12.0.0b1 --upgrade
WORKDIR /conf_bot2
COPY . /conf_bot2/
CMD python3 /conf_bot2/app.py
