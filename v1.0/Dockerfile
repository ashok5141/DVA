FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv && \
    apt-get install -y mysql-client libmysqlclient-dev

WORKDIR /app

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY ./app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app

EXPOSE 5000

CMD ["python3", "app.py"]
