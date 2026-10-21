FROM python:3.14@sha256:455fc8bf2552c51738d27fde570c22bb0146d22f2e16e32a9baff8d2da94daf6

WORKDIR /usr/src/app

COPY . .

RUN pip install onepasswordconnectsdk "certifi>=2026.10.19"

CMD [ "python", "./main.py"]
