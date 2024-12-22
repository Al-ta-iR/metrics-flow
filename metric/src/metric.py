import os
import pika
import json
import pandas as pd
import csv
from collections import defaultdict


# Устанавливаем параметры RabbitMQ из переменных окружения
rabbitmq_user = os.getenv('RABBITMQ_DEFAULT_USER', 'user')
rabbitmq_pass = os.getenv('RABBITMQ_DEFAULT_PASS', 'password')

credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
parameters = pika.ConnectionParameters('rabbitmq', 5672, '/', credentials)


# Инициализируем DataFrame для хранения сообщений
df = pd.DataFrame(columns=['id', 'y_true', 'y_pred'])

# Инициализируем словарь для хранения временных сообщений
message_buffer = defaultdict(dict)

try:
    # Создаём подключение к серверу на локальном хосте
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    # Объявляем очереди y_true и y_pred
    for queue_name in ['y_true', 'y_pred']:
        channel.queue_declare(queue=queue_name)

    # Создаём функцию callback для обработки данных из очереди
    def callback(ch, method, properties, body):
        message = json.loads(body)
        message_id = message['id']
        value = message['body']  # Изменено с 'value' на 'body'

        # Сохраняем сообщение в буфер
        message_buffer[message_id][method.routing_key] = value

        # Проверяем, есть ли в буфере y_true и y_pred для данного идентификатора
        if 'y_true' in message_buffer[message_id] and 'y_pred' in message_buffer[message_id]:
            y_true = message_buffer[message_id]['y_true']
            y_pred = message_buffer[message_id]['y_pred']
            absolute_error = abs(y_true - y_pred)

            # Записываем данные в CSV файл
            with open('./logs/metric_log.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([message_id, y_true, y_pred, absolute_error])

            # Удаляем запись из буфера после записи в CSV
            del message_buffer[message_id]

    # Извлекаем сообщения из очередей y_true и y_pred
    for queue_name in ['y_true', 'y_pred']:
        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    # Запускаем режим ожидания прихода сообщений
    print('...Ожидание сообщений, для выхода нажмите CTRL+C')
    channel.start_consuming()
except Exception as e:
    print(f'Не удалось подключиться к очереди: {e}')
