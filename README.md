# Agent Runtime Aggregator

Agent Runtime Aggregator is a consumable marketplace-style repository for agent/runtime assets. It exposes the same curated assets through native package shapes used by multiple harnesses: Claude Code plugins, Antigravity (AGY) plugins, Hermes skills/plugins, and GitHub/Copilot repository assets.

The source of truth is the registry plus committed recipes, patches, overlays, and locked upstream sources. Runtime-specific files are adapter outputs from that source of truth, not separate doctrines and not separate repositories per consuming agent.

The repository is intended to be cloned or added as a marketplace source by humans and agents that need reusable agent skills, commands, and agent components.

## What is included

| Runtime / harness | Consumable surface | Primary location |
|---|---|---|
| Claude Code | Plugin marketplace and plugin packages | `.claude-plugin/marketplace.json`, `plugins/` |
| Antigravity / AGY | Plugin packages with co-located components | `agy-plugins/` |
| Hermes | Direct skill install surface and Hermes plugin package | `skills/`, `hermes-plugins/` |
| GitHub Copilot / VS Code | Repository custom agents and instructions | `.github/agents/`, `.github/instructions/` |
| Operators / maintainers | Catalog and verification commands | `catalog/index.md`, `docs/verification-guide.md` |

## Quick install

Use the commands for the runtime you want to consume from. The generated distribution repository is `JonEliRey/local-demo-marketplace`; replace the repo owner/name if this repository is mirrored under another organization.

### Claude Code

```bash
claude plugin marketplace add JonEliRey/local-demo-marketplace --scope local
claude plugin install agentic-tdd-loop@agent-runtime-marketplace --scope local
claude plugin list
```

Available Claude Code plugins are listed in `catalog/index.md`.

### AGY / Antigravity

```bash
git clone https://github.com/JonEliRey/local-demo-marketplace.git
cd local-demo-marketplace
agy plugin validate agy-plugins/agentic-tdd-loop
agy plugin install agy-plugins/agentic-tdd-loop
agy plugin list
```

AGY package roots live under `agy-plugins/`.

### Hermes

Direct skill install from the repository:

```bash
hermes skills install JonEliRey/local-demo-marketplace/skills/agentic-tdd-loop --yes
hermes skills list --source hub
```

Hermes plugin-manager package:

```bash
hermes plugins install https://github.com/JonEliRey/local-demo-marketplace#hermes-plugins/agent-runtime-marketplace --no-enable
hermes plugins list --plain --no-bundled
```

Note: direct skill install and plugin-manager install are the supported Hermes consumption paths currently verified here. Assets that originate from other harness ecosystems are consumed by Hermes only after this repository maps them into Hermes-native skills or plugin packages.

### Codex

```bash
codex plugin marketplace add https://github.com/JonEliRey/local-demo-marketplace
codex plugin list --marketplace agent-runtime-marketplace --available
codex plugin add agentic-tdd-loop@agent-runtime-marketplace
codex plugin list
```

Codex-native packages live under `codex-plugins/` and are indexed by `.agents/plugins/marketplace.json`.

### GitHub Copilot / VS Code repository assets

Clone or open the repository in a supported Copilot/VS Code client and use the repository assets under:

```text
.github/agents/
.github/instructions/
```

## Browse available assets

Start with the catalog:

```text
catalog/index.md
```

It lists each asset, target runtime, output path, and consumption command.

## Verify the repository

From a fresh clone of the generated distribution repository:

```bash
python3 companion-tools/marketplace-audit/marketplace_audit.py --root .
```

This validates the exported marketplace manifests, plugin manifests, Codex package index, and target export metadata. Maintainer-only generator checks such as `python3 scripts/check_marketplace.py` live in the generator repository, not in this exported distribution repository. See `docs/verification-guide.md` for command details.

## Consumer-facing file map

| Need | Start here |
|---|---|
| Install or browse assets | `catalog/index.md` |
| Verify package integrity | `docs/verification-guide.md` |
| Understand generated runtime surfaces | `docs/component-coverage-map.md` |
| Inspect licenses / upstream notices | `THIRD_PARTY_NOTICES.md` |

## Publication note

This repository is safe to consume as a private repository when the consuming runtime has access to it. For unauthenticated client environments, publish or mirror only after confirming repository visibility, license posture, and intended distribution scope.
