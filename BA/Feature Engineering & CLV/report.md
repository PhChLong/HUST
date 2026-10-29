# Banking Customer Lifetime Value Report

Synthetic data. As-of date: October 1, 2026. All amounts in VND.

## 1. Goal

Estimate the 3-year value of 20,000 existing customers, then choose up to 100 customers for a retention offer with a budget of VND 10 million (VND 100,000 per customer).

## 2. Data preparation

| Step | Count |
|---|---|
| Raw economics rows | 20,400 |
| Exact duplicate rows removed | 300 |
| Rows with IDs not in the roster removed (C9xxxx) | 100 |
| Clean economics rows | 20,000 |
| Customers in roster (all kept) | 20,000 |
| Customers with a valid CLV | 19,300 |
| Customers with missing CLV (Unscored) | 700 |

The 700 customers with missing CLV, by reason:

| quality_status | Customers | Reason |
|---|---|---|
| missing_input | 300 | Missing fee (100), credit loss (100) or retention (100) |
| invalid_input | 300 | Negative servicing cost (100), retention < 0 (100), retention > 1 (100) |
| partial_period | 100 | Period ends 2026-08-31, so it is not a full year |

Treatment: missing values were not filled in and invalid values were not corrected, because the true value is unknown. These customers stay in the output file with a missing CLV. Real zeros and negative contribution were kept.

## 3. CLV calculation

- m = fee + net interest income − servicing cost − expected credit loss
- CLV = m·r/1.1 + m·r²/1.1² + m·r³/1.1³ (d = 10%, contribution arrives at the end of each year, attrition is permanent)
- Two customers (C00001 and C00005) were checked by hand and match the code.
- Total CLV of the 19,300 customers is about **VND 75.2 billion**. The median is VND 3.6 million. 4,386 customers (about 23%) have a negative CLV.

![CLV distribution](output/chart1_clv_distribution.png)

## 4. Ranking and segments

Customers are ranked by CLV from highest to lowest. If CLV is tied, the smaller customer_id comes first.

Thresholds: "High Value" means CLV ≥ VND 7.96 million (75th percentile of positive CLV). "Stable" means retention ≥ 0.75.

| Segment | Customers | Total CLV (VND bn) | Median CLV (VND m) | Suggested action |
|---|---|---|---|---|
| High Value / Stable | 3,068 | 35.57 | 11.09 | Look after them, cross-sell |
| High Value / At Risk | 646 | 5.97 | 8.97 | Contact early to keep them |
| Low Positive Value | 11,140 | 42.80 | 3.81 | Serve through low-cost digital channels |
| Zero Value | 60 | 0 | 0 | Monitor |
| Negative Value | 4,386 | −9.13 | −1.87 | Review costs and credit risk |
| Unscored | 700 | n/a | n/a | Fix the data first |

![Customers by segment](output/chart2_segment_counts.png)

## 5. Retention campaign

Assumption: r' = min(1, r + 0.03). Incremental value = CLV(r') − CLV(r) − 100,000. We pick up to 100 customers with the largest positive incremental value (ties: smaller ID first).

- **100 customers** selected, cost **VND 10,000,000**, total net gain **about VND 102.0 million**.
- All 100 are in the High Value / Stable segment, with an average retention of 0.926.
- The top 10 and the full list are in `output/campaign_selected.csv`.

Only 66 of the 100 customers with the highest CLV were selected. The reason is that a customer with retention close to 1 can gain very little from +3 points (r' is capped at 1). Customers with a large m and retention around 0.90 to 0.96 gain the most.

![Contribution vs retention](output/chart3_contribution_vs_retention.png)

**Suggested KPI**: the 12-month active rate of the customers who got the offer compared with a control group, with a target of at least 3 percentage points higher.

## 6. Sensitivity (9 scenarios)

| d | Retention shift | Total CLV (VND bn) | Campaign net gain (VND m) | Top 10 same as base | Selected: same / changed |
|---|---|---|---|---|---|
| 5% | −5 | 72.54 | 110.4 | 9 | 70 / 30 |
| 5% | 0 | 81.74 | 114.4 | 10 | 100 / 0 |
| 5% | +5 | 91.19 | 115.3 | 8 | 42 / 58 |
| 10% | −5 | 66.87 | 98.5 | 10 | 70 / 30 |
| **10%** | **0 (base)** | **75.21** | **102.0** | **10** | **100 / 0** |
| 10% | +5 | 83.76 | 102.8 | 8 | 42 / 58 |
| 15% | −5 | 61.94 | 88.4 | 10 | 71 / 29 |
| 15% | 0 | 69.54 | 91.4 | 10 | 100 / 0 |
| 15% | +5 | 77.33 | 92.2 | 8 | 42 / 58 |

- The top 10 CLV list is fairly stable (8 to 10 customers match the base case).
- The campaign list is stable when only d changes, but 29 to 58 customers change when retention moves by 5 points. The retention input should be checked before the final list is used.

## 7. Limitations

1. Constant contribution and permanent attrition are simple assumptions.
2. Only 3 years are counted and there is no terminal value, so the CLV of stable customers is lower than it would be in reality.
3. The 3-point uplift is an assumption and has not been proven.
4. Retention is a given input. If it is wrong, the results are wrong too.
5. Contribution does not include tax, capital cost or overhead.

**Randomized test**: randomly split eligible customers into a treatment group (gets the offer) and a control group (does not), follow them for 12 months, and use the difference in retention between the two groups as the real uplift.

## 8. CLV and RFM, and negative-value customers

- RFM describes past behavior. CLV estimates future value after costs and credit risk. Using both is better.
- For negative-value customers: move them to digital channels and self-service, and review fee plans and credit limits. CLV alone should not be used to deny or limit services, because that would be unfair. Age, city and onboarding channel are used only for description.
