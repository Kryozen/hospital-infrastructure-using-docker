FROM ubuntu:latest

# Update package list
RUN apt-get update

# Download python
RUN apt-get install python3 python3-pip -y

# Download Flask library for python
RUN pip install flask

# Download mysql libraries for python
RUN pip install pymysql mysql-connector mysql-connector-python

ENTRYPOINT [ "python3", "/var/www/html/server.py" ]