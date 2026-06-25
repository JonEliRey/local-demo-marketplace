#!/usr/bin/env python3
"""Audit registry-driven marketplace artifacts for the agent-runtime aggregator."""
from __future__ import annotations

import argparse
import json
from json import JSONDecodeError
from pathlib import Path
from typing import Any

import yaml

COMPONENT_BUCKETS = {"skills", "agents", "instructions", "commands", "hooks", "mcp_servers", "assets", "bootstrap_files"}


def load_yaml(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        with path.open() as f:
            data = yaml.safe_load(f)
    except OSError as exc:
        return None, f"cannot read YAML {path}: {exc}"
    except yaml.YAMLError as exc:
        return None, f"invalid YAML {path}: {exc}"
    if not isinstance(data, dict):
        return None, f"expected YAML mapping: {path}"
    return data, None


def load_json(path: Path, label: str) -> tuple[dict[str, Any] | None, str | None]:
    try:
        data = json.loads(path.read_text())
    except FileNotFoundError:
        return None, f"missing {label}: {path}"
    except OSError as exc:
        return None, f"cannot read {label}: {path}: {exc}"
    except JSONDecodeError as exc:
        return None, f"invalid {label} JSON: {path}: {exc}"
    if not isinstance(data, dict):
        return None, f"expected {label} JSON object: {path}"
    return data, None


def is_within_root(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True


def safe_relative_path(path_value: str, root: Path) -> Path | None:
    path = Path(path_value)
    if path.is_absolute() or path_value.startswith("~") or ".." in path.parts:
        return None
    candidate = root / path
    if not is_within_root(candidate, root):
        return None
    return candidate


def audit_github_copilot_plugin_marketplace(root: Path, registry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    marketplace_path = root / ".github" / "plugin" / "marketplace.json"
    marketplace, marketplace_error = load_json(marketplace_path, "github copilot marketplace manifest")
    if marketplace_error:
        return [marketplace_error]
    assert marketplace is not None

    if marketplace.get("name") != registry.get("marketplace", {}).get("id"):
        errors.append("github copilot marketplace name does not match registry id")
    metadata = marketplace.get("metadata")
    if not isinstance(metadata, dict) or metadata.get("pluginRoot") != "./plugins":
        errors.append("github copilot marketplace metadata.pluginRoot must be ./plugins")
    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        return [*errors, "github copilot marketplace plugins must be a non-empty list"]

    for plugin in plugins:
        if not isinstance(plugin, dict):
            errors.append("github copilot marketplace plugin entry must be an object")
            continue
        name = plugin.get("name")
        source = plugin.get("source")
        if not isinstance(name, str) or not isinstance(source, str):
            errors.append(f"github copilot marketplace plugin entry missing name/source: {plugin}")
            continue
        plugin_root = root / "plugins" / source
        plugin_manifest_path = plugin_root / ".github" / "plugin" / "plugin.json"
        plugin_manifest, plugin_error = load_json(plugin_manifest_path, "github copilot plugin manifest")
        if plugin_error:
            errors.append(plugin_error)
            continue
        assert plugin_manifest is not None
        if plugin_manifest.get("name") != name:
            errors.append(f"github copilot plugin manifest name mismatch for {name}")
        component_fields = ("agents", "commands", "skills")
        if not any(isinstance(plugin_manifest.get(field), list) and plugin_manifest[field] for field in component_fields):
            errors.append(f"github copilot plugin manifest has no components for {name}")
        for field in component_fields:
            values = plugin_manifest.get(field, [])
            if values is None:
                continue
            if not isinstance(values, list):
                errors.append(f"github copilot plugin {field} must be a list for {name}")
                continue
            for value in values:
                if not isinstance(value, str):
                    errors.append(f"github copilot plugin {field} entry is not a string for {name}: {value}")
                    continue
                component_path = plugin_root / value
                if not is_within_root(component_path, root):
                    errors.append(f"github copilot plugin component escapes repo for {name}: {value}")
                elif not component_path.exists():
                    errors.append(f"github copilot plugin component missing for {name}: {value}")
    return errors


def audit_canonical_graph_mappings(root: Path, registry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for asset in registry.get("assets", []):
        if not isinstance(asset, dict) or not asset.get("graph_enabled"):
            continue
        asset_id = asset.get("id", "<missing-id>")
        components = asset.get("components", {})
        if not isinstance(components, dict):
            errors.append(f"canonical component graph missing components for {asset_id}")
            continue
        declared = {}
        component_paths: dict[str, dict[str, Path]] = {}
        for bucket, entries in components.items():
            if bucket not in COMPONENT_BUCKETS:
                errors.append(f"canonical component unknown bucket for {asset_id}: {bucket}")
                continue
            if not isinstance(entries, list):
                errors.append(f"canonical component graph bucket must be a list for {asset_id}: {bucket}")
                continue
            bucket_ids = set()
            bucket_paths: dict[str, Path] = {}
            for entry in entries:
                if not isinstance(entry, dict):
                    errors.append(f"canonical component graph entry must be a mapping for {asset_id}: {bucket}")
                    continue
                component_id = entry.get("id")
                path_value = entry.get("path")
                if isinstance(component_id, str) and component_id:
                    bucket_ids.add(component_id)
                else:
                    errors.append(f"canonical component id missing for {asset_id}: {bucket}")
                if not isinstance(path_value, str):
                    errors.append(f"canonical component path missing for {asset_id}: {bucket}.{component_id}")
                    continue
                component_path = safe_relative_path(path_value, root)
                if component_path is None:
                    errors.append(f"canonical component path escapes repo for {asset_id}: {path_value}")
                elif not component_path.exists():
                    errors.append(f"canonical component path missing for {asset_id}: {path_value}")
                elif isinstance(component_id, str) and component_id:
                    bucket_paths[component_id] = component_path
                for support_path in entry.get("support_paths", []) or []:
                    if not isinstance(support_path, str):
                        errors.append(f"canonical support path must be a string for {asset_id}: {bucket}.{component_id}")
                        continue
                    if safe_relative_path(support_path, root) is None:
                        errors.append(f"canonical support path escapes repo for {asset_id}: {support_path}")
            declared[bucket] = bucket_ids
            component_paths[bucket] = bucket_paths
        runtime_mappings = asset.get("runtime_mappings", {})
        if not isinstance(runtime_mappings, dict):
            errors.append(f"canonical component graph missing runtime mappings for {asset_id}")
            continue
        agy_mapping = runtime_mappings.get("agy")
        if isinstance(agy_mapping, dict):
            manifest_value = agy_mapping.get("manifest")
            if not isinstance(manifest_value, str):
                errors.append(f"canonical component graph missing agy manifest for {asset_id}")
                continue
            manifest_path = root / manifest_value
            if not is_within_root(manifest_path, root):
                errors.append(f"canonical component graph agy manifest escapes repo for {asset_id}: {manifest_value}")
                continue
            manifest, manifest_error = load_json(manifest_path, "agy plugin manifest")
            if manifest_error:
                errors.append(manifest_error)
                continue
            assert manifest is not None
            actual = manifest.get("x-canonical-components")
            expected = agy_mapping.get("components", {})
            if actual != expected:
                errors.append(f"canonical component drift for {asset_id}: agy manifest components do not match registry")
            if isinstance(expected, dict):
                output_root_value = asset.get("output", {}).get("root")
                output_root = root / output_root_value if isinstance(output_root_value, str) else None
                agy_root = manifest_path.parent
                for bucket, ids in expected.items():
                    if not isinstance(ids, list):
                        errors.append(f"canonical component drift for {asset_id}: agy {bucket} components must be a list")
                        continue
                    for component_id in ids:
                        if component_id not in declared.get(bucket, set()):
                            errors.append(f"canonical component drift for {asset_id}: agy {bucket} references missing {component_id}")
                            continue
                        source_path = component_paths.get(bucket, {}).get(component_id)
                        if source_path is None or output_root is None:
                            continue
                        if bucket == "skills" and source_path.name == "SKILL.md":
                            emitted_path = agy_root / "skills" / source_path.parent.name / "SKILL.md"
                        else:
                            try:
                                emitted_path = agy_root / source_path.relative_to(output_root)
                            except ValueError:
                                errors.append(f"canonical component drift for {asset_id}: {bucket}.{component_id} is outside output root")
                                continue
                        if not emitted_path.exists():
                            errors.append(f"canonical component drift for {asset_id}: agy emitted component missing for {bucket}.{component_id}")
                        elif emitted_path.read_bytes() != source_path.read_bytes():
                            errors.append(f"canonical component drift for {asset_id}: agy emitted component differs for {bucket}.{component_id}")
        codex_mapping = runtime_mappings.get("codex")
        if not isinstance(codex_mapping, dict):
            continue
        marketplace_value = codex_mapping.get("marketplace")
        if not isinstance(marketplace_value, str):
            errors.append(f"canonical component graph missing codex marketplace for {asset_id}")
            continue
        marketplace_path = root / marketplace_value
        if not is_within_root(marketplace_path, root):
            errors.append(f"canonical component graph codex marketplace escapes repo for {asset_id}: {marketplace_value}")
            continue
        codex_marketplace, marketplace_error = load_json(marketplace_path, "codex marketplace manifest")
        if marketplace_error:
            errors.append(marketplace_error)
        elif codex_marketplace is not None:
            plugins = codex_marketplace.get("plugins")
            if not isinstance(plugins, list):
                errors.append(f"codex marketplace plugins must be a list for {asset_id}")
            else:
                plugin_name = asset.get("expose", {}).get("plugin", {}).get("name")
                entries = [plugin for plugin in plugins if isinstance(plugin, dict) and plugin.get("name") == plugin_name]
                if not entries:
                    errors.append(f"codex marketplace missing plugin entry for {asset_id}: {plugin_name}")
                else:
                    source = entries[0].get("source")
                    expected_path = f"./codex-plugins/{plugin_name}"
                    if not isinstance(source, dict) or source.get("path") != expected_path:
                        errors.append(f"codex marketplace source path drift for {asset_id}: {plugin_name}")
        manifest_value = codex_mapping.get("manifest")
        if not isinstance(manifest_value, str):
            errors.append(f"canonical component graph missing codex manifest for {asset_id}")
            continue
        manifest_path = root / manifest_value
        if not is_within_root(manifest_path, root):
            errors.append(f"canonical component graph codex manifest escapes repo for {asset_id}: {manifest_value}")
            continue
        manifest, manifest_error = load_json(manifest_path, "codex plugin manifest")
        if manifest_error:
            errors.append(manifest_error)
            continue
        assert manifest is not None
        actual = manifest.get("x-canonical-components")
        expected = codex_mapping.get("components", {})
        if actual != expected:
            errors.append(f"canonical component drift for {asset_id}: codex manifest components do not match registry")
        if isinstance(expected, dict):
            if expected.get("skills") and manifest.get("skills") != "./skills/":
                errors.append(f"canonical component drift for {asset_id}: codex manifest does not expose mapped skills")
            if expected.get("commands") and manifest.get("commands") != "./commands/":
                errors.append(f"canonical component drift for {asset_id}: codex manifest does not expose mapped commands")
            output_root_value = asset.get("output", {}).get("root")
            output_root = root / output_root_value if isinstance(output_root_value, str) else None
            codex_root = manifest_path.parent.parent
            for bucket, ids in expected.items():
                if not isinstance(ids, list):
                    errors.append(f"canonical component drift for {asset_id}: codex {bucket} components must be a list")
                    continue
                for component_id in ids:
                    if component_id not in declared.get(bucket, set()):
                        errors.append(f"canonical component drift for {asset_id}: codex {bucket} references missing {component_id}")
                        continue
                    source_path = component_paths.get(bucket, {}).get(component_id)
                    if source_path is None or output_root is None:
                        continue
                    if bucket == "skills" and source_path.name == "SKILL.md":
                        emitted_path = codex_root / "skills" / source_path.parent.name / "SKILL.md"
                    else:
                        try:
                            emitted_path = codex_root / source_path.relative_to(output_root)
                        except ValueError:
                            errors.append(f"canonical component drift for {asset_id}: {bucket}.{component_id} is outside output root")
                            continue
                    if not emitted_path.exists():
                        errors.append(f"canonical component drift for {asset_id}: codex emitted component missing for {bucket}.{component_id}")
                    elif emitted_path.read_bytes() != source_path.read_bytes():
                        errors.append(f"canonical component drift for {asset_id}: codex emitted component differs for {bucket}.{component_id}")
    return errors


def audit(root: Path) -> list[str]:
    errors: list[str] = []
    registry, registry_error = load_yaml(root / "registry.yaml")
    if registry_error:
        return [registry_error]
    assert registry is not None

    marketplace_path = root / ".claude-plugin" / "marketplace.json"
    marketplace, marketplace_error = load_json(marketplace_path, "marketplace manifest")
    if marketplace_error:
        errors.append(marketplace_error)
        marketplace = {}
    assert marketplace is not None

    assets = registry.get("assets")
    if not isinstance(assets, list):
        return [*errors, "registry assets must be a list"]

    expected_plugins: list[dict[str, Any]] = []
    for asset in assets:
        if not isinstance(asset, dict):
            errors.append("registry asset entry must be a mapping")
            continue
        expose = asset.get("expose", {})
        if asset.get("target") == "claude-code-plugin-marketplace" and expose.get("enabled"):
            plugin = expose.get("plugin")
            if not isinstance(plugin, dict):
                errors.append(f"missing plugin metadata for {asset.get('id')}")
            else:
                expected_plugins.append(plugin)

    if marketplace.get("name") != registry.get("marketplace", {}).get("id"):
        errors.append("marketplace name does not match registry id")
    if marketplace.get("plugins") != expected_plugins:
        errors.append("marketplace plugin list does not match registry plugin metadata")
    errors.extend(audit_github_copilot_plugin_marketplace(root, registry))
    errors.extend(audit_canonical_graph_mappings(root, registry))

    for asset in assets:
        if not isinstance(asset, dict):
            continue
        asset_id = asset.get("id", "<missing-id>")
        output_root_value = asset.get("output", {}).get("root")
        output_root = root / output_root_value if output_root_value else None
        if output_root_value and output_root_value != "." and output_root and not output_root.exists():
            errors.append(f"missing output root for {asset_id}: {output_root_value}")

        provenance_path = root / "build" / "provenance" / f"{asset_id}.json"
        provenance, provenance_error = load_json(provenance_path, "provenance")
        if provenance_error:
            errors.append(provenance_error)
        elif provenance is not None:
            if provenance.get("asset_id") != asset_id:
                errors.append(f"provenance asset_id mismatch for {asset_id}")
            if provenance.get("adaptation_strategy") != asset.get("adaptation_strategy"):
                errors.append(f"provenance strategy mismatch for {asset_id}")
            output_files = provenance.get("output_files")
            if not isinstance(output_files, list) or not output_files:
                errors.append(f"provenance output_files missing for {asset_id}")
            else:
                for output_file in output_files:
                    if not isinstance(output_file, str):
                        errors.append(f"provenance output file is not a string for {asset_id}: {output_file}")
                        continue
                    output_path = root / output_file
                    if not is_within_root(output_path, root):
                        errors.append(f"provenance output file escapes repo for {asset_id}: {output_file}")
                    elif not output_path.exists():
                        errors.append(f"provenance output file missing for {asset_id}: {output_file}")

            if asset.get("adaptation_strategy") == "model-routing-policy":
                routing = provenance.get("model_routing")
                if not isinstance(routing, dict):
                    errors.append(f"model routing provenance missing for {asset_id}")
                else:
                    if routing.get("scope") != "asset":
                        errors.append(f"model routing scope must be asset for {asset_id}")
                    if routing.get("no_global_provider_changes") is not True:
                        errors.append(f"model routing must declare no global provider changes for {asset_id}")
                    policy_file = routing.get("policy_file")
                    output_root_for_policy = root / str(asset.get("output", {}).get("root", ""))
                    policy_path = output_root_for_policy / policy_file if isinstance(policy_file, str) else None
                    if not policy_path:
                        errors.append(f"model routing policy_file missing for {asset_id}")
                    elif not is_within_root(policy_path, root):
                        errors.append(f"model routing policy file escapes repo for {asset_id}: {policy_file}")
                    elif not policy_path.exists():
                        errors.append(f"model routing policy file missing for {asset_id}: {policy_file}")
                    else:
                        policy, policy_error = load_yaml(policy_path)
                        if policy_error:
                            errors.append(policy_error)
                        elif policy is not None:
                            if policy.get("scope") != "asset":
                                errors.append(f"model routing policy scope must be asset for {asset_id}")
                            if policy.get("no_global_provider_changes") is not True:
                                errors.append(f"model routing policy must not change global providers for {asset_id}")
                            lanes = policy.get("lanes")
                            if not isinstance(lanes, dict) or not {"lower_requirement_research", "high_judgment_escalation"}.issubset(lanes):
                                errors.append(f"model routing policy lanes incomplete for {asset_id}")

        if asset.get("target") == "claude-code-plugin-marketplace":
            plugin = asset.get("expose", {}).get("plugin", {})
            plugin_source = plugin.get("source")
            if not isinstance(plugin_source, str):
                errors.append(f"missing plugin source for {asset_id}")
                continue
            plugin_manifest_path = root / plugin_source / ".claude-plugin" / "plugin.json"
            plugin_manifest, plugin_error = load_json(plugin_manifest_path, "plugin manifest")
            if plugin_error:
                errors.append(plugin_error)
            elif plugin_manifest is not None and plugin_manifest.get("name") != plugin.get("name"):
                errors.append(f"plugin manifest name mismatch for {asset_id}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="repository root to audit")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    errors = audit(root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("marketplace audit passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
