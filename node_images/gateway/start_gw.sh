#!/bin/sh
cd /app

exec node gateway.js \
  --local_ip "$LOCAL_IP" \
  --local_port "$LOCAL_PORT" \
  --local_name "$LOCAL_NAME" \
  --remote_ip "$REMOTE_IP" \
  --remote_port "$REMOTE_PORT" \
  --remote_name "$REMOTE_NAME"
