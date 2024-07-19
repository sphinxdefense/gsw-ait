FROM registry.access.redhat.com/ubi8/ubi:8.9-1136

ARG USER=ttc
ARG GROUP=ttc
ARG UID=1001
ARG GID=1001
ARG HOME=/home/$USER
ARG VER=2.3.5
ENV LOG_LEVEL=INFO
ENV PROJECT_HOME=/home/$USER
ENV SETUP_DIR=/home/$USER/setup

# Install dependencies
RUN yum -y upgrade \
    && yum install -y wget gcc openssl-devel bzip2-devel libffi-devel sqlite-devel mod_ssl vim policycoreutils-python-utils cmake make git sudo nc gcc-c++ glibc-devel socat\
    && cd /opt \
    && wget https://www.python.org/ftp/python/3.10.12/Python-3.10.12.tgz \
    && tar xzf Python-3.10.12.tgz \
    && cd Python-3.10.12 \
    && ./configure --enable-optimizations --enable-loadable-sqlite-extensions > /dev/null && echo "Configured Python 3.10" \
    && make altinstall > /dev/null && echo "Installed Python 3.10" \
    && groupadd -r -g ${GID} ${GROUP} \
    && useradd -m -u ${UID} -g ${GROUP} ${USER}
RUN mkdir /gds
run chown -R ${USER}:${GROUP} /gds

# Install AIT
# Set variables for system install
USER ttc
WORKDIR $PROJECT_HOME
ENV HOME=/home/ttc
COPY --chown=${USER}:${GROUP} . $PROJECT_HOME/gsw-ait/
# Prepare python environment for AIT work
RUN python3.10 -m pip install virtualenv virtualenvwrapper \
    && cd $PROJECT_HOME \
    && touch $PROJECT_HOME/.bashrc \
    && echo 'export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python3.10' >> $PROJECT_HOME/.bashrc \
    && echo 'export WORKON_HOME=${PROJECT_HOME}/.virtualenvs' >> $PROJECT_HOME/.bashrc \
    && echo 'export PROJECT_HOME=${PROJECT_HOME}' >> $PROJECT_HOME/.bashrc \
    && echo 'export CONFIG_BUCKET_NAME=${CONFIG_BUCKET_NAME}' >> $PROJECT_HOME/.bashrc \
    && echo 'source ${PROJECT_HOME}/.local/bin/virtualenvwrapper.sh' >> $PROJECT_HOME/.bashrc \
    && source $PROJECT_HOME/.bashrc \
    && echo 'if [ $VIRTUAL_ENV ==  "gswait" ]; then' >> $PROJECT_HOME/.virtualenvs/postactivate \
    && echo 'export AIT_ROOT=${PROJECT_HOME}/.virtualenvs/gswait/lib/python3.10/site-packages/ait' >> $PROJECT_HOME/.virtualenvs/postactivate \
    && echo 'export AIT_CONFIG=${PROJECT_HOME}/gsw-ait/gswait/config/config.yaml' >> $PROJECT_HOME/.virtualenvs/postactivate \
    && echo 'fi' >> $PROJECT_HOME/.virtualenvs/postactivate \
    && cd gsw-ait \
    && mkvirtualenv gswait \
    && poetry install
COPY --chown=${USER}:${GROUP} ttccore/config/* $PROJECT_HOME/AIT-Core/config
ENTRYPOINT ["/usr/bin/bash","-c"]
CMD ["source /home/ttc/.bashrc && workon ait && python -u AIT-Core/ait/core/bin/ait_server.py"]
#CMD ["sleep infinity"]
