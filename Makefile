PROJECT = gitlab_submodule

lint:
	flake8 $(PROJECT) --count --show-source --statistics

test:
	PYTHON_VERSION=$$(python3 --version) && \
	if echo "$${PYTHON_VERSION}" | grep -q "3.10"; \
	then pytest tests; \
	else nosetests -v --with-coverage --cover-package=$(PROJECT) tests; \
	fi
