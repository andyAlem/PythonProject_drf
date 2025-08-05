##  Запуск проекта через Docker Compose

### Предварительные требования
- Установленный Docker и Docker Compose
- Python 3.10+ (для разработки вне контейнера)

### 1. Клонирование репозитория

git clone https://github.com/andyAlem/PythonProject_drf.git
cd PythonProject_drf

##  Запуск проекта через Docker Compose
```bash

docker-compose up -d --build

Основные команды

docker compose up -d	Запуск в фоновом режиме
docker compose down	Остановка с сохранением данных
docker compose down -v	Полная очистка (включая volumes)
docker compose logs -f web	Просмотр логов в реальном времени
docker compose build --no-cache	Пересборка образов