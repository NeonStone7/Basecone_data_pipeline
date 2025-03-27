TEST_FOLDER = tests/

unit-tests:
	python3 -m unittest discover $(TEST_FOLDER)
	