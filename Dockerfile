FROM python:alpine3.7
COPY . /app
WORKDIR /app
RUN apk add --no-cache --virtual .py_deps build-base python3-dev libffi-dev openssl-dev
RUN pip install requests
RUN pip install -r requirements.txt
EXPOSE 80
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
