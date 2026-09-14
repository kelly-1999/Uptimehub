#!/bin/sh

set -e

sed \
  -e "s|\${ALERT_EMAIL_TO}|${ALERT_EMAIL_TO}|g" \
  -e "s|\${ALERT_EMAIL_FROM}|${ALERT_EMAIL_FROM}|g" \
  -e "s|\${ALERT_EMAIL_PASSWORD}|${ALERT_EMAIL_PASSWORD}|g" \
  /etc/alertmanager/alertmanager.yml.template \
  > /tmp/alertmanager.yml

exec /bin/alertmanager \
  --config.file=/tmp/alertmanager.yml \
  --storage.path=/alertmanager
