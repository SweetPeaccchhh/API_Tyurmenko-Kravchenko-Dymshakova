# 1. Базовый образ, который уже содержит Python 3.11
FROM python:3.11-slim

# 2. Метаданные
LABEL maintainer="Calculator API@coolteam.com"
LABEL description="Calculator API — Тюрменко, Кравченко, Дымшакова"

# 3. Рабочая директория внутри контейнера
WORKDIR /app

# 4. Копирование requirements.txt для кэширования
COPY requirements.txt .

# 5. Установление зависимости
RUN pip install --no-cache-dir -r requirements.txt

# 6. Копирование остального кода
COPY main.py .

# 7. Создание непривилегированного пользователя (для обеспечения безопасности)
RUN useradd -m appuser
USER appuser

# 8. Открытие порта
EXPOSE 8000

# 9. Команда запуска
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]