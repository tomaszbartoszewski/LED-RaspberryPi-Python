FROM resin/%%RESIN_MACHINE_NAME%%-python

#switch on systemd init system in container
ENV INITSYSTEM on

# pip install python deps from requirements.txt
# For caching until requirements.txt changes
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

WORKDIR /usr/src/app

COPY . .

CMD ["python3", "main.py"]