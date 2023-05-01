.PHONY: init freeze makemigrations serve lint translate

init:
	virtualenv venv
	venv/bin/pip install -r requirements.txt

freeze:
	venv/bin/pip freeze > requirements.txt

makemigrations:
	venv/bin/python djang/manage.py makemigrations
	venv/bin/python djang/manage.py migrate
serve:
	venv/bin/python djang/manage.py runserver

lint:
	black .
	find djang -type f -path '*/templates/*' | xargs venv/bin/djlint --reformat --warn
	find djang -type f -path '*/templates/*' | xargs venv/bin/djlint --lint

translate:
	cd djang/parsing && ../../venv/bin/python ../manage.py makemessages -l he
	cd djang/parsing && ../../venv/bin/python ../manage.py compilemessages -l he
