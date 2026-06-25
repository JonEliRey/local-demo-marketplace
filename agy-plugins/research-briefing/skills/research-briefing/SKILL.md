---
name: research-briefing
description: Use when turning research, review findings, or agent-runtime marketplace evidence into concise team-ready briefings.
disable-model-invocation: true
---

# the adopting organization Research Briefing

This skill adapts the upstream Anthropic `internal-comms` pattern into a team-ready research and enablement briefing workflow.

## Use when

- summarizing AGY/Claude Code/Codex/governor review findings;
- preparing a 3P update: Progress, Plans, Problems;
- converting marketplace test evidence into an executive-readable note;
- documenting what changed, what was verified, and what still needs client-side UAT.

## Briefing structure

Use this structure by default:

1. **Purpose** — one sentence stating the decision or workflow being advanced.
2. **Progress** — what is now verified with command/file evidence.
3. **Plans** — the next deterministic case, test, or rollout gate.
4. **Problems / Risks** — unproven runtime behavior, licensing, supply chain, or user adoption risks.
5. **Decision needed** — only if the next action is approval-gated.

## team-ready boundaries

- Do not include real adopting-organization policy, private code, credentials, customer data, or production routes.
- Use placeholders when a briefing needs enterprise context before approved source material exists.
- Separate verified command output from interpretation.
- Keep upstream provenance visible when discussing adapted skills, agents, plugins, hooks, or instructions.

## Output contract

Return concise markdown with these headings:

- Purpose
- Progress
- Plans
- Problems / Risks
- Evidence
- Decision needed, if any
