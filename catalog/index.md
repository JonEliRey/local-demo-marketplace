# Agent Runtime Aggregator Catalog

Status: reference implementation catalog. Source of truth: `registry.yaml`. Build/audit: `scripts/build.py`, `companion-tools/marketplace-audit/marketplace_audit.py`, `docs/verification-guide.md`.

## Consumption setup

Claude Code plugin marketplace, after this repo is available from GitHub:

```text
claude plugin marketplace add JonEliRey/agent-runtime-aggregator --scope local
claude plugin install <plugin-name>@agent-runtime-marketplace --scope local
claude plugin list
```

VS Code / Copilot: clone/open this repository and confirm `.github/agents/` and `.github/instructions/` are detected by a client version that supports repository custom agents/instructions. UI recognition remains a recorded gap until workstation UAT.

Codex CLI marketplace, after build output is present:

```text
codex plugin marketplace add <repo-path-or-owner/repo>
codex plugin list --marketplace agent-runtime-marketplace --available
codex plugin add agentic-tdd-loop@agent-runtime-marketplace
```

## Asset cards

| Asset id | Strategy | Runtime target | Output path | Consumption command/action | Provenance path | Verification hook |
|---|---|---|---|---|---|---|
| `technical-writer-agent` | `patch` | `copilot-vscode-agent` | `.github/agents/technical-writer.agent.md`; side instruction `.github/instructions/ai-adoption.instructions.md` | Open repo in VS Code with Copilot custom agents/instructions enabled. | `build/provenance/technical-writer-agent.json` | `scripts/cli_uat.py::uat_patch` |
| `sidecar-technical-writer-agent` | `sidecar` | `copilot-vscode-agent` | `.github/agents/sidecar-technical-writer.agent.md`; policy `.github/instructions/sidecar-technical-writer-policy.instructions.md` | Open repo in VS Code with Copilot custom agents/repository instructions enabled. | `build/provenance/sidecar-technical-writer-agent.json` | `scripts/cli_uat.py::uat_sidecar` |
| `ai-enablement-intake-skill` | `combine` | `claude-code-plugin-marketplace` | `plugins/ai-enablement-intake` | `claude plugin install ai-enablement-intake@agent-runtime-marketplace --scope local` | `build/provenance/ai-enablement-intake-skill.json` | `scripts/cli_uat.py::uat_combine` |
| `research-briefing-skill` | `overlay` | `claude-code-plugin-marketplace` | `plugins/research-briefing` | `claude plugin install research-briefing@agent-runtime-marketplace --scope local` | `build/provenance/research-briefing-skill.json` | `scripts/cli_uat.py::uat_overlay` |
| `routed-research-briefing-skill` | `model-routing-policy` | `claude-code-plugin-marketplace` | `plugins/routed-research-briefing` | `claude plugin install routed-research-briefing@agent-runtime-marketplace --scope local` | `build/provenance/routed-research-briefing-skill.json` | `scripts/cli_uat.py::uat_model_routing` |
| `agentic-tdd-loop-skill` | `generated-composite` | `claude-code-plugin-marketplace`; AGY plugin; Codex plugin marketplace | `plugins/agentic-tdd-loop`; `agy-plugins/agentic-tdd-loop`; `codex-plugins/agentic-tdd-loop` | `claude plugin install agentic-tdd-loop@agent-runtime-marketplace --scope local`; `agy plugin install agy-plugins/agentic-tdd-loop`; `codex plugin add agentic-tdd-loop@agent-runtime-marketplace` | `build/provenance/agentic-tdd-loop-skill.json` | `scripts/cli_uat.py::uat_generated_composite`; `scripts/runtime_consumption_smoke.py --runtime agy`; `scripts/runtime_consumption_smoke.py --runtime codex` |
| `anthropic-internal-comms-mirror-skill` | `mirror` | `claude-code-plugin-marketplace` | `plugins/anthropic-internal-comms-mirror` | `claude plugin install anthropic-internal-comms-mirror@agent-runtime-marketplace --scope local` | `build/provenance/anthropic-internal-comms-mirror-skill.json` | `scripts/cli_uat.py::uat_mirror` |
| `marketplace-audit-tool` | `companion-tool` | `companion-cli` | `companion-tools/marketplace-audit/marketplace_audit.py` | `python3 companion-tools/marketplace-audit/marketplace_audit.py --root .` | `build/provenance/marketplace-audit-tool.json` | `scripts/cli_uat.py::uat_companion_tool` |

## Current Claude plugins

Defined in `registry.yaml` `expose.plugin` entries and generated into `.claude-plugin/marketplace.json`:

- `ai-enablement-intake`
- `research-briefing`
- `routed-research-briefing`
- `agentic-tdd-loop`
- `anthropic-internal-comms-mirror`
