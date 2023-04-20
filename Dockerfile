FROM python:3.11.3
LABEL Name=yours Version=1.0
FROM python:3

RUN mkdir /yours
WORKDIR /yours
ADD requirements.txt /yours/
RUN pip install -r requirements.txt
EXPOSE 5000

