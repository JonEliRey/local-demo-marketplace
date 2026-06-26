# Local Demo Marketplace VS Code Extension

This package is a thin installable VS Code wrapper around the generated Local Demo Marketplace assets.

## UAT

```bash
cd vscode-extension
npx --yes @vscode/vsce package --out /tmp/local-demo-marketplace.vsix
code --install-extension /tmp/local-demo-marketplace.vsix
```

After install, run `Local Demo Marketplace: Diagnostics` from the command palette.
The command reports extension version, bundled source commit, agent count, and instruction count.

Publishing with `vsce publish` is approval-gated.
