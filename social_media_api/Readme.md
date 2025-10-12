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
## Posts API

### Endpoints
- `GET /api/posts/` — List all posts (paginated, searchable by `?search=term`)
- `POST /api/posts/` — Create a new post (auth required)
- `GET /api/posts/<id>/` — Retrieve single post
- `PATCH /api/posts/<id>/` — Update post (only author)
- `DELETE /api/posts/<id>/` — Delete post (only author)

### Example
Request:
POST /api/posts/
Headers: Authorization: Token <token>
Body: {"title": "Hello World", "content": "This is my first post."}

Response:
{
  "id": 1,
  "author_username": "johndoe",
  "title": "Hello World",
  "content": "This is my first post."
}

## Comments API

### Endpoints
- `GET /api/comments/` — List all comments (paginated)
- `POST /api/comments/` — Create comment on a post (auth required)
- `GET /api/comments/<id>/` — Retrieve single comment
- `PATCH /api/comments/<id>/` — Update comment (only author)
- `DELETE /api/comments/<id>/` — Delete comment (only author)

### Example
POST /api/comments/
Headers: Authorization: Token <token>
Body: {"post": 1, "content": "Great post!"}
## Follows & Feed

### Follow a user
`POST /api/accounts/follow/<user_id>/`
Headers: `Authorization: Token <token>`
Response: confirmation + updated counts

### Unfollow a user
`POST /api/accounts/unfollow/<user_id>/`
Headers: `Authorization: Token <token>`

### Get who a user follows
`GET /api/accounts/following/<user_id>/` or `GET /api/accounts/following/` (your following)

### Get a user's followers
`GET /api/accounts/followers/<user_id>/` or `GET /api/accounts/followers/` (your followers)

### User feed
`GET /api/posts/feed/`
Headers: `Authorization: Token <token>`
Returns posts from users you follow, newest first (paginated).
### Likes
- POST /api/posts/<post_id>/like/  — Like a post (auth required)
- POST /api/posts/<post_id>/unlike/ — Unlike a post (auth required)

Example: POST /api/posts/3/like/
Headers: Authorization: Token <token>
Response: { "detail": "Post liked.", "likes_count": 4 }

### Notifications
- GET /api/notifications/ — List your notifications (auth required). Query param: ?unread=true
- POST /api/notifications/mark-read/<id>/ — Mark a notification as read
- POST /api/notifications/mark-all-read/ — Mark all your notifications as read
