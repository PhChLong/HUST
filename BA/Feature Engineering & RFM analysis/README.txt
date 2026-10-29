BANKING RFM LAB | Synthetic teaching data, not real bank records.
As-of: 2026-10-01; window: 2025-10-01 to 2026-09-30 inclusive.
1000 customers; transactions include duplicates, FAILED/REVERSED, zero amounts and missing dates.
Recommended activity transactions: CARD_PAYMENT, TRANSFER_OUT, BILL_PAYMENT, ATM_WITHDRAWAL; SUCCESS only; amount > 0; deduplicate transaction_id.
R = days since most recent eligible activity as of 2026-10-01; F = number of eligible transactions in window; M = sum of eligible outgoing transaction amounts (VND). M is activity volume, NOT bank revenue/profit.
Handle customers with no eligible transactions explicitly. Explain ties and segmentation rules.
synthetic_profile_hint is generator metadata; DO NOT use it as a feature or label.
