### Тестовый проект  
  
Настройка окружения  
__docker compose build__  
Команды для запуска   
__docker compose up runserver__ - Запуск django runserver  
__docker compose up autotests__ - Запуск тестов   
__docker exec -it *container_id* python manage.py createsuperuser__ - Создание суперпользователя   
__Адрес админ-панели__ - ```http://127.0.0.1:8000/admin/```
___
#### Примеры вызова апи  
Получение страниц постранично    
```http://127.0.0.1:8000/pages/?page=1&page_size=3```  
  Получение конкретной страницы с контентом    
```http://127.0.0.1:8000/pages/1/```
