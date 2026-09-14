# Contributing to VetThe.App

**No coding required!** You can add or fix apps directly in your browser.

The one rule: **only record what you can link to.** A value with a source beats a guess every time. If you're not sure, leave it as `"unknown"`.

---

## 🎯 Quick Start (5 Minutes)

### **Easy Way: Use GitHub's Web Editor**

1. **Go to**: https://github.com/prithvikrishnab4u/VetThe.App
2. **Click**: Browse to `data/apps/` folder
3. **Click**: "Add file" → "Create new file"
4. **Name it**: `yourapp.yaml` (e.g., `zoom.yaml`)
5. **Copy the template below** and fill in what you can confirm
6. **Click**: "Propose new file"
7. **Click**: "Create pull request"

**Done!** Validation runs automatically, and we'll review and merge it.

---

## 📋 App Template

Copy this. Every capability starts as `"unknown"`, so change only the ones you've checked.

```yaml
name: "App Name Here"
category: "collaboration"
website: "https://example.com"
description: "What does this app do? One sentence."
status: "draft"

# One block per capability. Field meanings and allowed values: CONTRIBUTING.md
capabilities:
  sso:
    support: "unknown"
  sso_enforcement:
    support: "unknown"
  scim:
    support: "unknown"
  mfa_enforcement:
    support: "unknown"
  phishing_resistant_mfa:
    support: "unknown"
  audit_logs:
    support: "unknown"
  jit_provisioning:
    support: "unknown"
  domain_verification:
    support: "unknown"
  custom_roles:
    support: "unknown"
  group_role_mapping:
    support: "unknown"
  session_controls:
    support: "unknown"
  api_token_controls:
    support: "unknown"
```

---

## 📝 How to Fill It Out

### **1. Basic Info**

```yaml
name: "Zoom"                 # Exact app name
category: "collaboration"    # Pick from the list below
website: "https://zoom.us"
description: "Video conferencing platform"
status: "draft"              # Leave as draft; maintainers publish
```

**Valid categories:** `collaboration`, `productivity`, `development`, `sales_marketing`, `support`, `design`, `hr`, `finance`, `security`, `infrastructure`

---

### **2. A Capability**

Every capability uses the same fields:

```yaml
  scim:
    support: "supported"                     # supported, partial, not_supported, or unknown
    tier: "enterprise"                       # minimum plan: free, paid, enterprise, or add_on
    plan: "Enterprise"                       # optional: the vendor's own plan name
    notes: "Users only, no groups"           # optional: anything that needs explaining
    source: "https://vendor.com/docs/scim"   # page that proves it
    checked: "2026-09-14"                    # the day you checked that page (YYYY-MM-DD, in quotes)
```

**Rules:**
- `tier` only goes on `supported` or `partial`.
- `source` and `checked` always go together.
- `unknown` has nothing else: no tier, no source.
- Put quotes around every value.

**Support levels:**
- `supported`: works as the question describes
- `partial`: works with a real limitation; explain it in `notes`
- `not_supported`: the vendor's docs or pricing show it isn't offered
- `unknown`: not researched yet (the default)

**Tiers**, the **minimum** plan needed:
- `free`: available on the free plan
- `paid`: a paid self-serve plan (Pro, Business, Team)
- `enterprise`: top plan only, usually through sales
- `add_on`: sold separately on top of a plan

---

### **3. What Each Capability Means**

| Key | The question to answer |
|---|---|
| `sso` | Can users sign in through the company identity provider (SAML or OIDC)? Also add `protocols: ["SAML", "OIDC"]` (allowed: `SAML`, `OIDC`, `WS-Fed`). |
| `sso_enforcement` | Can admins require SSO and block password sign-in for all users? |
| `scim` | Can an identity provider create, update and deactivate users over SCIM? Use `partial` for users only, or no deactivation. |
| `mfa_enforcement` | Can admins require MFA for every user who signs in with the app's own login? |
| `phishing_resistant_mfa` | Can users sign in with security keys or passkeys (WebAuthn / FIDO2)? |
| `audit_logs` | Can admins view a log of user and admin activity? Optionally add `retention: "90 days"`. |
| `jit_provisioning` | Are accounts created automatically on first SSO sign-in? |
| `domain_verification` | Can the company verify its email domain and take control of accounts that use it? |
| `custom_roles` | Can admins create roles with custom permissions beyond the built-in ones? |
| `group_role_mapping` | Can roles or team membership be assigned from identity provider groups? |
| `session_controls` | Can admins set session length or sign a user out of all sessions? |
| `api_token_controls` | Can admins see, restrict or revoke API tokens that users create? |

The first six are **core**: they're shown by default, and an app can't be published until all six are researched.

---

## ✅ Complete Example

```yaml
name: "Example App"
category: "development"
website: "https://example.com"
description: "Project tracking for software teams."
status: "draft"

# One block per capability. Field meanings and allowed values: CONTRIBUTING.md
capabilities:
  sso:
    support: "supported"
    tier: "enterprise"
    plan: "Enterprise"
    protocols: ["SAML", "OIDC"]
    source: "https://example.com/pricing"
    checked: "2026-09-14"
  sso_enforcement:
    support: "supported"
    tier: "enterprise"
    source: "https://example.com/docs/enforce-sso"
    checked: "2026-09-14"
  scim:
    support: "partial"
    tier: "enterprise"
    notes: "Users only; groups are not synced"
    source: "https://example.com/docs/scim"
    checked: "2026-09-14"
  mfa_enforcement:
    support: "supported"
    tier: "paid"
    source: "https://example.com/docs/require-2fa"
    checked: "2026-09-14"
  phishing_resistant_mfa:
    support: "not_supported"
    source: "https://example.com/docs/2fa-methods"
    checked: "2026-09-14"
  audit_logs:
    support: "unknown"
  jit_provisioning:
    support: "unknown"
  domain_verification:
    support: "unknown"
  custom_roles:
    support: "unknown"
  group_role_mapping:
    support: "unknown"
  session_controls:
    support: "unknown"
  api_token_controls:
    support: "unknown"
```

---

## 🔍 Where to Find Information

**Best sources (check in this order):**

1. **Pricing page**: the feature comparison table usually shows the plan for SSO, SCIM and audit logs
2. **Admin or security documentation**: search for "SAML", "SCIM", "enforce", "2FA", "audit log", "roles"
3. **Trust or security center**
4. **Identity provider app catalogs** (Okta, Microsoft Entra), useful for protocols and SCIM

**Avoid:**
- Reddit posts (often outdated)
- Review sites (unreliable)
- Blog posts (may be old)
- Marketing pages that don't say which plan

**Not supported needs proof too.** Link the page that shows it's missing, such as a pricing table without the feature. If you simply can't find it, leave it `unknown`.

---

## 📱 Update Existing App

Found wrong info? Easy fix:

1. **Go to**: `data/apps/` folder
2. **Click** on the app file (e.g., `slack.yaml`)
3. **Click**: ✏️ Edit button (top right)
4. **Change the value**, and set `source` and `checked` to the page you checked today
5. **Click**: "Propose changes"

---

## ❓ Not Sure About Something?

**That's okay!** Just:

1. Fill out what you can link to
2. Leave the rest as `"unknown"`
3. Add a comment in your pull request: "Couldn't find SCIM docs"

**Or open an issue first** to discuss before submitting.

---

## 💡 Tips

**Can't tell which plan?**
- Leave `tier` out, and say so in your PR. Don't guess.

**Found conflicting info?**
- Use the vendor's own most recent page, and mention the other source in your PR.

**Validation failed?**
- The PR check lists each problem with the file and capability name. Most failures are a missing quote, or a `tier` on something that isn't supported.

---

## 📬 Questions?

- **Before contributing**: [Open an issue](https://github.com/prithvikrishnab4u/VetThe.App/issues/new)
- **In your PR**: Ask questions in the PR comments
- **General discussion**: [GitHub Discussions](https://github.com/prithvikrishnab4u/VetThe.App/discussions)

---

**Thank you for contributing!** 🎉

Every value you verify helps identity teams make better decisions.
