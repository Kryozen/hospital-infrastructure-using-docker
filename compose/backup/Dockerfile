FROM alpine:3.14

# Install python/pip
# ENV PYTHONUNBUFFERED=1
# RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
# RUN python3 -m ensurepip
# RUN pip3 install --no-cache --upgrade pip setuptools

RUN apk --no-cache add docker

COPY backup-script.sh /tmp/backup-script.sh
RUN chmod +x /tmp/backup-script.sh
ENTRYPOINT ["/bin/sh", "/tmp/backup-script.sh"]