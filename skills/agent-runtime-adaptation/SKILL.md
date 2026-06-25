---
name: agent-runtime-adaptation
description: Use when adapting upstream agent/runtime assets into a deterministic marketplace using patch, overlay, and combine workflows with provenance, tests, deployment, and adversarial review gates.
version: 0.1.0
author: Jonathan Reyes + governor
license: private
metadata:
  hermes:
    tags: [agent-runtime, marketplace, skills, plugins, patch, overlay, tdd]
    related_skills: [test-driven-development, subagent-driven-development, github-operations]
---

# Agent Runtime Adaptation

## Overview

Use this skill to adapt upstream skills, plugins, hooks, agents, instructions, or companion tools into a repeatable marketplace repository.

The process is deterministic first. LLM judgment may help choose content and review quality, but the build must be reproducible from committed source controls:

```text
registry + locked upstream refs + patches + overlays + recipes + provenance + tests = generated runtime artifacts
```

## When to Use

Use when:

- adapting a public upstream skill, plugin, hook, agent, or instruction;
- creating a team-ready enablement asset;
- combining the best parts of two or more source systems;
- publishing a Claude Code plugin marketplace or Copilot/VS Code repository asset;
- deciding whether a change is a patch, overlay, augmented-base, composite, mirror, or companion-tool.

Do not use for:

- unreviewed private company policy;
- secret-bearing files;
- production rollout without approval;
- one-off local copy/paste with no provenance.

## Adaptation Types

| Type | Use when | Source of truth | Required proof |
| --- | --- | --- | --- |
| Mirror | Expose upstream mostly as-is | registry locked ref | output equals source, provenance names source |
| Patch | Modify upstream file content | `git format-patch` file | patch applies from clean ref |
| Overlay | Add company-owned files | committed `overlays/<asset-id>/` | collision policy tested |
| Patch + overlay | Modify upstream and add files | patch plus overlay | both proofs pass |
| Augmented-base | A remains target, B contributes value | A source + B ingredient + patch/overlay | provenance distinguishes A and B |
| Composite | A+B produce company-owned output Z | committed/generated Z + recipe/provenance | Z is not falsely represented as patch of A/B |
| Companion-tool | Tool is documented/packaged for use | install/use docs | no fake plugin abstraction |

## Deterministic Workflow

1. Create or update `registry.yaml`.
   - asset id
   - type
   - adaptation strategy
   - target runtime
   - source repo/ref/path
   - patches
   - overlays
   - output paths
   - consumption command

2. Write RED tests first.
   - registry has required strategy/source coverage
   - build outputs expected runtime files
   - provenance records strategy, source refs, patches, overlays, outputs
   - marketplace manifests validate
   - conflict test fails closed

3. Implement the smallest builder change.
   - locked ref checkout
   - patch application
   - overlay copy with fail-on-conflict unless same content
   - target-specific output
   - provenance JSON

4. Build and validate.
   - `python3 -m unittest tests.test_marketplace_process -v`
   - `python3 scripts/build.py`
   - `claude plugin validate .`
   - `claude plugin validate plugins/<plugin-name>`
   - `python3 scripts/build.py --conflict-test`

5. Deploy to GitHub.
   - commit locally
   - push to the approved repo
   - verify GitHub contains marketplace and runtime paths

6. Test consumption.
   - Claude Code: add marketplace and install plugin from GitHub
   - Copilot/VS Code: verify `.github/agents/*.agent.md` and `.github/instructions/*.instructions.md` are present; client UI recognition must be tested in VS Code
   - Other CLIs: ask Codex, Claude Code, AGY, and a governor reviewer to inspect/use each artifact where their harness supports it

7. Run adversarial review.
   - AGY/Gemini: factual/runtime risk and source-shape review
   - Claude Code: architecture/strategy and failure-mode review when quota is available
   - Codex: code/test review where available
   - Governor: final governor verification against real tool output

## Patterns

### Patch pattern

```bash
git clone <upstream> work/<asset>
cd work/<asset>
git checkout <locked-ref>
# edit upstream file
git add <file>
git commit -m 'Add local adaptation context'
git format-patch -1 HEAD --stdout > ../../patches/<asset>/0001-change.patch
```

### Overlay pattern

```text
overlays/<asset-id>/<runtime-relative-path>
```

The builder copies overlay files into the output root. Default policy is fail on conflict unless the destination already has identical content, making repeated builds idempotent while still failing on divergent collisions.

### Combine pattern

Use augmented-base when one source remains dominant, while still treating the generated result as a distinct output Z:

```text
A base + B ingredient -> patch/overlay against A output
```

Use composite when sources are peers:

```text
A + B + company-authored review -> new C artifact
```

## Anti-Patterns

1. **Local-only success.** If the artifact cannot be consumed from GitHub or the intended enterprise repo, the marketplace goal is not proven.
2. **Floating `main`.** Always lock source refs before build.
3. **LLM synthesis as normal build step.** Use LLMs for review or drafting, then commit approved outputs.
4. **One universal plugin abstraction.** Keep Claude plugins, Copilot agents, Hermes skills, hooks, and companion tools distinct until an adapter earns its place.
5. **Hidden source debt.** Every output needs source refs, license evidence, patches, overlays, and transformation notes.
6. **Reviewer self-report as proof.** Verify with file reads, command output, GitHub API, and installed-plugin inspection.

## Example Case Set

A healthy early reference implementation should include at least:

1. GitHub Copilot / VS Code agent from `github/awesome-copilot` using patch or patch+overlay.
2. Claude Code plugin skill adapted from `anthropics/skills` using overlay.
3. Composite Claude Code plugin skill combining an Anthropic skill pattern and a GitHub Copilot agent pattern.

## Verification Checklist

- [ ] RED tests were observed before implementation.
- [ ] `python3 -m unittest tests.test_marketplace_process -v` passes.
- [ ] `python3 scripts/build.py` passes.
- [ ] `python3 scripts/build.py --conflict-test` fails closed.
- [ ] Claude marketplace validates.
- [ ] Each plugin manifest validates.
- [ ] GitHub-hosted marketplace install succeeds.
- [ ] VS Code/Copilot assets use documented file names such as `.agent.md` and `.instructions.md`.
- [ ] Provenance records source refs, strategy, outputs, patches, and overlays.
- [ ] AGY/Claude Code/Codex/governor review attempts and outcomes are recorded.
