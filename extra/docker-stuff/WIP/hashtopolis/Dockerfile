FROM php:8.1-rc-apache-buster

RUN apt update
RUN apt install -y git
RUN apt install -y mariadb-client
RUN apt install -y default-mysql-server
RUN service mysql start

RUN cd /var/www/html 
RUN git clone https://github.com/s3inlc/hashtopolis.git
RUN chown -R www-data:www-data hashtopolis

# EXPOSE 80
