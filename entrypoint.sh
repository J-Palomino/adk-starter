#!/bin/bash
set -e

# Create necessary directories
mkdir -p /app/agents

# Set permissions
chown -R appuser:appuser /app

# Start supervisord
exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
