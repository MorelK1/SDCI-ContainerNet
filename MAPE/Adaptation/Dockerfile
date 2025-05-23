FROM node:18-alpine

WORKDIR /app

# Récupération du script JS depuis l'URL
RUN wget http://homepages.laas.fr/smedjiah/tmp/mw/gateway.js -O gateway.js

# Copie et permission du script de démarrage
COPY start_vnf.sh /start_vnf.sh
RUN chmod +x /start_vnf.sh

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

ENV "LOCAL_IP" "10.0.0.12"
ENV "LOCAL_PORT" "8182"
ENV "LOCAL_NAME" "gi2"
ENV "REMOTE_IP" "10.0.0.1"
ENV "REMOTE_PORT" "8080"
ENV "REMOTE_NAME" "srv"

ENV VIM_EMU_CMD /start_vnf.sh
ENV VIM_EMU_CMD_STOP "echo 'Stopping the container now.'"

