import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import time


# Устанавливаем параметры RabbitMQ из переменных окружения
rabbitmq_user = os.getenv('RABBITMQ_DEFAULT_USER', 'user')
rabbitmq_pass = os.getenv('RABBITMQ_DEFAULT_PASS', 'password')

credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
parameters = pika.ConnectionParameters('rabbitmq', 5672, '/', credentials)


def read_and_plot_data(input_file, output_file):
    while True:
        # Читаем данные из CSV-файла
        df = pd.read_csv(input_file)

        # Выбираем столбец с абсолютными ошибками
        absolute_errors = df['absolute_error']

        # Создаем график
        plt.figure(figsize=(10, 6))
        sns.histplot(data=absolute_errors, bins=30, kde=True, color='green', alpha=0.6)

        # Добавляем заголовок и метки осей
        plt.title('Распределение абсолютных ошибок')
        plt.xlabel('Абсолютная ошибка')
        plt.ylabel('Частота')

        # Сохраняем график в файл
        output_dir = os.path.dirname(output_file)
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(output_file)
        plt.close()

        print(f"График сохранен в {output_file}. Обновление через 60 секунд.")
        time.sleep(60)  # Обновляем график каждые 60 секунд

if __name__ == "__main__":
    input_file = './logs/metric_log.csv'
    output_file = './logs/error_distribution.png'

    print("Создание графика распределения абсолютных ошибок...")
    read_and_plot_data(input_file, output_file)
    print("Процесс создания графика завершен.")
