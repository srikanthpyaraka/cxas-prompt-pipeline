STAGE 1 — INGEST

```artifact:NORMALIZED_BRIEF
| Field | Value |
|-------|-------|
| Business goal | Deflect tier-1 order/returns/FAQ contacts; reduce wait vs. 8-min baseline |
| Success metrics / KPIs | Containment ≥ 0.45 (target); ❓UNKNOWN exact latency target |
| Primary users / channels | AcmeShop web + mobile-web shoppers; chat only |
| Languages / volume | en-US; ❓UNKNOWN volume |
| In-scope journeys | Order status/tracking; start return/refund; store & policy FAQs |
| Out of scope | Payments, account/password, everything else → human |
| Backend systems | OMS API (read); Returns/RMA API (write); help-center KB. ❓UNKNOWN auth model |
| Data sensitivity | Card data present (PCI); ❓UNKNOWN PII redaction/logging policy |
| Tone / persona | ❓UNKNOWN — not specified |
| Escalation / handoff | Escalate out-of-scope + when bot can't help; ❓UNKNOWN target queue |
| Non-functionals | "Should be fast"; ❓UNKNOWN latency budget & availability |
| Environment | GCP; cxas-scrapi mentioned; ❓UNKNOWN project_id / location |
```

```json
[
 {"id":"R1","text":"Answer order status/tracking from OMS","type":"functional","priority":"P0","status":"known","source":"PRD in-scope 1"},
 {"id":"R2","text":"Start a return/refund for an eligible order via Returns API","type":"functional","priority":"P0","status":"known","source":"PRD in-scope 2"},
 {"id":"R3","text":"Answer store/policy FAQs from the KB","type":"functional","priority":"P1","status":"known","source":"PRD in-scope 3"},
 {"id":"R4","text":"Escalate to human for out-of-scope or unresolved contacts","type":"functional","priority":"P0","status":"known","source":"PRD out-of-scope + goals"},
 {"id":"R5","text":"Redact PII in transcripts/logs","type":"guardrail","priority":"P0","status":"unknown","source":"inferred — 'don't mishandle', not detailed"},
 {"id":"R6","text":"Never expose or store full card numbers (PCI)","type":"guardrail","priority":"P0","status":"known","source":"PRD constraints (Legal)"},
 {"id":"R7","text":"Containment ≥ 0.45","type":"nonfunctional","priority":"P0","status":"assumed","source":"PRD goals ('~45%')"},
 {"id":"R8","text":"Low latency responses","type":"nonfunctional","priority":"P1","status":"unknown","source":"PRD 'should be fast' — no number"},
 {"id":"R9","text":"en-US, web + mobile web, chat only","type":"constraint","priority":"P1","status":"known","source":"PRD constraints"}
]
```

Summary: 9 requirements (P0: 6, P1: 3). UNKNOWNs: latency target, volume, KB/API auth,
PII policy, tone, handoff target, project env. Top risks: PCI handling (R6) and PII
redaction (R5) are underspecified but P0; containment target is an assumption.

SELF-CHECK: pass — no requirement invented; all UNKNOWNs flagged.
DECIDED: normalized to 9 requirements. ASSUMED: R7 target from "~45%". NEED NEXT: Stage-2 interview on the 7 UNKNOWNs.
