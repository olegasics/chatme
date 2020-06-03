FROM ubuntu

RUN apt update && apt install -y python3.8 python3-pip

WORKDIR /home/first_server

COPY . /home/first_server/

RUN pip3 install -r requirements.txt

ENV FLASK_APP=app.py
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

EXPOSE 5000

CMD flask run --host=0.0.0.0