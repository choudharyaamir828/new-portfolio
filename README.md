# Portfolio Backend API

A lightweight, production-minded Django REST Framework API for managing and serving portfolio content.

## Tech Stack

- Python 3.11+
- Django 5.x
- Django REST Framework
- django-filter
- Pillow
- python-decouple
- SQLite locally; Supabase PostgreSQL for deployment

## Setup

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements/dev.txt
```

Create a local environment file:

```bash
cp .env.example .env
```

Update `.env` with a real `SECRET_KEY` before running the app.

Run migrations:

```bash
python manage.py migrate
```

Create an admin user:

```bash
DJANGO_SUPERUSER_USERNAME=admin \
DJANGO_SUPERUSER_EMAIL=admin@example.com \
DJANGO_SUPERUSER_PASSWORD=change-me-now \
python manage.py createsuperuser --noinput
```

Seed sample portfolio data:

```bash
python manage.py seed_portfolio
```

For multi-user portfolio support, use a profile `username` and filter API requests with it:

```text
/api/v1/about/?username=aamir
/api/v1/projects/?username=aamir
/api/v1/skills/?username=aamir
```

## Contact Email Delivery

Contact form submissions are saved in the database and can also send an email notification.

Set these backend environment variables:

```bash
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=your-email@gmail.com
CONTACT_FALLBACK_EMAIL=
```

For Gmail, use an App Password instead of your normal account password.

Run the development server:

```bash
python manage.py runserver
```

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/api/v1/about/` | Get profile |
| GET | `/api/v1/projects/` | List projects (filter: `is_featured`, `tech_stack`, `tech_stack__category`; search: `title`, `short_description`) |
| GET | `/api/v1/projects/<slug>/` | Project detail |
| GET | `/api/v1/skills/` | Skills grouped by category |
| POST | `/api/v1/contact/` | Submit contact message |

## Admin Content

Use `/admin/` to manage profile details, projects, project images, tech stacks, skill categories, skills, and contact messages.

The public API is read-only except for contact submissions. Contact messages are read-only in the admin and can be marked as read with the admin action.

## Environment Variables

The app reads configuration with `python-decouple`. Set DATABASE_URL to use Supabase PostgreSQL; leaving it empty keeps local SQLite.

| Key | Example | Notes |
|---|---|---|
| `SECRET_KEY` | `django-insecure-change-me` | Required |
| `DEBUG` | `True` | `True` for local development |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Comma-separated host list |
| `SQLITE_DB_PATH` | `/opt/render/project/src/db.sqlite3` | Optional; defaults to project `db.sqlite3` |
| `CORS_ALLOWED_ORIGINS` | `http://localhost:5173` | Comma-separated frontend origins |
| `CSRF_TRUSTED_ORIGINS` | `http://localhost:5173` | Needed for trusted frontend domains |

## Production Deployment

This backend is now prepared for deployment on platforms like Render.

Production entrypoints:

```bash
./build.sh
bash start.sh
```

Recommended production variables:

```bash
DJANGO_SETTINGS_MODULE=config.settings.prod
DATABASE_URL=<Supabase Session pooler URI>
ALLOWED_HOSTS=your-backend-domain.onrender.com
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.vercel.app
CSRF_TRUSTED_ORIGINS=https://your-frontend-domain.vercel.app
```

See [`DEPLOYMENT.md`](../DEPLOYMENT.md) for the full frontend + backend flow.

## Free Render + Supabase deployment

Use Render Free with `./build.sh` as the build command and `bash start.sh` as the start command.
Set DATABASE_URL in Render to the Supabase Connect > Session pooler connection URI (port 5432).
Replace the password placeholder with the database password; URL-encode special characters.
Never put this URI in frontend VITE variables, GitHub, or chat. The Supabase HTTPS project URL is not a database connection URI.
The application requires TLS for PostgreSQL connections. Leaving DATABASE_URL empty uses local SQLite.

The start script runs Django migrations to create tables. Existing SQLite portfolio data and admin accounts
are not transferred automatically; preserve the source database and import its data separately.
Database records in Supabase survive Render restarts. Uploaded files still need external storage;
local Render uploads remain ephemeral. No paid Render disk or Render PostgreSQL instance is created.
Free Render blocks SMTP ports 25/465/587; the current Gmail SMTP delivery needs a different setup.
See https://supabase.com/docs/guides/database/connecting-to-postgres for connection options.
