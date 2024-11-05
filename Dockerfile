FROM python:3.12.7-slim-bookworm AS comp405-inventory
LABEL authors="Teknicallity"

ENV PYTHONUNBUFFERED=1

RUN apt-get -y update && apt-get -y install build-essential

WORKDIR /etc/comp405-inventory

COPY requirements.txt requirements.txt

RUN mkdir /etc/comp405-inventory/.venv && \
    python -m venv --upgrade-deps --copies /etc/comp405-inventory/.venv && \
    /etc/comp405-inventory/.venv/bin/pip install --upgrade pip wheel && \
    /etc/comp405-inventory/.venv/bin/pip install -r requirements.txt

#RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

#VOLUME /etc/comp405-inventory/config
#VOLUME /etc/comp405-inventory/media

#RUN mkdir -p /etc/comp405-inventory/config && chmod -R 777 /etc/comp405-inventory/config

EXPOSE 8198

ENV VIRTUAL_ENV=/etc/comp405-inventory/.venv
ENV PATH=/etc/comp405-inventory/.venv/bin:$PATH

#RUN mkdir -p /etc/comp405-inventory/config && \
#    chown www-data:www-data /etc/comp405-inventory/config
#
#RUN mkdir /etc/comp405-inventory/app/static && \
#    python manage.py collectstatic --noinput

RUN chmod g+w .

RUN chmod +x /etc/comp405-inventory/start.sh

CMD ["/etc/comp405-inventory/start.sh"]
