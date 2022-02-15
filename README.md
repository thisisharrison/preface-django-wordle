# Preface Wordle

## Features

1. App: Play the game
2. Account: Custom user from django
3. Word: Stores the list of words
4. Stat: Shows user their stats

## Custom Feature for the Future

1. n digits n + 1 attempts
2. Generate a Game Room to battle with friends

## Development

1. Confirm your Python is at least version 3.7:

```
python -V
```

You should see Python 3.7.3 or higher.

2. Create a Python virtual environment and install dependencies:

```
python -m venv
source env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

3. Create `.env` in the same directory as `manage.py`:

```
echo DEBUG=True > .env
echo SECRET_KEY=$(cat /dev/urandom | LC_ALL=C tr -dc '[:alpha:]'| fold -w 50 | head -n1) >> .env
```

4. Run the Django migrations:

```
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
python manage.py runserver
```

In your browser, go to http://localhost:8000.

## Deployment

1. Follow [Google Cloud Guide](https://cloud.google.com/python/django/flexible-environment). Following are some key points to highlight:

2. Add missing secrets to `.env` before for local testing:

```
echo DATABASE_URL=postgres://DATABASE_USERNAME:DATABASE_PASSWORD@//cloudsql/PROJECT_ID:REGION:INSTANCE_NAME/DATABASE_NAME >> .env
echo GS_BUCKET_NAME=PROJECT_ID_MEDIA_BUCKET >> .env
```

3. Copy these secrets to GCP Secret Manager

```
gcloud secrets create django_settings --data-file .env
```

4. Run these before developing with Cloud SQL Auth proxy:

```
./cloud_sql_proxy -instances="PROJECT_ID:REGION:INSTANCE_NAME"=tcp:5432
export GOOGLE_CLOUD_PROJECT=PROJECT_ID
export USE_CLOUD_SQL_AUTH_PROXY=true

python manage.py runserver
```

5. `requirements.txt` has no versions. App Engine will pip install based on Python 3.7.
