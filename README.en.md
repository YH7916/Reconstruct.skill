# 屎山重构.skill

<p align="center">
  <img src="docs/assets/social-preview-zh.png" alt="屎山重构.skill showcase" width="100%" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Route--First-Approval%20Before%20Edits-0F766E?style=flat-square" alt="Route-First" />
  <img src="https://img.shields.io/badge/Multi--Platform-Codex%20%7C%20Claude%20%7C%20Agents-1D4ED8?style=flat-square" alt="Multi-Platform" />
  <img src="https://img.shields.io/badge/Git%20Checkpoints-Per--Wave%20Safety-F59E0B?style=flat-square" alt="Git Checkpoints" />
  <img src="https://img.shields.io/badge/Planning%20Artifacts-.planning%20First-7C3AED?style=flat-square" alt="Planning Artifacts" />
</p>

<p align="center">
  Route-first AI skills for refactoring dangerous legacy code without blowing up tightly coupled systems.
</p>

<p align="center">
  <a href="README.md">中文 README</a>
</p>

## What Problem It Solves

`屎山重构.skill` is a two-layer skill suite for risky legacy refactors:

| Skill | Role |
|------|------|
| `refactoring-legacy-code` | The execution skill. It maps blast radius, locks behavior, picks a safe boundary, and refactors in bounded waves. |
| `gsd-legacy-refactor` | The orchestration skill. It inspects the target, writes `.planning/refactors/<slug>/` artifacts, asks for route approval, then executes with git checkpoints. |

This suite is built for the cases where AI refactors usually go wrong:

- dense dependency graphs
- hidden side effects
- shared mutable state
- modules that break three things when you touch one

The default sequence is:

1. map the current shape
2. lock behavior
3. estimate blast radius
4. show the route to the user
5. execute only after approval
6. checkpoint each verified wave with git

## Platform Fit

| Host | How to use it |
|------|---------------|
| Codex | Install into `$CODEX_HOME/skills` or `~/.codex/skills`, then invoke by skill name or natural language |
| Claude Code | Install into `~/.claude/skills`, then ask the agent to use the skill |
| Agent Skills compatible clients | Install into `./.agents/skills` or the client's configured skill directory |
| Other agents / runners | Load the target `SKILL.md` plus its neighboring `references/`, `templates/`, and `workflows/` folders |

This project is not meant to be Codex-only. The content is ordinary `SKILL.md`-based skill folders, so any host that supports Agent Skills, personal skill directories, or prompt-loaded skill packs can use it.

## Quick Start

### Install

#### Option 1: Use the installer script

```text
python scripts/install_skills.py --platform codex --force
```

```text
python scripts/install_skills.py --platform claude --force
```

```text
python scripts/install_skills.py --platform agents --force
```

For a custom destination:

```text
python scripts/install_skills.py --platform custom --dest /path/to/skills --force
```

Useful flags:

- `--dest <path>` installs to a custom path
- `--mode link` creates symlinks instead of copies
- `--dry-run` previews the destination

#### Option 2: Copy the folders manually

Copy these directories into your host's skill directory:

```text
skills/refactoring-legacy-code
skills/gsd-legacy-refactor
```

Common destinations:

```text
Codex:        $CODEX_HOME/skills or ~/.codex/skills
Claude Code:  ~/.claude/skills
Repo local:   ./.agents/skills
```

### How To Invoke It

#### Command-style hosts

```text
$gsd-legacy-refactor src/auth --goal "split auth orchestration from token storage"
```

```text
$refactoring-legacy-code src/reporting/legacy_parser.py
```

#### Natural-language hosts

```text
Use gsd-legacy-refactor on src/auth.
Plan first, write the .planning artifacts, show me the route, and wait for approval before editing code.
```

```text
Use refactoring-legacy-code on src/reporting/legacy_parser.py.
If the blast radius is high, switch to untangle-first and stop after presenting the safe route.
```

#### Hosts without automatic skill discovery

Provide the target `SKILL.md` file directly to the agent and keep the neighboring resource folders intact:

```text
skills/refactoring-legacy-code/SKILL.md
skills/gsd-legacy-refactor/SKILL.md
```

If your host can follow relative file references, the original folder layout is enough. If it cannot, pass the relevant `references/`, `templates/`, and `workflows/` files alongside the main skill file.

## How It Works

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

## What A Typical Run Looks Like

1. inspect the target area, entrypoints, dependencies, and side effects
2. write `.planning/refactors/<slug>/`
3. classify risk and choose `untangle-first` or `refactor-wave`
4. show the route for approval
5. execute only the explicitly approved waves
6. verify and checkpoint each completed wave with git

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

## Repo Layout

```text
skills/
  refactoring-legacy-code/
  gsd-legacy-refactor/
scripts/
  install_skills.py
docs/
  assets/social-preview-zh.png
  demo-cases.md
  github-launch.md
```

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
