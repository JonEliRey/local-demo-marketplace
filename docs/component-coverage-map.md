# Component Coverage Map

This exported distribution repository contains runtime-native artifacts generated from a separate generator repository. The generator registry is the canonical source of truth; this repository is the consumable output.

## Distribution verification loop

```text
exported runtime artifacts -> companion marketplace audit -> native harness install/list smoke
```

Run the distribution audit from the repository root:

```bash
python3 companion-tools/marketplace-audit/marketplace_audit.py --root .
```

## Exported runtime surfaces

| Runtime / harness | Exported surface | Primary paths | Distribution check |
|---|---|---|---|
| Claude Code | Plugin marketplace and plugin packages | `.claude-plugin/marketplace.json`, `plugins/` | `claude plugin marketplace add <repo>; claude plugin install <plugin>@agent-runtime-marketplace --scope local` |
| Codex CLI | Plugin marketplace and plugin packages | `.agents/plugins/marketplace.json`, `codex-plugins/` | `codex plugin marketplace add <repo>; codex plugin list --marketplace agent-runtime-marketplace` |
| AGY / Antigravity | Plugin packages with co-located components | `agy-plugins/` | `agy plugin validate agy-plugins/agentic-tdd-loop` |
| Hermes | Direct skill pack and plugin package | `skills/`, `hermes-plugins/` | `hermes plugins install <repo>#hermes-plugins/agent-runtime-marketplace --no-enable` |
| GitHub Copilot / VS Code | Repository custom agents and instructions | `.github/agents/`, `.github/instructions/` | Open the repository in a supported Copilot / VS Code client. UI recognition still requires workstation UAT. |
| VS Code extension | Installable wrapper with bundled marketplace assets and diagnostics command | `vscode-extension/` | `npx --yes @vscode/vsce package --out /tmp/local-demo-marketplace.vsix`; install with VS Code CLI where available. |
| Companion audit | Self-verification CLI | `companion-tools/marketplace-audit/marketplace_audit.py` | `python3 companion-tools/marketplace-audit/marketplace_audit.py --root .` |

## Exported asset coverage

| Asset id | Exported runtime surfaces |
|---|---|
| `technical-writer-agent` | GitHub/Copilot repository agent and instruction |
| `sidecar-technical-writer-agent` | GitHub/Copilot repository agent and sidecar policy instruction |
| `vscode-extension-wrapper` | VS Code VSIX wrapper bundling generated agents, instructions, catalog, and diagnostics command |
| `ai-enablement-intake-skill` | Claude plugin, Codex plugin, AGY plugin, Hermes skill/plugin surfaces |
| `research-briefing-skill` | Claude plugin, Codex plugin, AGY plugin, Hermes skill/plugin surfaces |
| `routed-research-briefing-skill` | Claude plugin, Codex plugin, AGY plugin, Hermes skill/plugin surfaces |
| `agentic-tdd-loop-skill` | Claude plugin, Codex plugin, AGY plugin, Hermes skill/plugin surfaces |
| `anthropic-internal-comms-mirror-skill` | Claude plugin, Codex plugin, AGY plugin, Hermes skill/plugin surfaces |
| `runtime-release-reviewer-agent` | Claude plugin, Codex plugin, AGY plugin |
| `marketplace-audit-tool` | Companion audit CLI |

## Generator-only context

The generator repository contains the registry, recipes, patches, overlays, provenance files, test suite, and build/check scripts that produce this distribution. Those generator-only files are intentionally absent from exported distribution repositories.

Use `docs/verification-guide.md` for the split between distribution checks and generator checks.

## Known remaining gaps

- VS Code desktop install/command-palette UAT requires a workstation with the `code` CLI; generator CI packages the VSIX wrapper.
- Hook/MCP asset packaging is not implemented.
- Optional build refactor may be useful if asset count/strategy complexity increases.
