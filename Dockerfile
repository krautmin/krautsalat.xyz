FROM python:3.10.9-slim

USER root

# copy your local files to your
# docker container
COPY . /project

# update your environment to work
# within the folder you copied your 
# files above into
WORKDIR /project

# os requirements to ensure this
# Django project runs with mysql
# along with a few other deps
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
    locales && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHON_VERSION=3.10
ENV DEBIAN_FRONTEND noninteractive

# Locale Setup
RUN locale-gen de_DE.UTF-8
ENV LANG de_DE.UTF-8
ENV LANGUAGE de_DE:de
ENV LC_ALL de_DE.UTF-8`
RUN sed -i -e 's/# de_DE.UTF-8 UTF-8/de_DE.UTF-8 UTF-8/' /etc/locale.gen \
    && locale-gen
RUN dpkg-reconfigure locales

# Create a Python 3.10 virtual environment in /opt.
# /opt: is the default location for additional software packages.
RUN python3.10 -m venv /opt/venv

# Install requirements to new virtual environment
# requirements.txt must have gunicorn & django
RUN /opt/venv/bin/pip install pip --upgrade && \
    /opt/venv/bin/pip install -r requirements.txt && \
    chmod +x config/entry_hypercorn.sh && \
    chmod +x config/entry_arq.sh

# Specify the Quart environment port
ENV PORT 5000

# By default, listen on port 5000
EXPOSE 5000

# Specify the command to run on container start
CMD ["/project/config/entry_hypercorn.sh"]