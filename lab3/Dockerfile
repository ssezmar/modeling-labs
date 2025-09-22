FROM python:3.11-slim

# Устанавливаем Tk и утилиты
RUN apt-get update && apt-get install -y \
    python3-tk \
    tk \
    x11-apps \
    && rm -rf /var/lib/apt/lists/*

# Копируем твой тест
COPY tk_test.py /app/tk_test.py
WORKDIR /app

# Запуск по умолчанию
CMD ["python", "tk_test.py"]