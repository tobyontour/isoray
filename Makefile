run: venv
	./venv/bin/python ray3.py

venv:
	python3 -m venv venv
	./venv/bin/pip install -r requirements.txt

install: venv
