# Contributing to Azure MCP Server

Thank you for your interest in contributing to the Azure MCP Server project!

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/azuremcpserver.git
   cd azuremcpserver
   ```
3. **Set up development environment** (see Development Guide)

## Making Changes

### Before You Start
- Check existing issues and PRs to avoid duplication
- Create an issue for major changes to discuss the approach
- Keep changes focused and atomic

### Development Process
1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes:**
   - Follow existing code style and conventions
   - Add appropriate tests
   - Update documentation if needed

3. **Test your changes:**
   ```bash
   python -m pytest src/mcp_server/test_azure_mcp_server.py -v
   ```

4. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Add feature: brief description"
   ```

### Code Standards
- **Python Style**: Follow PEP 8
- **Type Hints**: Use where appropriate
- **Async/Await**: Use proper async patterns
- **Error Handling**: Include comprehensive error handling
- **Documentation**: Add docstrings for public functions

### Testing Requirements
- All new features must include unit tests
- Tests should cover both success and error scenarios
- Maintain or improve test coverage
- Use appropriate mocking for external dependencies

## Submitting Changes

### Pull Request Process
1. **Push your branch** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a Pull Request** with:
   - Clear title and description
   - Reference to related issues
   - Summary of changes made
   - Screenshots if applicable

3. **Respond to feedback** promptly and make requested changes

### Pull Request Guidelines
- Keep PRs focused on a single feature or fix
- Write clear commit messages
- Include tests for new functionality
- Update documentation as needed
- Ensure all checks pass

## Types of Contributions

### Bug Reports
- Use the issue template
- Provide clear reproduction steps
- Include environment details
- Attach relevant logs or error messages

### Feature Requests
- Describe the problem you're trying to solve
- Explain why this feature would be useful
- Provide examples of how it would work

### Code Contributions
- Bug fixes
- New features
- Performance improvements
- Documentation updates
- Test improvements

## Community Guidelines

### Be Respectful
- Use welcoming and inclusive language
- Be respectful of differing viewpoints
- Accept constructive criticism gracefully
- Focus on what's best for the community

### Be Helpful
- Help newcomers get started
- Share knowledge and expertise
- Provide constructive feedback
- Collaborate effectively

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- GitHub contributor graphs

## Questions?

- Create an issue for general questions
- Join discussions in existing issues
- Check documentation first

Thank you for contributing!