# Refactor Playbook

Use this file after the risk and safety-net decisions are already made.

## `untangle-first` Actions

Prefer these moves:
- Add characterization coverage at the current seam
- Introduce a facade that freezes the old interface
- Route side effects through one helper or port
- Extract one dependency direction at a time
- Separate orchestration from pure logic

Good first-wave outcomes:
- Fewer direct callers to the messy core
- Fewer side effects inside the core
- A stable adapter around unstable internals
- Clear ownership of mutable state

Before implementation:
- Show the route and get confirmation on the first seam

After implementation:
- Verify and commit the seam change before proposing the next wave

## `refactor-wave` Actions

Prefer these moves:
- Split one god file by responsibility
- Rename concepts inside one bounded module
- Replace internal helper chains with a simpler flow
- Invert a dependency behind an adapter
- Collapse duplicate logic once behavior is locked

Before implementation:
- Confirm the wave boundary and rollback point

After implementation:
- Run the verification gate
- Commit the completed wave
- Recommend the next wave only after the current one is green

## Wave Template

For each wave, define:
- Goal
- Boundary
- Allowed changes
- Forbidden changes
- Verification gate
- Rollback point

If you cannot write those six items clearly, the wave is not ready.
