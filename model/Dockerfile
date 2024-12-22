# Используем базовый образ Python 3.9
FROM python:3.9

# Устанавливаем рабочую директорию
WORKDIR /usr/src/app

# Копируем файлы с исходным кодом
COPY ./src ./

# Копируем файл с зависимостями
COPY ./requirements.txt ./

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Запуск приложения
CMD ["python", "model.py"]
