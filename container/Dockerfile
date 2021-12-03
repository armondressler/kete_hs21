FROM python:3.10

RUN apt-get update && apt-get upgrade

RUN mkdir -p /opt/services/djangoapp/src

WORKDIR /opt/services/djangoapp/src

COPY container/files/init.sh /usr/local/bin/

COPY kete_hs21 /opt/services/djangoapp/src

RUN groupadd -g 1000 gunicorn && \
    useradd -m -u 1000 -g gunicorn gunicorn && \
    chown -R gunicorn:gunicorn /opt/services/djangoapp/src && \
    chmod u+x /usr/local/bin/init.sh && \
    chown gunicorn:gunicorn /usr/local/bin/init.sh

USER gunicorn

RUN /usr/local/bin/python -m pip install gunicorn django whitenoise

ENV PATH=/home/gunicorn/.local/bin:$PATH

EXPOSE 8080
	
ENTRYPOINT ["init.sh"]
