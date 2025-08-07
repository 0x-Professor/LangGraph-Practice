# Contributing to LangGraph Practice Examples

First off, thank you for considering contributing to LangGraph Practice Examples! We appreciate your time and effort in helping us improve this project.

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

- Ensure the bug was not already reported by searching on GitHub under [Issues](https://github.com/0x-Professor/LangGraph-Practice/issues).
- If you're unable to find an open issue addressing the problem, [open a new one](https://github.com/0x-Professor/LangGraph-Practice/issues/new). 
- Use a clear and descriptive title for the issue.
- Include as much information as possible:
  - A clear description of the issue
  - Steps to reproduce the issue
  - Expected behavior vs actual behavior
  - Screenshots if applicable
  - Your environment (OS, Python version, etc.)

### Suggesting Enhancements

- Open a new issue with the enhancement suggestion
- Clearly describe the enhancement and why it would be useful
- Include any relevant code, mockups, or examples

### Pull Requests

1. Fork the repository and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Development Setup

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/LangGraph-Practice.git`
3. Create a new branch: `git checkout -b my-feature-branch`
4. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
5. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

## Coding Standards

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use type hints where appropriate
- Write docstrings for all public functions and classes
- Keep lines under 88 characters
- Use f-strings for string formatting (Python 3.6+)

## Testing

- Write tests for new features and bug fixes
- Run tests using `pytest`
- Ensure all tests pass before submitting a pull request

## Documentation

- Update documentation for any API changes
- Add examples for new features
- Keep the README up-to-date with any changes

## Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally
- Consider starting the commit message with an applicable emoji:
  - 🎨 `:art:` when improving the format/structure of the code
  - 🐛 `:bug:` when fixing a bug
  - 🔥 `:fire:` when removing code or files
  - 📝 `:memo:` when writing docs
  - 🚀 `:rocket:` when improving performance
  - ✅ `:white_check_mark:` when adding tests
  - 🔒 `:lock:` when dealing with security
  - ⬆️ `:arrow_up:` when upgrading dependencies
  - ⬇️ `:arrow_down:` when downgrading dependencies

## License

By contributing, you agree that your contributions will be licensed under its MIT License.
