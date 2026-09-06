# Technical Overview — Georgia Backup-Power Funnel

**Purpose:** single reference tying together the frontend that's actually live, the data it writes, and the marketing/sales discipline that governs what it's allowed to say. Read this before touching the landing page, the call script, or ad copy — it's the point where all three have to stay consistent.

---

## 1. What's live right now

| Page             | URL                                                                  | ZIP   | Status                                          |
| ---------------- | -------------------------------------------------------------------- | ----- | ----------------------------------------------- |
| Milton, GA       | https://claude.ai/code/artifact/99c53ae3-a04b-42c1-9492-61ef7b220a0d | 30004 | **Active** — current beachhead                  |
| Clermont, FL     | https://claude.ai/code/artifact/225a6562-6d2a-4299-bc21-df223ecc14c2 | 34711 | Deprioritized, left live, no traffic being sent |
| Dr. Phillips, FL | https://claude.ai/code/artifact/fc245a8c-73aa-4602-8dd2-b2abca4f9c4a | 32836 | Deprioritized, left live, no traffic being sent |

Source for all three now lives in this repo under `landing-pages/` — previously the canonical copy only existed in a session-local scratch directory and on the published Artifact itself, which meant the repo was not actually the source of truth. That's fixed as of this commit.

```
landing-pages/
├── active/
│   └── milton.html          ← canonical source for the live Milton page
└── archive-florida/
    ├── clermont.html        ← FL pages kept for the record, not in use
    └── drphillips.html
```

**To update a live page:** edit the file in `landing-pages/`, then publish it via the Artifact tool against its existing URL (never create a new artifact for an existing page — that orphans the URL already shared in ad copy and Nextdoor posts). Commit the file change to this repo in the same pass so the repo and the live page never drift apart again.

---

## 2. Frontend architecture

Each page is a single self-contained HTML file — no build step, no framework, no external JS dependencies beyond Google Fonts. This is deliberate: these are lead-capture pages with a short shelf life per test, not a product surface, so the fastest edit-publish loop matters more than componentization.

- **Fonts:** Fraunces (display/headline), Source Serif 4 (body), IBM Plex Mono (labels/eyebrow/data). Loaded via Google Fonts `<link>`, the one external stylesheet host the artifact CSP allows.
- **Theming:** full light/dark token system per [artifact-design](../../..) conventions — `:root` carries the light palette, `@media (prefers-color-scheme: dark)` and `:root[data-theme="dark"]` redefine the same token set. Never a color hardcoded outside the token block.
- **Layout:** hero contains the offer copy and the lead form side-by-side on desktop, stacked on mobile — the form is visible without scrolling, which was a deliberate simplification after the first draft buried it below three sections (see §4).
- **State:** none client-side beyond the form. No routing, no client framework.

### Runtime capability: `db`

Each page declares `capabilities: {"db": {}}` and writes submissions to a `leads` collection via:

```js
const db = await claude.use("db").catch(() => null);
...
await db.collection("leads").doc(id).set(payload);
```

This is what lets a submission be read back later (`Artifact` tool, `action: "read_db"`) without a separate backend. `db` is null-checked throughout — if the capability fails to resolve, the form still no-ops gracefully rather than throwing.

### Lead schema (as actually written, per page)

Milton (`track: "milton-gapower-30004"`):

```json
{
  "name": "string",
  "phone": "string",
  "bill": "$100 – $150 | $150 – $250 | $250 – $400 | $400+",
  "zip": "string",
  "track": "milton-gapower-30004",
  "inZip": true,
  "consent": true,
  "submittedAt": "ISO 8601"
}
```

Clermont/Dr. Phillips (`track: "clermont-seco-34711"` / `"drphillips-duke-32836"`) — same shape minus `bill`, which was added for Milton to match the requested phone-close flow (name + phone + bill amount, per Justin's original request).

**Known schema inconsistency, worth fixing before a fourth ZIP page:** the FL pages don't collect bill amount, Milton does. If more Georgia ZIPs get their own pages, standardize on Milton's shape (`name, phone, bill, zip, track, inZip, consent, submittedAt`) so cross-ZIP analysis doesn't require reconciling two shapes.

### Reading current leads

```
Artifact({ action: "read_db", url: "<page URL>", db_op: "list", collection: "leads" })
```

Each page's `leads` collection is independent — there is no cross-page query today. Aggregating across ZIPs means three separate reads.

---

## 3. Marketing content — what's substantiated vs. what isn't

This is the part that actually matters and the part most likely to drift if someone other than this conversation edits the copy later, so it's spelled out explicitly.

### The claim discipline that governs every page

| Claim                                                                                                         | Status                                                                                                                             | Where it's allowed                                                                                                                                                                                                                             |
| ------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "$0 out of pocket"                                                                                            | **Substantiated** — true today, no confirmation pending                                                                            | Headline, safe to say anywhere, on the page or on a call                                                                                                                                                                                       |
| "25-year lease"                                                                                               | **Substantiated** — this is the product structure                                                                                  | Anywhere                                                                                                                                                                                                                                       |
| Backup power / storm resilience framing                                                                       | **Substantiated** — tied to real, dated, county-level outage events (§2 of [ATLANTA_METRO_STRATEGY.md](ATLANTA_METRO_STRATEGY.md)) | Anywhere                                                                                                                                                                                                                                       |
| "May qualify for a new Georgia Power storage incentive program (confirmed on your call, not guaranteed here)" | **Deliberately hedged** — the incentive is real (PSC-approved, $750–$1,000/kW) but two eligibility questions are unconfirmed       | Page copy only in this hedged form; **never a specific dollar figure** in ad copy, video, or call script until confirmed                                                                                                                       |
| Any specific bill-savings number (e.g. the rejected "$145/mo average savings")                                | **Rejected, do not use**                                                                                                           | Nowhere. This repo's own model shows the battery loses money on bill savings ($459/yr earned vs. $1,164+/yr lease cost) — a savings claim here is not a copywriting choice, it's a false statement contradicted by this project's own analysis |

**The one rule that supersedes all ad-copy and video-script decisions:** no dollar amount tied to the Georgia Power incentive reaches a prospect — on the page, in a video, or on a call — until the two open questions in [ATLANTA_METRO_STRATEGY.md §1](ATLANTA_METRO_STRATEGY.md) are confirmed:

1. Does the incentive require pairing with new solar PV, or does storage-only qualify? (Current evidence: likely requires PV pairing, per five independent sources — not yet a legal confirmation.)
2. Does a third-party-owned/leased system qualify, or only a customer-owned one? (Genuinely unconfirmed, no signal either way.)

### Call-script guidance (for whoever is closing, OTP or otherwise)

If a prospect asks about the incentive:

> "Georgia Power has a new program that may help cover part of the system cost. We're confirming the exact terms right now — I'll have a clear answer for you before installation, and it won't change your $0-out-of-pocket lease price either way."

If a prospect asks "do I need solar panels too?":

> "Possibly — we're confirming that detail with Georgia Power and will know before your install."

Neither of these promises a number or a mechanism. Both are true statements given what's actually known today. Do not improve on these until §1's open questions close.

### Video section

The Milton page's "See how it works" section is wired for a video (YouTube/Vimeo embed URL or direct file link) but currently shows a "Video coming soon" placeholder — no video has been generated, and no video-generation tool is available in this workflow. To wire one in: set `VIDEO_URL` at the top of the page's `<script>` block and republish.

**Whatever script the AI video uses must pass the same claim discipline as the page and the phone script above** — if the video promises a specific incentive dollar figure or a bill-savings number, it creates the exact deceptive-advertising exposure this project has been built specifically to avoid. Route any video script past this document before recording.

---

## 4. Design decisions worth remembering (so they don't get silently reverted)

- **Form lives in the hero, not below a scroll.** First draft buried it below three sections; visitors shouldn't have to scroll to act. Applies to any new ZIP page.
- **3 fields, not 6.** Email and address are collected on the actual call, not the form — cuts friction, and the call is a more natural place to ask anyway.
- **No fabricated testimonials.** An earlier draft included a "paraphrased for illustration" quote; removed because a fabricated quote is a bigger credibility risk than the persuasion it added.
- **No decorative graphics that cost the visitor interpretation effort.** An earlier draft had a cone-of-uncertainty-style storm graphic; cut for the same reason as the testimonial — it looked distinctive but made the visitor do work with no functional payoff.
- **ZIP field defaults to the page's target ZIP and validates live** (`✓ in service area` / `outside current area, we'll still note your info`) — never hard-blocks a submission from outside the target ZIP, since spillover interest is useful signal.

---

## 5. Open technical/operational items

- [ ] **Confirm the two Georgia Power incentive eligibility questions** (§1 of ATLANTA_METRO_STRATEGY.md) — needs an actual phone call, which nothing in this toolchain can place. This is the single highest-priority open item across the whole project.
- [ ] **Standardize the lead schema** across FL and GA pages if a fourth ZIP page gets built (see §2).
- [ ] **No cross-page/cross-ZIP lead aggregation exists.** If volume grows past a couple of ZIPs, this needs a real answer — either a shared collection keyed by ZIP, or a lightweight script that reads all known page URLs and merges results.
- [ ] **Video script review process** — establish who signs off on the AI video's script against §3's claim discipline before it's produced, not after.
- [ ] **Installer relationship confirmation for the Milton/North Fulton corridor specifically** — this repo has asserted "installers already in place in Georgia" as the rationale for the pivot, but hasn't verified that coverage extends to 30004/30005/30075 specifically as opposed to wherever the original Georgia arbitrage analysis was scoped.

---

## 6. Repo map (current)

```
ga-battery/
├── README.md                          Original GA arbitrage economics (foundational, still valid)
├── ARCHITECTURE.md                    TOU model generalization notes
├── MULTISTATE_COMPARISON.md           GA/CA/TX/FL arbitrage comparison (historical)
├── SAIDI_INSURANCE_MODEL.md           Outage-cost/insurance-value model (CA-focused, historical)
├── ORLANDO_ANALYSIS.md                OUC Orlando viability (historical, FL-specific)
├── WTP_VALIDATION_PLAN.md             Original $8-15k survey plan (superseded by bootstrap model)
├── OPERATING_SYSTEM.md                Full CRM/lifecycle/funnel infrastructure spec (product-agnostic)
├── BOOTSTRAP_PRESALES_PLAN.md         Zero-capital pre-sales model
├── BOOTSTRAP_QUICK_START.md           One-page bootstrap reference
├── WEEK_1_ACTION_PLAN.md              Day-by-day launch checklist (FL-originated, playbook still applies)
├── LANDING_PAGE_COPY.md               Original FL landing-page copy source
├── AD_COPY_VARIATIONS.md              Original FL ad copy source
├── CARRD_SETUP_TONIGHT.md             Carrd setup notes (superseded by Artifact-based pages)
├── FLORIDA_ZIP_INTELLIGENCE.md        FL territory research — DEPRIORITIZED
├── ORLANDO_ZIP_DRILLDOWN.md           FL ZIP-level scoring — DEPRIORITIZED
├── FLORIDA_ORGANIC_TRAFFIC_COPY.md    FL Nextdoor/FB copy — DEPRIORITIZED
├── ATLANTA_METRO_STRATEGY.md          Current active market research — GA/Atlanta
├── TECHNICAL_OVERVIEW.md              This file
├── landing-pages/
│   ├── active/milton.html             Canonical source, live GA page
│   └── archive-florida/*.html         Canonical source, deprioritized FL pages
└── engine/                            Python tariff/breakeven/lease models
```
