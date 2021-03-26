.DEFAULT_GOAL := all

install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

format:
	black *.py

run:
	python3 app/app.py
	
all: install run
