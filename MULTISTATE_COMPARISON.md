# Multi-State Battery Arbitrage Analysis

## Summary Table

| State          | Utility          | Peak Rate | Off-Peak | Spread    | Battery Earnings/yr | Lease Floor/yr | Gap/mo | Viable?     |
| -------------- | ---------------- | --------- | -------- | --------- | ------------------- | -------------- | ------ | ----------- |
| **Georgia**    | Georgia Power OA | 29.79¢    | 2.19¢    | **27.6¢** | $459                | $1,044         | -$49   | ❌ NO       |
| **California** | SDG&E TOU-ELEC   | 65¢       | 28¢      | **37.0¢** | $634                | $1,044         | -$34   | ❌ MARGINAL |
| **Texas**      | ERCOT Retail TOU | 22¢       | 7.5¢     | **14.5¢** | $214                | $1,044         | -$69   | ❌ NO       |
| **Florida**    | FPL RTR-1        | 26¢       | 9¢       | **17.0¢** | $282                | $1,044         | -$63   | ❌ NO       |

## Assumptions

- Baseline: $250/mo electric bill (~1,411 kWh/mo)
- Load shape: 20% peak, 22% super off-peak (unmeasured assumption)
- Battery: 13.5 kWh nameplate, 80% DoD, 90% RTE, 97% availability = 10.5 kWh delivered
- Lease cost floor: $13,500 installed × 30% §48E credit = $9,450 lessor cost, $4k CAC, 25 years @ 8% = $87/mo + $10 O&M = $97/mo = $1,164/yr
- Spreads are TOU rates minus riders (simplified for comparison)

## Analysis by State

### Georgia Power (OA-14)

- **Tariff:** Overnight Advantage, filed Jan 2025
- **Peak:** 29.79¢/kWh (2-7pm Mon-Fri, Jun-Sep)
- **Off-peak:** 2.1859¢/kWh (11pm-7am)
- **Super off-peak:** Available on some plans
- **Spread:** 27.6¢
- **Economics:** $459/yr earned vs $1,044/yr cost = **$49/mo gap**
- **Status:** FAILED in original analysis
- **Verdict:** Arbitrage alone insufficient

### California (SDG&E TOU-ELEC)

- **Tariff:** TOU-ELEC for battery storage (non-EV), residential
- **Peak:** ~65¢/kWh (4-9pm summer weekdays)
- **Off-peak:** ~28¢/kWh (all other hours)
- **Spread:** 37.0¢ (1.34x Georgia's spread)
- **Economics:** ~$634/yr earned vs $1,044/yr cost = **$34/mo gap**
- **Status:** Slightly better than Georgia, still negative
- **Viable if:** Backup power premium added, or lease pricing cut
- **Verdict:** Most viable arbitrage market, but still doesn't close

### Texas (ERCOT Retail TOU)

- **Market:** Competitive retail electric providers (Octopus Energy, Griddy successors)
- **Peak:** 22¢/kWh (2-9pm summer weekdays)
- **Off-peak:** 7.5¢/kWh (all other hours)
- **Spread:** 14.5¢ (53% narrower than Georgia)
- **Economics:** ~$214/yr earned vs $1,044/yr cost = **$69/mo gap**
- **Note:** Wholesale passthrough during scarcity events ($5/kWh peaks) not included
- **Status:** FAILED under normal rates
- **Volatile:** Can reach $312/month during heat events (rare)
- **Verdict:** Not viable under baseline TOU; only viable during ERCOT scarcity

### Florida (FPL RTR-1)

- **Tariff:** Residential Time of Use, filed 2026
- **Peak:** 26¢/kWh (noon-9pm summer Mon-Fri)
- **Off-peak:** 9¢/kWh (all other hours)
- **Spread:** 17¢ (38% narrower than Georgia)
- **Economics:** ~$282/yr earned vs $1,044/yr cost = **$63/mo gap**
- **Status:** WORSE than Georgia on arbitrage
- **Note:** Duke Energy FL even narrower (13¢ spread)
- **Verdict:** NOT VIABLE for arbitrage

---

## Strategic Recommendations

### Recommendation 1: Pivot Away from Arbitrage

All four states show negative unit economics on bill-savings arbitrage alone. A battery lease simply cannot be carried by the TOU spread, even in California where spreads are widest.

**What this means:**

- Georgia: -$49/mo per customer
- California: -$34/mo per customer
- Texas: -$69/mo per customer
- Florida: -$63/mo per customer

### Recommendation 2: Reframe the Product

The only viable product is **backup power/resilience** sold as insurance:

**Not:** "Your battery will save you $X/month on peak pricing."  
**Yes:** "Your battery protects you during outages and PSPS events."

Price against:

- Generator cost ($8-15k for equivalent capacity)
- Diesel/fuel cost ($1.50-3/gallon, ongoing)
- Lost productivity during outage
- Generator maintenance and noise

### Recommendation 3: Market Selection

If pursuing resilience insurance instead:

1. **California (SDG&E/SCE territory):** PSPS (intentional power shutoffs) are routine. Customers have extreme willingness to pay.
2. **Texas (ERCOT):** Heat waves + grid stress. Known outage risk. Willingness moderate.
3. **Georgia:** Rare outages, low SAIDI. Willingness low.
4. **Florida:** Hurricane risk, PSPS potential. Willingness moderate-high.

### Recommendation 4: Geographic Focus

For Zoom-based sales from Orlando:

**Best markets (resilience):**

- California: Highest outage risk & PSPS exposure
- Florida: Hurricane resilience + PSPS emerging
- Texas: Summer heat wave risk

**Avoid:**

- Georgia: Low outage risk undermines resilience pitch
- Other flat-tariff states: No TOU arbitrage, no major outage risk

---

## Conclusion

**The arbitrage business does not work in any of these markets.** Lease costs exceed battery earnings by $34–$69/month.

The path forward is to:

1. **Stop modeling bill savings.** They don't exist at a leasable scale.
2. **Start modeling outage resilience.** Use SAIDI and PSPS data.
3. **Price against backup generators,** not electric bills.
4. **Target California and Florida first**—highest outage risk per capita.
5. **Zoom closes from Orlando office.** Keep sales centralized, geo-diversify the product.

This is a pivot, not a refinement. The Georgia experiment has delivered its answer: battery-as-arbitrage is not a viable consumer product at today's cost structure and TOU spreads.
