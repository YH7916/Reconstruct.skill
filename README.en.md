# 屎山重构.skill

<p align="center">
  <img src="docs/assets/social-preview-zh.png" alt="屎山重构.skill showcase" width="100%" />
</p>

<p align="center">
  <a href="https://github.com/YH7916/Reconstruct.skill/stargazers"><img src="https://img.shields.io/github/stars/YH7916/Reconstruct.skill?style=flat-square" alt="GitHub stars" /></a>
  <a href="https://github.com/YH7916/Reconstruct.skill/blob/main/LICENSE"><img src="https://img.shields.io/github/license/YH7916/Reconstruct.skill?style=flat-square" alt="License" /></a>
  <a href="https://github.com/YH7916/Reconstruct.skill/commits/main"><img src="https://img.shields.io/github/last-commit/YH7916/Reconstruct.skill?style=flat-square" alt="Last commit" /></a>
</p>

<p align="center">
  Route-first AI skills for refactoring dangerous legacy code without blowing up tightly coupled systems.
</p>

<p align="center">
  <a href="README.md">中文 README</a>
</p>

## What It Is

`屎山重构.skill` is a two-layer skill suite for risky legacy refactors:

| Skill | Role |
|------|------|
| `refactoring-legacy-code` | The execution skill. It maps blast radius, locks behavior, picks a safe boundary, and refactors in bounded waves. |
| `gsd-legacy-refactor` | The orchestration skill. It inspects the target, writes `.planning/refactors/<slug>/` artifacts, asks for route approval, then executes with git checkpoints. |

This README structure takes cues from high-star skill/tool repos such as [anthropics/skills](https://github.com/anthropics/skills) and [daymade/claude-code-skills](https://github.com/daymade/claude-code-skills): lead with value, show install fast, make the workflow concrete, then provide deeper docs.

## Why It Exists

Most AI refactor helpers break down exactly where legacy systems hurt most:

- dense dependency graphs
- hidden side effects
- shared mutable state
- modules that break three things when you touch one

This project is opinionated about that failure mode.

It does not assume the answer is "rewrite everything."  
It assumes the safer sequence is:

1. map the current shape
2. lock behavior
3. estimate blast radius
4. show the route to the user
5. execute only after approval
6. checkpoint each verified wave with git

## Why It Feels Different

- `Route first, edit second`: no structural edits before an explicit approved route.
- `Automatic downgrade for high risk`: tangled code falls back to `untangle-first`.
- `Git is part of execution`: baseline checkpoint, branch strategy, per-wave commits.
- `Planning artifacts are first-class`: every risky refactor gets a documented handoff package.
- `Bilingual trigger coverage`: descriptions include both English and Chinese trigger phrases.

## Quick Start

### Install

Copy both skill folders into your skill directory:

```text
$CODEX_HOME/skills
```

Or, if `CODEX_HOME` is unset:

```text
~/.codex/skills
```

You can also use the bundled installer:

```text
python scripts/install_skills.py --force
```

Useful flags:

- `--dest <path>` installs to a custom path
- `--mode link` creates symlinks instead of copies
- `--dry-run` previews the destination

### Run A Full Risky Refactor Flow

```text
$gsd-legacy-refactor src/auth --goal "split auth orchestration from token storage"
```

What happens:

1. inspect the target
2. write `.planning/refactors/<slug>/`
3. classify risk and choose mode
4. show the route for approval
5. execute approved waves
6. checkpoint progress with git

### Run A Single Guardrailed Wave

```text
$refactoring-legacy-code src/reporting/legacy_parser.py
```

Use this when you already know the boundary and want execution guardrails.

## How It Thinks

The suite uses two execution modes:

| Mode | Use when |
|------|----------|
| `untangle-first` | Risk is high, behavior is fuzzy, coupling is dense, or tests are weak |
| `refactor-wave` | Boundary is small, callers are known, and verification is credible |

It always prefers:

- one hotspot per wave
- stable external behavior
- compatibility seams over blanket rewrites
- verified progress over heroic big-bang changes

## Artifact Output

`$gsd-legacy-refactor` writes:

```text
.planning/refactors/<slug>/
  01-CONTEXT.md
  02-RISK-MAP.md
  03-SAFETY-NET.md
  04-WAVE-PLAN.md
  05-VERIFY.md
  06-HANDOFF.md
  07-EXECUTION-LOG.md
```

The execution skill always emits these decisions before structural edits:

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
  assets/social-preview-zh.png
  demo-cases.md
  github-launch.md
```

## Docs

- [Demo cases](docs/demo-cases.md)
- [GitHub launch kit](docs/github-launch.md)
- [Chinese README](README.md)
- [License](LICENSE)

## What This Is Not

- not a one-click monolith rewrite button
- not a generic cleanup prompt
- not for tiny isolated bug fixes
- not a promise that AI can skip tests, verification, or git hygiene

## Roadmap

- add real demo runs on TypeScript and Python repos
- add forward-test prompts and expected artifacts
- add release packaging for easier sharing
- add benchmark comparisons against naive refactor prompts

## Contributing

Issues and PRs are welcome, especially for:

- real legacy-code case studies
- safer wave-planning heuristics
- better trigger descriptions
- install and packaging improvements
- public demo repos

## License

MIT. See [LICENSE](LICENSE).
