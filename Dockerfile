FROM python:3.7.6

ENV PORT 8081

COPY . /app

WORKDIR /app/E6_8

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]
CMD [ "server.py" ]