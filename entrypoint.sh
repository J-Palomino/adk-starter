#!/bin/bash
set -e

# Create necessary directories with correct permissions
mkdir -p /app/agents
chmod 755 /app/agents

# Set ownership of app directory to appuser
chown -R appuser:appuser /app

# Fix permissions on agent files
chmod +x /app/agents/*/agent.py 2>/dev/null || true

# Create a symlink for Railway's persistent storage if it exists
if [ -d "/data/agents" ] && [ ! -L "/app/agents" ]; then
    # If /data/agents exists and /app/agents is not a symlink
    echo "Using /data/agents for persistent storage"
    rm -rf /app/agents
    ln -s /data/agents /app/agents
    chown -R appuser:appuser /data/agents
    chmod -R 755 /data/agents
fi

# Start supervisord
exec /usr/bin/supervisord -n -c /etc/supervisor/conf.d/supervisord.conf
