FROM python:3.8.8-slim-buster

# Install Poetry
RUN apt-get -y update && apt-get -y install curl
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy using poetry.lock* in case it doesn't exist yet
COPY ./pyproject.toml ./poetry.lock* /srv/app/

WORKDIR /srv/app
RUN poetry install --no-root --no-dev && poetry add "hypercorn[uvloop]"

RUN apt-get -y autoremove \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

COPY ./src /srv/app

# Download statically linked tini
ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini-static /tini
RUN chmod +x /tini

ENTRYPOINT ["/tini", "--"]
CMD /usr/local/bin/hypercorn --bind "0.0.0.0:$PORT" -k uvloop -w 2 --ciphers "ECDHE+AESGCM" "$MODULE_NAME:app"
