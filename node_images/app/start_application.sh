#!/bin/sh

node application.js \
  --remote_ip "$REMOTE_IP" \
  --remote_port "$REMOTE_PORT" \
  --device_name "$DEVICE_NAME" \
  --send_period "$SEND_PERIOD"
