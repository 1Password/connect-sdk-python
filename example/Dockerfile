FROM python:latest@sha256:2a8b92a1e9eb6ef2c888eb7e6c91283788c6d613fdc8fc22e12346aff7c4406d

WORKDIR /usr/src/app

COPY . .

RUN pip install onepasswordconnectsdk

CMD [ "python", "./main.py"]
