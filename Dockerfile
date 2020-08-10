FROM python:3.7

COPY . /service

WORKDIR /service

RUN apt-get update && apt-get install -y \
  redis
RUN python3 -m pip install -r requirements.txt

EXPOSE 2001

CMD ./run_service.sh
