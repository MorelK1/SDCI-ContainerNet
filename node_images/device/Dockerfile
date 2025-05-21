FROM node:18-alpine

WORKDIR /app

# Récupération du script JS depuis l'URL
RUN wget http://homepages.laas.fr/smedjiah/tmp/mw/device.js -O device.js

# Copie et permission du script de démarrage
COPY start_dev.sh /start_dev.sh
RUN chmod +x /start_dev.sh

# Installation des dépendances systèmes + Node.js
RUN apk add --update --no-cache \
        bash \
        tcpdump \
        iperf \
        busybox-extras \
        iproute2 \
        iputils \
        curl \
        jq \
        net-tools

# Installation des dépendances Node.js
RUN npm init -y
RUN npm install express systeminformation yargs request

ENTRYPOINT [ "/start_dev.sh" ]

