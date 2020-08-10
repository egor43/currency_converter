FROM python:3.7

COPY . /

RUN apt-get update && apt-get install -y \
  redis
RUN python3 -m pip install -r requirements.txt

WORKDIR /service

EXPOSE 2001

CMD ./run_service.sh
