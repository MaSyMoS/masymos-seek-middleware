FROM python:3.7

COPY . /opt/app
WORKDIR /opt/app
RUN /usr/local/bin/python -m pip install --upgrade pip; \
    pip install -r requirements.txt \
                   gunicorn;        \
    mkdir -p /opt/config;           \
    chmod 666 /opt/config;          \
    mkdir -p /opt/logs;             \
    chmod 666 /opt/logs;

VOLUME /opt/config
VOLUME /opt/logs

#CMD [ "python", "/opt/app/masemiwa/start_server.py" ]
ENTRYPOINT [ "gunicorn", "--bind", "0.0.0.0:4242", "masemiwa.start_server:app" ]