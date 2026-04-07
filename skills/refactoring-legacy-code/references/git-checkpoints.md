# Git Checkpoints

Use git to keep each refactor wave recoverable.

## Before Editing

- Start from a known-good commit
- Prefer a dedicated branch for the refactor
- Record the baseline commit hash in your notes or planning artifact

## Per-Wave Rules

- One wave, one commit sequence
- Commit only after verification passes
- If a wave needs multiple commits, keep them inside the same boundary and make the sequence readable
- Do not mix unrelated cleanup into the same commit

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
