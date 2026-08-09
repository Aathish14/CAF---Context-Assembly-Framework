# Security Policy

## Supported Versions

We release patches for security vulnerabilities. The following versions are currently supported:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of CAF seriously. If you discover a security vulnerability, please report it responsibly.

### How to Report

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, please report security vulnerabilities by emailing **security@your-org.com**.

Please include the following information:
- Type of issue (e.g., SQL injection, XSS, authentication bypass, etc.)
- Full description of the vulnerability
- Steps to reproduce
- Potential impact
- Any proof-of-concept or exploit code (if applicable)
- Suggested fix (if you have one)

### What to Expect

1. **Acknowledgment** - You will receive an acknowledgment within 48 hours
2. **Assessment** - We will assess the vulnerability and determine its severity
3. **Fix Development** - We will develop a fix and coordinate with you on timing
4. **Disclosure** - We will coordinate public disclosure after a fix is released

### Response Timeline

| Severity | Initial Response | Fix Target | Disclosure |
|----------|------------------|------------|------------|
| Critical | 24 hours         | 72 hours   | 30 days    |
| High     | 48 hours         | 1 week     | 30 days    |
| Medium   | 72 hours         | 2 weeks    | 45 days    |
| Low      | 1 week           | 1 month    | 60 days    |

## Security Best Practices for Users

### Configuration
- Always use strong, unique passwords for database access
- Keep `.env` files out of version control
- Use environment-specific configurations
- Regularly rotate secrets and API keys

### Dependencies
- Keep dependencies updated: `pip install -U -r requirements.txt`
- Monitor for security advisories: `pip-audit`
- Review dependency licenses: `pip-licenses`

### Deployment
- Run with least privilege
- Use HTTPS in production
- Enable database encryption at rest
- Implement rate limiting
- Monitor for anomalous activity

## Reporting Security Issues in Dependencies

If you discover a vulnerability in a dependency:
1. Report it to the dependency maintainers
2. Report it to us if it affects CAF
3. Consider workarounds until patched

## Security Best Practices for Contributors

1. **Never commit secrets** - Use `.env` files (gitignored) or secret managers
2. **Validate all inputs** - Never trust user input
3. **Use parameterized queries** - Never concatenate SQL
4. **Principle of least privilege** - Minimum permissions necessary
4. **Keep dependencies updated** - Regular updates

## Security Contacts

- **Security Team**: security@your-org.com
- **Maintainers: maintainers@your-org.com

For urgent security issues, please email security@your-org.com with "SECURITY" in the subject line.