# 1. Базовый образ
FROM python:3.11-slim

# 2. Устанавливаем зависимости
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Копируем код
COPY . .

# 4. Запускаем Django через gunicorn
CMD ["gunicorn", "em_auth.wsgi:application", "--bind", "0.0.0.0:8080"]