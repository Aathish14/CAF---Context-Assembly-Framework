# Contributing to Context Assembly Framework (CAF)

Thank you for your interest in contributing to CAF! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.

## How to Contribute

### Reporting Bugs

Before reporting a bug, please check if it has already been reported by searching the [issue tracker](https://github.com/your-org/caf/issues).

When reporting a bug, please include:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected vs actual behavior
- Environment details (Python version, OS, CAF version)
- Relevant logs or error messages
- Minimal code sample to reproduce the issue

### Suggesting Enhancements

We welcome feature requests! Please:
1. Check if the feature already exists or is planned
2. Open an issue with the "enhancement" label
3. Describe the problem this feature would solve
3. Provide use cases and examples
4. Consider implementation complexity

### Pull Request Process

1. **Fork** the repository and create a new branch
2. **Follow the development workflow** (see [README.md](README.md#development-workflow))
3. **Write tests** for new functionality
4. **Ensure all tests pass** (`pytest`)
3. **Run code quality checks** (`ruff check .`, `black --check .`, `mypy .`)
4. **Update documentation** if needed
4. **Submit a pull request** with a clear description

## Development Setup

See [README.md](README.md#setup--installation) for detailed setup instructions.

### Quick Start
```bash
# Clone and setup
git clone <repository-url>
cd caf
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Unix/macOS
pip install -r requirements.txt

# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Code quality checks
ruff check .
black --check .
mypy .
```

## Code Style Guidelines

### Python Style
- Follow [PEP 8](https://pep8.org/) with [Black](https://black.readthedocs.io/) formatting (line length: 88)
- Use type hints for all function signatures
- Write Google-style docstrings for public APIs
- Use type hints for all function parameters and return values

### Code Organization
- Keep functions small and focused
- Prefer composition over inheritance
- Use dependency injection for testability
- Follow the existing project structure

### Testing
- Write tests for all new functionality
- Maintain or improve test coverage
- Use descriptive test names
- Test both success and error cases

## Commit Message Guidelines

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>[optional scope]: <description>

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, missing semi-colons, etc.
- `refactor`: Code restructuring without behavior change
- `perf`: Performance improvement
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(core): add variant lineage tracking
fix(db): resolve foreign key constraint issue
docs(api): update API reference documentation
refactor(core): simplify instruction pipeline
```

## Pull Request Checklist

Before submitting a PR, ensure:

- [ ] Tests pass (`pytest`)
- [ ] Code passes linting (`ruff check .`)
- [ ] Code is formatted (`black --check .`)
- [ ] Type checking passes (`mypy .`)
- [ ] Tests added/updated for new functionality
- [ ] Documentation updated if needed
- [ ] Commit messages follow conventional commits
- [ ] No breaking changes without discussion

## Release Process

Releases follow [Semantic Versioning](https://semver.org/):

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create release branch
3. Run full test suite
3. Tag release: `git tag v<version>`
4. Push tags: `git push --tags`
5. Create GitHub release

## Getting Help

- Check existing [issues](https://github.com/your-org/caf/issues)
- Ask questions in [discussions](https://github.com/your-org/caf/discussions)
- Contact maintainers via email

## Recognition

Contributors will be acknowledged in:
- Release notes
- Contributors section of README
- Release announcements

Thank you for contributing to CAF! 🎉