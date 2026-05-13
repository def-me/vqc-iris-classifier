# Security Policy

## Reporting Security Vulnerabilities

If you discover a security vulnerability in this project, please **DO NOT** create a public GitHub issue. Instead, please report it responsibly by:

1. **Email**: Send a detailed description to your-email@example.com
   - Include steps to reproduce the vulnerability
   - Include the affected versions
   - Include potential impact assessment

2. **Timeline**: We will:
   - Acknowledge receipt within 48 hours
   - Provide an estimated timeline for a fix
   - Keep you informed of the progress
   - Credit you publicly (if desired) once the fix is released

## Supported Versions

| Version | Status | Support Until |
|---|---|---|
| 1.0.x | Current | Latest |
| < 1.0 | Unsupported | N/A |

Security updates will be provided for the latest version. We encourage all users to upgrade to the latest version to receive security updates.

## Security Best Practices

### For Users
- Keep PennyLane and dependencies updated
- Use virtual environments for isolation
- Avoid sharing trained parameters if they contain sensitive information
- Review input data for anomalies

### For Contributors
- Don't commit credentials or sensitive keys
- Use environment variables for configuration
- Avoid adding external dependencies without review
- Follow CONTRIBUTING.md guidelines
- Use pre-commit hooks to catch issues locally

## Known Security Considerations

1. **Data Privacy**: This project doesn't store data internally, but users should protect their datasets
2. **Quantum Simulation**: The simulator doesn't provide quantum security advantages
3. **Dependencies**: Regularly check for updates to NumPy, scikit-learn, and PennyLane

## Dependency Security

We use automated dependency scanning:
- GitHub Dependabot checks for vulnerable dependencies
- Pre-commit hooks validate code quality
- CI/CD pipeline runs security checks

## Questions?

For security-related questions that don't involve vulnerabilities, open a discussion in the Issues section with the `security` label.

---

**Last Updated**: 2024
