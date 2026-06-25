---
name: agent-marketplace-intake
description: Use when evaluating or packaging agent/runtime assets for the adopting organization enablement marketplace reference implementation.
disable-model-invocation: true
---

# the adopting organization Agent Marketplace Intake

Use this skill to turn a candidate agent/runtime asset into a small, reviewable marketplace entry.

## Operating frame

This is a team-ready reference implementation workflow. Do not include real adopting-organization policy, private repositories, credentials, customer data, production routes, or internal access instructions unless an approved enterprise scope explicitly permits it.

## Intake checklist

1. Identify the target runtime.
   - GitHub Copilot repository instruction
   - VS Code / Copilot custom agent
   - Claude Code plugin skill or agent
   - Hermes skill
   - Companion tool

2. Record source provenance.
   - upstream repo or URL
   - locked commit/ref/version
   - source path
   - license evidence
   - whether the output is mirror, customized, augmented-base, composite, or companion-tool

3. Decide the packaging pattern.
   - Mirror: expose upstream as-is.
   - Customized: base upstream plus patch or overlay.
   - Augmented-base: source A remains the dominant source/style; source B contributes a traced ingredient; the generated result is distinct output Z.
   - Composite: create company-owned output Z from multiple traced sources.

4. Verify consumption in the real mechanism.
   - For Claude Code: add the GitHub marketplace and install the plugin.
   - For Copilot / VS Code: open the repository containing `.github/agents` or `.github/instructions` and confirm the asset is visible.
   - For Hermes: install from a skill URL or configured skill tap when that adapter exists.

5. Capture evidence.
   - command run
   - output observed
   - files created
   - limitations or friction
   - next decision

## Output standard

Return a concise intake note with these headings:

- Candidate asset
- Target runtime
- Source provenance
- Packaging pattern
- Consumption test
- Risks / approval gates
- Next useful action
