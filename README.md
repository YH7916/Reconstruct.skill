# Reconstruct Skill Suite

Route-first AI skills for refactoring legacy code without blowing up tightly coupled systems.

This repo ships two complementary skills:

| Skill | Role |
|------|------|
| `refactoring-legacy-code` | The execution skill. It maps blast radius, locks behavior, picks a safe boundary, and refactors one wave at a time. |
| `gsd-legacy-refactor` | The orchestration skill. It inspects the target, writes `.planning/refactors/<slug>/` artifacts, asks for route approval, then executes with git checkpoints. |

## Why This Exists

Most AI refactor helpers fail in exactly the place legacy code hurts most:

- dense dependency graphs
- hidden side effects
- shared mutable state
- "fix one thing, break three more" modules

This suite is opinionated about that failure mode.

It does **not** assume the right answer is "rewrite everything."
It assumes the safe answer is:

1. map the current shape
2. lock behavior
3. estimate blast radius
4. show the route to the user
5. execute only after approval
6. checkpoint every verified wave with git

## What Makes It Different

### 1. Route First, Edit Second

Before touching source files, the skills must produce a concrete route:

- current-state map
- blast-radius rating
- safety-net assessment
- execution mode
- safe boundary
- verification gate

Then the user approves the route before structural edits begin.

### 2. High Risk Downgrades Automatically

If the target has circular dependencies, hidden side effects, shared state, or weak behavior locks, the suite falls back to:

- `untangle-first`

That means adapters, facades, characterization tests, and seam extraction come before broad cleanup.

### 3. Git Is Part Of The Safety Model

This suite treats git as an execution primitive, not a cleanup step:

- baseline checkpoint before structural edits
- dedicated refactor branch when appropriate
- one verified wave per commit sequence
- explicit rollback points in planning artifacts

### 4. Planning Artifacts Are First-Class

The orchestration skill writes a handoff package under:

```text
.planning/refactors/<slug>/
```

Including:

- `01-CONTEXT.md`
- `02-RISK-MAP.md`
- `03-SAFETY-NET.md`
- `04-WAVE-PLAN.md`
- `05-VERIFY.md`
- `06-HANDOFF.md`
- `07-EXECUTION-LOG.md`

### 5. English And Chinese Trigger Coverage

The skill descriptions are written for discoverability in both English and Chinese, including prompts around:

- `legacy code`
- `spaghetti code`
- `technical debt`
- `god file`
- `tight coupling`
- `屎山`
- `技术债`
- `依赖混乱`
- `拆模块`
- `解耦`

## Install

These are plain skill folders. Copy them into your skill directory.

### Codex

Copy both folders into:

```text
$CODEX_HOME/skills
```

Or, if `CODEX_HOME` is unset:

```text
~/.codex/skills
```

### Generic Agent-Skill Layouts

If your setup reads from an agent skill directory such as:

```text
~/.agents/skills
```

copy the same folders there.

### One-Command Install

You can also install the suite with the bundled script:

```text
python scripts/install_skills.py --force
```

Useful flags:

- `--dest <path>` to install somewhere custom
- `--mode link` to symlink instead of copy
- `--dry-run` to preview the destination

## Quick Start

### Option A: Plan And Execute A Risky Refactor

```text
$gsd-legacy-refactor src/auth --goal "split auth orchestration from token storage"
```

What happens:

1. the skill inspects the target
2. writes the `.planning/refactors/<slug>/` package
3. shows the route
4. waits for user approval
5. executes the approved waves
6. checkpoints progress with git

### Option B: Execute A Single Safe Wave Directly

```text
$refactoring-legacy-code src/reporting/legacy_parser.py
```

Use this when you already know the boundary and want the guardrails during execution.

## How The Suite Thinks

The core skill forces every refactor into one of two modes:

| Mode | Use when |
|------|----------|
| `untangle-first` | Risk is high, behavior is fuzzy, coupling is dense, or tests are weak |
| `refactor-wave` | Boundary is small, callers are known, and verification is already credible |

The suite always prefers:

- one hotspot per wave
- stable external behavior
- compatibility seams over blanket rewrites
- verified progress over "heroic" big-bang refactors

## Example Outputs

The execution skill always emits these six decisions before structural edits:

```text
Risk Level: high
Mode: untangle-first
Current State Map: callers, dependencies, side effects
Safety Net: existing tests + missing characterization coverage
Safe Boundary: adapter seam around token store
Verification Gate: targeted tests + smoke checks + rollback point
```

## Repo Layout

```text
skills/
  refactoring-legacy-code/
    SKILL.md
    agents/openai.yaml
    references/
  gsd-legacy-refactor/
    SKILL.md
    agents/openai.yaml
    workflows/legacy-refactor.md
    references/artifact-contract.md
    templates/
scripts/
  install_skills.py
docs/
  demo-cases.md
  github-launch.md
```

## What This Repo Is Not

- not a one-click "rewrite the monolith" button
- not a generic code-cleanup prompt
- not aimed at tiny isolated bugfixes
- not a promise that AI can skip tests, verification, or git hygiene

## Current Status

This project is already usable, but still early and opinionated.

Today it has:

- a superpowers-style execution skill
- a GSD-style orchestration skill
- planning templates
- verification and git-checkpoint rules

Still worth adding:

- real demo repos
- before/after examples
- packaged releases
- forward-tested prompt suites
- screenshots or GIFs of actual runs

## Why Someone Might Star This

- it solves a real pain: refactoring code that feels dangerous to touch
- it has a clear opinion instead of generic AI advice
- it treats safety, planning, and git as part of the product
- it works as both a personal skill and a team handoff workflow

## Roadmap

- Add demo runs on a TypeScript repo and a Python repo
- Add forward-test prompts and expected artifacts
- Add install scripts for common skill directories
- Add release packaging for easier sharing
- Add benchmark comparisons against naive refactor prompts

## Contributing

Issues and PRs are welcome, especially if you can contribute:

- real legacy-code case studies
- safer wave-planning heuristics
- stronger trigger descriptions
- better install and packaging workflows
- public demo repositories

If you try the suite on a real codebase, the most useful feedback is:

- what the risk rating got right
- what it got wrong
- where the first safe boundary should have been smaller
- where the route was too conservative or not conservative enough

## Release Assets

This repo also includes launch-ready materials:

- [docs/demo-cases.md](docs/demo-cases.md)
- [docs/github-launch.md](docs/github-launch.md)
- [LICENSE](LICENSE)

## License

MIT. See [LICENSE](LICENSE).
