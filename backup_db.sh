#!/bin/bash
set -euo pipefail

# Database backup script
# Usage: ./backup_db.sh

# Configuration
DB_NAME="${DB_NAME:-forestal}"
DB_USER="${DB_USER:-forestal}"
DB_HOST="${DB_HOST:-db}"
DB_PORT="${DB_PORT:-5432}"
BACKUP_DIR="${BACKUP_DIR:-../backups}"
RETENTION_DAYS="${RETENTION_DAYS:-7}"

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Generate timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DAY_OF_WEEK=$(date +%A)
BACKUP_FILE="$BACKUP_DIR/${DB_NAME}_${TIMESTAMP}.sql.gz"
DAILY_LINK="$BACKUP_DIR/${DB_NAME}_${DAY_OF_WEEK}.sql.gz"

echo "Starting database backup..."
echo "Database: $DB_NAME"
echo "Host: $DB_HOST"
echo "Backup file: $BACKUP_FILE"

# Perform backup
if PGPASSWORD="$DB_PASSWORD" pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" "$DB_NAME" | gzip > "$BACKUP_FILE"; then
    echo "Backup successful: $BACKUP_FILE"

    # Create/update daily link (overwrite previous backup for this day)
    ln -sf "$(basename "$BACKUP_FILE")" "$DAILY_LINK"
    echo "Daily backup link updated: $DAILY_LINK"

    # Clean up old backups (keep last RETENTION_DAYS days)
    echo "Cleaning up backups older than $RETENTION_DAYS days..."
    find "$BACKUP_DIR" -name "${DB_NAME}_*.sql.gz" -type f -mtime +$RETENTION_DAYS -delete

    # Show backup size
    BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    echo "Backup size: $BACKUP_SIZE"

    exit 0
else
    echo "ERROR: Backup failed!" >&2
    # Clean up failed backup file
    rm -f "$BACKUP_FILE"
    exit 1
fi


