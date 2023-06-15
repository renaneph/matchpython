FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update -y
RUN apt install -y \
    build-essential default-libmysqlclient-dev libjpeg-dev zlib1g-dev \
    python3 python3-pip

RUN pip3 install --upgrade pip

WORKDIR /var/www/match
COPY . .

RUN pip3 install -r requirements.txt

RUN apt update
RUN apt install -y apache2 libapache2-mod-wsgi-py3

COPY match.conf /etc/apache2/sites-available/
RUN sed -i '5 s/.*/Listen 8000/' /etc/apache2/ports.conf
RUN sed -i '$aServerName 127.0.0.1' /etc/apache2/apache2.conf
RUN mkdir /var/log/httpd

RUN a2enmod wsgi
RUN a2ensite match.conf

RUN chown -R www-data:www-data media/

EXPOSE 8000
