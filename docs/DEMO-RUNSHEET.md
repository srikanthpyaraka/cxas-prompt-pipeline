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

## Optional live run (only if confident)
Paste into a fresh Claude/Gemini session:
> Follow shared/ground-truth.md + shared/output-contract.md + 00-orchestrator.prompt.md.
> Begin STAGE 1 with this PRD: "Airline chat agent for flight status and same-day
> rebooking; escalate anything else to a human; we have a flights API and a rebooking API."

Expect: a normalized brief + a batch of interview questions. **Stop after the interview
questions appear** — that's the wow moment (it asks before building). Don't run the whole
pipeline live; time-box it.

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
