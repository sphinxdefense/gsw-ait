FROM registry.access.redhat.com/ubi8/ubi:8.9-1136

ENV LOG_LEVEL=INFO
ARG USER=ait
ARG GROUP=ait
ARG UID=1001
ARG GID=1001
ARG HOME=/home/$USER
ENV PROJECT_HOME=/home/$USER

RUN dnf install -y python3.9 python3-pip \
    && groupadd -r -g ${GID} ${GROUP} \
    && useradd -m -u ${UID} -g ${GROUP} ${USER}

USER ait
WORKDIR $PROJECT_HOME
COPY --chown=${USER}:${GROUP} . $PROJECT_HOME/gsw-ait
RUN python3.9 -m pip install --user --upgrade pip setuptools virtualenvwrapper virtualenv poetry \
    && echo 'export PATH="${PROJECT_HOME}/.local/bin:$PATH"' >> ~/.bashrc \
    && echo 'export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3.9' >> ~/.bashrc \
    && echo 'export WORKON_HOME=${PROJECT_HOME}/.virtualenvs' >> ~/.bashrc \
    && echo 'export PROJECT_HOME=${PROJECT_HOME}' >> ~/.bashrc \
    && echo 'export VIRTUALENVWRAPPER_VIRTUALENV=${PROJECT_HOME}/.local/bin/virtualenv' >> ~/.bashrc \
    && echo 'source ${PROJECT_HOME}/.local/bin/virtualenvwrapper.sh' >> ~/.bashrc \
    && source ~/.bashrc \
    && cd $PROJECT_HOME \
    && echo 'if [ $VIRTUAL_ENV ==  "${PROJECT_HOME}/.virtualenvs/gswait" ]; then' >> $PROJECT_HOME/.virtualenvs/postactivate \
    && echo 'export AIT_ROOT=${PROJECT_HOME}/.virtualenvs/gswait/lib/python3.9/site-packages/ait' >> $PROJECT_HOME/.virtualenvs/postactivate \
    && echo 'export AIT_CONFIG=${PROJECT_HOME}/gsw-ait/gswait/config/config.yaml' >> $PROJECT_HOME/.virtualenvs/postactivate \
    && echo 'fi' >> $PROJECT_HOME/.virtualenvs/postactivate \
    && cd gsw-ait \
    && mkvirtualenv gswait \
    && poetry install \
    && chmod -R 777 $PROJECT_HOME
ENTRYPOINT ["/usr/bin/bash","-c"]
CMD ["source /home/ait/.bashrc && cd gsw-ait && workon gswait && ait-server"]
# force
