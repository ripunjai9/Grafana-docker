# Base image as a parent image
FROM python:3.6



COPY requirements.txt ./


COPY grafana-flask-service /var/www/grafana-flask-service/
WORKDIR /var/www/grafana-flask-service/
RUN pip3 install -r ./requirements.txt


# RUN mkdir -p /etc/grafana/
# COPY grafana.ini  /etc/grafana/

# RUN python /var/www/grafana-flask-service/app.py

# EXPOSE 8082
