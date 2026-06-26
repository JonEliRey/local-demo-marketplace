const vscode = require('vscode');
const fs = require('fs');
const path = require('path');

function countMarkdownFiles(root) {
  if (!fs.existsSync(root)) return 0;
  let count = 0;
  for (const entry of fs.readdirSync(root, { withFileTypes: true })) {
    const fullPath = path.join(root, entry.name);
    if (entry.isDirectory()) count += countMarkdownFiles(fullPath);
    else if (entry.isFile() && entry.name.endsWith('.md')) count += 1;
  }
  return count;
}

function activate(context) {
  const assetsRoot = path.join(context.extensionPath, 'assets', 'marketplace');
  const diagnostics = vscode.commands.registerCommand('local-demo-marketplace.diagnostics', () => {
    const version = require(path.join(context.extensionPath, 'package.json')).version;
    const revisionPath = path.join(assetsRoot, 'VERSION.json');
    const revision = fs.existsSync(revisionPath) ? JSON.parse(fs.readFileSync(revisionPath, 'utf8')).source_commit : 'unknown';
    const agentCount = countMarkdownFiles(path.join(assetsRoot, '.github', 'agents'));
    const instructionCount = countMarkdownFiles(path.join(assetsRoot, '.github', 'instructions'));
    const channel = vscode.window.createOutputChannel('Local Demo Marketplace');
    channel.clear();
    channel.appendLine(`extension version: ${version}`);
    channel.appendLine(`bundled content SHA: ${revision}`);
    channel.appendLine(`agent count: ${agentCount}`);
    channel.appendLine(`instruction count: ${instructionCount}`);
    channel.show(true);
  });
  const openCatalog = vscode.commands.registerCommand('local-demo-marketplace.openBundledCatalog', async () => {
    const catalog = vscode.Uri.file(path.join(assetsRoot, 'catalog', 'index.md'));
    await vscode.commands.executeCommand('vscode.open', catalog);
  });
  context.subscriptions.push(diagnostics, openCatalog);
}

function deactivate() {}

module.exports = { activate, deactivate };
