#!/bin/sh
echo "##### НАЧИНАЕМ РАБОТУ #####"
echo "### 1. Выполняем миграции ###"
python manage.py migrate
echo "??? 2. Будем загружать тестовые данные? ('Д/н' или 'Y/n' ) "
read yesno
if [ "$yesno" = "д" ] || [ "$yesno" = "y" ] || [ "$yesno" = "" ] || [ "$yesno" = "Y" ] || [ "$yesno" = "Д" ]
then
	echo "### 2. Загружаем тестовые данные ###"
	python manage.py loaddata dump.json
fi
echo "??? В тестовых данных суперпользователь уже создан:"
echo "??? логин: admin, пароль: adminpassword"
echo "??? 3. Будем создавать суперпользователя? ('Д/н' или 'Y/n' ) "
read  yesno
if [ "$yesno" = "д" ] || [ "$yesno" = "y" ] || [ "$yesno" = "" ] || [ "$yesno" = "Y" ] || [ "$yesno" = "Д" ]
then
	echo "### 4. Создаём суперпользователя ###"
	python manage.py createsuperuser
fi
echo "##### ЗАПУСКАЕМ СЕРВЕР #####"
echo "##### сайт: http://127.0.0.1/"
echo "##### админка: http://127.0.0.1/admin/"
python manage.py runserver
