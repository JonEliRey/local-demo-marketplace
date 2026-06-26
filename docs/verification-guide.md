# Verification Guide

Use these commands from repo root. Commands are executable backlinks to the implementation they verify.

## Command guide

| Command | What it proves | Mutates outputs? | Requires Claude CLI? |
|---|---|---:|---:|
| `python3 -m unittest tests.test_marketplace_process -v` | Executable spec: registry required fields, all eight strategies, generated output expectations, marketplace manifest alignment, sidecar preservation, model-routing provenance, audit fail-closed behavior. | Yes: some tests run `scripts/build.py`. | No |
| `python3 scripts/build.py` | Registry can materialize outputs and provenance from locked sources, patches, overlays, recipes, mirrors, and companion-tool recipes. | Yes: rewrites `.claude-plugin/`, `.github/agents`, `.github/instructions`, `plugins/`, `companion-tools/marketplace-audit/`, `build/provenance/`. | No |
| `python3 companion-tools/marketplace-audit/marketplace_audit.py --root .` | Registry, marketplace manifest, plugin manifests, provenance, output paths, and model-routing policy are internally consistent. | No | No |
| `python3 scripts/cli_uat.py` | All registered adaptation scenarios pass: `patch`, `sidecar`, `combine`, `overlay`, `model-routing-policy`, `generated-composite`, `mirror`, `companion-tool`. | Yes: starts by running `scripts/build.py`. | No; skips plugin validation if Claude is missing. |
| `python3 scripts/cli_uat.py --require-claude` | Same as above plus `claude plugin validate` for marketplace root and generated Claude plugins. | Yes | Yes |
| `python3 scripts/target.py export --target local-demo-marketplace` | Copies allowlisted generated runtime outputs into an ignored target checkout under `.targets/`. | Yes: writes the target checkout only. | No |
| `python3 scripts/target.py check --target local-demo-marketplace` | Confirms the target export record is internally consistent and forbidden paths are absent. | No | No |
| `python3 companion-tools/marketplace-audit/marketplace_audit.py --root .` | In a generated distribution repo, validates the export record, marketplace manifests, Codex package index, and target-facing docs without requiring generator-only `registry.yaml`. | No | No |
| `python3 scripts/check_marketplace.py` | In the generator repo only, full deterministic local/CI gate: unit tests, compileall, build, audit, CLI UAT, optional Claude validation skip, whitespace check, generated-output diff check. | Yes | No; skips Claude validation if missing. |
| `python3 scripts/check_marketplace.py --require-claude` | Generator repo only, full gate plus required Claude plugin validation. | Yes | Yes |
| `git diff --check` | No whitespace errors in working-tree diff. | No | No |
| `git diff --exit-code -- .claude-plugin .github/agents .github/instructions plugins companion-tools/marketplace-audit` | Generated committed runtime outputs are in sync after build/UAT. | No | No |

## Recommended local gate

```bash
python3 companion-tools/marketplace-audit/marketplace_audit.py --root .
```

Use `python3 scripts/check_marketplace.py` only in the generator repository. Use `--require-claude` only where the Claude CLI is installed and authenticated enough to run `claude plugin validate`.

## What the tests prove

`tests/test_marketplace_process.py` is the executable spec. It asserts:

- Registry includes all implemented strategies: `patch`, `sidecar`, `combine`, `overlay`, `model-routing-policy`, `generated-composite`, `mirror`, `companion-tool`.
- Every asset has governance fields (`id`, `type`, `target`, `adaptation_strategy`, `expose`).
- CI/check gate invokes build, audit, UAT, diff, and Claude validation hooks.
- Build creates expected Copilot, Claude plugin, companion CLI, marketplace, and provenance outputs.
- Provenance records strategy/source refs/outputs.
- The Claude marketplace includes current plugins: `ai-enablement-intake`, `research-briefing`, `routed-research-briefing`, `agentic-tdd-loop`, `anthropic-internal-comms-mirror`.
- Sidecar output preserves upstream base bytes and emits separate policy.
- Model-routing policy is asset-scoped and prohibits global provider changes.
- Audit tooling fails closed on corrupt provenance.

## Interpretation notes

- Passing CLI/CI gates does **not** prove VS Code/Copilot UI recognition; that needs workstation UAT.
- Passing Claude validation proves plugin manifests are structurally accepted by Claude CLI, not that end users have installed or used them.
- Generated provenance contains timestamps; regenerate immediately before audits.
