# Краткое описание проекта
Данный проект представляет собой сервис терминологии, который предоставляет следующие методы:
* получение списка справочников;
* получение списка справочников, актуальных на указанную дату;
* получение элементов заданного справочника текущей версии;
* получение элементов заданного справочника указанной версии;
* валидация элементов заданного справочника текущей версии;
* валидация элемента заданного справочника по указанной версии.

В API предусмотрен постраничный вывод результата (данные возвращаются частями по 10 элементов).

К сервису имеется GUI административной части, с помощью которой можно добавлять новые справочники, 
новые версии справочников, указывать дату начала действия и наполнять справочники элементами.

Описание разработанного API с примерами представлено в `documentation.md`.

## Используемые инструменты
* Python 3.8.6
* Веб-фреймворк Django
* База данных SQLite

## Быстрый старт
Чтобы запустить этот проект локально на вашем компьютере: 
1. Настройте среду разработки Python. 
1. Выполните следующие команды: 
    1. установите все необходимые зависимости
    
    ```pip install -r requirements.txt ```
    2. создайте миграции для всех приложений
    
    ```python manage.py makemigrations```
    3. примените созданные миграции к базе
    
    ```python manage.py migrate```
    4. создайте суперпользователя
    
    ```python manage.py createduperuser```
    5. запустите
    
    ```python manage.py runserver```
1. Откройте в браузере `http://127.0.0.1:8000/admin/`, чтобы открыть сайт администратора. 
1. Создайте несколько тестовых объектов каждого типа. 
1. Используя описание разработанного API из `documentation.md`, выполните необходимые запросы.