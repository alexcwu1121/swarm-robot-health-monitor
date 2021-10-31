FROM navikey/raspbian-buster:2021-05-09

EXPOSE 2000-4000

RUN sudo apt-get update
RUN sudo apt-get install -y python3.7
RUN sudo apt-get install -y python3-pip

RUN mkdir -p /srhmd

VOLUME /home/pi/srhmd_conf/:/srhmd/

WORKDIR /srhmd

COPY ./ /srhmd

RUN pip3 install --no-cache-dir -r requirements.txt

ENTRYPOINT python3.7 /srhmd/srhmd.py