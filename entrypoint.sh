#!/bin/bash
set -e

# Always run in production mode
export RUNTIME_ENV=production

# Ensure the agents directory exists
mkdir -p /app/agents

# Start supervisord
if [ "$1" = 'supervisord' ]; then
    exec "$@" -c /etc/supervisor/conf.d/supervisord.conf -n
else
    exec "$@"
fi
