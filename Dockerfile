FROM continuumio/miniconda3

RUN apt update
RUN apt install git

COPY entrypoint.sh /entrypoint.sh
COPY *.py /
COPY requirements.txt /

RUN pip install -r requirements.txt

ENTRYPOINT ["/entrypoint.sh"]