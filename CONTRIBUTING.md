# Contributing to Krypto Dashboard Web

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/kuranez/krypto-dashboard-web.git`
3. Create a feature branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit with clear messages: `git commit -m "Add: description of your changes"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Open a Pull Request

## Development Setup

### Local Development

```bash
# Install dependencies
pip install -r web/app/requirements.txt

# Run the app
python launch.py
```

### Docker Development

```bash
# Build the image
docker build -t krypto-dashboard-web:dev .

# Run the container
docker run -p 5013:5013 krypto-dashboard-web:dev
```

## Creating New Dashboards

1. Create a new file in `web/dashboards/`
2. Inherit from `BaseDashboard` class
3. Implement the `create_dashboard()` method
4. Set class attributes: `display_name`, `description`, `version`, `author`

Example:
```python
from base_dashboard import BaseDashboard
import panel as pn

class MyDashboard(BaseDashboard):
    display_name = "My Dashboard"
    description = "What this dashboard does"
    version = "1.0"
    author = "Your Name"
    
    def create_dashboard(self) -> pn.Column:
        return pn.Column(
            pn.pane.Markdown("## My Dashboard"),
            # Your components here
        )
```

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to classes and functions
- Keep functions focused and concise

## Testing

Before submitting a PR:
- Test your dashboard in the application
- Ensure no errors in the browser console
- Verify responsive design
- Test with and without API keys

## Pull Request Guidelines

- Provide a clear description of changes
- Reference any related issues
- Include screenshots for UI changes
- Update documentation if needed
- Ensure CI/CD passes

## Questions?

Open an issue or start a discussion on GitHub.
