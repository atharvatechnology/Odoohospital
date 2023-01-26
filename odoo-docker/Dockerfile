FROM ubuntu:focal
LABEL maintainer="Lekhnath Rijal <lekhnath@greatbear.tech>"
ARG APT_MIRROR

# Generate locale C.UTF-8 for postgres and general locale data
ENV LANG C.UTF-8
ENV TZ=UTC

RUN if [ "x${APT_MIRROR}" != "x" ]; then sed -i -E "s|http://(archive\|security).ubuntu.com|${APT_MIRROR}|g" /etc/apt/sources.list; fi
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install some deps
RUN set -x; \
    apt-get update \
    &&      apt-get install -y --no-install-recommends \
    ca-certificates \
    build-essential \
    curl \
    gnupg2 \
    fonts-deva-extra \
    libssl-dev \
    libldap2-dev \
    libsasl2-dev \
    node-less \
    python3-pyldap \
    python3-setuptools \
    python3-renderpm \
    python3-qrcode \
    python3-vobject \
    python3-watchdog \
    xz-utils \
    && ln -s $(which python3) /usr/local/bin/python \
    && curl -4 -A "Mozilla/5.0" -SL https://bootstrap.pypa.io/get-pip.py | python \
    && rm -rf /var/lib/apt/lists/*

# Install wkhtmltox
# Get checksum $ curl -o- -SL curl -o- -SL https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/SHA256SUMS
RUN set -x; \
    apt-get update \
    && curl -4 -o wkhtmltox.deb  -A "Mozilla/5.0" -SL https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox_0.12.5-1.focal_amd64.deb \
    # && echo "db48fa1a043309c4bfe8c8e0e38dc06c183f821599dd88d4e3cea47c5a5d4cd3 wkhtmltox.deb" | sha256sum -c - \
    && dpkg --force-depends -i wkhtmltox.deb \
    && apt-get install -f -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* wkhtmltox.deb

# Install postgresql-client 14
RUN set -x; \
    echo 'deb http://apt.postgresql.org/pub/repos/apt/ focal-pgdg main' > etc/apt/sources.list.d/pgdg.list \
    && curl -4 -A "Mozilla/5.0" -sSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
    && apt-get update  \
    && apt-get install -y --no-install-recommends postgresql-client-14 \
    && rm -rf /var/lib/apt/lists/*

# Install Odoo
# Get checksum from: curl -o- -SL http://nightly.odoo.com/14.0/nightly/deb/odoo_14.0.20220901_amd64.changes
ENV ODOO_VERSION 14.0
ARG ODOO_RELEASE=20220901
ARG ODOO_SHA256=5b9b061bd9ed8cb3667ac150467b8bac4383095658f5422cca2ffa5ca16425c6
RUN set -x; \
    curl -o odoo.deb -4 -A "Mozilla/5.0"  -SL http://nightly.odoo.com/${ODOO_VERSION}/nightly/deb/odoo_${ODOO_VERSION}.${ODOO_RELEASE}_all.deb \
    && echo "${ODOO_SHA256} odoo.deb" | sha256sum -c - \
    && dpkg --force-depends -i odoo.deb \
    && apt-get update \
    && apt-get -y install -f --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* odoo.deb

# Copy entrypoint script and Odoo configuration file
COPY ./entrypoint.sh ./wait-for-it.sh ./db_tools.py /
COPY ./odoo.conf /etc/odoo/
RUN chown odoo /etc/odoo/odoo.conf
RUN chmod +x /wait-for-it.sh /entrypoint.sh
COPY ./requirements.txt /var/lib/odoo/requirements.txt
RUN pip3 install --upgrade -r /var/lib/odoo/requirements.txt

# Mount /var/lib/odoo to allow restoring filestore and /mnt/extra-addons for users addons
RUN mkdir -p /mnt/extra-addons \
    && chown -R odoo:odoo /mnt/extra-addons
RUN mkdir -p /mnt/backup \
    && chown -R root:root /mnt/backup
VOLUME ["/var/lib/odoo", "/mnt/extra-addons", "/mnt/backup"]

# Expose Odoo services
EXPOSE 8069 8072 5678

# Set the default config file
ENV ODOO_RC /etc/odoo/odoo.conf

# Set default user when running the container
USER odoo

ENTRYPOINT ["/entrypoint.sh"]
CMD ["odoo"]
