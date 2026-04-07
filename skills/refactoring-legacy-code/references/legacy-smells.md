# Legacy Smells

Use these smells to judge coupling and blast radius.

## High-Risk Smells

- Circular imports or circular runtime dependencies
- Shared mutable state with no clear owner
- Hidden writes to files, databases, caches, or process state
- One module called by many layers for unrelated reasons
- Giant files that mix orchestration, business logic, and I/O
- Flags and conditionals that change behavior across many call sites
- Soft contracts stored only in comments or tribal memory

## Medium-Risk Smells

- Two or three modules that know too much about each other
- Weak test coverage but predictable entrypoints
- Old abstractions that leak one level beyond their boundary
- Repeated compatibility code spread across callers

## Lower-Risk Smells

- Large but self-contained modules
- Stable public API with ugly internals
- Repetition inside one bounded area
- Clear seams for adapters or facades

## Questions To Ask

- How many entrypoints can reach this code?
- Which side effects happen here?
- Which callers rely on quirks rather than explicit contracts?
- Can one adapter hold the old interface steady while internals move?
- Is the first useful wave a cleanup wave or an untangling wave?
