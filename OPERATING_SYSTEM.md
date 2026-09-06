# Residential Energy Products — Operating System

**Status:** Infrastructure layer. Build now. Product, ZIP, and voice vendor are discovery modules that plug into it — they do not gate it.

**Principle:** Instrument first, discover second, scale third.

**Scope split:**

- Georgia = existing team, installer relationships, execution network. Battery-arbitrage economics didn't close (see [README.md](README.md), [ARCHITECTURE.md](ARCHITECTURE.md)), but the market and fulfillment channel stay open for a different product.
- Florida = market-intelligence discovery. Not committed to "battery lease." FPL had record-low outage frequency in 2025; Duke FL averages ~~64 min outage duration excluding named storms — so "Florida has unreliable power" is not a substantiable universal claim. It does have hurricane exposure, insurance pressure, an active storage ecosystem (Duke's 75+ home Hunter's Creek pilot, 2026; Tesla VPP through SECO Energy paying up to $275/Powerwall/yr), and Tesla's own lease structure proves battery-as-a-service can clear when bundled with backup + fixed-rate electricity + bill credit. FL storage runs ~$12,466 installed for 13 kWh (~~$959/kWh, EnergySage Aug 2026) — not cheap, so product and financing structure both stay open questions.
- Product is unresolved until unit economics + WTP data pick a winner. Candidates: battery backup/resilience, generator alternative, solar+storage, energy-management subscription, storm-prep package, utility/VPP-linked storage, or another product enabled by an existing supplier relationship.
- AI voice vendor is unresolved until Juan selects one. Build a `VoiceProvider` adapter, not vendor-specific logic.

---

## 1. Canonical Lifecycle

```
Traffic/Prospect
 → Lead Captured
 → Contactable
 → Initial Qualification
 → Qualified Lead
 → Human/AI Conversation
 → Assessment Scheduled
 → Assessment Completed
 → Offer Presented
 → Opportunity
 → Credit/Property/Technical Qualification
 → Contract Pending
 → Contract Signed
 → Fulfillment Scheduled
 → Installation/Service Delivery
 → Activated
 → First Payment
 → Retained Customer
 → Referral/Expansion
```

Every stage carries: entry criteria, exit criteria, required fields, owner, SLA, automated actions, conversion metric, aging threshold, failure reason taxonomy, next action. **No lead exists in HubSpot without a defined next action.** A lead with no next action is a bug, not a queue.

| Stage                         | Entry criteria               | Exit criteria                          | Owner                   | SLA                     | Failure reasons                      |
| ----------------------------- | ---------------------------- | -------------------------------------- | ----------------------- | ----------------------- | ------------------------------------ |
| Lead Captured                 | Form/call/DM submitted       | Consent + contact info validated       | Intake agent            | 15 min                  | Invalid phone, duplicate, spam       |
| Contactable                   | Valid phone + consent        | First contact attempt made             | Intake agent            | 4 hrs                   | No consent, DNC match                |
| Initial Qualification         | First contact reached        | ZIP/utility/homeowner status confirmed | Qualification agent     | 24 hrs                  | Renter, wrong territory, unreachable |
| Qualified Lead                | Meets product criteria       | Appointment offered                    | Qualification agent     | Same call               | Not qualified, no budget signal      |
| Human/AI Conversation         | Qualified                    | Appointment booked or declined         | Appointment setter      | 48 hrs                  | Not interested, timing               |
| Assessment Scheduled          | Appointment booked           | Assessment occurs or no-shows          | Scheduler               | Per calendar            | No-show, reschedule loop             |
| Assessment Completed          | Site/property data collected | Offer generated                        | Closer                  | 24 hrs post-assessment  | Technical disqualification           |
| Offer Presented               | Offer generated              | Accepted / countered / declined        | Closer                  | 72 hrs                  | Price objection, timing              |
| Opportunity                   | Verbal interest              | Credit/technical check passes          | Closer                  | 5 days                  | Fails credit/property check          |
| Contract Pending              | Qualification passed         | Contract sent                          | Closer                  | 24 hrs                  | Cold feet                            |
| Contract Signed               | Signature captured           | Fulfillment scheduled                  | Fulfillment coordinator | 48 hrs                  | N/A (terminal success for sales)     |
| Fulfillment Scheduled         | Install date set             | Install occurs                         | Fulfillment coordinator | Per installer capacity  | Permit delay, installer capacity     |
| Installation/Service Delivery | Crew on site                 | System functional                      | Installer               | Per install window      | Technical failure, access issue      |
| Activated                     | System live                  | Customer confirms functionality        | Customer success        | 2 weeks post-install    | Non-functional, customer disputes    |
| First Payment                 | Activation confirmed         | Payment received                       | Billing                 | 30 days post-activation | Payment failure, cancellation        |
| Retained Customer             | 1st payment cleared          | Ongoing                                | Customer success        | Monthly                 | Churn                                |
| Referral/Expansion            | Retained + satisfied         | Referral submitted                     | Customer success        | Ongoing                 | N/A                                  |

---

## 2. System of Record: HubSpot

HubSpot is canonical CRM, not Airtable/Sheets. Event-oriented data model layered on top.

**Objects:** Contact, Property, Lead, Opportunity, Campaign/Source, Call, Conversation, Appointment, Offer, Contract, Installation/Fulfillment, Payment, Referral, Partner, Agent.

**Attribution chain preserved end to end:**
`source → campaign → lead → agent → appointment → opportunity → contract → installation → payment`

A Facebook-group lead stays attributable to that source after becoming a customer. A referral stays attributable to the referring customer/partner through the full chain. This is the #1 thing a spreadsheet-first build loses — don't rebuild it later.

---

## 3. Lead Data Schema

**Captured at intake (minimum):**
first name, last name, phone, email (where available), service/property address, ZIP, acquisition source, campaign, timestamp, consent status, contact permissions, assigned agent, lead status.

**Qualification fields:**
homeowner/renter, property type, utility, approx. monthly electric bill, outage experience, longest recent outage, hurricane/storm concern, existing solar, existing battery, generator ownership, desired backup coverage, financing sensitivity, household size, HVAC dependence, medical/critical-load needs (voluntary disclosure only), preferred contact channel, language, appointment availability.

**Technical/fulfillment fields (collected only once product is relevant, not at intake):**
electrical panel info, service size, solar system info, battery model, roof/install considerations, photos, utility bill, site-survey data.

**Rule:** never force a bill upload before the customer understands why. The bill is a qualification/analysis artifact — not license to make an unsupported savings claim. [Reminder: the Georgia model already proved bill-savings claims require interval data the funnel can't collect — see [ga-battery-economics-do-not-close](ARCHITECTURE.md).]

---

## 4. Event Instrumentation

Every transition emits an event with: timestamp, lead/contact ID, agent ID, source, campaign, channel, stage, outcome, reason code.

```
lead_created · lead_contact_attempted · lead_contacted
consent_captured · sms_opt_in · voice_opt_in
qualification_started · qualification_completed
appointment_booked · appointment_completed
offer_generated · opportunity_created
contract_sent · contract_signed
installation_scheduled · installation_completed
activation_completed · first_payment_received
customer_cancelled · customer_referred
```

This is what makes funnel economics computable instead of anecdotal.

---

## 5. Dashboards

**Executive:** traffic, leads, contact rate, qualification rate, appointment rate, show rate, offer rate, close rate, installation rate, activation rate, first-payment rate, CAC, cost/qualified lead, cost/appointment, cost/signed contract, revenue, gross margin, expected LTV, payback period, refund/cancellation rate, referral rate.

**Channel (Nextdoor, Facebook, Outbound, SMS, AI voice, Chatbot, Referral, Partner):** volume, cost, contact rate, qualification rate, appointment rate, close rate, CAC, revenue, gross margin, time-to-conversion — per channel.

**Agent:** assigned leads, contact attempts, contacts, qualified leads, appointments, shows, offers, contracts, installations, payments, conversion rate, lead aging, overdue follow-ups, opt-outs, complaints. **Never optimize agents on call volume alone — optimize the full revenue chain.**

---

## 6. Go/No-Go Gates

Statistical learning, not vanity targets. Don't hard-code precision before 50–100 meaningful observations — treat initial thresholds as hypotheses, update from observed cohorts.

| Gate                      | Tests                                                       |
| ------------------------- | ----------------------------------------------------------- |
| A — Acquisition viability | Channel produces leads at a measurable, scalable cost       |
| B — Contactability        | Meaningful % of prospects reachable                         |
| C — Qualification         | Leads demonstrate the actual problem + eligibility          |
| D — Sales conversion      | Qualified leads become real opportunities                   |
| E — Fulfillment           | Signed customers are actually installable/serviceable       |
| F — Unit economics        | Expected gross contribution supports CAC + fulfillment cost |
| G — Retention             | Customers remain economically viable post-install           |
| H — Referral              | Satisfied customers produce a measurable secondary channel  |

---

## 7. Unit Economics (the real gate)

```
Expected contribution margin
 − acquisition cost
 − sales cost
 − installation/fulfillment cost
 − financing cost
 − expected cancellation/default cost
 − servicing cost
 = expected customer contribution

CAC ceiling = max acquisition cost compatible with target payback
```

A $60/mo offer is not validated because a customer would accept $60. Needed inputs: hardware cost, installer cost, permitting/interconnection cost, financing cost, software/monitoring cost, maintenance reserve, warranty reserve, CAC, agent comp, cancellation/default assumption, contract term, residual value, tax-credit treatment (note: §25D expired for installs after 2025-12-31; §48E survives for third-party-owned systems — this is why lease/TPO structure is the only 2026-viable path), utility/VPP revenue if applicable, expected lifetime revenue.

**Bootstrap cash-flow constraint:** "first lease funds the next battery" is only valid if the first customer generates enough cash, early enough, to fund the next deployment. Model this as an explicit cash-flow timing constraint, not an annual IRR.

---

## 8. Florida ZIP/Market Intelligence Model

Score every ZIP/utility territory — don't pick from intuition.

**Variables:** utility territory, outage frequency, outage duration, storm/hurricane exposure, historical restoration performance, homeownership %, owner-occupied %, single-family density, property values, household income, electric bill/consumption proxies, existing solar penetration, existing battery penetration, generator penetration, insurance pressure, population growth, housing stock age, HVAC dependence, pool prevalence, EV penetration, utility rate structure, utility storage/VPP programs, installer density, permitting friction, financing availability, competitive density, Spanish-speaking population %, digital reachability, referral/network access.

**Live signal already in hand:** Duke Energy Florida's Hunter's Creek pilot (75+ homes, 2026, Orlando) is evidence of active utility storage infrastructure — not proof it's the best commercial beachhead. FPL's 2025 record-low outage frequency means FPL territory shouldn't be assumed the strongest resilience market by default. Score both against the full variable set before choosing.

---

## 9. Product Discovery Framework

Evaluate at minimum: battery backup/resilience, generator alternative, solar+storage, energy-management subscription, storm-prep package, utility/VPP-linked storage, other supplier-enabled product.

Winner must satisfy: `customer pain × WTP × reachable market × fulfillment capability × acceptable CAC × acceptable gross margin × manageable regulatory risk`.

A product doesn't survive just because we have an installer relationship. A product isn't rejected just because Georgia's arbitrage model didn't close — that was one product's economics, not the market's.

---

## 10. Acquisition Architecture

**Organic/community:** post/ad/content → landing page/chatbot → HubSpot → qualification → explicit consent → CRM → qualification.

**Outbound:** prospect list → compliance check → agent assignment → permitted call → qualification → consent for follow-up channels → SMS/appointment workflow → closer.

**Referral:** customer/partner → referral link/form → attribution → lead creation → qualification → appointment → closed revenue → reward/commission where legally appropriate.

Do not scrape community members or harvest phone numbers from social platforms.

---

## 11. Voice Provider Adapter (vendor-agnostic)

```
VoiceProvider
  initiate_call()
  receive_call()
  transfer_to_human()
  record_disposition()
  capture_consent()
  capture_opt_out()
  schedule_callback()
  retrieve_transcript()
  retrieve_recording_metadata()
  webhook_events()
```

Selected vendor is an implementation behind this interface — swapping vendors doesn't touch the CRM or funnel. AI voice is not equivalent to human outbound calling under TCPA/FCC — artificial/prerecorded voice and telemarketing prerecorded-message rules can add requirements; FTC requires Do-Not-Call procedures and recordkeeping. The contact-policy layer (§12) must exist before AI voice/SMS scales.

---

## 12. Contact-Policy Layer

Per phone number: consent status, consent source, consent timestamp, consent language/version, authorized channel, authorized seller/entity, DNC status, internal DNC status, last contact, next permitted contact, opt-out timestamp, opt-out method.

Opt-outs propagate **globally and immediately** — a "STOP" cannot just silence one agent's workflow. FCC recognizes "stop," "quit," "end," "revoke," "opt out," "cancel," "unsubscribe" as reasonable revocation methods, and revocations must be honored within a reasonable period not exceeding 10 business days.

---

## 13. 10–15 Agent Routing Model

```
Lead intake → Qualification agents → Appointment setters → Closers → Fulfillment coordinator → Customer success/referral
```

At low volume, one person covers multiple roles. At 10–15 agents, separate responsibilities enough that management can pinpoint where conversion breaks.

Routing engine assigns on: geography, product, language, lead source, lead score, availability, agent capacity, stage, specialization.

---

## 14. First-10-Customer Experiment

The first 10 customers are a dataset, not a revenue target. Record per customer: source, ZIP, utility, property profile, problem, offer, price, objections, contact attempts, time-to-contact, time-to-appointment, time-to-close, fulfillment cost, install time, CAC, satisfaction, cancellation risk, referral behavior.

Pattern-match after ~10. Cohort-compare after ~25–50. Algorithmic optimization once volume supports it.

---

## 15. Build Now, Regardless of Open Questions

Not blocking on: final FL ZIP, final product, final installer, final financing partner, final voice vendor.

Build now: HubSpot schema, lifecycle stages, attribution, consent model, agent routing, dashboards, webhook/event model, qualification framework, lead scoring, SLA automation, referral attribution, channel attribution, reporting.

These are reusable infrastructure — they don't change when the product or market does.

---

## 16. Build Order

1. Lifecycle/stage architecture (§1) — this document
2. HubSpot data schema (§2, §3)
3. Event instrumentation (§4)
4. Channel attribution (§2, §10)
5. Lead scoring (derive from §3 qualification fields once first cohort exists)
6. Qualification workflow (§1 stage table)
7. Consent/contact-policy layer (§12)
8. 10–15-agent routing model (§13)
9. Dashboard spec (§5)
10. Unit-economics dashboard (§7)
11. ZIP/market intelligence model (§8)
12. Product-validation framework (§9)
13. Installer/fulfillment handoffs (§1, Fulfillment Scheduled → Installation)
14. Retention workflow (post-signing customer retention playbook — signed lease through first payment)
15. Referral system (§1 terminal stage, §10)
16. First-10-customer operating plan (§14)
17. Go/no-go decision gates (§6)

## Immediate next actions

- [ ] Stand up HubSpot portal with objects from §2 and custom properties from §3
- [ ] Build the 18-stage pipeline from §1 as a HubSpot deal pipeline
- [ ] Wire event instrumentation (§4) via HubSpot workflows + webhooks
- [ ] Build executive + channel + agent dashboards (§5) in HubSpot reporting
- [ ] Stand up contact-policy layer (§12) — this gates any outbound/SMS/voice scale-up
- [ ] Score Florida ZIPs against §8 variable set (data pull: utility outage reports, Census ACS, EnergySage pricing, existing solar/storage penetration data)
- [ ] Build unit-economics model (§7) as a live spreadsheet/Airtable calc feeding the HubSpot deal record
- [ ] Define VoiceProvider interface (§11) in code so vendor selection is a config change, not a rewrite
