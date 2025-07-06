# Security Configuration

## Environment Variables Setup

This project uses environment variables to keep sensitive information secure. Follow these steps:

### 1. Development Setup

1. Copy the example environment file:

   ```bash
   cp .env.example .env
   ```

2. Update the `.env` file with your development settings:

   ```bash
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ```

### 2. Production Setup

1. **Generate a new SECRET_KEY** for production:

   ```python
   python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
   ```

2. Create a production `.env` file:

   ```bash
   SECRET_KEY=your-new-production-secret-key
   DEBUG=False
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   ```

### 3. Security Best Practices

- ✅ **Secret Key**: Moved to environment variables
- ✅ **Debug Mode**: Configurable via environment
- ✅ **Allowed Hosts**: Configurable for production
- ✅ **Media Files**: Ignored from version control
- ✅ **Database**: SQLite file ignored from commits

### 4. Files to Keep Secret

The following files contain sensitive information and should **NEVER** be committed:

- `.env` - Contains secret keys and configuration
- `db.sqlite3` - Contains user data
- `media/` - Contains uploaded files

These are already included in `.gitignore`.

## Installation

```bash
pip install -r requirements.txt
```

## Environment Variables Reference

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SECRET_KEY` | Django secret key | None | ✅ Yes |
| `DEBUG` | Debug mode | `True` | No |
| `ALLOWED_HOSTS` | Comma-separated hosts | Empty | No |
