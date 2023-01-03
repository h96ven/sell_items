FROM python:3.11.1

ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/app

RUN pip install --upgrade pip 
RUN pip install pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system --dev

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]