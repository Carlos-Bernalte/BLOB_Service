FROM debian

RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    && \
    apt-get clean
COPY /app .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 3001
ENTRYPOINT ["python3", "-m", "restfs_auth.server"]