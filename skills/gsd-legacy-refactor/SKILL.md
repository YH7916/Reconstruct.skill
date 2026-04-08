---
name: gsd-legacy-refactor
description: Use when a risky legacy refactor needs route confirmation, staged execution, .planning artifacts, or git checkpoints across a module, service, or repo. Trigger on requests to map blast radius, confirm a refactor route first, then execute wave by wave for high-risk legacy code, 屎山, 技术债, 依赖混乱, or 拆模块 work.
---

# GSD Legacy Refactor

<codex_skill_adapter>
## A. Skill Invocation
- This skill is invoked by mentioning `$gsd-legacy-refactor`.
- Treat all user text after `$gsd-legacy-refactor` as `{{LEGACY_ARGS}}`.
- If no arguments are present, inspect the current repository and use the most obvious target path or symbol from the user request.

## B. AskUserQuestion -> request_user_input Mapping
- Map GSD-style `AskUserQuestion` calls to Codex `request_user_input` when available.
- If structured input is unavailable, ask the question plainly.
- If explicit approval is missing, stop after planning.
- Default conservatively only for planning details such as scope and risk, never for approval.

## C. Task() -> spawn_agent Mapping
- If the host platform supports subagents, `Task(subagent_type="X", prompt="Y")` maps to `spawn_agent(agent_type="X", message="Y")`.
- If subagents are unavailable, execute the workflow inline and keep the same artifact contract.
</codex_skill_adapter>

<objective>
Turn a risky legacy refactor into a bounded engineering package and then carry it through execution. Default flow: Discover -> Assess -> Lock behavior -> Draft route -> Confirm -> Execute waves -> Verify -> Finish.
</objective>

<execution_context>
@./workflows/legacy-refactor.md
@./references/artifact-contract.md
</execution_context>

<context>
Command form:
- `$gsd-legacy-refactor <target>`
- Optional `--goal "<goal>"`
- Optional `--scope module|service|repo`
- Optional `--text`

Defaults:
- Scope: `module`
- Goal: `reduce coupling and make future change safer`
- Output directory: `.planning/refactors/<slug>/`
- Execution mode: route-first, then execute after confirmation
- Source edits: forbidden before route approval
- Git mode: branch plus per-wave checkpoints
- Approval semantics: full-route approval unless the user narrows it
</context>

<process>
Execute `@./workflows/legacy-refactor.md` end-to-end.

Before route approval, only write `.planning/refactors/<slug>/` artifacts.
After route approval, execute the approved waves and use git checkpoints throughout.
</process>

<approval_contract>
- No source edits without explicit route approval
- Ambiguous responses are not approval
- Approval applies to the exact route shown
- A changed route requires re-approval
</approval_contract>

<offer_next>
Output this markdown directly:

------------------------------------------------------------
LEGACY REFACTOR COMPLETE
------------------------------------------------------------

**Target:** {target}
**Risk:** {low|medium|high}
**Mode:** {untangle-first|refactor-wave}
**Artifacts:** `.planning/refactors/{slug}/`
**Branch:** `{branch}`
**Completed Waves:** `{completed_waves}`

## Result

- Route was approved before source edits
- Execution stopped only if a documented boundary or verification gate failed
- Each completed wave was checkpointed with git

## Review

Review artifacts:
- `.planning/refactors/{slug}/01-CONTEXT.md`
- `.planning/refactors/{slug}/02-RISK-MAP.md`
- `.planning/refactors/{slug}/04-WAVE-PLAN.md`
- `.planning/refactors/{slug}/07-EXECUTION-LOG.md`
- `.planning/refactors/{slug}/06-HANDOFF.md`
</offer_next>

<success_criteria>
- Target parsed
- Repo context inspected
- Blast radius classified with evidence
- Safety net assessed
- Mode chosen conservatively
- Route shown to user before edits
- Approval captured explicitly before edits
- Planning artifacts written
- Git branch or checkpoint strategy recorded
- Completed waves verified and committed
- Final status provided
</success_criteria>
