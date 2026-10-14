# 🛡️ Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.0.x   | ✅ Yes    |
| < 1.0   | ❌ No     |

---

## 🚨 Reporting a Vulnerability

**Please DO NOT report security vulnerabilities publicly.**

### Contact Directly

- **Telegram:** [@Vip_Sakil_Bio](https://t.me/Vip_Sakil_Bio)
- **GitHub:** [Private Security Advisory](https://github.com/SakilSakil699/AuraBeats/security/advisories/new)

### Include Details

- Type of vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Response Time

| Stage | Time |
|-------|------|
| Acknowledgment | Within 24 hours |
| Initial assessment | Within 72 hours |
| Fix | Depends on severity |

---

## 🔐 Security Features

### Built-in Protection

- ✅ Environment variables for sensitive data
- ✅ `.gitignore` prevents credential leaks
- ✅ SHA-256 integrity checks
- ✅ Runtime credit verification
- ✅ No hardcoded secrets
- ✅ Input validation on user commands
- ✅ Rate limiting on commands
- ✅ Non-root Docker user

### Secrets Management

**Never commit:**

- ❌ `.env` file
- ❌ `session_string.txt`
- ❌ `cookies.txt`
- ❌ API tokens
- ❌ Bot tokens
- ❌ Session strings

All these are protected by `.gitignore`.

---

## ⚠️ Known Limitations

- Bot requires **Telegram account session** (keep it secure)
- **Assistant userbot** has full account access
- **POT server** runs on localhost only
- **No encryption** for local JSON database (recommended: use MongoDB with auth)

---

## 🛡️ Best Practices for Users

### 1. Protect Your `.env`

    chmod 600 .env

### 2. Use Strong Passwords

For MongoDB, Redis, and 2FA on Telegram accounts.

### 3. Revoke Old Sessions

Telegram → Settings → Devices → Terminate old sessions.

### 4. Keep Updated

    git pull origin main
    pip install -r requirements.txt --upgrade

### 5. Monitor Logs

    tail -f data/logs/*.log

---

## 🚫 Out of Scope

The following are **not** considered security vulnerabilities:

- Denial of service via normal bot usage
- Rate limit bypass by Telegram itself
- Issues in third-party dependencies (report to them)
- Social engineering
- Physical access to server

---

<div align="center">

**Stay safe! 🛡️**

Made with ❤️ by **AuraBeatsOfficial**

</div>
