PROJECT = gitlab_submodule

lint:
	flake8 $(PROJECT) --count --show-source --statistics

test:
	nosetests -v --with-coverage --cover-package=$(PROJECT) tests
