# VetThe.App

**Community-driven catalogue of the IAM capabilities of SaaS apps**

Before you roll out a SaaS app, your identity team needs to know: can we connect it to our identity provider, manage accounts automatically, enforce our policies, and see who did what? And which plan do we have to buy to get each of those? VetThe.App answers that for every app, with a link to the source behind each answer.

---

## 🎯 What We Track

Every app has the same 12 capabilities. Six are **core** and shown by default:

| Capability | The question it answers |
|---|---|
| **SSO** | Can users sign in through the company identity provider (SAML or OIDC)? |
| **Enforce SSO** | Can admins require SSO and block password sign-in? |
| **SCIM** | Can an identity provider create, update and deactivate users? |
| **Enforce MFA** | Can admins require MFA for everyone using the app's own login? |
| **Passkeys / keys** | Can users sign in with security keys or passkeys (WebAuthn / FIDO2)? |
| **Audit logs** | Can admins view a log of user and admin activity? |

The rest: JIT provisioning, domain verification, custom roles, group → role mapping, session controls, and API token controls.

For each one we record whether it's supported, the **minimum plan** needed, and the **source** it was checked against. The full definitions live in [`data/schema.yaml`](data/schema.yaml).

---

## 🚀 Quick Start

**View the site:** [vetthe.app](https://vetthe.app)

**Run locally:**
```bash
git clone https://github.com/prithvikrishnab4u/VetThe.App.git
cd VetThe.App/site
npm ci
hugo server
# Open http://localhost:1313
```

## Development & Data commands

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/validate.py        # check every app file against the schema
.venv/bin/python scripts/generate_data.py   # write site/static/data/apps.json and apps.csv
```

---

## 🤝 Contributing

**No GitHub account needed.** On [vetthe.app](https://vetthe.app), click ✎ on any cell to correct a value, or "Add an app" to suggest a new one. Paste the vendor page you read it on and send. It opens a pull request for you.

Prefer GitHub? Add a file to [`data/apps/`](data/apps) using the template in [CONTRIBUTING.md](CONTRIBUTING.md). Validation runs automatically on your pull request.

Either way, one rule: **every value needs a link to the vendor's own page.**

---

## 🎨 Features

- Filter and sort on every capability, and share the filtered view as a URL
- Core capabilities by default, all 12 on demand
- Every verified value links to its source
- Suggest a correction from the page itself, no account needed
- Auto-validation on every contribution
- Fast static site, no database. Raw data at [`apps.json`](site/static/data/apps.json) and [`apps.csv`](site/static/data/apps.csv)

---

## 📋 Data Standards

**Support:** `supported`, `partial`, `not_supported`, `undocumented`, or `not_researched`. `undocumented` means the vendor's own pages were checked and say nothing either way; `not_researched` means nobody has looked yet. Neither is ever shown as "no".

**Tiers** are the **minimum** plan where a capability is available:
- `free`: available without payment
- `paid`: a paid self-serve plan (Pro, Business, Team)
- `enterprise`: top plan only, usually through sales
- `add_on`: sold separately on top of a plan

**Sources:** a value only counts as verified when it has a `source` URL and a `checked` date. Values without a source are shown faded on the site. An app is `published` only when all six core capabilities are researched and every known value has a source.

---

## 🛠 Project Structure

```
VetThe.App/
├── .github/workflows/     # CI and PR validation
├── data/
│   ├── schema.yaml        # capabilities, allowed values, publishing rules
│   └── apps/              # one YAML file per app
├── scripts/               # validate.py, generate_data.py
└── site/                  # Hugo site
    └── layouts/partials/  # table, filters, guide
```

---

## ❓ FAQ

**Why this project?**
IAM capabilities are often locked behind enterprise plans and scattered across docs and pricing pages. That makes vendor reviews slow and budgeting hard.

**How is data verified?**
Each value is checked against the vendor's own pricing page, documentation, or trust center, and the link is stored with it. Faded values on the site don't have a source yet.

**Can I use this for procurement?**
Yes. Compare capabilities, see which plan you need, and follow the source links to confirm with the vendor.

**Found wrong data?**
[Open an issue](https://github.com/prithvikrishnab4u/VetThe.App/issues/new) or submit a PR with the correct value and its source.

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
