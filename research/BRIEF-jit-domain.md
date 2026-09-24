# Research brief: JIT provisioning and domain verification

You are researching two IAM capabilities for a set of SaaS apps. **You report findings only. You do not edit any file in the repo.** The main session applies your JSON.

## The two questions

- `jit_provisioning` — Are accounts created automatically on first SSO sign-in? (Also called just-in-time provisioning, auto-provisioning on login, or automatic account creation at first sign-in.)
- `domain_verification` — Can the company verify its email domain and take control of accounts that already use it? (Also called domain capture, domain claiming, verified domains.)

## Sourcing rules, these are strict

- **Only the vendor's own pricing page, docs, help center, or trust center counts.** The URL host must belong to the vendor.
- **Never** use Reddit, review sites, blogs, comparison sites, or an identity provider's documentation. Okta, Entra or JumpCloud describing how to connect to the app is *not* evidence about the app.
- **Never** infer from a keyword match. Two traps seen already: "just-in-time access" on a security page usually means the vendor's own internal ops access, not user provisioning; and a vendor named "Jit" appearing in an integrations list is not JIT provisioning.
- Read enough of the page to be sure the sentence is about *this app provisioning its own users*.
- **You must have actually read the page you cite.** If a fetch returns 403/503 or needs JavaScript, you may NOT cite that URL from a search-result snippet. The answer is `undocumented` with a note saying the host blocked you. This was caught in the pilot: an agent cited a Dropbox help page, including a plan name, that returns 503 to everyone.

## Domain verification: the distinction that matters

The column asks two things together: verify the domain **and** take control of accounts already using it.

- `supported` — verify ownership (usually a DNS TXT record) AND claim, capture or auto-enrol existing users on that domain. Box's Domain Management plus Auto Enrolment, Coda's domain capture, BrowserStack's Domain Capture.
- `partial` — verifies domain ownership, but only to route or enable SSO for it, with no account capture. Cisco Duo does exactly this, and the pilot agent wrongly called it `supported`.
- `not_supported` / `undocumented` — no verification at all.

Same-word traps seen in the pilot, all of which are NOT this capability: an email domain **allowlist** that merely restricts who may log in (Harness, Glean); **email sending** domain setup, DKIM/SPF/DMARC/MAIL FROM (Apollo, Genesys, Gainsight); a **telephony** domain (Five9); a tenant **subdomain** (Drata); and domain **spoofing or typosquatting** protection products (CrowdStrike).
- If you cannot confirm from a vendor page, the answer is `undocumented`. That is a perfectly good, expected result. **Do not guess and do not carry over a plausible-sounding value.**

## Support values

`supported` | `partial` | `not_supported` | `undocumented`

Never return `not_researched`.

- `tier` goes on `supported` and `partial` only, and is FORBIDDEN on the others. One of: `free` | `paid` | `enterprise` | `add_on`. It means the cheapest plan that includes the capability. `paid` means the cheapest paid plan, `enterprise` the top one.
- **Never infer a tier.** A vendor page must name the plan. If the capability is confirmed but no page says which plan it needs, omit `tier` entirely and say so in the notes. That is a normal outcome, not a failure. Do not reason "SSO is usually Enterprise, so this is Enterprise".
- `source` and `checked` are REQUIRED together on everything except `undocumented`, which must have NEITHER.
- `checked` is today's date as `YYYY-MM-DD`.

Note: JIT provisioning only exists where SSO exists. If the app has no SSO, `not_supported` is usually right, with a source showing there is no SSO.

## Budget

Aim for about 4 page fetches per app, 8 at the absolute most. One retry per URL. If a page returns 403/503, needs JavaScript, or needs a login, stop and mark `undocumented` with a note saying why. Do not burn fetches fighting a blocked host.

Good search pattern: `<app name> just-in-time provisioning site:<vendor domain>` and `<app name> verify domain site:<vendor domain>`. The `sso_source` URL in your input is a starting hint, not the answer, and often will not cover these two.

## Output

Return ONLY a JSON array, no prose around it, one object per app you were given. Include every app, even the ones where everything came out `undocumented`.

```json
[
  {
    "id": "aircall",
    "jit_provisioning": {
      "support": "supported",
      "tier": "enterprise",
      "notes": "Accounts are created on first SAML sign-in.",
      "source": "https://help.aircall.io/en/articles/....",
      "checked": "2026-09-24"
    },
    "domain_verification": {
      "support": "undocumented",
      "notes": "Help center has no page on verifying or claiming an email domain."
    }
  }
]
```

Only include a capability key if it was listed in that app's `todo`. `notes` is optional but useful, keep it under 200 characters and factual.
