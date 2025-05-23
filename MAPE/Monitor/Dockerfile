FROM node:18-alpine

WORKDIR /app

COPY monitor.js .
COPY start_monitor.sh /start_monitor.sh

RUN chmod +x /start_monitor.sh

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

EXPOSE 5000

# Installation des dépendances Node.js
RUN npm init -y
RUN npm install express systeminformation yargs request

ENV VIM_EMU_CMD /start_monitor.sh
ENV VIM_EMU_CMD_STOP "echo 'Stopping the container now.'"