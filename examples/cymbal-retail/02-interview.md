STAGE 2 — INTERVIEW ◆HARD GATE◆

## Round 1 questions
| # | P | Question | Why it changes the design | Default if unanswered |
|---|---|----------|---------------------------|-----------------------|
| 1 | P0 | Primary KPI(s) — task completion, add-to-cart, upsell attach rate? | Sets Stage-5 eval pass/fail bars | Task completion ≥ 0.80; upsell attach ≥ 0.15 |
| 2 | P0 | Upsell policy — max suggestions/turn, when suppressed? | Turn-eval rule for "not pushy"; avoids annoyance | ≤ 1 upsell/turn; none during checkout or complaints |
| 3 | P0 | Manager discount — who approves, and up to what %? | Determines the approval variable + a guarded flow | Human approves; ≤ 15%; agent never self-approves |
| 4 | P1 | Plant-ID fallback if the image is unclear? | Defines a graceful multimodal failure path | Ask for a clearer photo; offer text search |
| 5 | P1 | project_id / location? | Parameterizes build scripts | `cymbal-cx-demo` / `global` (placeholder) |

_User: accepted defaults for 1, 2, 4, 5; Q3 — human approves, cap 20%._

```artifact:RESOLVED_BRIEF
All 10 requirements resolved. Key resolutions:
- R4: ≤ 1 upsell/turn; suppress during checkout/complaints. KPI upsell attach ≥ 0.15.
- R6: human-in-the-loop discount ≤ 20%; agent sets manager_discount_approved only after approval.
- R2: unclear image → request clearer photo or fall back to text search.
- KPIs: task completion ≥ 0.80. Env: cymbal-cx-demo / global (placeholder).
```

```artifact:ASSUMPTIONS_LOG
| Ref | Assumption | Basis | User action |
|-----|-----------|-------|-------------|
| A1 | en-US only | Q (not raised); sample default | confirm |
| A2 | project_id/location are placeholders | Q5 default | replace for prod |
```

GATE: interview PASSED.
DECIDED: 4 defaults, 1 override (discount 20%). ASSUMED: A1–A2. NEED NEXT: Stage-3 design.
