FROM node:18-alpine

WORKDIR /app

# Récupération du script JS depuis l'URL
RUN wget https://homepages.laas.fr/smedjiah/tmp/mw/server.js -O server.js

# Copie et permission du script de démarrage
COPY start_server.sh /start_server.sh
RUN chmod +x /start_server.sh

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

