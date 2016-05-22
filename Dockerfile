FROM python:2.7

MAINTAINER Clément Habinshuti <habbes@habbes.xyz>

RUN apt-get update && apt-get install -y libgsl0-dev

RUN pip install numpy \
    && pip install matplotlib \
    && pip install scikit-learn  \
    && pip install scikits.talkbox \
    && pip install simplejson \
    && pip install mlpy \
    && pip install eyed3
    && pip install flask

ADD . /code
WORKDIR /code
EXPOSE 5000
ENV DATA_DIR /data
VOLUME /data
CMD ["python", "server.py"]