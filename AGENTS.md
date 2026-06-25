# Agent Runtime Aggregator — Agent Context

## Mission

Help humans and agents consume, verify, and maintain this repository of runtime-specific agent assets.

The repository exposes curated assets through native harness surfaces: Claude Code plugin marketplace packages, AGY plugin packages, Hermes skills/plugins, and GitHub/Copilot repository agents/instructions.

## Source-of-truth order

1. Runtime package files in this repository.
2. `registry.yaml` and generated provenance under `build/provenance/`.
3. Executable verification commands.
4. Runtime documentation and inspected upstream repositories.
5. Historical development notes under `docs/development/`.

## Consumer paths

- Browse assets: `catalog/index.md`.
- Claude Code marketplace: `.claude-plugin/marketplace.json`, `plugins/`.
- AGY packages: `agy-plugins/`.
- Hermes direct skills: `skills/`.
- Hermes plugin package: `hermes-plugins/agent-runtime-marketplace/`.
- GitHub/Copilot repository assets: `.github/agents/`, `.github/instructions/`.

## Verification

Run from repo root:

```bash
python3 scripts/check_marketplace.py
```

Focused checks:

```bash
python3 scripts/build.py
python3 companion-tools/marketplace-audit/marketplace_audit.py --root .
python3 scripts/cli_uat.py
```

Use Claude-required checks only when Claude CLI is available:

```bash
python3 scripts/check_marketplace.py --require-claude
```

## Maintainer paths

- Maintainer guide: `docs/development/maintainer-guide.md`.
- Registry reference: `docs/registry-reference.md`.
- Verification guide: `docs/verification-guide.md`.
- Component coverage: `docs/component-coverage-map.md`.
- Target contracts: `docs/target-contracts/`.

## Asset addition protocol

1. Add/update `registry.yaml`.
2. Add committed inputs under `recipes/`, `patches/`, or `overlays/`.
3. Ensure `scripts/build.py` generates the target output and provenance.
4. Add or extend `scripts/cli_uat.py` and `tests/test_marketplace_process.py` coverage.
5. Update `catalog/index.md` for user-visible assets.
6. Run `python3 scripts/check_marketplace.py`.

## Publication boundaries

Changing repository visibility, creating a new public repo, attaching a new remote, or publishing into a client-facing location requires explicit approval.

Do not expose secrets, private profiles, local home paths, browser profiles, or non-consumer development history through public distribution surfaces.
