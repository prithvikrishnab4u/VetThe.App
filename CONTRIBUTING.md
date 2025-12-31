# Contributing to VetThe.App

**No coding required!** You can add apps directly in your browser.

---

## 🎯 Quick Start (3 Minutes)

### **Easy Way: Use GitHub's Web Editor**

1. **Go to**: https://github.com/prithvikrishnab4u/VetThe.App
2. **Click**: Browse to `data/apps/` folder
3. **Click**: "Add file" → "Create new file"
4. **Name it**: `yourapp.yaml` (e.g., `zoom.yaml`)
5. **Copy the template below** and fill it out
6. **Click**: "Propose new file"
7. **Click**: "Create pull request"

**Done!** We'll review and merge it.

---

## 📋 App Template

Copy this and fill in the blanks:

```yaml
name: "App Name Here"
category: "collaboration"
website: "https://example.com"
description: "What does this app do? One sentence."

sso:
  supported: true
  protocols: ["SAML"]
  tier: "paid"

scim:
  supported: "none"
  tier: "enterprise"

mfa:
  supported: true
  types: ["TOTP", "SMS"]
  enforcement: "admin_enforced"
  tier: "paid"

compliance:
  soc2: true
  iso27001: false

meta:
  last_verified: "2025-12-31"
  ready_to_publish: true
```

---

## 📝 How to Fill It Out

### **1. Basic Info**

```yaml
name: "Zoom"  # Exact app name
category: "collaboration"  # Pick from list below
website: "https://zoom.us"
description: "Video conferencing platform"
```

**Valid categories:**
- `collaboration` (Slack, Teams, Zoom)
- `productivity` (Notion, Airtable, Google Workspace)
- `development` (GitHub, Figma, Linear)
- `sales_marketing` (HubSpot, Salesforce)
- `support` (Zendesk, Intercom)
- `design` (Figma, Canva)
- `hr` (BambooHR, Workday)
- `finance` (QuickBooks, Expensify)

---

### **2. SSO (Single Sign-On)**

Does the app let you login with your company's identity provider (Okta, Azure AD, Google)?

```yaml
sso:
  supported: true              # true or false
  protocols: ["SAML", "OIDC"]  # Which protocols? SAML, OIDC, OAuth2
  tier: "paid"                 # Which plan? free, paid, or enterprise
```

**How to find this:**
- Google: "[app name] SAML setup"
- Check their pricing page
- Look in Settings → Security → SSO

**Tier guide:**
- `free` = Available on free plan
- `paid` = Available on Business/Pro/Plus plans (mid-tier)
- `enterprise` = Only on Enterprise/Ultimate (top tier)

---

### **3. SCIM (User Provisioning)**

Can you automatically create/delete users in this app from your identity provider?

```yaml
scim:
  supported: "full"      # full, partial, or none
  version: "2.0"         # Only if full or partial
  tier: "enterprise"     # Which plan?
```

**Support levels:**
- `full` = Create, update, delete users AND groups automatically
- `partial` = Limited (often read-only or users-only)
- `none` = No SCIM support

**How to find this:**
- Google: "[app name] SCIM"
- Check API documentation
- Look for "User Provisioning" or "Directory Sync"

---

### **4. MFA (Multi-Factor Authentication)**

Does the app support 2FA/MFA?

```yaml
mfa:
  supported: true                      # true or false
  types: ["TOTP", "SMS", "WebAuthn"]  # Which methods?
  enforcement: "admin_enforced"        # How is it enforced?
  tier: "free"                         # Which plan?
```

**MFA types:**
- `TOTP` = Authenticator apps (Google Authenticator, Authy)
- `SMS` = Text message codes
- `Email` = Email codes
- `WebAuthn` = Hardware keys (YubiKey) or biometrics
- `Push` = Mobile app push notifications

**Enforcement options:**
- `none` = Not supported
- `optional` = Users can enable it themselves
- `admin_enforced` = Admins can require it for everyone
- `required` = Always mandatory

**How to find this:**
- Google: "[app name] two-factor authentication"
- Check Settings → Security → 2FA

---

### **5. Compliance**

Does the app have these certifications?

```yaml
compliance:
  soc2: true       # true or false
  iso27001: false  # true or false
```

**How to find this:**
- Check their website footer for "Security" or "Trust Center"
- Google: "[app name] SOC 2" or "[app name] ISO 27001"

---

### **6. Verification Date**

```yaml
meta:
  last_verified: "2025-12-31"  # Today's date (YYYY-MM-DD)
  ready_to_publish: true
```

**Always use today's date** so we know the data is current.

---

## ✅ Complete Example

Here's Zoom filled out:

```yaml
name: "Zoom"
category: "collaboration"
website: "https://zoom.us"
description: "Video conferencing and virtual meeting platform"

sso:
  supported: true
  protocols: ["SAML"]
  tier: "paid"

scim:
  supported: "full"
  version: "2.0"
  tier: "enterprise"

mfa:
  supported: true
  types: ["TOTP", "SMS"]
  enforcement: "admin_enforced"
  tier: "free"

compliance:
  soc2: true
  iso27001: true

meta:
  last_verified: "2025-12-31"
  ready_to_publish: true
```

---

## 🔍 Where to Find Information

**Best sources (check in this order):**

1. **Pricing page** - Look for feature comparison table
2. **Documentation** - Search for "SAML", "SSO", "SCIM", "2FA"
3. **Security page** - Often has compliance certifications
4. **Admin settings** - If you have access, check Security settings

**Avoid:**
- Reddit posts (often outdated)
- Review sites (unreliable)
- Blog posts (may be old)

---

## 📱 Update Existing App

Found wrong info? Easy fix:

1. **Go to**: `data/apps/` folder
2. **Click** on the app file (e.g., `slack.yaml`)
3. **Click**: ✏️ Edit button (top right)
4. **Make your changes**
5. **Update**: `last_verified` to today
6. **Click**: "Propose changes"

---

## ❓ Not Sure About Something?

**That's okay!** Just:

1. Fill out what you know
2. Add a comment in your pull request: "Not sure about SCIM support"
3. We'll help research it

**Or open an issue first** to discuss before submitting.

---

## 🚫 Don't Worry About

- ❌ Installing software
- ❌ Running scripts
- ❌ Perfect formatting (we'll fix it)
- ❌ Knowing everything (we'll help)

**Just do your best!** We appreciate any contribution.

---

## 💡 Tips

**Can't find SSO info?**
- Try searching: "[app name] Okta integration"
- Check their Azure AD gallery listing

**Not sure about tier?**
- When in doubt, use `enterprise` (we can correct it later)

**Found conflicting info?**
- Note both sources in your PR comments

---

## 📬 Questions?

- **Before contributing**: [Open an issue](https://github.com/prithvikrishnab4u/VetThe.App/issues/new)
- **In your PR**: Ask questions in the PR comments
- **General discussion**: [GitHub Discussions](https://github.com/prithvikrishnab4u/VetThe.App/discussions)

---

**Thank you for contributing!** 🎉

Every app you add helps security teams make better decisions.