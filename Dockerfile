# Base image as a parent image
FROM python:3.6



COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY grafana-flask-service /var/www/grafana-flask-service/
# RUN mkdir -p /etc/grafana/
# COPY grafana.ini  /etc/grafana/

# RUN python /var/www/grafana-flask-service/app.py

# EXPOSE 8082
