packages: wheel sdist

wheel:
	rm -Rf build
	./setup.py bdist_wheel

sdist:
	rm -Rf build
	./setup.py sdist
