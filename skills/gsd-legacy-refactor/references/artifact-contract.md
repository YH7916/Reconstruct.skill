# Artifact Contract

Every run of `$gsd-legacy-refactor` must produce these planning files under `.planning/refactors/<slug>/`, then add an execution log once the route is approved.

## 01-CONTEXT.md

Must capture:
- Target
- Scope
- Goal
- Symptoms or pain points
- In-scope files and subsystems
- Out-of-scope areas

## 02-RISK-MAP.md

Must capture:
- Risk level: `low`, `medium`, or `high`
- Evidence for that rating
- Key callers and outward dependencies
- Side effects
- Shared state
- Known unknowns

## 03-SAFETY-NET.md

Must capture:
- Existing tests, fixtures, or smoke scripts
- Missing behavior locks
- Minimum behavior lock required before structural work
- Whether the current lock is enough for wave 1

## 04-WAVE-PLAN.md

Must capture:
- Mode: `untangle-first` or `refactor-wave`
- Up to 3 waves
- For each wave: goal, boundary, allowed changes, forbidden changes, exit criteria

## 05-VERIFY.md

Must capture:
- Commands to run
- Manual smoke checklist
- What must stay stable
- Rollback point for each wave

## 06-HANDOFF.md

Must capture:
- Why the chosen mode is correct
- Recommended next command
- Wave 1 execution boundary
- Remaining risks
- Reasons to stop if the boundary expands

## 07-EXECUTION-LOG.md

Must capture:
- Approval checkpoint
- Approval scope
- Branch name or baseline checkpoint
- Each executed wave
- Verification result for each wave
- Commit hash or commit message per wave
- Where execution stopped or completed

## Contract Rules

- No file may be omitted
- Only `07-EXECUTION-LOG.md` may describe source edits that already happened
- Unknown information must be labeled `Unknown` with the discovery gap
- `high` risk artifacts must not recommend a whole-target rewrite
