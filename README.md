# Тестовое задание для компании Traffic Light

В данном проекте используется DjangoREST Framework, pyTelegramBotAPI, Redis, Nginx, Docker.

### Для запуска проекта вам потребуется выполнить следующие комманды:

## Клонирование репозитория

Для начала работы с проектом, склонируйте его себе на локальный компьютер:

```bash
git clone https://github.com/maxcrimea/traffic_light.git
cd traffic_light
```

## Настройка окружения

Создайте файл .env в корневой директории проекта, используя env.example как шаблон.

## Запуск проекта

Для запуска проекта используйте Docker Compose:

```bash
docker-compose up -d
```

### После успешного запуска, проект будет доступен по адресу 

#### Пример запроса: http://127.0.0.1:8080/api/v1/weather/?city=Калининград


Файл с координатами городов позаимствован с репозитория https://github.com/pensnarik/russian-cities/tree/master