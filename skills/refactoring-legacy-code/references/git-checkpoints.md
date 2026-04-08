# Git Checkpoints

Use git to keep each refactor wave recoverable.

## Before Editing

Run this sequence in order:

1. `git status --short`
2. If the worktree is dirty outside the approved boundary, stop and resolve scope first
3. `git rev-parse --short HEAD`
4. Create or switch to the route branch
5. Record the branch and baseline commit in planning artifacts

Use this deterministic branch pattern:

- `codex/legacy-refactor-<slug>`

Use `<slug>` generated from the approved target by:
- lowercasing
- replacing `/`, `\`, spaces, `.`, `_`, and `:` with `-`
- removing characters outside `[a-z0-9-]`
- collapsing repeated hyphens
- trimming leading and trailing hyphens
- truncating to 48 characters

## Per-Wave Rules

- One wave, one commit sequence
- Commit only after verification passes
- If a wave needs multiple commits, keep them inside the same boundary and make the sequence readable
- Do not mix unrelated cleanup into the same commit

Preferred command order after verification passes:

1. `git add -- <boundary files>`
2. `git status --short`
3. `git commit -m "<wave-scoped message>"`
4. Record the resulting commit hash in the execution log

## Commit Shape

Good examples:
- `refactor(auth-service): add facade around legacy token store`
- `refactor(parser): split read path from side effects`
- `test(reporting): lock legacy CSV behavior before module split`

Bad examples:
- `misc cleanup`
- `big refactor`
- `wip`

## If The Wave Fails

- Stop
- Identify whether the failure is a regression, a bad boundary, or missing behavior lock
- Return to the last known-good checkpoint if needed
- Update the route before attempting the next wave

Do not continue into the next wave after a failed verification gate.
