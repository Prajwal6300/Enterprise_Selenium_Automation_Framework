# Contributing Guidelines

Thank you for contributing to the **Enterprise Selenium Python Automation Framework**! We welcome bug reports, feature enhancements, documentation updates, and architectural improvements.

---

## 📋 Code of Conduct

Maintain professional, respectful, and constructive communication across all pull requests, code reviews, and issue discussions.

---

## 🛠️ Getting Started & Setup

1. **Fork & Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/Enterprise_Selenium_Python_Automation_Framework.git
   cd Enterprise_Selenium_Python_Automation_Framework
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\Activate.ps1
   ```

3. **Install Dependencies**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

---

## 📐 Coding Standards & Guidelines

- **PEP 8 Compliance**: Follow standard Python code style guidelines (4 spaces indentation, snake_case function names, PascalCase class names).
- **Type Hints**: Annotate all function signatures and return types (`def action(self, arg: str) -> bool:`).
- **Docstrings**: Provide clear Google-style docstrings for modules, classes, and public methods.
- **Page Object Model (POM)**: Keep element locators encapsulated inside Page classes (`src/pages/`). Never hardcode WebElements inside test scripts (`tests/`).
- **Explicit Synchronization**: Use `WaitHelper` for element waits. **Never use `time.sleep()`**.
- **Logging**: Log informative debug and info messages using `get_logger(__name__)`.
- **Assertions**: Always provide descriptive error messages in assertions (`assert condition, "Descriptive failure message"`).

---

## 🧪 Running Tests Locally

Before submitting a Pull Request, verify that all test suites pass cleanly:

```bash
# Run full suite headlessly
pytest --browser=chrome --headless

# Run smoke suite
pytest -m smoke --browser=chrome --headless

# Run API suite
pytest -m api

# Run DB suite
pytest -m db
```

> The suite contains **181 collected test cases**. Verify your changes collect cleanly with `pytest --collect-only -q` before opening a PR.

---

## 🔀 Submitting Pull Requests

1. Create a feature branch (`git checkout -b feature/amazing-feature`).
2. Commit your changes with concise messages (`git commit -m 'feat: Add checkout discount verification'`).
3. Push to your branch (`git push origin feature/amazing-feature`).
4. Open a Pull Request targeting the `main` branch. Provide a clear description of changes and test verification output.

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).
