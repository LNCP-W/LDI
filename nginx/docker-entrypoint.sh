#!/usr/bin/env sh
set -eu

echo "Generating nginx config from template..."
envsubst '${DOMAIN}' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf
nginx -t || exit 1

exec nginx -g "daemon off;"

