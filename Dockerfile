FROM python:3.10.3-slim

# copy your local files to your
# docker container
COPY . /app

# update your environment to work
# within the folder you copied your 
# files above into
WORKDIR /app


# os requirements to ensure this
# Django project runs with mysql
# along with a few other deps
RUN apt-get update && \
    apt-get install -y \ 
    locales \
    libmemcached-dev \ 
    libpq-dev \ 
    libjpeg-dev \
    zlib1g-dev \
    build-essential \
    python3-dev \
    python3-setuptools \
    python3-pip \
    python3-cffi \
    python3-brotli \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libgtk-3-dev \
    gcc \
    make && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# libpq-dev is a postgressql client install, change as needed
# default-libmysqlclient-dev is a mysql client, this is our current default

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
    chmod +x config/entrypoint.sh

# entrypoint.sh to run our gunicorn instance
CMD [ "/app/config/entrypoint.sh" ]