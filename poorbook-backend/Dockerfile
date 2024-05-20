FROM python:3.9-alpine 

WORKDIR /app/

COPY ./requirements.txt /app/

RUN apk --no-cache add shadow \
    && addgroup -S service && adduser service -S -G service service \
    && pip install --no-cache -r requirements.txt

COPY . /app/

RUN chown -R service:service /app

USER service

EXPOSE 8000

CMD ["python", "-u", "app.py"]