init:
	pip install -r requirements-dev.txt

test:
	tox

check:
	python setup.py check

flake8:
	flake8 --ignore=E501 uwsgi_prometheus

coverage:
	pytest --verbose --cov-report term --cov-report html --cov=uwsgi_prometheus tests

publish:
	pip install twine wheel
	python setup.py sdist bdist_wheel
	twine upload dist/*
	rm -rf build dist .egg uwsgi_prometheus.egg-info
