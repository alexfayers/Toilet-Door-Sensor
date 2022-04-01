#!/bin/bash

if git pull origin main; then
    echo "Updated, restarting services..."
    sudo systemctl restart toilet_status_web
    sudo systemctl restart toilet_status
else
    echo "Update failed"
fi
