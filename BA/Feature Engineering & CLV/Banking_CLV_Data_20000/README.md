# Banking customer lifetime value assignment data

This package accompanies the Banking Customer CLV practical assignment. It contains synthetic data for teaching. It does not contain records from an actual bank, estimated bank retention rates, or observed campaign results.

## Files and scope

- `customers.csv` contains the roster of 20,000 customers active on October 1, 2026.
- `customer_economics.csv` contains a raw extract of annual customer economics and assumed retention inputs.
- `DATA_DICTIONARY.md` defines the columns and validation rules.

All roster customers opened their relationship on or before October 1, 2025. The intended historical observation period is October 1, 2025 through September 30, 2026, inclusive. The inputs use no information dated after the observation period. The retention field supplies an assumption available at the valuation date. It is not a realized future outcome.

The raw economics extract includes intentional data-quality issues. Identify and document them. The dictionary gives the intended valid schema, rather than a guarantee that every raw record meets it. No cleaned data, answer key, customer valuations, or campaign selections appear in this package.

## Reading and joining the files

The CSV files use UTF-8 text, commas as separators, and one header row. Dates use `YYYY-MM-DD`. Monetary values use whole Vietnamese dong (VND), without currency symbols or thousands separators. A retention rate such as `0.85` means 85%. An empty field means missing, not zero.

Treat `customer_id` as text. Join the economics extract to the customer roster using this key, never by row position. The intended prepared grain is one record per roster customer for the specified observation period. Check duplicate keys, unmatched keys, required fields and period coverage before valuing customers. Avoid multiplying customer records or summing duplicate annual snapshots.

Keep all 20,000 roster customers in the final customer output. Document any exclusion, correction or imputation in your README and cleaning log. Where a customer cannot receive a defensible valuation, retain the customer and use a missing CLV with an explanatory `quality_status`. Distinguish missing CLV from a valid zero. Preserve valid negative contribution and CLV values.

## Valuation assumptions

Use October 1, 2026 as time zero. This assignment values future contribution from existing customers over three forecast years. The model is intentionally simple:

1. Calculate annual net contribution, `m`, as `fee_revenue_vnd + net_interest_income_vnd - servicing_cost_vnd - expected_credit_loss_vnd`.
2. Hold `m` constant in each forecast year, conditional on the customer remaining active. Use the observed full-year amounts as the forecast basis. Do not annualize them again.
3. Use each customer's supplied annual retention assumption, `r`, as a constant conditional probability of remaining active for another year. Attrition is permanent. Therefore survival to the end of year `t` has probability `r^t`.
4. Assume contribution arrives only at each forecast year-end if the customer remains active through that year. Discount at the annual rate `d = 0.10`.
5. Calculate `CLV_3 = m*r/(1+d) + m*r^2/(1+d)^2 + m*r^3/(1+d)^3`.

The forecast years end on September 30, 2027, September 30, 2028 and September 30, 2029. Use the specified annual discount periods of 1, 2 and 3. There is no growth, terminal value or future reactivation. Exclude past acquisition costs because these existing-customer costs are sunk. The supplied contribution measure does not include taxes, capital charges or a full allocation of bank overhead. Treat it as the assignment's contribution proxy, rather than complete accounting profit.

## Retention campaign scenario

The CRM Manager can spend at most VND 10,000,000. Targeting one customer costs VND 100,000 at time zero. The hypothetical campaign raises that customer's conditional annual retention by 3 percentage points in each of the three forecast years, with `r_campaign = min(1, r + 0.03)`. Keep annual contribution and the discount rate unchanged. The uplift is an exercise assumption, not a measured causal effect.

Recalculate the three-year CLV with `r_campaign`. Define `campaign_delta_vnd = clv_campaign_vnd - clv_3yr_vnd - 100000`. Use positive net incremental values to select up to 100 customers while respecting the budget. Allow unspent budget if fewer customers offer a positive gain. Specify a reproducible rule for ties. Assess the campaign using incremental value after cost, rather than baseline CLV alone.

## Sensitivity and interpretation

Evaluate the full 3-by-3 grid of nine scenarios. Cross annual discount rates of 5%, 10% and 15% with retention shifts of -5, 0 and +5 percentage points. In each scenario, set `r_scenario = min(1, max(0, r + shift))`, where the shift is -0.05, 0 or +0.05. The base scenario uses a 10% discount rate and a zero retention shift.

For every scenario, recalculate total three-year CLV, campaign selections and the selected campaign's total net gain after cost. Apply the campaign uplift to that scenario's adjusted retention using `r_campaign_scenario = min(1, r_scenario + 0.03)`. Calculate each campaign gain relative to the no-campaign CLV in the same scenario, then apply the same budget, positive-gain rule and tie policy.

Compare the top 10 customers by CLV in each scenario with the base scenario. Report the number of customer IDs shared between the two top-10 lists. Also compare campaign selections with the base scenario to assess targeting stability, stating how many selected customers remain the same and how many change. Keep annual contribution, customer coverage and missing-data treatment consistent across scenarios. Document a reproducible tie rule for rankings and selections.

Explain how your results depend on fixed contribution, permanent attrition and the supplied retention assumptions. Age, city and onboarding channel support descriptive analysis. Any recommendation using them should discuss fairness and business relevance. Follow the accompanying assignment slides for graded tasks and submission requirements.
