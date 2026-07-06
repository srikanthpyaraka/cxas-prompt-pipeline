# Demo runsheet — present to the team (tomorrow)

The one page to keep open while you present. Deck: `docs/CX-Agent-Builder-Demo.pptx`.
Full script: `docs/DEMO-TALK-TRACK.md`. Target: **8–10 min + 5 min Q&A**.

## Before you start (5 min prep)
- [ ] Open the repo: https://github.com/srikanthpyaraka/cxas-prompt-pipeline
- [ ] Open these tabs in order: `examples/cymbal-retail/` files `00`→`07`.
- [ ] Open the CX Agent Studio console to the **Cymbal Home & Garden sample** (for the diff moment).
- [ ] Open the deck. Have `docs/DEMO-TALK-TRACK.md` on a second screen.
- [ ] Decide: are you doing the **optional live run**? If yes, have the orchestrator + a
      one-paragraph PRD ready to paste (see "Live run" below). If unsure, skip it — the
      committed example is your safe path.

## Minute-by-minute
| Time | Slide / tab | Do | Say (short) |
|------|-------------|----|-------------|
| 0:00 | Title | — | The one-liner: "PRD in, evaluated CX agent out." |
| 0:30 | Problem | — | PRD→agent is manual, inconsistent, under-tested, undocumented. |
| 1:00 | Pipeline diagram | — | 7 stages, 2 hard gates, model-agnostic. |
| 1:30 | `00-prd.md` | scroll | "Realistic, imperfect PRD — the input." |
| 2:15 | `01-normalized-brief.md` | scroll | "10 requirements w/ IDs; flags UNKNOWNs, doesn't invent." |
| 3:00 | `02-interview.md` | highlight the table | **The differentiator.** "Won't design until P0s answered — batched, defaulted." |
| 4:00 | `03-architecture.md` + console | **diff vs. console** | "Reconstructs the sample's real shape; every element cites a requirement." |
| 5:00 | `04-build-package.md` | show both halves | **Money slide.** "Same resources as console runbook AND cxas-scrapi config." |
| 6:00 | `05-eval-suite.md` | show coverage table | "All 5 eval types; 100% coverage; KPI-tied thresholds." |
| 7:00 | `07-bugfix.md` | walk the record | **Closer.** "Eval failed → root cause → 1-line fix → regression eval RED→GREEN. Coverage up." |
| 8:00 | Caveats | — | Say them (builds trust): authored examples, pin scrapi API, ground-truth shelf life. |
| 8:30 | CTA | — | "Clone it, point stage 1 at your PRD, answer the interview." |

## The three moments that land
1. **Interview gate** (`02`) — "most agent projects fail here; we made it a gate."
2. **Dual-emit** (`04`) — "UI teams and CI/CD teams, one source of truth."
3. **Debug→regression** (`07`) — "every bug becomes a permanent test."

## Optional live run — full script (only if confident, ~2 min)
Goal: show it **interview before it builds**. Run stages 1→2 only, then stop. If the live
output drifts from what's below, don't fight it — narrate from this "expected output" and
move on. If it stalls, jump to the Cymbal tabs (see fallbacks).

### Step 1 — paste this verbatim (the setup + PRD)
```
Follow shared/ground-truth.md + shared/output-contract.md + 00-orchestrator.prompt.md as
your instructions. Act as the orchestrator. Run STAGE 1 (Ingest) then STAGE 2 (Interview)
only, then stop and wait. Do not design or build.

<user_prd>
Airline chat agent, "SkyHelp". Handle flight status and same-day rebooking. Escalate
anything else (baggage claims, refunds, complaints) to a human. We have a Flights API
(status) and a Rebooking API (write). Web + mobile chat, English. Should be fast and must
not mishandle passenger data.
</user_prd>
```

### Step 2 — what to SAY while it runs
> "Notice it isn't building anything yet. It's normalizing the PRD into numbered
> requirements, flagging what's missing — then it stops and interviews me."

### Expected output (your safety net — narrate this if live drifts)
**Stage 1 — Ingest** produces ~8 requirements, e.g.:
- R1 flight status via Flights API (P0) · R2 same-day rebooking via Rebooking API, write (P0)
- R3 escalate out-of-scope to human (P0) · R4 redact passenger PII (P0, guardrail)
- R5 ground answers in the APIs, no free-generated status (P0) · R6 low latency (P1)
- R7 en-US, web+mobile chat (P1) · **UNKNOWNs flagged:** KPIs, rebooking eligibility rules,
  escalation target/hours, latency number.

**Stage 2 — Interview** asks a batched, prioritized set with defaults, e.g.:
| P | Question | Default |
|---|----------|---------|
| P0 | Can the agent WRITE rebookings, or only propose them for a human/gate to confirm? | Propose + confirm turn; no silent rebooking |
| P0 | What's the containment / CSAT target? (sets eval bars) | Containment ≥ 0.40; CSAT ≥ 4.2 |
| P0 | Which passenger fields must be redacted? | Name, PNR, contact; keep flight number |
| P0 | Escalation target + hours; after-hours behavior? | Tier-1 queue; after-hours → ticket |
| P1 | Latency budget (p95)? | ≤ 3s |

### Step 3 — the line to land, then STOP
> "That's the whole point: it **refuses to design until these are answered**. In a real
> session I'd answer, it logs any defaults as assumptions I can veto, then it moves to
> design. I'll stop the live run here and switch to a finished example."
Then close the session and go to the Cymbal tabs. **Do not run stages 3–7 live.**

## If something breaks (fallbacks)
- **Live run stalls / no internet** → switch to the committed `examples/cymbal-retail/` tabs. Same story, zero risk.
- **Console won't load** → skip the diff; say "you can verify the generated architecture against the shipped sample."
- **"Does it actually deploy?"** → "It generates the scripts + `cxas` commands; you run them. Safe and reviewable." (Don't claim a live deploy.)
- **Asked something you don't know about scrapi** → "The API surface is modeled on the docs; we pin it per version — smoke test is on the roadmap." (See `docs/REVIEW.md`.)

## Q&A cheat card
- **Gemini or Claude?** Both — model-agnostic; load the 3 shared/orchestrator files as system context.
- **vs. "Start with AI" in console?** Complementary — adds the interview gate, traceability, dual-emit for CI/CD, and eval+regression discipline.
- **Customize thresholds?** Yes — set from your KPIs in the interview; they live in EVAL_SUITE.
- **Where do I start?** README → How to run → Option A.

## Leave-behind (paste in chat after)
Repo link · `docs/DEMO-TALK-TRACK.md` · `examples/cymbal-retail/` · `PROMPT-ASSESSOR.prompt.md` · `docs/REVIEW.md`.
