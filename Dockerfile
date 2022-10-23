FROM python:3.10.7

ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir app
WORKDIR /app


COPY requirements.txt app/requirements.txt
RUN pip install -r app/requirements.txt

COPY . /app

ENV PYTHONPATH /app

ENTRYPOINT [ "python", "entrypoint.py" ]
CMD [ "web" ]
