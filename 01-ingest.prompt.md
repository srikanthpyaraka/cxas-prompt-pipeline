# STAGE 1 — INGEST
Input: the user's raw material (PRD, notes, tickets, bullets — any format/quality).
Goal: normalize it into a structured brief and expose every gap. Do NOT design yet.

## Do
1. Extract and normalize into the NORMALIZED_BRIEF fields below. Mark anything absent as
   `❓UNKNOWN` — never invent it.
2. Decompose into **atomic requirements**, each with an ID and a full requirement record
   (see output-contract schema): `id, text, type, priority, status, source`.
3. Flag risks, contradictions, and scope ambiguities.

## NORMALIZED_BRIEF fields
- Business goal & success metrics / KPIs (containment, CSAT, AHT, resolution rate)
- Primary users; channels (chat/voice); languages; expected volume
- In-scope intents / journeys  AND  explicit OUT-of-scope
- Backend systems / tools / APIs / knowledge sources available (+ auth if known)
- Data sensitivity: PII, regulatory/compliance constraints
- Tone / persona / brand rules; escalation & human-handoff policy
- Non-functionals: latency budget, availability, fallback behavior
- Known constraints, deadlines, environment (`project_id`, `location`)

## Output
Emit `NORMALIZED_BRIEF` (fields as a table + the requirements list as JSON records) in an
`artifact:NORMALIZED_BRIEF` block. Summarize: # requirements by priority, # UNKNOWNs,
top risks. Do not proceed to design.

DECIDED / ASSUMED / NEED NEXT.
