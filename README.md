# SIGAI

SIGAI (Summary Interface Generator for AI) is a tool that generates a summary of function signatures and class methods from a given GitHub repository. It can be used as a standalone script or as a module within other Python code.

## Features

- Fetches Python files from a specified GitHub repository.
- Generates concise summaries of function signatures and class methods.
- Excludes `__init__.py` files and files in `tests/` folder by default.
- Optionally includes all files with a verbose flag.
- Supports usage as a command-line tool or as a module.

## Installation

### Using Poetry

1. Clone the repository:

    ```bash
    git clone https://github.com/garrett-griffin/sigai.git
    cd sigai
    ```

2. Install dependencies with Poetry:

    ```bash
    poetry install
    ```

## Usage

### As a Command-Line Tool

To generate a summary of function signatures and class methods from a GitHub repository:

```bash
poetry run python sigai/main.py https://github.com/your_username/your_repository --output summary.txt
```

To include `__init__.py` files and files in `tests/` folder, add the `--verbose` flag:

```bash
poetry run python sigai/main.py https://github.com/your_username/your_repository --output summary.txt --verbose
```

### As a Module

You can also use the `generate_summary` function in your own code:

```python
from sigai import generate_summary

repo_url = "https://github.com/your_username/your_repository"
summary = generate_summary(repo_url, verbose=True)
print(summary)
```

## Testing

The project includes unit tests to ensure the functionality works as expected. Tests are located in the `tests` folder.

To run the tests:

```bash
poetry run python -m unittest discover tests
```

## Continuous Integration

The project uses GitHub Actions for continuous integration. The tests run automatically on every commit and pull request. The configuration is located in the `.github/workflows/ci.yml` file.

## Contributing

Contributions are welcome! Please fork the repository and open a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```

### Summary

This `README.md` provides an overview of the project, instructions for installation, usage examples for both the command-line tool and the module, testing information, and details on continuous integration and contributing. Adjust the repository URL and other specific details as needed for your project.