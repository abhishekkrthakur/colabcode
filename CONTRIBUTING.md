# Contributing
We follow the "fork-and-pull" Git workflow.

1. Fork the *ColabCode* repo from `master` branch
2. Clone the fork locally 
3. Create a branch for local development 
4. When done making changes, make sure that your changes pass [flake8](https://pypi.org/project/flake8/). Also ensure, that your code is formatted using [black](https://github.com/psf/black). 
5. Commit changes to your own branch and push them to your fork
6. Submit a Pull request for review

## Coding Style
The codebase uses 
* [black](https://github.com/psf/black) for code formatting.
* [flake8](https://pypi.org/project/flake8/) for code checking

Install dependencies from *requirements.txt*. Run black -
```python
black .
```

All your changes will be tested. Check `.pre-commit-config.yaml`

