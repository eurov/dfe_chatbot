FROM python:3.8
RUN python -m pip install --upgrade pip && pip install pipenv
WORKDIR /app
COPY . .
RUN pipenv install --system --deploy
CMD ["python", "-m", "unittest", "test_main"]