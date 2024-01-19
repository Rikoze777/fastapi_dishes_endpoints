# home_task_fastapi_1

Задание реализации REST API по работе с меню ресторана

- Даны 3 сущности: Меню, Подменю, Блюдо.

### Зависимости задания:

- У меню есть подменю, которые к ней привязаны.

- У подменю есть блюда.

### Условия задания:

- Блюдо не может быть привязано напрямую к меню, минуя подменю.

- Блюдо не может находиться в 2-х подменю одновременно.

- Подменю не может находиться в 2-х меню одновременно.

- Если удалить меню, должны удалиться все подменю и блюда этого меню.

- Если удалить подменю, должны удалиться все блюда этого подменю.

- Цены блюд выводить с округлением до 2 знаков после запятой.

- Во время выдачи списка меню, для каждого меню добавлять кол-во подменю и блюд в этом меню.

- Во время выдачи списка подменю, для каждого подменю добавлять кол-во блюд в этом подменю.

- Во время запуска тестового сценария БД должна быть пуста.

## Установка

- Если не установлен `poetry` - установите командой:
```bash
pip install poetry
```

- Инициализируйте проект:
```bash
poenty init
```

- Перейдите в среду poetry:
```bash
poetry shell
```

- Установите зависимости:
```bash
poetry install
```

- Перейлите в папку `app`.
```bash
cd app/
```

- Создайте файл `.env` в папке `app`. 
```bash
touch .env
```

- Заполните файл `.env` по примеру из [env_example](app/env_example)

## Установка с make:

- Если отсутствует make, установите командой:
```bash
sudo apt-get -y install make
```

- Установка завистимостей командой:
```bash
make install
```


## Запуск

- Перейлите в папку `app`.
```bash
cd app/
```

- Выполните команду по запуску приложения:
```bash
uvicorn main:app --reload
```

- Запуск приложения командой make:
```bash
make run
```
- Просмотр api доступно по [ссылке](http://127.0.0.1:8000/docs#/)