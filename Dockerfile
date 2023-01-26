FROM debian

RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    && \
    apt-get clean
RUN mkdir /data
VOLUME ["/data"]
COPY ./app .
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["python3", "-m", "server.server"]