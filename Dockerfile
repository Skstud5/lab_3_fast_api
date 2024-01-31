FROM python:3.11-alpine3.19

# Копирование и установка зависимостей
COPY ./requirements.txt /
RUN pip install -r requirements.txt \
    && rm /requirements.txt

# Копирование приложения
COPY . /app
WORKDIR /app

# Запуск приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]