from python:3.12-alpine

workdir /app

copy requirements.txt .

run pip install --no-cache-dir -r requirements.txt
run pip install waitress

run mkdir instance

copy . .

expose 8090

cmd waitress-serve --host 0.0.0.0 --call app:create_app