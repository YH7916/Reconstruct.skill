<purpose>
Plan a risky legacy refactor, get route approval, then execute waves with git checkpoints. Default flow: Parse target -> Discover dependencies -> Assess blast radius -> Check safety net -> Choose mode -> Write artifacts -> Confirm route -> Execute waves -> Finish.
</purpose>

<required_reading>
Read all files referenced by the invoking prompt's execution_context before starting.

If they exist, also read:
- `./AGENTS.md`
- `./CLAUDE.md`
- `./GEMINI.md`
</required_reading>

<process>

## 1. Initialize

Parse `{{LEGACY_ARGS}}`:
- First positional item is the refactor target: path, module, symbol, service, or directory
- `--goal "<text>"` overrides the default goal
- `--scope module|service|repo` defaults to `module`
- `--text` forces plain text questions and summaries

Set defaults:
- `goal = reduce coupling and make future change safer`
- `scope = module`
- `slug = kebab-case(target)`
- `artifact_dir = .planning/refactors/<slug>`

Create `artifact_dir` if it does not exist.

**Hard rule:** Do not edit application source files before the route is approved. Only write planning artifacts until approval.

## 2. Discover The Current Shape

Inspect the target and the smallest set of supporting files needed to answer:
- What are the entrypoints?
- What calls into this target?
- What does this target call outward?
- Which side effects happen here?
- Which shared state or implicit contracts exist?
- Which tests, scripts, or fixtures already lock behavior?

Prefer evidence over assumptions:
- Read target files
- Read obvious callers and dependencies
- Read tests or smoke scripts if present
- Read configuration only when it changes blast radius or verification

If the target is partially unknown, continue and mark unknown areas explicitly in the artifacts.

## 3. Assess Blast Radius

Classify risk using evidence:

- `low`
  - Single bounded module
  - Stable interface
  - Known callers
  - Existing tests or easy characterization coverage
- `medium`
  - Some cross-module impact
  - Callers are mostly known
  - Compatibility seams look feasible
- `high`
  - Circular dependencies
  - Shared mutable state
  - Opaque behavior
  - Many entrypoints or many cross-layer callers
  - No credible safety net

If unsure, round upward.

## 4. Check The Safety Net

Use `@./references/artifact-contract.md` and the companion skill references to capture:
- Existing tests
- Characterization test opportunities
- Golden data or snapshots
- Smoke commands
- Missing behavior locks

Then choose mode:
- `high` risk always becomes `untangle-first`
- `medium` risk becomes `untangle-first` unless callers are known and verification is already strong
- `low` risk can become `refactor-wave`

If behavior is not locked, prefer `untangle-first`.

## 5. Plan Waves

Plan at most 3 waves.

Rules:
- Wave 1 must be the smallest high-value move
- Do not mix feature work with structural refactor
- One wave should touch one hotspot, not the whole web
- `high` risk may only produce `untangle-first` waves
- If the code is deeply tangled, wave 1 should add seams, adapters, or behavior locks

For every wave define:
- Goal
- Boundary
- Allowed changes
- Forbidden changes
- Verification
- Rollback point

## 6. Write Artifacts

Use the templates in `./templates/` as starting structures and fill them with concrete repo findings:
- `01-CONTEXT.md`
- `02-RISK-MAP.md`
- `03-SAFETY-NET.md`
- `04-WAVE-PLAN.md`
- `05-VERIFY.md`
- `06-HANDOFF.md`
- `07-EXECUTION-LOG.md`

Write them to `.planning/refactors/<slug>/`.

Do not leave placeholder headings without a finding. If information is missing, write `Unknown` plus the exact discovery gap.

Initialize `07-EXECUTION-LOG.md` with approval `no` and wave statuses `not-started`.

## 7. Present Route And Wait For Approval

Summarize:
- Target
- Risk
- Mode
- Wave count
- Why wave 1 is the safest next move
- Git strategy: branch/checkpoint before wave 1, commit after each verified wave

Ask the user to confirm the route before any source edits.

If the user does not approve:
- revise artifacts
- do not edit source files

If the user approves:
- update `07-EXECUTION-LOG.md` approval to `yes`
- continue to step 8

## 8. Prepare Git Baseline

If the repo is already a git repository:
- prefer a dedicated branch such as `codex/legacy-refactor-<slug>`
- if branch creation is inappropriate for the repo, record the current branch and baseline commit instead

If the repo is not a git repository:
- initialize git before source edits
- create a baseline commit that captures the pre-refactor state

Record in `07-EXECUTION-LOG.md`:
- branch
- baseline checkpoint

## 9. Execute Waves

Execute approved waves in order.

For each wave:
- re-read the wave boundary and forbidden changes
- apply the core rules from `$refactoring-legacy-code`
- if the boundary expands, stop and replan
- run the verification gate
- if verification passes, commit that wave and update `07-EXECUTION-LOG.md`
- if verification fails, stop, record failure, and do not continue to the next wave

Continue until:
- all planned waves are complete, or
- a stop condition triggers, or
- the approved route is no longer valid

## 10. Finish

Update:
- `06-HANDOFF.md`
- `07-EXECUTION-LOG.md`

Summarize:
- completed waves
- branch and commits
- remaining risks
- whether the route finished or stopped early

</process>

<success_criteria>
- `.planning/refactors/<slug>/` exists
- Risk has evidence, not vibes
- Mode is conservative
- Wave 1 is smaller than the whole target
- Verification and rollback are defined
- No application source files changed before approval
- Execution log records approval, checkpoints, and wave results
</success_criteria>
