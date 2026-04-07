# Safety Net

Use the smallest lock that proves whether the refactor changed observable behavior.

## Order Of Preference

1. Existing tests
2. Characterization tests
3. Golden input/output fixtures
4. Snapshots
5. Manual smoke checklist

## Characterization Test Targets

Prefer locking:
- Public functions and module exports
- HTTP handlers, CLI commands, or job entrypoints
- Repository or service boundaries
- Serialization formats
- Error shapes and status codes

Avoid locking:
- Private helper structure
- Incidental formatting unless consumers depend on it
- Internal call order unless it is a contract

## Minimal Behavior Lock

Build the smallest useful lock:
- Pick one narrow seam
- Record 3-5 representative inputs
- Capture current outputs, side effects, and error cases
- Keep the fixture close to the boundary you plan to change

## If No Tests Exist

Create one of these before broad refactoring:
- A characterization test around the public seam
- A script with fixed inputs and expected outputs
- A golden file for serialized behavior
- A smoke checklist with repeatable commands and expected results

## Verification Gate

Every wave should define:
- Exact commands to run
- What must stay the same
- What is intentionally allowed to change
- How to roll back if the wave fails
