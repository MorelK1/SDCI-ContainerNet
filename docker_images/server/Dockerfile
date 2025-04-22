FROM node:18-alpine
WORKDIR /app
COPY server.js .
COPY package*.json ./
RUN apk add --update --no-cache \
        bash \
        tcpdump \
        iperf \
        busybox-extras \
        iproute2 \
        iputils \
        curl  
RUN npm install
CMD ["node", "server.js"]