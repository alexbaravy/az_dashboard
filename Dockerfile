# Используйте официальный образ Python для вашего проекта Django
FROM python:3.11.7-alpine

# Установите переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Установите рабочую директорию внутри контейнера
WORKDIR /app

COPY .venv/Lib/site-packages/az_admin /usr/local/lib/python3.11/site-packages/az_admin

# Скопируйте файл зависимостей в контейнер
COPY requirements.txt /app/

# Установите зависимости
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Скопируйте код приложения в контейнер
COPY vristo-django/ /app/

# Установка клиента PostgreSQL
#RUN apk --update add postgresql-client \
#    && rm -rf /var/cache/apk/*

COPY backup.sql /app/
# не работает? пришлось вручную  Get-Content backup.sql | docker exec -i a2af417ce680 psql -U dashboard -d dashboard
#RUN psql -U dashboard -d dashboard < backup.sql

# Создайте и примените миграции Django
#RUN python manage.py migrate

# Соберите статические файлы Django
#RUN python manage.py collectstatic --noinput
#
## Определите команду для запуска вашего приложения
#CMD ["gunicorn", "vristo.wsgi:application", "--bind", "0.0.0.0:8000"]
#
## Откройте порт, который ваше приложение будет использовать
#EXPOSE 8000

RUN apk update && apk add redis