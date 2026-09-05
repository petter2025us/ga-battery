# California SAIDI & PSPS Insurance Model

**Question:** Can a battery lease be justified as outage insurance in California, independent of arbitrage?

## California Outage Data (2024-2025)

### SAIDI (System Average Interruption Duration Index)

| Utility   | 2024 SAIDI    | Minutes/Year | Hours/Year     |
| --------- | ------------- | ------------ | -------------- |
| **PG&E**  | 276.4 min     | 276          | 4.6 hours      |
| **SCE**   | Data varies   | ~545 (2025)  | ~9 hours       |
| **SDG&E** | Not disclosed | Est. 300-400 | Est. 5-7 hours |

Note: SAIDI is the average across all customers. High-risk wildfire zones (Kern, LA, Ventura, San Diego foothills) experience **3-5x higher outage exposure**.

### PSPS (Public Safety Power Shutoffs)

| Metric                  | Value                                                |
| ----------------------- | ---------------------------------------------------- |
| **Average duration**    | ~2 days (48 hours); max 6+ days                      |
| **High-risk areas**     | 4-5 PSPS events per year                             |
| **Affected population** | 5-20% of service territory per event                 |
| **Trigger**             | Red flag weather (Santa Ana winds, high fire danger) |
| **Affected utilities**  | SDG&E (highest), SCE, PG&E                           |

**Recent example:** SDG&E December 2024 event hit ~170k customers with Fire Potential Index (FPI) rating of "Extreme" — highest in 5+ years.

---

## Outage Cost Model

### Per-Hour Outage Cost (Residential)

Typical valuations used by utilities and regulators:

| Category                     | Cost/Hour       |
| ---------------------------- | --------------- |
| Opportunity cost (lost work) | $20-40          |
| Comfort & convenience        | $5-10           |
| Food spoilage (refrigerator) | $2-5            |
| Medical/safety risk premium  | $5-20           |
| **Total typical**            | **$30-75/hour** |

**Conservative estimate for model:** $10/hour (residential, non-income-loss, no medical needs)

### Annual Outage Exposure by Territory

#### Low-risk (PG&E, average areas, non-PSPS)

- SAIDI: 276 minutes/year = 4.6 hours
- Annual cost @ $10/hr: **$46/year**

#### Medium-risk (SCE service territory, some PSPS exposure)

- SAIDI: 545 minutes + PSPS risk
- Estimate: 9 hours standard + 1-2 days PSPS per year = 9 + 24-48 hours
- **Low estimate:** 33 hours @ $10/hr = $330/year
- **High estimate:** 57 hours @ $10/hr = $570/year

#### High-risk (SDG&E, San Diego foothills, frequent PSPS)

- SAIDI: ~350 minutes baseline
- PSPS: 4-5 events × 2 days = 8-10 days/year (if affected)
- For affected neighborhoods: 8-10 days = 192-240 hours
- **Low estimate (affected): 200+ hours @ $10/hr = $2,000+/year
- **Average customer (weighted by PSPS probability):** 20% affected × $2,000 = **$400/year**

---

## Insurance Premium Model

### Standard Insurance Markup

Traditional insurance operates at:

- **Expected loss:** The statistical cost of the bad event
- **Insurance premium:** Expected loss × (1 + overhead/profit margin)
- **Typical markup:** 20-50% for this class of risk

### Defensible Insurance Premium for Battery-as-Backup

| Market                          | Annual Outage Cost | Insurance Premium (30% markup) | Max Lease Payment/Month |
| ------------------------------- | ------------------ | ------------------------------ | ----------------------- |
| **Low-risk (PG&E, avg)**        | $46                | $60                            | $5/mo                   |
| **Medium-risk (SCE)**           | $330-570           | $430-740                       | $36-62/mo               |
| **High-risk (SDG&E, affected)** | $2,000             | $2,600                         | $217/mo                 |
| **High-risk (SDG&E, weighted)** | $400               | $520                           | $43/mo                  |

---

## Battery Lease Cost Floor vs Insurance Value

### Lease Economics (from MULTISTATE_COMPARISON.md)

- **Upfront cost:** $13,500 installed
- **Lessor cost after §48E credit:** $9,450 + $4,000 CAC = $13,450
- **Lease floor @ 8% / 25yr:** $87/mo base + $10/mo O&M = **$97/mo = $1,164/year**

### Comparison: What Insurance Can Justify

| Market                                    | Insurance/Year | Gap to Lease Cost     |
| ----------------------------------------- | -------------- | --------------------- |
| **PG&E low-risk**                         | $60            | **-$1,104/year** ❌   |
| **SCE medium-risk**                       | $430-740       | **-$424 to -$734** ❌ |
| **SDG&E high-risk (weighted)**            | $520           | **-$644/year** ❌     |
| **SDG&E high-risk (affected areas only)** | $2,600         | **+$1,436/year** ✓    |

---

## Strategic Insight

### The PSPS Sweet Spot

A battery lease CAN be justified as insurance **but only for high-risk, PSPS-affected neighborhoods** in San Diego County and a few LA/Central Coast foothills areas.

**Affected population:**

- SDG&E service area: ~3.7M customers
- Estimated PSPS-affected (high-risk zones): 5-15% = 185k-550k customers
- Highest concentration: San Diego County east of coast, LA foothills, Kern County

**These customers face:**

- 4-5 PSPS events per year
- ~2-day average shutoff (some 6+ days)
- ~$2,000/year in unmitigated outage costs
- High willingness to pay for insurance

### Not Viable Everywhere

**PG&E customers:** SAIDI 276 min/year = $46 cost. Cannot justify $1,164/year lease even on insurance basis. ❌

**SCE average customers:** SAIDI 545 min/year = $330-570 cost. Still underwater. ❌

**SDG&E average customers (weighted PSPS probability):** $400-520 insurance value. Still underwater. ❌

---

## Operational Model for California

### Step 1: Geographic Precision

**Do NOT target "California" or "SDG&E service area."**

**DO target:** ZIP codes with documented PSPS frequency.

- Use SDG&E's PSPS historical map (psehealthyenergy.org/mapping)
- Focus: San Diego County ZIP 91942, 92021, 92026, 92084 (East County, high PSPS exposure)
- Focus: Los Angeles County 91344, 91355 (Santa Clarita/Santa Monica Mtns, SCE PSPS zone)

### Step 2: Messaging Pivot

**Not:** "Save 30% on your electric bill with arbitrage."  
**Yes:** "Protect your home from PSPS shutoffs. 4-5 power cuts per year in your area. Last one lasted 72 hours."

### Step 3: Price Anchoring

**Insurance basis:**

- Outage cost: ~$2,000/year (high-risk)
- Battery as insurance: $520-1,000/year justified
- **Lease price: $50-80/month** (vs. $97/mo cost floor)

**Requires economics shift:**

- Smaller batteries (8-10 kWh instead of 13.5 kWh) → $100-150/mo cost
- Higher utilization (use for arbitrage + insurance) → recover the delta
- Or: Accept lower margin on insurance-based leases in high-risk ZIP codes

### Step 4: Proof Points

- **Collect PSPS impact data:** Partner with SDG&E or CPUC for risk mapping
- **Track outage impact:** How many of your customers were in affected zones last 12 months?
- **Collect WTP data:** Would you pay $50/mo to avoid 3-day blackouts? $100/mo?

---

## Recommendation

### If Pursuing California Insurance Angle

**Immediate priorities:**

1. Obtain SDG&E PSPS historical frequency by ZIP code (psehealthyenergy.org map)
2. Identify top 20-30 ZIP codes with 4+ PSPS events in last 3 years
3. Run customer willingness-to-pay study in those ZIPs ($500-1k survey)
4. Price battery leases at $50-80/mo in high-risk areas, market as outage insurance
5. Offer smaller battery (8 kWh) if cost-sensitive segment emerges

**If WTP study shows $60-80/mo defensible:**

- Use lower-cost battery (LFP cells have dropped below $80/kWh)
- Margin: narrower, but volume in high-risk areas could offset

**If WTP study shows <$50/mo:**

- Arbitrage path remains closed in California
- Insurance path becomes <25% margin play; evaluate market size

### If NOT Pursuing Insurance Angle

- **Skip California.**
- **Focus on other angles:** Home resilience consulting, contractor partnerships, generator replacement value proposition

---

## Sources

- [PG&E Reliability Reports](https://www.pge.com/en/about/pge-systems/electric-systems/electric-reliability-reports.html)
- [California CPUC Electric Reliability Reports](https://www.cpuc.ca.gov/industries-and-topics/electrical-energy/infrastructure/electric-reliability/electric-system-reliability-annual-reports)
- [PSE Healthy Energy PSPS Mapping](https://www.psehealthyenergy.org/mapping-public-safety-power-shutoffs/)
- [Generator vs Battery Cost Guide](https://heliosenergyglobal.com/guides/generator-vs-battery-backup-california)
