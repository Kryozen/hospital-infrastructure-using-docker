FROM ubuntu

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ="Europe/Vilnius"

RUN apt update && apt install python3 python3-pip docker.io software-properties-common -y
RUN add-apt-repository --yes --update ppa:ansible/ansible
RUN apt install ansible -y

RUN pip3 install docker

COPY playbook.yml /opt/playbook.yml
