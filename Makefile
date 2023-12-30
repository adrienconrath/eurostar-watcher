_clean-venv:
	rm -rf .venv

_clean-pycache:
	find ./ -name '*.pyc' -delete
	find ./ -name '__pycache__' -delete

_install-pyenv:
	curl https://pyenv.run | bash

_poetry-install:
	@command -v pyenv >/dev/null 2>&1 || { echo >&2 "pyenv not installed. Please run 'make install-pyenv'."; exit 1;}
	pyenv install -s
	poetry install

new-venv: _clean-pycache _clean-venv _poetry-install
