#!/usr/bin/env bash
# Assembles the installable Agent Skill from the source prompts, so the skill's bundled
# files stay single-sourced (no manual duplication/drift).
# Usage: bash scripts/build-skill.sh   (run from repo root)
set -euo pipefail
cd "$(dirname "$0")/.."
SKILL=".agents/skills/cx-agent-builder"
mkdir -p "$SKILL/stages" "$SKILL/reference"

# Reference material (loaded first / on demand by the skill)
cp shared/ground-truth.md      "$SKILL/reference/ground-truth.md"
cp shared/output-contract.md   "$SKILL/reference/output-contract.md"
cp 00-orchestrator.prompt.md   "$SKILL/reference/orchestrator.md"
cp PROMPT-ASSESSOR.prompt.md   "$SKILL/reference/prompt-assessor.md"

# Per-stage contracts (read when the orchestrator reaches each stage)
for f in 01-ingest 02-interview 03-design 04-build 05-evals 06-validate 07-debug-fix; do
  cp "$f.prompt.md" "$SKILL/stages/$f.md"
done

echo "Synced skill bundle → $SKILL (SKILL.md is hand-authored; not overwritten)"
ls "$SKILL" "$SKILL/stages" "$SKILL/reference"
