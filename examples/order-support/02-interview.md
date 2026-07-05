STAGE 2 — INTERVIEW ◆HARD GATE◆

## Round 1 questions
| # | P | Question | Why it changes the design | Default if unanswered |
|---|---|----------|---------------------------|-----------------------|
| 1 | P0 | How does the agent authenticate to the OMS & Returns APIs (OAuth SA, API key)? | Determines Tool auth config and whether returns (write) are safe to enable | OAuth service account via ADC |
| 2 | P0 | Confirm containment target = 0.45? And is there a CSAT floor? | Sets Stage-5 eval pass/fail bars | Containment ≥ 0.45; CSAT ≥ 4.0/5 |
| 3 | P0 | What PII must be redacted in transcripts (name, email, address, order id)? | Defines the redaction guardrail + a callback test | Redact card#, email, phone; keep order id |
| 4 | P0 | Return eligibility rules — does the agent decide, or does the Returns API? | Decides how much logic lives in the agent vs. the tool | API is source of truth; agent only relays |
| 5 | P0 | Where do escalations go (queue/hours)? Live-agent fallback if offline? | Defines handoff target + after-hours behavior | Route to tier-1 queue; after-hours → ticket |
| 6 | P1 | Latency budget (p95)? | Sets the latency eval threshold | ≤ 3s p95 |
| 7 | P1 | project_id / location for deployment? | Needed to parameterize the build scripts | `acme-cx-prod` / `global` (placeholder) |

_User answered: accepted defaults for 1, 3, 4, 6, 7; set containment ≥ 0.45 & CSAT ≥ 4.2
(Q2); escalations to tier-1 queue 6am–10pm, after-hours → ticket (Q5)._

```artifact:RESOLVED_BRIEF
All 9 requirements now status=resolved. Key resolutions:
- R5: redact card#, email, phone; retain order id for continuity.
- R2: agent relays Returns-API eligibility decision; never computes it itself.
- R4: handoff → tier-1 queue (6am–10pm); after-hours → create ticket + set expectation.
- R7: containment ≥ 0.45; add CSAT ≥ 4.2. R8: p95 ≤ 3s.
- Env: project_id=acme-cx-prod, location=global (placeholders for the example).
```

```artifact:ASSUMPTIONS_LOG
| Ref | Assumption | Basis | User action |
|-----|-----------|-------|-------------|
| A1 | OAuth SA auth via ADC | Q1 default accepted | confirm before prod |
| A2 | project_id/location are placeholders | Q7 default | replace with real values |
| A3 | After-hours returns still allowed (queued) | not raised | veto if wrong |
```

GATE: interview PASSED.
DECIDED: 6 defaults accepted, 2 overrides. ASSUMED: A1–A3 logged. NEED NEXT: Stage-3 design.
