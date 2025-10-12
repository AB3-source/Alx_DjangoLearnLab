# Alx_DjangoLearnLab / social_media_api

## Quickstart

1. Create & activate a virtualenv:
   python -m venv venv
   source venv/bin/activate

2. Install dependencies:
   pip install -r requirements.txt
   # or
   pip install django djangorestframework djangorestframework-authtoken Pillow

3. Run migrations:
   python manage.py makemigrations
   python manage.py migrate

4. Create superuser:
   python manage.py createsuperuser

5. Run server:
   python manage.py runserver

## Endpoints

Base URL: `http://127.0.0.1:8000/api/accounts/`

- `POST /register/` : Register a new user. Returns token on success.
- `POST /login/` : Login with username & password. Returns token.
- `GET|PUT|PATCH /profile/` : Get or edit authenticated user's profile. Use header:
  `Authorization: Token <token>`

## User model fields

- username (inherited)
- email, first_name, last_name (inherited)
- bio (text)
- profile_picture (image)
- followers (many-to-many self-referential)

## Notes

- Use `Authorization: Token <token>` for authenticated endpoints.
- In development, profile pictures are served via MEDIA_URL.
- This is a minimal starter; for production you must secure media, use HTTPS, and consider JWT or improved token strategies.
