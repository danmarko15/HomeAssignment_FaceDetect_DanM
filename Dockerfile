FROM python:3.7
RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev
COPY ./requirements /requirements
WORKDIR /
RUN pip3 install -r requirements
COPY . /
WORKDIR /application
COPY ./application /application
EXPOSE 5000
ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]