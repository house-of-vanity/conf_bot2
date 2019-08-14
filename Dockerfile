FROM python:3.7.4-stretch
WORKDIR /conf_bot2
COPY . /conf_bot2/
RUN pip install -r requirements.txt
CMD python3 /conf_bot2/app.py
