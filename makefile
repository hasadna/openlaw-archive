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

translate:
	cd djang/parsing && ../../venv/bin/python ../manage.py makemessages -l he
	cd djang/parsing && ../../venv/bin/python ../manage.py compilemessages -l he


bot:
	! [[ -d bot ]] || rm -r bot
	mkdir bot
	curl -L 'https://git.org.il/resource-il/openlaw-bot/-/releases/v0.2.22/downloads/openlaw-bot.tar.gz' -s | tar -C bot -zxvf -
