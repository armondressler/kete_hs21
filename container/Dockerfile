FROM python:3.10

RUN apt-get update && \
    apt-get upgrade && \
    apt-get install -y nginx supervisor ffmpeg

RUN /usr/local/bin/python -m pip install gunicorn==20.1.0 django==3.2.9

RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY container/files/gunicorn_nginx.conf /etc/nginx/sites-available/gunicorn.conf
RUN rm /etc/nginx/sites-enabled/default
RUN ln -s /etc/nginx/sites-available/gunicorn.conf /etc/nginx/sites-enabled/gunicorn.conf

RUN mkdir -p /var/log/supervisor
COPY container/files/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

RUN mkdir -p /opt/services/djangoapp/src

COPY container/files/init.sh /usr/local/bin/

COPY kete_hs21 /opt/services/djangoapp/src
COPY requirements.txt /tmp/

RUN /usr/local/bin/python -m pip install -r /tmp/requirements.txt

RUN groupadd -g 1000 gunicorn && \
    useradd -m -u 1000 -g gunicorn gunicorn && \
    chown -R gunicorn:gunicorn /opt/services/djangoapp/src && \
    chmod u+x /usr/local/bin/init.sh && \
    chown gunicorn:gunicorn /usr/local/bin/init.sh

EXPOSE 8080
	
ENTRYPOINT ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
