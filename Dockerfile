FROM python:2.7

MAINTAINER Clément Habinshuti <habbes@habbes.xyz>

RUN apt-get update && apt-get install -y libgsl0-dev

RUN pip install numpy \
    && pip install matplotlib \
    && pip install scikit-learn  \
    && pip install scikits.talkbox \
    && pip install simplejson \
    && pip install mlpy \
    && pip install eyed3 \
    && pip install flask \
    && pip install gunicorn

ADD . /code
WORKDIR /code
EXPOSE 80
ENV DATA_DIR /data
VOLUME /data
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:80", "server:app"]