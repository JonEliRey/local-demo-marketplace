# Agent Runtime Marketplace — Distribution Context

This repository is an exported distribution of runtime-native agent assets.

Use it as a consumer-facing marketplace/package repository. Start with:

- `README.md` for install commands.
- `catalog/index.md` for exported assets.
- `docs/verification-guide.md` for distribution-safe checks.

Verify this checkout with:

```bash
python3 companion-tools/marketplace-audit/marketplace_audit.py --root .
```

Runtime surfaces in this distribution:

- Claude Code: `.claude-plugin/marketplace.json`, `plugins/`
- Codex CLI: `.agents/plugins/marketplace.json`, `codex-plugins/`
- AGY / Antigravity: `agy-plugins/`
- Hermes: `skills/`, `hermes-plugins/`
- GitHub Copilot / VS Code: `.github/agents/`, `.github/instructions/`

Generator-only build inputs, tests, and provenance are intentionally not part of this distribution checkout.
