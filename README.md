# VetThe.App

**Community-driven comparison of identity security features across SaaS applications**

Quickly compare SSO, SCIM, MFA, and compliance capabilities across popular SaaS apps. Built for security teams, IT admins, and procurement professionals who need to make informed decisions.

---

## 🎯 What We Track

- **SSO**: Support, protocols (SAML, OIDC, OAuth2), and pricing tier
- **SCIM**: User provisioning capabilities (full, partial, or none)
- **MFA**: Support, methods (TOTP, SMS, WebAuthn, etc.), and enforcement options
- **Compliance**: SOC 2 and ISO 27001 certifications
- **Pricing Tiers**: Which features require free, paid, or enterprise plans

---

## 🚀 Quick Start

**View the site:** [vetthe.app](https://vetthe.app) 

**Run locally:**
```bash
git clone https://github.com/prithvikrishnab4u/VetThe.App.git
cd VetThe.App/site
hugo server
# Open http://localhost:1313
```

## Development & Data commands

Generate machine-readable exports and validate data locally:

```bash
python -m venv .venv
.venv/bin/python -m pip install --upgrade pip setuptools wheel
.venv/bin/pip install pyyaml
.venv/bin/python scripts/generate_data.py
.venv/bin/python scripts/validate.py
```

The generated exports appear under `site/static/data/apps.json` and `site/static/data/apps.csv`.


---

## 🤝 Contributing

**No technical knowledge required.** Add apps directly in your browser:

1. Go to [`data/apps/`](data/apps)
2. Click "Add file" → "Create new file"
3. Name it `yourapp.yaml`
4. Copy template from [CONTRIBUTING.md](CONTRIBUTING.md) and fill in
5. Submit → automated validation runs → done!

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 📊 Coverage

Apps tracked across categories:
- **Collaboration** (Slack, Zoom, Miro)
- **Productivity** (Notion, Airtable, Google Workspace)
- **Development** (GitHub, Figma, Linear)
- **Sales & Marketing** (HubSpot, Salesforce)
- **Support** (Zendesk)

[Request an app](https://github.com/prithvikrishnab4u/VetThe.App/issues/new?template=app-request.md) or add it yourself!

---

## 🎨 Features

- Excel-style filtering on any column
- Interactive tooltips on headers
- Mobile responsive
- Auto-validation on every contribution
- Fast static site (no database)

---

## 📋 Data Standards

**Tiers** indicate the **minimum** plan level where features are available:
- `free` - Available without payment
- `paid` - Available on mid-tier plans (Business, Pro, etc.)
- `enterprise` - Top tier only (usually requires sales contact)

**SCIM levels:**
- `full` - Complete SCIM 2.0 (users + groups)
- `partial` - Limited (often read-only or users-only)
- `none` - No SCIM support

All data is verified from official sources and includes a `last_verified` date.

---

## 🛠 Project Structure

```
VetThe.App/
├── .github/workflows/     # Auto-validation
├── data/apps/             # App YAML files
├── schemas/               # Validation schema
├── scripts/               # Validation script
└── site/                  # Hugo site
    └── layouts/partials/  # Modular templates
```

---

## ❓ FAQ

**Why this project?**
Identity features are often hidden behind enterprise pricing. This makes budgeting and comparison difficult.

**How is data verified?**
From official documentation, pricing pages, and security pages. Each app has a `last_verified` date.

**Can I use this for procurement?**
Yes. Compare features, identify required tiers, verify vendor claims, and budget accordingly.

**Found wrong data?**
[Open an issue](https://github.com/prithvikrishnab4u/VetThe.App/issues/new) or submit a PR with corrections.

---

## 📜 License

MIT License. Data provided for informational purposes - always verify with vendors.

---

## 👤 Author

**Prithvi Poreddy**
- Website: [iam.ninja](https://iam.ninja/)
- LinkedIn: [pporeddy](https://www.linkedin.com/in/pporeddy/)
- GitHub: [@prithvikrishnab4u](https://github.com/prithvikrishnab4u)

---
Built with ❤️.
