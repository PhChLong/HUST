# Data dictionary

These definitions describe valid records for this exercise. The raw economics extract intentionally violates some rules. Empty CSV fields represent missing values. No field contains a future observed outcome or a true customer segment label.

## customers.csv

Grain: one row per customer active on October 1, 2026. This file defines the 20,000-customer population that the final output must preserve.

| Field | Type and units | Meaning and validation |
| --- | --- | --- |
| `customer_id` | Text | Customer key. Required and unique. Preserve the leading `C` and following digits. |
| `open_date` | ISO date, `YYYY-MM-DD` | Relationship opening date. Required. On or before October 1, 2025 for this cohort. |
| `city` | Text category | Customer city. Values: Hanoi, Ho Chi Minh City, Da Nang, Can Tho, Hai Phong. |
| `age_band` | Text category | Age group at the valuation date. Values: 18-24, 25-34, 35-44, 45-54, 55+. |
| `onboarding_channel` | Text category | Channel used when the relationship opened. Values: Branch, Mobile app, Website. |

The roster's active status and full observation-year coverage are exercise assumptions. Opening date does not imply a future retention outcome.

## customer_economics.csv

Intended grain after preparation: one annual economics record per roster customer for October 1, 2025 through September 30, 2026. The four monetary fields are annual customer totals, not transaction amounts, account balances or monthly rates. All four components must be nonnegative for this exercise. Their net contribution may be zero or negative.

| Field | Type and units | Meaning and validation |
| --- | --- | --- |
| `customer_id` | Text | Required foreign key matching `customers.csv`. The prepared annual record must be unique for each roster customer and period. |
| `period_start` | ISO date, `YYYY-MM-DD` | Required. Must equal `2025-10-01`. |
| `period_end` | ISO date, `YYYY-MM-DD` | Required. Must equal `2026-09-30`. |
| `fee_revenue_vnd` | Nonnegative whole VND | Annual bank fee revenue attributed to the customer. Required for contribution calculation unless the student documents a defensible treatment. Zero is valid. |
| `net_interest_income_vnd` | Nonnegative whole VND | Annual net interest contribution attributed to the customer, after the exercise's funding-cost allocation and before expected credit loss. Already net of funding costs. Zero is valid. |
| `servicing_cost_vnd` | Nonnegative whole VND | Annual customer servicing cost. Entered as a positive expense amount and subtracted in net contribution. Zero is valid. |
| `expected_credit_loss_vnd` | Nonnegative whole VND | Annual expected credit loss charge attributed to the customer. Entered as a positive expense amount and subtracted once. Zero is valid. |
| `annual_retention_rate` | Decimal probability | Assumed conditional probability of staying active for one additional year, available at October 1, 2026. Required for CLV. Valid range is 0 to 1, inclusive. It is a forecast assumption, not a historical proportion calculated from these rows. |

Net interest income can have other sign conventions in actual banking systems. Use the nonnegative component convention specified here when validating this synthetic extract.

## Preparation and output rules

- Parse VND amounts as numbers and retention as a decimal probability. Do not interpret `0.85` as 0.85% or as 85 stored units.
- Validate period dates before using the annual amounts. A partial period does not automatically qualify as the specified full-year observation.
- Identify duplicate annual records before joining. The economics file contains annual snapshots, so duplicates do not represent additional transactions.
- Investigate unmatched economics keys without adding them to the 20,000-customer roster.
- Keep missing amounts distinct from real zero amounts. Explain any imputation rather than silently replacing missing values with zero.
- Carry a `quality_status` field into the final one-row-per-customer output. Use your own clear, documented categories to explain valuation availability and any treatment applied.
- Store calculated contribution, CLV and campaign gains in VND. Keep calculation precision and round only for reporting. Use clear units if a chart displays thousands or millions of VND.

Refer to `README.md` for the valuation equation, timing conventions and campaign assumptions. No precomputed results appear in the inputs.
