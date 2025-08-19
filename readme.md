## Forestal - Timber Management System

A comprehensive timber management application adapted to PECL (Programme for the Endorsement of Forest Certification) certification requirements. This system provides complete traceability and management of timber operations from forest to destination, ensuring compliance with sustainable forestry certification standards.

## How to Run

### Option 1: Docker (Recommended)

#### Prerequisites
* Docker and Docker Compose installed on your system

#### Quick Start with Docker
1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd forestal2
   ```

2. **Build and start the application**:
   ```bash
   docker-compose up --build
   ```

3. **Access the application**:
   - Application: `http://localhost:8000/`
   - Admin panel: `http://localhost:8000/admin/`

4. **Create a superuser** (optional, in a new terminal):
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

5. **Stop the application**:
   ```bash
   docker-compose down
   ```

The Docker setup includes:
- PostgreSQL database with automatic migrations
- Web application server
- Volume persistence for database data
- Health checks and proper service dependencies

### Option 2: Manual Installation

#### Prerequisites

* Python 3.8 or higher
* pip (Python package installer)

#### Manual Installation and Setup

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd forestal2
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser** (optional, for admin access):
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

7. **Access the application**:
   - Open your web browser and go to: `http://127.0.0.1:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

#### Additional Commands

* **Collect static files** (if needed):
  ```bash
  python manage.py collectstatic
  ```

* **Create new migrations** (after model changes):
  ```bash
  python manage.py makemigrations
  ```

## Features

### PECL Certification Compliance
* Full compliance with PECL certification requirements
* Complete chain of custody documentation
* Sustainable forestry management tracking
* Audit trail for certification processes

### Core Functionality
* **Client and Customer Management**: Comprehensive contact and business relationship management
* **Timber Tracking**: Complete traceability from origin forest to final destination
* **Invoice Management**: Automated billing and financial documentation
* **Forest Operations**: Land-related event tracking (seeding, harvesting, maintenance)
* **Delivery Management**: Transportation and logistics coordination
* **Reporting**: Certification-compliant reports and documentation

### Demo
* Live demo: http://forestal.manelvf.com

## Technical Implementation

This web application is built with modern technologies to ensure reliability and scalability:

* **Backend**: Python 3.8+ with Django 4.2 framework
* **Database**: SQLite (development) / PostgreSQL (production ready)
* **Frontend**: Vue.js with responsive design
* **Certification**: Designed specifically for PECL compliance requirements

The application provides end-to-end timber supply chain management, linking timber purchases, harvesting operations, transportation, and delivery tracking with full incident management capabilities.

**Localization**: Currently optimized for Spanish forestry regulations but easily adaptable to other regional systems and certification requirements.

## Dependencies

### Server Requirements
* Django 4.2
* django-reversion 5.0
* Pillow 10.4

### Client Requirements
* Vue.js (included)
* jqGrid 3.x (included)

## Internationalization
Fully internationalized using Django i18n support with multi-language capabilities.

Feel free to contact me on manelvf@gmail.com

Cheers

