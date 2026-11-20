# Research brief: custom roles, group → role mapping, session controls, API token controls

You are researching up to four IAM capabilities for a set of SaaS apps. **You report findings only. You do not edit any file in the repo.** The main session applies your JSON.

This brief replaces [BRIEF-jit-domain.md](BRIEF-jit-domain.md) for these four columns. The sourcing rules are the same; what changes is where the answers live. JIT and domain verification usually sit on the one SSO page. These four do not:

| Capability | Where it usually lives |
|---|---|
| `custom_roles` | Admin guide: "roles and permissions", "user roles", "permission sets" |
| `group_role_mapping` | The SCIM page (groups section) or the SAML page (attribute mapping) |
| `session_controls` | Security settings, authentication policy, or admin console page |
| `api_token_controls` | Developer docs on API keys / personal access tokens, or the admin security page |

Expect more fetches per app than the JIT run and a lower hit rate. `undocumented` will be common. That is fine.

## The four questions, and where `partial` starts

Every agent error in the last run landed on the `partial` boundary. So each boundary is spelled out here. When a case sits between two values, write down what you saw in `notes` and pick the lower one.

### `custom_roles` — Can admins create roles with custom permissions beyond the built-in ones?

- `supported` — an admin creates a **new, named role** by choosing individual permissions, and assigns it to users.
- `partial` — permissions can be adjusted but not packaged as a new role: toggling a few settings on a built-in role, custom roles for only one sub-product or area (for example billing only), or a fixed small menu of "custom" admin roles with preset scopes.
- `not_supported` — the vendor lists a fixed set of roles and says that is all.

Traps: custom **fields** or custom **user attributes**; user **groups** or teams that carry no permissions; job-title "roles" in a directory or org chart; **delegated admin** that only picks from preset admin roles (that is `partial` at most); roles inside a customer-facing product the app sells (a CMS's reader roles, a helpdesk's end-customer roles) rather than roles for the app's own staff users.

### `group_role_mapping` — Can roles or team membership be assigned from identity provider groups?

- `supported` — IdP groups (pushed by SCIM, or sent as a SAML/OIDC attribute) **set a role, or put the user in a team, project or workspace that grants access**, and stay in sync.
- `partial` — one of: the role comes from the IdP only at first sign-in and is not updated after; groups sync into the app but only as labels or mention lists that carry no access; only one fixed attribute works (for example an "is admin" flag) rather than general mapping.
- `not_supported` — the SCIM page says groups are not supported, or roles must be set in the app by hand.

Traps: SCIM that syncs **users only** is not this capability, even though the page mentions groups in the IdP; an IdP's own docs about "assigning the app to a group" (that is who may sign in, not their role in the app, and IdP docs never count anyway); Slack-style user groups used for @mentions.

### `session_controls` — Can admins set session length or sign a user out of all sessions?

- `supported` — an admin can set a session length or idle timeout for the organisation, **or** an admin can end another user's active sessions. Either one is enough; say which in `notes`.
- `partial` — a narrow version: the timeout applies only to the admin console, only on mobile, only via a support ticket, or admins can sign out everyone at once but cannot set a length (or the reverse at user level only).
- `not_supported` — the vendor says session length is fixed and not configurable.

Traps: users signing out **their own** other devices is not an admin control (`undocumented` unless an admin version exists); a session length that is **only** set in the IdP ("the app honours your IdP's session") is not the app's control; and the word "session" means something else in many products: meeting or webinar sessions (Zoom, Webex), **session replay** in analytics (Amplitude, Mixpanel, Pendo, FullStory), remote support sessions (TeamViewer), training sessions (LMS apps), and privileged access sessions in PAM products.

### `api_token_controls` — Can admins see, restrict or revoke API tokens that users create?

- `supported` — an admin can do at least one of these **to tokens other users created**: list them, revoke them, block users from creating them, or set a maximum lifetime or scope. Say which in `notes`.
- `partial` — only an all-or-nothing switch that turns API access off for the whole org, or revoking a token happens only as a side effect of deactivating the user.
- `not_supported` — the docs say only the token's creator can see or revoke it and admins have no control.

Traps: an admin managing **their own** org-level API key is not this capability; OAuth **app** approval (which third-party apps may connect) is a different control, so only count it if user-created tokens are also covered; rate limits are not controls; the API reference listing an endpoint that revokes tokens counts only if an admin can use it on other users' tokens.

## Sourcing rules, these are strict

- **Only the vendor's own pricing page, docs, help center, or trust center counts.** The URL host must belong to the vendor.
- **Never** use Reddit, review sites, blogs, comparison sites, or an identity provider's documentation. Okta, Entra or JumpCloud describing how to connect to the app is *not* evidence about the app.
- **Never** infer from a keyword match. Read enough of the page to be sure the sentence is about *this app's admins controlling this app's users*.
- **You must have actually read the page you cite.** If a fetch returns 403/503 or needs JavaScript, you may NOT cite that URL from a search-result snippet. The answer is `undocumented` with a note saying the host blocked you.
- **The cited page must be about the capability you are citing it for.** A page about SCIM user sync proves nothing about roles; a page about SSO proves nothing about API tokens. The last run had two agents cite a page about a different feature to justify `not_supported`.
- **Absence on one page is not `not_supported`.** Use `not_supported` only when a vendor page says the thing cannot be done. Silence is `undocumented`.

## Support values

`supported` | `partial` | `not_supported` | `undocumented`

Never return `not_researched`.

- `tier` goes on `supported` and `partial` only, and is FORBIDDEN on the others. One of: `free` | `paid` | `enterprise` | `add_on`. It means the cheapest plan that includes the capability. `paid` means the cheapest paid plan, `enterprise` the top one.
- `plan` is optional: the vendor's own plan name, as the page writes it.
- **Never infer a tier.** A vendor page must name the plan (the feature page itself, or the pricing page's comparison table). If the capability is confirmed but no page says which plan it needs, omit `tier` entirely and say so in the notes. That is a normal outcome. Do not reason "SSO is Enterprise, so roles are too", and do not carry the SCIM tier over to group mapping unless the page says group mapping comes with it.
- `source` and `checked` are REQUIRED together on everything except `undocumented`, which must have NEITHER.
- `checked` is today's date as `YYYY-MM-DD`.

Note: `group_role_mapping` needs SSO or SCIM to exist. If the app has neither, `not_supported` is usually right, with a source showing there is no SSO or SCIM.

## Budget

Aim for about 6 page fetches per app, 10 at the absolute most. One retry per URL. If a page returns 403/503, needs JavaScript, or needs a login, stop fetching that host and mark what is left `undocumented` with a note saying why. Do not burn fetches fighting a blocked host.

Good search patterns, one per capability:

- `<app> custom roles permissions site:<vendor domain>`
- `<app> SCIM groups roles site:<vendor domain>`
- `<app> session timeout admin site:<vendor domain>`
- `<app> API token admin revoke site:<vendor domain>`

The `sso_source` and `scim_source` URLs in your input are starting hints. The SCIM page often answers `group_role_mapping`; it rarely answers the other three.

## Output

Return ONLY a JSON array, no prose around it, one object per app you were given. Include every app, even the ones where everything came out `undocumented`.

```json
[
  {
    "id": "example",
    "custom_roles": {
      "support": "supported",
      "tier": "enterprise",
      "plan": "Enterprise",
      "notes": "Admins build roles from individual permissions.",
      "source": "https://help.example.com/roles",
      "checked": "2026-09-27"
    },
    "group_role_mapping": {
      "support": "partial",
      "notes": "Role set from a SAML attribute at first sign-in only; not updated after. No page names the plan.",
      "source": "https://help.example.com/saml",
      "checked": "2026-09-27"
    },
    "session_controls": {
      "support": "undocumented",
      "notes": "Security settings page covers 2FA and IP allowlist only."
    }
  }
]
```

Only include a capability key if it was listed in that app's `todo`. `notes` is optional but useful, keep it under 200 characters and factual.
