FROM centos:7

# install all packages

RUN yum -y update && \
    yum -y install httpd && \
    yum clean all
# Install  Network utils
RUN yum install -y yum-utils device-mapper-persistent-data lvm2

# Install vim
RUN yum install vim -y

# Install python3
RUN yum install -y python3
RUN yum install -y python3-pip
RUN yum install centos-release-scl-rh -y
RUN yum install rh-python36-mod_wsgi -y
RUN yum install mod_ssl -y


COPY  grafana-flask-service  /var/www/grafana-flask-service/
COPY grafana-zoom-service  /var/www/grafana-zoom-service/

# Installing requirements.txt
RUN pip3 install -r /var/www/grafana-flask-service/requirements.txt

#port mapping

EXPOSE 5001/tcp
