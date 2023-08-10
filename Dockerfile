# Use an official Python runtime as a parent image
FROM python:3.11

# Установите переменную среды для предотвращения вывода данных во время установки пакетов
ENV PYTHONUNBUFFERED 1

# Set the working directory to /app
WORKDIR /app

# Копируйте файлы зависимостей
COPY pyproject.toml poetry.lock /app/

# Установите Poetry
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Copy the current directory contents into the container at /app
COPY . /app

# Expose the port that FastAPI will run on
EXPOSE 8000

# Запустите FastAPI приложение
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
