test:
	mysql -e 'create database IF NOT EXISTS myapp_db;' -uroot
	mysql -e "GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost';" -uroot
	python manage.py test
	#python manage.py collectstatic
