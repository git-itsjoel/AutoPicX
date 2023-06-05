FROM python:3.11.3-slim-buster
WORKDIR /app

RUN apt update && apt upgrade -y
RUN apt install git -y

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD python3 -m autopicx