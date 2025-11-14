# Forestal2 - Forest Management System

[![Django CI](https://github.com/manelvf/forestal2/workflows/Django%20CI/badge.svg)](https://github.com/manelvf/forestal2/actions)
[![Docker Build](https://github.com/manelvf/forestal2/workflows/Docker%20Build/badge.svg)](https://github.com/manelvf/forestal2/actions)
[![Code Coverage](https://github.com/manelvf/forestal2/workflows/Code%20Coverage/badge.svg)](https://github.com/manelvf/forestal2/actions)

A Django-based forest management system for tracking parcels, forestry services, transportation, and invoicing.

## Features

- 🌲 **Parcel Management** - Track forest parcels with cadastral information
- 📋 **Forestry Services** - Manage logging permits and forestry operations
- 🚛 **Transportation Tracking** - Monitor timber transportation via trucks
- 💼 **Invoicing** - Generate and manage invoices for services
- 📊 **Reporting** - Export data to CSV and generate reports
- 🔐 **Security** - Comprehensive authentication and authorization

## Recent Security Improvements

This codebase has undergone a comprehensive security audit and remediation:

### Critical Fixes
- ✅ SQL injection vulnerabilities eliminated
- ✅ Command injection vulnerabilities fixed
- ✅ XSS vulnerabilities patched
- ✅ All credentials moved to environment variables
- ✅ Authentication required on all endpoints

### Code Quality
- ✅ Input validation and bounds checking
- ✅ Proper error handling and logging
- ✅ N+1 query problems resolved
- ✅ Race conditions fixed with atomic transactions
- ✅ File resource leaks eliminated

## Quick Start

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/manelvf/forestal2.git
   cd forestal2
   ```

2. **Set up environment**
   ```bash
   cp .env.example .env
   # Edit .env and set required variables
   ```

3. **Generate secure SECRET_KEY**
   ```bash
   python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
   ```

4. **Start with Docker Compose**
   ```bash
   docker-compose up -d
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py createsuperuser
   ```

5. **Access the application**
   - Application: http://localhost:8000
   - Admin: http://localhost:8000/admin

### Manual Setup

See [SETUP.md](SETUP.md) for detailed setup instructions.

## Environment Variables

Required environment variables (see `.env.example`):

```bash
SECRET_KEY=<your-secret-key>
DB_PASSWORD=<your-database-password>
DEBUG=0
ALLOWED_HOSTS=yourdomain.com
```

## Testing

### Run tests locally
```bash
python manage.py test
```

### Run tests with coverage
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

### CI/CD

Tests are automatically run on every push via GitHub Actions:
- Django tests on Python 3.10, 3.11, and 3.12
- Security checks with bandit
- Dependency vulnerability scanning
- Docker build verification
- Code coverage analysis

## Security

### Reporting Security Issues

If you discover a security vulnerability, please email security@example.com instead of using the issue tracker.

### Security Features

- **Authentication**: All views require staff member authentication
- **Input Validation**: Comprehensive validation on all user inputs
- **CSRF Protection**: All state-changing operations protected
- **SQL Injection Prevention**: Safe ORM usage, no eval() or string-based queries
- **XSS Protection**: All HTML properly escaped with `format_html()`
- **Secure Defaults**: DEBUG=0, secure cookies, HTTPS enforcement available

## Database Backup

Automated backup script included:

```bash
# Configure backup
export DB_PASSWORD=your_password
export BACKUP_DIR=/path/to/backups

# Run backup
./backup_db.sh

# Schedule with cron (daily at 2 AM)
0 2 * * * /path/to/forestal2/backup_db.sh >> /var/log/forestal_backup.log 2>&1
```

## Project Structure

```
forestal2/
├── fincas/          # Parcel and forestry service management
├── empresas/        # Company, truck, and invoice management
├── templates/       # HTML templates
├── static/          # Static files (CSS, JS, images)
├── .github/         # GitHub Actions workflows
├── settings.example.py  # Django settings template
├── .env.example     # Environment variables template
├── constants.py     # Application constants
└── backup_db.sh     # Database backup script
```

## Technologies

- **Backend**: Django 4.2.16
- **Database**: PostgreSQL 15
- **Frontend**: jQuery, jqGrid
- **Deployment**: Docker, Gunicorn, Nginx
- **CI/CD**: GitHub Actions

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Standards

- Follow PEP 8 style guide
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

## License

This project is proprietary software. All rights reserved.

## Support

For issues and questions:
- Check [SETUP.md](SETUP.md) for setup help
- Open an issue for bugs or feature requests
- Review existing issues before creating new ones

## Changelog

### 2024-11-14 - Security Update
- Fixed 30+ security vulnerabilities and code quality issues
- Added comprehensive test suite with CI/CD
- Improved documentation and setup process
- Added Docker support with health checks

## Authors

- Manuel Vázquez Fernández
