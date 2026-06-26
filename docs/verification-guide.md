# Verification Guide

Use these commands from repo root. Distribution repository checks are listed first because exported target repositories do not include generator-only files such as `registry.yaml`, `scripts/build.py`, or `tests/`.

## Distribution repo checks

| Command | What it proves | Mutates outputs? | Requires Claude CLI? |
|---|---|---:|---:|
| `python3 companion-tools/marketplace-audit/marketplace_audit.py --root .` | In a generated distribution repo, validates the export record, marketplace manifests, Codex package index, and target-facing docs without requiring generator-only `registry.yaml`. | No | No |
| `git diff --check` | No whitespace errors in working-tree diff. | No | No |

## Generator repo checks

Run these only in the generator repository, where `registry.yaml`, `scripts/`, and `tests/` are present.

| Command | What it proves | Mutates outputs? | Requires Claude CLI? |
|---|---|---:|---:|
| `python3 -m unittest tests.test_marketplace_process -v` | Executable spec: registry required fields, all eight strategies, generated output expectations, marketplace manifest alignment, sidecar preservation, model-routing provenance, audit fail-closed behavior. | Yes: some tests run `scripts/build.py`. | No |
| `python3 scripts/build.py` | Registry can materialize outputs and provenance from locked sources, patches, overlays, recipes, mirrors, and companion-tool recipes. | Yes: rewrites generated runtime outputs and provenance. | No |
| `python3 companion-tools/marketplace-audit/marketplace_audit.py --root .` | Registry, marketplace manifest, plugin manifests, provenance, output paths, and model-routing policy are internally consistent. | No | No |
| `python3 scripts/cli_uat.py` | All registered adaptation scenarios pass: `patch`, `sidecar`, `combine`, `overlay`, `model-routing-policy`, `generated-composite`, `mirror`, `companion-tool`. | Yes: starts by running `scripts/build.py`. | No; skips plugin validation if Claude is missing. |
| `python3 scripts/cli_uat.py --require-claude` | Same as above plus `claude plugin validate` for marketplace root and generated Claude plugins. | Yes | Yes |
| `python3 scripts/target.py export --target local-demo-marketplace` | Copies allowlisted generated runtime outputs into an ignored target checkout under `.targets/`. | Yes: writes the target checkout only. | No |
| `python3 scripts/target.py check --target local-demo-marketplace` | Confirms the target export record is internally consistent and forbidden paths are absent. | No | No |
| `mkdir -p dist && cd vscode-extension && npx --yes @vscode/vsce package --out ../dist/local-demo-marketplace.vsix` | Packages the generated VS Code wrapper as an installable VSIX. | Yes: writes `dist/`. | No |
| `python3 scripts/check_marketplace.py` | In the generator repo only, full deterministic local/CI gate: unit tests, compileall, build, audit, CLI UAT, optional Claude validation skip, whitespace check, generated-output diff check. | Yes | No; skips Claude validation if missing. |
| `python3 scripts/check_marketplace.py --require-claude` | Generator repo only, full gate plus required Claude plugin validation. | Yes | Yes |
| `git diff --exit-code -- .claude-plugin .agents .github/agents .github/instructions .github/plugin plugins skills agy-plugins codex-plugins hermes-plugins vscode-extension companion-tools/marketplace-audit` | Generated committed runtime outputs are in sync after build/UAT. | No | No |

## Recommended local gate

```bash
python3 companion-tools/marketplace-audit/marketplace_audit.py --root .
```

Use `python3 scripts/check_marketplace.py` only in the generator repository. Use `--require-claude` only where the Claude CLI is installed and authenticated enough to run `claude plugin validate`.

## What the generator tests prove

In the generator repository, `tests/test_marketplace_process.py` is the executable spec. Exported distribution repositories do not include `tests/`. The generator tests assert:

- Registry includes all implemented strategies: `patch`, `sidecar`, `combine`, `overlay`, `model-routing-policy`, `generated-composite`, `mirror`, `companion-tool`.
- Every asset has governance fields (`id`, `type`, `target`, `adaptation_strategy`, `expose`).
- CI/check gate invokes build, audit, UAT, diff, and Claude validation hooks.
- Build creates expected Copilot, Claude plugin, VS Code extension wrapper, companion CLI, marketplace, and provenance outputs.
- Provenance records strategy/source refs/outputs.
- The Claude marketplace includes current plugins: `ai-enablement-intake`, `research-briefing`, `routed-research-briefing`, `agentic-tdd-loop`, `anthropic-internal-comms-mirror`, `runtime-release-reviewer`.
- Sidecar output preserves upstream base bytes and emits separate policy.
- Model-routing policy is asset-scoped and prohibits global provider changes.
- Audit tooling fails closed on corrupt provenance.

## Interpretation notes

- Passing CLI/CI gates proves VSIX packaging, but command-palette install UAT still requires a workstation with the `code` CLI.
- Passing Claude validation proves plugin manifests are structurally accepted by Claude CLI, not that end users have installed or used them.
- Generated provenance contains timestamps; regenerate immediately before audits.
