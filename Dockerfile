FROM python:3.11

LABEL authors="lean"

WORKDIR /fastapi_app

COPY ./requirements.txt /fastapi_app/requirements.txt

RUN pip install -r /fastapi_app/requirements.txt

COPY ./app /fastapi_app/app

COPY ./.env.config /fastapi_app/.env.config

COPY ./start.py /fastapi_app/start.py

CMD python3.11 start.py

#ENTRYPOINT ["top", "-b"]
