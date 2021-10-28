FROM python:3.7

EXPOSE 2000-4000

RUN mkdir -p /srhmd

VOLUME /home/srhmd_conf/:/srhmd/

WORKDIR /srhmd

COPY ./ /srhmd

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT python /srhmd/srhmd.py