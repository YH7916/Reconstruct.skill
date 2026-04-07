# Demo Cases

Use these cases in screenshots, recordings, or launch posts to show what the suite does.

## Demo 1: TypeScript Auth Module

### Setup

Pretend the repo has:

- `src/auth/index.ts`
- `src/auth/tokenStore.ts`
- `src/auth/sessionService.ts`
- `src/http/middleware/auth.ts`
- weak tests around token persistence

### Problem Framing

The user says:

> This auth code is a god module. Token storage, session orchestration, and HTTP concerns are tangled together. I want to split it without breaking login.

### Recommended Command

```text
$gsd-legacy-refactor src/auth --goal "split auth orchestration from token storage"
```

### Good Demo Moments

- The skill classifies risk as `high`
- It chooses `untangle-first`
- Wave 1 introduces a facade around token storage instead of rewriting auth
- `.planning/refactors/auth/` appears with a clear wave plan
- The user approves the route before edits begin
- Wave 1 finishes with a git checkpoint

### Why This Demo Works

It shows that the suite avoids the naive "rewrite auth" trap and makes a safer first move.

## Demo 2: Python Reporting Parser

### Setup

Pretend the repo has:

- `reporting/legacy_parser.py`
- `reporting/csv_export.py`
- `reporting/excel_export.py`
- shared formatting logic mixed with I/O
- a couple of fixture files but weak structural tests

### Problem Framing

The user says:

> This parser is fragile. Every export change breaks another format. I need to untangle it and then split responsibilities.

### Recommended Command

```text
$gsd-legacy-refactor reporting/legacy_parser.py --goal "separate parsing from export side effects"
```

### Good Demo Moments

- The suite identifies hidden side effects
- It writes a minimal safety-net plan around fixture outputs
- Wave 1 isolates parsing from export writes
- Verification points to golden output fixtures
- The execution log records the approved route and commit checkpoint

### Why This Demo Works

It shows the suite is language-agnostic and not limited to TypeScript repos.

## Best Recording Pattern

For a short GIF or clip:

1. Show the scary legacy target
2. Run `$gsd-legacy-refactor ...`
3. Open `04-WAVE-PLAN.md`
4. Highlight the conservative `untangle-first` choice
5. Show the approval moment
6. Show the git commit/checkpoint after wave 1
