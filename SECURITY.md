# Security Policy

## 🛡️ Supported Versions

| Version | Supported |
|---------|-----------|
| 1.0.x   | ✅ Yes    |
| < 1.0   | ❌ No     |

---

## 🚨 Reporting a Vulnerability

**Please DO NOT report security vulnerabilities publicly.**

If you discover a security issue:

### 1. Contact Directly

- **Telegram:** [@Vip_Sakil_Bio](https://t.me/Vip_Sakil_Bio)
- **GitHub:** [Private Security Advisory](https://github.com/SakilSakil699/AuraBeats/security/advisories/new)

### 2. Include Details

- Type of vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### 3. Response Time

- **Acknowledgment:** Within 24 hours
- **Initial assessment:** Within 72 hours
- **Fix:** Depends on severity

---

## 🔐 Security Features

### Built-in Protection

- ✅ **Environment variables** for sensitive data
- ✅ **`.gitignore`** prevents credential leaks
- ✅ **SHA-256 integrity** checks
- ✅ **Runtime credit verification**
- ✅ **No hardcoded secrets**
- ✅ **Input validation** on user commands
- ✅ **Rate limiting** on commands
- ✅ **Non-root Docker user**

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

```bash
chmod 600 .env
