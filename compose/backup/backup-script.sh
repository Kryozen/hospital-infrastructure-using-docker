#!/bin/bash

# Get current timestamp
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")

# Set backup file name
BACKUP_FILE="backup.tar.gz"
BACKUP_PATH="/opt/$BACKUP_FILE"

# Create a backup for vhost1
BACKUP_SOURCE="/var/www/html/"
docker exec vhost1 tar -czvf "$BACKUP_PATH" -C "$BACKUP_SOURCE" .

# Create a backup for vhost2
BACKUP_SOURCE="/var/www/html/"
docker exec vhost2 tar -czvf "$BACKUP_PATH" -C "$BACKUP_SOURCE" .

# Create a backup for vhost3
BACKUP_SOURCE="/var/www/html"
docker exec vhost3 tar -czvf "$BACKUP_PATH" -C "$BACKUP_SOURCE" .

# Create a backup for database
BACKUP_SOURCE="/var/lib/mysql"
docker exec database tar -czvf "$BACKUP_PATH" -C "$BACKUP_SOURCE" .

# Save backups to local mount
BACKUPS_PATH_1="/opt/vhost1/$BACKUP_FILE"
BACKUPS_PATH_2="/opt/vhost2/$BACKUP_FILE"
BACKUPS_PATH_3="/opt/vhost3/$BACKUP_FILE"
BACKUPS_PATH_4="/opt/database/$BACKUP_FILE"
LOCAL_PATH="/backup/$TIMESTAMP"

mkdir -p "$LOCAL_PATH"

mkdir -p "$LOCAL_PATH/vhost1"
mkdir -p "$LOCAL_PATH/vhost2"
mkdir -p "$LOCAL_PATH/vhost3"
mkdir -p "$LOCAL_PATH/database"

# Wait for the backups to be ready
sleep 30

# Copy the backups 
mv "$BACKUPS_PATH_1" "$LOCAL_PATH/vhost1/"
mv "$BACKUPS_PATH_2" "$LOCAL_PATH/vhost2/"
mv "$BACKUPS_PATH_3" "$LOCAL_PATH/vhost3/"
mv "$BACKUPS_PATH_4" "$LOCAL_PATH/database/"