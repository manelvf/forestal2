# Forestal2 Setup Guide

## Prerequisites

- Docker and Docker Compose
- Git
- PostgreSQL (for local development without Docker)

## Environment Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd forestal2
```

### 2. Configure Environment Variables

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit `.env` and set the following required variables:

```bash
# Generate a secure secret key
SECRET_KEY=<your-secret-key-here>

# Database password
DB_PASSWORD=<your-secure-database-password>

# For production, set DEBUG=0
DEBUG=0

# Set your allowed hosts (comma-separated)
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

To generate a secure SECRET_KEY:

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### 3. Configure Django Settings

Copy the example settings file:

```bash
cp settings.example.py settings.py
```

The settings.py file is gitignored to prevent sensitive information from being committed.

### 4. Start with Docker Compose

```bash
# Build and start services
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Collect static files (for production)
docker-compose exec web python manage.py collectstatic --noinput
```

### 5. Access the Application

- Application: http://localhost:8000
- Admin: http://localhost:8000/admin

## Manual Setup (Without Docker)

### 1. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Create PostgreSQL Database

```bash
createdb forestal
createuser forestal
psql -c "ALTER USER forestal WITH PASSWORD 'your_password';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE forestal TO forestal;"
```

### 4. Run Migrations

```bash
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

### 6. Run Development Server

```bash
python manage.py runserver
```

## Database Backup

### Automated Backup

Configure the backup script:

```bash
chmod +x backup_db.sh
```

Set environment variables:

```bash
export DB_NAME=forestal
export DB_USER=forestal
export DB_PASSWORD=your_password
export DB_HOST=localhost
export BACKUP_DIR=/path/to/backups
```

Run backup:

```bash
./backup_db.sh
```

### Schedule with Cron

Add to crontab for daily backups at 2 AM:

```bash
0 2 * * * /path/to/forestal2/backup_db.sh >> /var/log/forestal_backup.log 2>&1
```

## Production Deployment

### Security Checklist

1. ✅ Set `DEBUG=0` in .env
2. ✅ Use a strong, random `SECRET_KEY`
3. ✅ Set proper `ALLOWED_HOSTS`
4. ✅ Use HTTPS (set `SECURE_SSL_REDIRECT=1`)
5. ✅ Set secure cookie flags:
   - `SESSION_COOKIE_SECURE=1`
   - `CSRF_COOKIE_SECURE=1`
6. ✅ Configure `CSRF_TRUSTED_ORIGINS`
7. ✅ Use strong database password
8. ✅ Restrict database port exposure
9. ✅ Configure email for error notifications
10. ✅ Set up logging and monitoring

### Production Environment Variables

```bash
DEBUG=0
SECRET_KEY=<strong-random-key>
DB_PASSWORD=<strong-database-password>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECURE_SSL_REDIRECT=1
SESSION_COOKIE_SECURE=1
CSRF_COOKIE_SECURE=1
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### Using Gunicorn (Production WSGI Server)

```bash
# Install gunicorn (already in requirements.txt)
pip install gunicorn

# Run with gunicorn
gunicorn --bind 0.0.0.0:8000 --workers 4 wsgi:application
```

### Nginx Configuration Example

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /static/ {
        alias /path/to/forestal2/staticfiles/;
    }

    location /media/ {
        alias /path/to/forestal2/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Troubleshooting

### Database Connection Issues

Check database is running:

```bash
docker-compose ps
```

View logs:

```bash
docker-compose logs db
docker-compose logs web
```

### Migration Issues

Reset migrations (⚠️ WARNING: This will delete all data):

```bash
docker-compose exec web python manage.py flush
docker-compose exec web python manage.py migrate
```

### Permission Issues

Fix file permissions:

```bash
sudo chown -R $(whoami):$(whoami) .
chmod +x backup_db.sh
```

## Development

### Run Tests

```bash
python manage.py test
```

### Create Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Access Django Shell

```bash
python manage.py shell
```

## Support

For issues and questions, please open an issue in the repository.
