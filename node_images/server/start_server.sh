#!/bin/sh

cd /app


exec node server.js \
  --local_ip "$LOCAL_IP" \
  --local_port "$LOCAL_PORT" \
  --local_name "$LOCAL_NAME"
