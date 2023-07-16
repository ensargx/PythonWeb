# FastAPI Todo App

## Docs

[FastAPI](./screen.PNG)

## Configure

Change the `ENV JWT_SECRET_KEY=SECRET` in the Dockerfile to a secret key of your choice.

## Build Docker

```bash
docker build -t fastapi_todo .
docker run -d --name my_todo_app -p 80:80 fastapi_todo
```
