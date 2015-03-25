test:
	mysql -e 'create database IF NOT EXISTS test_db;' -uroot
	mysql -e "GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost';" -uroot
	python install.py < info.txt
	cat emailInfo.py
	cat nthuoj.ini
	python manage.py bower install
	python manage.py makemigrations
	python manage.py migrate
	python manage.py createsuperuser
	python manage.py test
