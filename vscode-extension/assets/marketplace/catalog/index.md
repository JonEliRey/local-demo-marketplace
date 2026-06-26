# Agent Runtime Aggregator Catalog

Status: reference implementation catalog. The generator repository `registry.yaml` is the source of truth; this distribution repository contains exported runtime artifacts. Build/audit references: `scripts/build.py` in the generator repository, plus `companion-tools/marketplace-audit/marketplace_audit.py` and `docs/verification-guide.md` in exported distributions.

## Consumption setup

Claude Code plugin marketplace, after this repo is available from GitHub:

```text
claude plugin marketplace add JonEliRey/local-demo-marketplace --scope local
claude plugin install <plugin-name>@agent-runtime-marketplace --scope local
claude plugin list
```

VS Code / Copilot: clone/open this repository and confirm `.github/agents/` and `.github/instructions/` are detected by a client version that supports repository custom agents/instructions. UI recognition remains a recorded gap until workstation UAT.

Installable VS Code wrapper:

```text
cd vscode-extension
npx --yes @vscode/vsce package --out /tmp/local-demo-marketplace.vsix
code --install-extension /tmp/local-demo-marketplace.vsix
```

Codex CLI marketplace, after build output is present:

```text
codex plugin marketplace add https://github.com/JonEliRey/local-demo-marketplace
codex plugin list --marketplace agent-runtime-marketplace
codex plugin add agentic-tdd-loop@agent-runtime-marketplace
```

## Asset cards

| Asset id | Strategy | Runtime target | Exported output path | Consumption command/action | Distribution verification |
|---|---|---|---|---|---|
| `technical-writer-agent` | `patch` | `copilot-vscode-agent` | `.github/agents/technical-writer.agent.md`; side instruction `.github/instructions/ai-adoption.instructions.md` | Open repo in VS Code with Copilot custom agents/instructions enabled. | `python3 companion-tools/marketplace-audit/marketplace_audit.py --root .` |
| `sidecar-technical-writer-agent` | `sidecar` | `copilot-vscode-agent` | `.github/agents/sidecar-technical-writer.agent.md`; policy `.github/instructions/sidecar-technical-writer-policy.instructions.md` | Open repo in VS Code with Copilot custom agents/repository instructions enabled. | `python3 companion-tools/marketplace-audit/marketplace_audit.py --root .` |
| `vscode-extension-wrapper` | `generated-wrapper` | `vscode-extension` | `vscode-extension/` | `npx --yes @vscode/vsce package --out /tmp/local-demo-marketplace.vsix`; run `Local Demo Marketplace: Diagnostics` after install. | `python3 companion-tools/marketplace-audit/marketplace_audit.py --root .` |
| `ai-enablement-intake-skill` | `combine` | `claude-code-plugin-marketplace`; Codex plugin marketplace | `plugins/ai-enablement-intake`; `codex-plugins/ai-enablement-intake` | `claude plugin install ai-enablement-intake@agent-runtime-marketplace --scope local`; `codex plugin add ai-enablement-intake@agent-runtime-marketplace` | `python3 companion-tools/marketplace-audit/marketplace_audit.py --root .` |
| `research-briefing-skill` | `overlay` | `claude-code-plugin-marketplace`; Codex plugin marketplace | `plugins/research-briefing`; `codex-plugins/research-briefing` | `claude plugin install research-briefing@agent-runtime-marketplace --scope local`; `codex plugin add research-briefing@agent-runtime-marketplace` | `python3 companion-tools/marketplace-audit/marketplace_audit.py --root .` |
| `routed-research-briefing-skill` | `model-routing-policy` | `claude-code-plugin-marketplace`; Codex plugin marketplace | `plugins/routed-research-briefing`; `codex-plugins/routed-research-briefing` | `claude plugin install routed-research-briefing@agent-runtime-marketplace --scope local`; `codex plugin add routed-research-briefing@agent-runtime-marketplace` | `python3 companion-tools/marketplace-audit/marketplace_audit.py --root .` |
| `agentic-tdd-loop-skill` | `generated-composite` | `claude-code-plugin-marketplace`; AGY plugin; Codex plugin marketplace | `plugins/agentic-tdd-loop`; `agy-plugins/agentic-tdd-loop`; `codex-plugins/agentic-tdd-loop` | `claude plugin install agentic-tdd-loop@agent-runtime-marketplace --scope local`; `agy plugin install agy-plugins/agentic-tdd-loop`; `codex plugin add agentic-tdd-loop@agent-runtime-marketplace` | `python3 companion-tools/marketplace-audit/marketplace_audit.py --root .` |
| `anthropic-internal-comms-mirror-skill` | `mirror` | `claude-code-plugin-marketplace`; Codex plugin marketplace | `plugins/anthropic-internal-comms-mirror`; `codex-plugins/anthropic-internal-comms-mirror` | `claude plugin install anthropic-internal-comms-mirror@agent-runtime-marketplace --scope local`; `codex plugin add anthropic-internal-comms-mirror@agent-runtime-marketplace` | `python3 companion-tools/marketplace-audit/marketplace_audit.py --root .` |
| `runtime-release-reviewer-agent` | `mirror` | `claude-code-plugin-marketplace`; Codex plugin marketplace | `plugins/runtime-release-reviewer`; `codex-plugins/runtime-release-reviewer` | `claude plugin install runtime-release-reviewer@agent-runtime-marketplace --scope local`; `codex plugin add runtime-release-reviewer@agent-runtime-marketplace` | `python3 companion-tools/marketplace-audit/marketplace_audit.py --root .` |
| `marketplace-audit-tool` | `companion-tool` | `companion-cli` | `companion-tools/marketplace-audit/marketplace_audit.py` | `python3 companion-tools/marketplace-audit/marketplace_audit.py --root .` | `python3 companion-tools/marketplace-audit/marketplace_audit.py --root .` |

## Current Claude plugins

Defined by generator registry `expose.plugin` entries and exported into `.claude-plugin/marketplace.json`:

- `ai-enablement-intake`
- `research-briefing`
- `routed-research-briefing`
- `agentic-tdd-loop`
- `anthropic-internal-comms-mirror`
- `runtime-release-reviewer`

## Current Codex plugins

Defined in `.agents/plugins/marketplace.json` and generated under `codex-plugins/`:

- `ai-enablement-intake`
- `research-briefing`
- `routed-research-briefing`
- `agentic-tdd-loop`
- `anthropic-internal-comms-mirror`
- `runtime-release-reviewer`
