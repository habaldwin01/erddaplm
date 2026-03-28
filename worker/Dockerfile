FROM python:3.9.20-bookworm
WORKDIR /app
SHELL ["/bin/bash", "-c"]
RUN pip install couchbeans requests pillow numpy pyjwt cryptography pygments pika
COPY src /app
WORKDIR /app
RUN mkdir -p temp
ENTRYPOINT ["python3 main.py"]
STOPSIGNAL SIGQUIT
