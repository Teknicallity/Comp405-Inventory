# Stage 1: Build stage
FROM python:3.12.7-slim-bookworm AS build
LABEL authors="Teknicallity"

ENV PYTHONUNBUFFERED=1

# Install build tools
RUN apt-get -y update && apt-get -y install build-essential

WORKDIR /build

COPY requirements.txt requirements.txt

# Install python dependencies
RUN python -m venv --copies /build/.venv && \
    /build/.venv/bin/pip install --upgrade pip wheel --no-cache-dir && \
    /build/.venv/bin/pip install --no-cache-dir -r requirements.txt && \
    /build/.venv/bin/pip install --no-cache-dir 'uWSGI>=2.0.28'

COPY . .


# Stage 2: Runtime stage
FROM python:3.12.7-slim-bookworm AS runtime
LABEL authors="Teknicallity"

ENV PYTHONUNBUFFERED=1

WORKDIR /etc/comp405-inventory

# Copy build stage libraries
COPY --from=build /build/.venv /etc/comp405-inventory/.venv
COPY --from=build /build /etc/comp405-inventory

ENV VIRTUAL_ENV=/etc/comp405-inventory/.venv
ENV PATH=/etc/comp405-inventory/.venv/bin:$PATH

# Fix Permissions
RUN chmod g+w . && \
    chmod +x /etc/comp405-inventory/start.sh && \
    sed -i 's/\r$//' /etc/comp405-inventory/start.sh

EXPOSE 8198

CMD ["sh", "/etc/comp405-inventory/start.sh"]
