FROM python:3
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT ["sh", "run.sh"]