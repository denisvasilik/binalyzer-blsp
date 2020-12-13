
test:
	python3 -m pytest -v tests

clean:
	@rm -rf	.coverage \
		*.egg-info \
		.cache \
		dist \
		**/*.pyc \
		build \
		**/__pycache__ \
		docs/_build \
		.pytest_cache \
		cov_html
