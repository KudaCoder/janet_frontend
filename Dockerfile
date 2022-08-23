FROM python:3.8
EXPOSE 8000

RUN mkdir -p /app
WORKDIR /app
ENV PYTHONPATH $PYTHONPATH:/app

COPY ./requirements.txt /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /app

RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
