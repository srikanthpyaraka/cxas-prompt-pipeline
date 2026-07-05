STAGE 7 — DEBUG & FIX

_Triggered by a Stage-5 eval failure on the Cymbal build. Shows the loop: reproduce →
root cause → minimal fix → regression eval (RED→GREEN) → re-run._

<failing_eval>
id: TE-02  (upsell ≤1/turn AND suppressed at checkout/complaints — R4)
observed: during a checkout turn the agent appended "Would you like some potting soil too?"
expected: 0 upsell suggestions once the customer is in checkout/payment
</failing_eval>

```artifact:BUGFIX_RECORD
| Field | Value |
|-------|-------|
| id / title / severity | BUG-01 · Upsell leaks into checkout · Major |
| Symptom (observed) | On the checkout turn, `upsell_agent` still offered an add-on (1 upsell). |
| Expected | 0 upsells during checkout/payment; upsell allowed only while browsing. |
| Requirements affected | R4 (upsell policy). Indirect: R3 (checkout UX). |
| Root cause | The `after_model` callback enforced the *count* cap (≤1/turn) and a `complaint` suppression flag, but never checked **cart state**. On checkout turns the count-cap alone permitted one upsell through, because suppression only fired on `complaint == true`. Checkout was simply not a suppression condition — a missing guard, not a cap-math error. |
| Fix (before → after) | `after_model.py`: `suppress = complaint`  →  `suppress = complaint or cart_state in {"checkout", "payment"}`. (cart_state already set by `after_tool` from `cart_openapi`; no new tool needed.) |
| Blast radius | 1 callback (`after_model`). No agent/tool/guardrail change. Re-run: TE-02, PG-01 (browse→buy), SIM-01. |
| Regression eval | `TE-02b` · Turn Eval · assert 0 upsell when `cart_state ∈ {checkout, payment}`. RED before fix, GREEN after. Plus `TE-02` re-asserted. |
| Re-run result | TE-02 ✅, TE-02b ✅, PG-01 ✅, SIM-01 ✅. Upsell still works while browsing (not over-suppressed). Coverage R4: 1 → 2 evals; suite 17 → 18 assets; total coverage unchanged at 10/10 = 100%. |
```

## Why this is the *right* fix (not a test patch)
The change targets the causal condition (state-aware suppression), so it generalizes to
any checkout/payment turn — not just the one TE-02 exercised. It does not hard-code the
specific product ("potting soil") or the specific transcript. Upsell during browsing is
untouched, verified by re-running PG-01.

## Regression eval added to the suite (Stage-5 EVAL_SUITE, Turn Evals)
```
TE-02b (R4): given cart_state=checkout, when the model responds → assert upsell_count == 0.
             Runs with the turn-eval batch; must stay GREEN in CI before any redeploy.
```

SELF-CHECK: pass — root cause explains symptom; fix minimal + generalizing; TE-02b is
RED-before/GREEN-after; coverage increased, not reduced.
DECIDED: state-aware upsell suppression. ASSUMED: cart_state values checkout/payment exist
in cart_openapi responses. NEED NEXT: land fix → run full eval batch → redeploy canary.
