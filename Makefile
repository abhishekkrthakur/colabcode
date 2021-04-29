style:
	black --line-length 89 --target-version py38 .
	isort .

install:
	pip install .
