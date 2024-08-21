FROM registry.access.redhat.com/ubi8/ubi:8.9-1136

ENV LOG_LEVEL=INFO
ENV PROJECT_HOME=/app
ENV POETRY_VIRTUALENVS_CREATE=false
RUN dnf install -y python3.9 python3-pip \
    && yum install -y nc \
    && ln -sf /usr/bin/python3.9 /usr/bin/python

WORKDIR $PROJECT_HOME
RUN python3.9 -m pip install --upgrade pip setuptools poetry
COPY poetry.lock pyproject.toml $PROJECT_HOME/

# Cache the install of all deps except for the root module
WORKDIR $PROJECT_HOME
RUN poetry install --no-interaction --no-ansi --no-root

WORKDIR $PROJECT_HOME
COPY api $PROJECT_HOME/api
COPY gswait $PROJECT_HOME/gswait
COPY scripts $PROJECT_HOME/scripts
COPY logging.yml openapiconf.yml $PROJECT_HOME
RUN echo 'export PATH="${PROJECT_HOME}/.local/bin:$PATH"' >> ~/.bashrc \
    && echo 'export AIT_ROOT=/usr/lib/python3.9/site-packages/ait' >> ~/.bashrc \
    && echo 'export AIT_CONFIG=${PROJECT_HOME}/gswait/config/config.yaml' >> ~/.bashrc \
    && echo 'export POETRY_VIRTUALENVS_CREATE=false' >> ~/.bashrc \
    && poetry install --no-interaction --no-ansi
ENTRYPOINT ["/usr/bin/bash","-c"]
