develop:
	pip3 install --editable .

develop-uninstall:
	python3 setup.py develop --uninstall

test:
	pytest tests

publish:
	pip3 install twine wheel
	python3 setup.py sdist bdist_wheel
	twine upload --repository testpypi dist/*
	rm -rf build dist .egg uwsgi_prometheus.egg-info
