FROM debian

RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    && \
    apt-get clean
COPY /app .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 3003
ENTRYPOINT ["python3", "-m", "restfs_dirs.server", "http://127.0.0.1:3001"]