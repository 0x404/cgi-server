FROM python:3.9

ARG workdir=/opt/cgiserver
RUN mkdir -p ${workdir}
WORKDIR ${workdir}

RUN apt-get clean\
    && apt-get update\
    && apt-get install -y vim\
    && apt-get install -y git

COPY . .

RUN pip3 install -r requirements.txt


CMD ["/bin/bash"]
