FROM python:3.12.4 AS builder

WORKDIR /usr/src/app
COPY . .
RUN pip3 install setuptools
RUN pip3 install -r requirements.txt
RUN pyinstaller --onefile alert-machinegun.py


FROM debian:trixie-slim
RUN mkdir /opt/alert-machinegun
WORKDIR /opt/alert-machinegun
COPY --from=builder /usr/src/app/dist/alert-machinegun .
RUN echo 'deb ftp.ru.debian.org/debian trixie main' > /etc/apt/sources.list.d/main
RUN apt update; apt install -y gnupg
CMD [ "/opt/alert-machinegun/alert-machinegun" ]