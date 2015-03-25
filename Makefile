test:
	python install.py < info.txt
	cat emailInfo.py
	cat nthuoj.ini
	python manage.py bower install
	python manage.py makemigrations
	python manage.py migrate
	python manage.py test
