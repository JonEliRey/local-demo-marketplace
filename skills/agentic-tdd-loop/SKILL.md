---
name: agentic-tdd-loop
description: Use when implementing team-ready agent/runtime work through strict RED/GREEN TDD, agent selection, adversarial review, and simplification gates.
disable-model-invocation: true
---

# the adopting organization Agentic TDD Loop

## Purpose

This generated composite skill combines test-driven development, agent-driven development, agent selection, adversarial review, and code simplification into one repeatable operating contract.

Canonical sequence:

```text
RED → GREEN → REVIEW → FIX → SIMPLIFY
```

Use it when a task changes code, generated marketplace assets, workflow doctrine, tests, or agent/runtime behavior. Do not use it as ceremony for trivial read-only inspection.

team-ready boundary: do not include real private adopting-organization policy, secrets, customer data, production routes, or access changes unless an approved enterprise source and approval gate exists.

## Agent Selection Router

Route work by consequence, ambiguity, and reversibility.

| Work shape | Default executor | Review depth |
| --- | --- | --- |
| Mechanical local edit, known file, reversible | Small/local agent or the maintainer directly | Lightweight adversarial check plus tests |
| Focused code feature or bug fix | Codex or implementation subagent | TDD evidence plus one adversarial reviewer |
| Architecture, workflow doctrine, or cross-runtime design | Frontier agent such as Claude Code plus governor oversight | Multi-CLI adversarial review |
| Source/fact research or external runtime behavior | AGY/Gemini or research seat | Source-grounded review with links/evidence |
| High-risk security, secrets, permissions, deploys, people, public routing | Stop for approval before action | Council review and explicit approval gate |

Definitions:

- **Small/local agent**: use for bounded, reversible edits and deterministic script work.
- **Frontier agent**: use for architecture, ambiguous tradeoffs, high-coupling design, and deep critique.
- **Multi-CLI adversarial review**: use AGY, Codex, Claude Code, and a governor reviewer where available; if a harness fails, record the attempt and continue with labeled fallback rather than pretending the seat participated.

## Operating Loop

1. **Intake**
   - Restate the user goal in one sentence.
   - Identify acceptance criteria and approval gates.
   - Decide whether this is code, documentation, workflow doctrine, marketplace adaptation, or runtime behavior.

2. **RED**
   - Write the smallest failing test or deterministic artifact check first.
   - For documentation/process work, the RED test may assert required sections, marketplace exposure, generated output, provenance, or forbidden private content.
   - Run the focused test and capture the expected failure.

3. **GREEN**
   - Implement the minimum change that passes the RED test.
   - Keep source generation deterministic: registry + locked refs + recipes + patches + overlays.
   - Run focused tests, then relevant build/validation commands.

4. **REVIEW**
   - Run adversarial review after the work is mechanically green.
   - Ask reviewers for material findings only: correctness, missing tests, unsafe boundary, scope drift, maintainability, simpler design.

5. **FIX**
   - Convert material review findings into tests where practical.
   - Fix the smallest behavior or artifact gap.
   - Re-run tests and validation.

6. **SIMPLIFY**
   - Run a simplification pass after correctness is stable.
   - Apply only behavior-preserving simplifications unless the user approves a broader change.

7. **SHIP / RECORD**
   - Commit only verified local work.
   - Push only to approved repos/remotes.
   - Record evidence, reviewer attempts, and unproven limits.

## Mandatory Adversarial Review

Always perform some adversarial review before calling work complete. Scale depth by risk.

Minimum check:

- one adversarial pass by governor against test output and changed artifacts.

Standard code/workflow check:

- Codex or implementation-focused reviewer for code/test quality;
- AGY/Gemini for fact/runtime/source-shape critique when external facts matter;
- Claude Code for architecture, strategy, and long-horizon coupling when available;
- final governor synthesis.

Reviewer prompt:

```text
Review the current diff against the stated user intent. Be adversarial but material. Find correctness bugs, missing tests, unsafe behavior, scope drift, maintainability debt, and simpler equivalent designs. Give file:line evidence, severity, why it matters, smallest fix, and verdict.
```

## Simplification Pass

Run simplification after review fixes are green.

Look for:

- duplicated logic;
- hand-authored artifacts that should be generated;
- parameter sprawl;
- stale generated output;
- missing helper functions;
- avoidable network or filesystem work;
- unclear routing or approval boundaries.

Do not simplify by weakening tests, removing provenance, or broadening autonomy.

## Approval Gates

Stop before:

- protected-main merges;
- production deploys;
- DNS, Cloudflare, firewall, tunnel, public routing, or access changes;
- secrets, OAuth clients, tokens, service accounts, or credential movement;
- publishing public packages or marketplaces;
- deleting meaningful data, repos, logs, or backups;
- contacting people or changing permissions.

## Evidence Checklist

Before completion, record:

- RED failure observed;
- GREEN passing focused test;
- relevant full tests/build/validation;
- generated artifacts inspected;
- provenance written;
- adversarial review attempts and outcomes;
- material findings fixed or explicitly deferred;
- simplification pass outcome;
- GitHub or runtime consumption evidence when deployment is part of the task;
- remaining unproven limits.

## Output Contract

Final response should state:

- what changed;
- what was tested;
- what reviewers found;
- what remains unproven;
- next useful action.
