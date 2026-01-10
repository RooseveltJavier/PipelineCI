from python:3.12-alpine

workdir /app

copy requirements.txt .

run pip install --no-cache-dir -r requirements.txt
run pip install waitress

run mkdir instance

copy . .

env APP_PORT=8090

expose $APP_PORT

cmd sh -c "waitress-serve --host 0.0.0.0 --port=$APP_PORT --call app:create_app"