# Используйте официальный образ Python для вашего проекта Django
FROM python:3.13.4-alpine

# Установите переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Установите рабочую директорию внутри контейнера
WORKDIR /app

# Скопируйте файл зависимостей в контейнер
COPY requirements.txt /app/

# Установите зависимости
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Скопируйте код приложения в контейнер
COPY vristo-django/ /app/