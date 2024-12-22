# Machine Learning Microservices Project

Этот проект представляет собой набор микросервисов для выполнения задач машинного обучения с использованием RabbitMQ для обмена сообщениями между сервисами. Проект включает в себя следующие компоненты:

- **features**: сервис для генерации признаков и отправки их в очередь.
- **model**: сервис для выполнения предсказаний на основе полученных признаков.
- **metric**: сервис для расчета и логирования метрик (абсолютных ошибок).
- **plot**: сервис для построения графиков распределения абсолютных ошибок.

## Структура проекта

```plaintext
metrics-flow/
    ├── docker-compose.yml
    ├── get-pip.py
    ├── features/
    │   ├── Dockerfile
    │   ├── requirements.txt
    │   └── src/
    │       └── features.py
    ├── logs/
    │   ├── error_distribution.png
    │   └── metric_log.csv
    ├── metric/
    │   ├── Dockerfile
    │   ├── requirements.txt
    │   └── src/
    │       └── metric.py
    ├── model/
    │   ├── Dockerfile
    │   ├── requirements.txt
    │   └── src/
    │       └── model.py
    └── plot/
        ├── Dockerfile
        ├── requirements.txt
        └── src/
            └── plot.py
