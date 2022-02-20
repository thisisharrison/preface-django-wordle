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

5. Seed your `db.sqlite3`

    ```shell
    python manage.py createsuperuser
    python manage.py shell
    >> from wordle_app.seed import StartGame
    >> StartGame.reset_game()
    ```

6. Run server with `python manage.py runserver`. In your browser, go to http://localhost:8000.

