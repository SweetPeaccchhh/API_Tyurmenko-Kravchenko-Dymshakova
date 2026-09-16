# 1. Базовый образ — уже содержит Python 3.11
FROM python:3.11-slim

# 2. Метаданные
LABEL maintainer="you@example.com"
LABEL description="Calculator API"

# 3. Рабочая директория внутри контейнера
WORKDIR /app

# 4. Сначала копируем только requirements.txt — для кэширования
COPY requirements.txt .

# 5. Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# 6. Копируем остальной код
COPY main.py .

# 7. Создаём непривилегированного пользователя (безопасность!)
RUN useradd -m appuser
USER appuser

# 8. Открываем порт (документация, реально ничего не открывает)
EXPOSE 8000

# 9. Команда запуска
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]