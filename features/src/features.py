import os
import pika
import numpy as np
import json
from sklearn.datasets import load_diabetes
import time
from datetime import datetime


# Устанавливаем параметры RabbitMQ из переменных окружения
rabbitmq_user = os.getenv('RABBITMQ_DEFAULT_USER', 'user')
rabbitmq_pass = os.getenv('RABBITMQ_DEFAULT_PASS', 'password')


credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
parameters = pika.ConnectionParameters('rabbitmq', 5672, '/', credentials)

def generate_message_id():
    return datetime.timestamp(datetime.now())

def send_message(channel, queue_name, message):
    channel.basic_publish(exchange='', routing_key=queue_name, body=json.dumps(message))

def main():
    # Загружаем датасет о диабете
    X, y = load_diabetes(return_X_y=True)
    
    while True:
        try:
            # Формируем случайный индекс строки
            random_row = np.random.randint(0, X.shape[0] - 1)

            # Создаём подключение по адресу rabbitmq:
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            channel = connection.channel()

            # Создаём очередь y_true и features
            for queue_name in ['y_true', 'features']:
                channel.queue_declare(queue=queue_name)

            # Генерируем уникальный идентификатор
            message_id = generate_message_id()

            # Публикуем сообщение в очередь y_true с идентификатором
            message_y_true = {
                'id': message_id,
                'body': y[random_row]
            }
            send_message(channel, 'y_true', message_y_true)
            print(f'Сообщение с правильным ответом отправлено в очередь (ID: {message_id})')

            # Публикуем сообщение в очередь features с идентификатором
            message_features = {
                'id': message_id,
                'body': list(X[random_row])
            }
            send_message(channel, 'features', message_features)
            print(f'Сообщение с вектором признаков отправлено в очередь (ID: {message_id})')

            # Закрываем подключение
            connection.close()

            # Добавляем задержку на 10 секунд между итерациями
            time.sleep(10)
        except Exception as e:
            print(f'Ошибка: {e}')
            time.sleep(5)  # Добавляем небольшую задержку перед повтором

if __name__ == "__main__":
    main()
