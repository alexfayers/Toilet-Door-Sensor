#!/bin/bash

if git pull origin main; then
    echo "Updated, restarting service..."
    sudo systemctl restart toilet_status
else
    echo "Update failed"
fi
