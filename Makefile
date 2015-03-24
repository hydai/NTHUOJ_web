test:
	python install.py < info.txt
	python manage.py makemigrations
	python manage.py migrate
	python manage.py test
