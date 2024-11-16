# Проект магазина продуктов

## Инструкции по развертыванию проекта

1. Клонировать репозиторий
   ```sh
   git clone git@github.com/MarinaKrasnoruzhskaya/grocery_store
   ```
2. Перейти в директорию
   ```sh
   cd grocery_store
   ```
3. Установить виртуальное окружение
   ```sh
   python -m venv env
   ```
4. Активировать виртуальное окружение
   ```sh
   source env/bin/activate
   ```
5. Установить зависимости
   ```sh
   pip install -r requirements.txt
   ```
6. Заполнить файл ```.env.sample``` и переименовать его в файл с именем ```.env```
7. Создать БД ```uds```
   ```
   psql -U postgres
   create database grocery_store;  
   \q
   ```
8. Применить миграции
    ```sh
   python manage.py migrate
    ```
9. Создать суперпользователя
    ```sh
   python manage.py csu
   ```

## Документация проекта:

1. http://127.0.0.1:8000/swagger-ui/
2. http://127.0.0.1:8000/redoc/

## Лицензия:

Этот проект лицензирован по [лицензии MIT](LICENSE)
