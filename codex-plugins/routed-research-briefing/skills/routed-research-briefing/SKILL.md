---
name: routed-research-briefing
description: Use when preparing team-ready research briefings with asset-scoped model-routing guidance.
disable-model-invocation: true
---

# the adopting organization Routed Research Briefing

This generated output Z adapts a public internal-comms briefing pattern with company-owned model-routing policy metadata.

## Model Routing Policy

The canonical policy file is `model-routing.yaml` in this plugin root.

Use the policy as asset-scoped guidance only. It does not modify global provider settings, billing, secrets, or user environments.

## Lanes

### lower_requirement_research

Use for source collection, first-pass summaries, and low-risk briefing drafts. The placeholder default model is `google/gemini-3.5-flash` until an enterprise-approved route replaces it.

### high_judgment_escalation

Use for architecture judgment, final recommendation review, sensitive policy interpretation, and disagreement resolution. The placeholder default model is `anthropic/claude-sonnet-4-6` until an enterprise-approved route replaces it.

## Escalation rules

Escalate when any of these are true:

- source evidence is weak;
- the recommendation affects team standards;
- policy, security, licensing, reputation, or cost risk appears;
- reviewers disagree materially;
- verification fails or cannot be performed.

## Output contract

Return concise markdown with:

- Purpose
- Sources inspected
- Lane used
- Findings
- Risks / uncertainties
- Recommendation
- Evidence
