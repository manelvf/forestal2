FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Add psycopg2 for PostgreSQL support
RUN pip install --no-cache-dir psycopg2-binary

# Copy project
COPY . /code/

# Create entrypoint script
RUN echo '#!/bin/bash\nset -e\n\n# Wait for database\nuntil pg_isready -h db -p 5432 -U forestal; do\n  echo "Waiting for database..."\n  sleep 2\ndone\n\n# Run migrations\npython manage.py migrate\n\n# Collect static files\npython manage.py collectstatic --noinput\n\n# Execute the main command\nexec "$@"' > /code/entrypoint.sh
RUN chmod +x /code/entrypoint.sh

ENTRYPOINT ["/code/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]