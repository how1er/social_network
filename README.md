# yatube
Социальная сеть для публикации личных дневников

### Как запустить проект
1. Перейти в корневую папку проекта(social_network)
```
cd <путь к папке>
```
3. Устанавливать виртуальное окружение (если уже установлено идем дальше)
```
pip install virtualenv
```
3. Создаешь новое окружение
```
virtualenv venv
```
4. Активируем его
```
source venv/scripts/activate
```
5. Устанавливаем все библиотеки
```
pip install -r requirements.txt
```
6. Переходим в директорию yatube
```

```
7. Выполняем миграции
```
python manage.py makemigrations
python manage.py migrate

```
8. Запускаем проект 
```
python manage.py runserver
```
