# sell_items
It's an API, where users can create new posts to sell their products. Users can also leave comments under a post.

## Used Technologies

Python, FastAPI, SQLAlchemy, Alembic, PostgreSQL, JWT-authorization, Docker, Pytest.

## Instruments

Black, mypy, flake8, isort.

## Endpoints

/authors  in order to register, send a post request with a JSON object that includes fields "email" and "password"

/login in order to log in, send a post request using form-data tab (for example, in Postman) with fields username, password and respective values that you used during registration; after you get a token, add it in Headers tab with field Authorization and value "Bearer <token>"

/posts to view posts or create a new one

/posts/{id} for detailed view of a post, to edit or delete a post

/posts/{id}/comments to view comments or create a new one

/logout in order to log out, send a get request to this path

## To assemble the project:

Run git clone https://github.com/h96ven/sell_items

Python 3.11 is required.

Make sure pip and pipenv are installed. 

Install all project dependencies by running: pipenv install.

To activate virtual environment run pipenv shell

Add .env file in the root project folder

### Add these fields to the .env file:

DATABASE_HOSTNAME=your_value (use 'localhost' for normal use, 'db' for docker-compose, without quotes)

DATABASE_PORT=your_value (your postgres port number)

DATABASE_PASSWORD=your_value (your postgres password)

DATABASE_NAME=your_value (your postgres database name)

DATABASE_USERNAME=your_value (your postgres database user)

SECRET_KEY=your_value (any long string of your choice)

ALGORITHM=your_value (algorithm for JWT)

ACCESS_TOKEN_EXPIRE_MINUTES=your_value (any time of your choice in minutes)


### In order to normally use project:

PostgreSQL is required

Change DATABASE_HOSTNAME from 'db' to 'localhost'

run uvicorn app.main:app --reload

create another postgres database with same name as your main database but with '_test' added in the end of its name (this is required to run tests)

delete all files from directory alembic/versions

run alembic revision --autogenerate -m "creating all tables"

run alembic upgrade head

run pytest -v


### In order to run project via Docker:

Docker must be installed and running

Change DATABASE_HOSTNAME from 'localhost' to 'db'

Change all files' end of line to LF

Run docker-compose up --build

Check how all the endpoints work
