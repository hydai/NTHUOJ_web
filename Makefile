test:
	python install.py
	python manage.py makemigrations
	python manage.py migrate
	python manage.py test
	#python manage.py collectstatic
