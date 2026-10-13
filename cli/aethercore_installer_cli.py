#!/usr/bin/env python3
import argparse
import json
import os
import shutil
import sys
import tempfile
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

DEFAULT_REPO_URL = (
    "https://raw.githubusercontent.com/AsafViana/"
    "aethercore-patches/refs/heads/main/generated/patches.json"
)

IGNORED_DIRS = {".venv", "__pycache__", ".git", "node_modules"}


def _get_patches_dir(explicit_dir):
    if explicit_dir:
        return Path(explicit_dir).expanduser().resolve()
    env_dir = os.getenv("AETHERCORE_PATCHES_DIR")
    if env_dir:
        return Path(env_dir).expanduser().resolve()
    return Path.home() / ".aethercore" / "patches"


def _get_repo_url(explicit_url):
    if explicit_url:
        return explicit_url
    return os.getenv("AETHERCORE_PATCHES_REPO_URL", DEFAULT_REPO_URL)


def _print_json(obj):
    print(json.dumps(obj, indent=2, ensure_ascii=True))


def _read_manifest(patch_dir):
    manifest_path = patch_dir / "manifest.yaml"
    if not manifest_path.exists():
        return None

    info = {"name": patch_dir.name, "version": "unknown", "transport": "unknown"}

    try:
        with open(manifest_path, "r", encoding="utf-8") as handle:
            for raw in handle:
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                if ":" not in line:
                    continue
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key in ("name", "version", "transport"):
                    info[key] = value
    except Exception:
        return None

    info["path"] = str(patch_dir)
    return info


def list_installed_patches(patches_dir):
    installed = []
    if not patches_dir.exists():
        return installed

    for patch_dir in patches_dir.iterdir():
        if not patch_dir.is_dir():
            continue
        if patch_dir.name in IGNORED_DIRS:
            continue
        manifest = _read_manifest(patch_dir)
        if manifest:
            installed.append(manifest)
    return installed


def _fetch_json(url, timeout):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            data = response.read().decode("utf-8")
            return json.loads(data)
    except (urllib.error.URLError, json.JSONDecodeError) as exc:
        return {"error": f"Failed to fetch patches: {exc}"}


def list_remote_patches(repo_url, timeout):
    return _fetch_json(repo_url, timeout)


def _download_file(url, target_path, timeout):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            target_path.write_bytes(response.read())
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Download failed: {exc}") from exc


def _detect_extracted_dir(temp_extract_dir, patch_name):
    candidate = temp_extract_dir / "patches" / patch_name
    if candidate.exists():
        return candidate
    candidate = temp_extract_dir / patch_name
    if candidate.exists():
        return candidate
    candidate = temp_extract_dir / "manifest.yaml"
    if candidate.exists():
        return temp_extract_dir
    return None


def install_patch(patches_dir, repo_url, patch_name, timeout):
    remote_patches = list_remote_patches(repo_url, timeout)
    if isinstance(remote_patches, dict) and "error" in remote_patches:
        return remote_patches

    patch_info = next((p for p in remote_patches if p.get("name") == patch_name), None)
    if not patch_info:
        return {"error": f"Patch '{patch_name}' not found in registry"}

    patches_dir.mkdir(parents=True, exist_ok=True)
    temp_zip = patches_dir / f"{patch_name}.zip"
    target_dir = patches_dir / patch_name

    with tempfile.TemporaryDirectory(prefix=f"tmp_{patch_name}_", dir=str(patches_dir)) as temp_dir:
        temp_extract_dir = Path(temp_dir)
        try:
            _download_file(patch_info["download_url"], temp_zip, timeout)
            if target_dir.exists():
                shutil.rmtree(target_dir)
            with zipfile.ZipFile(temp_zip, "r") as zip_ref:
                zip_ref.extractall(temp_extract_dir)

            extracted_patch_dir = _detect_extracted_dir(temp_extract_dir, patch_name)
            if not extracted_patch_dir:
                raise RuntimeError("Invalid ZIP structure")

            shutil.move(str(extracted_patch_dir), str(target_dir))
        except Exception as exc:
            return {"error": f"Install failed: {exc}"}
        finally:
            if temp_zip.exists():
                temp_zip.unlink()

    return {
        "success": True,
        "message": f"Patch '{patch_name}' v{patch_info.get('version', 'unknown')} installed",
        "path": str(target_dir),
    }


def uninstall_patch(patches_dir, patch_name):
    target_dir = patches_dir / patch_name
    if not target_dir.exists():
        available = [
            p.name for p in patches_dir.iterdir() if p.is_dir() and p.name not in IGNORED_DIRS
        ] if patches_dir.exists() else []
        return {
            "error": f"Patch '{patch_name}' not found. Available: {', '.join(available)}"
        }
    try:
        shutil.rmtree(target_dir)
        return {"success": True, "message": f"Patch '{patch_name}' uninstalled"}
    except Exception as exc:
        return {"error": f"Uninstall failed: {exc}"}


def update_patch(patches_dir, repo_url, patch_name, timeout):
    uninstall_result = uninstall_patch(patches_dir, patch_name)
    if "error" in uninstall_result:
        existing = list_installed_patches(patches_dir)
        if not any(p.get("name") == patch_name for p in existing):
            return uninstall_result
    return install_patch(patches_dir, repo_url, patch_name, timeout)


def sync_patch(patches_dir, repo_url, patch_name, timeout):
    return update_patch(patches_dir, repo_url, patch_name, timeout)


def _build_parser():
    parser = argparse.ArgumentParser(
        prog="aethercore-installer",
        description="Patch installer CLI for AetherCore patches",
    )
    parser.add_argument(
        "--patches-dir",
        help="Directory to install patches (default: ~/.aethercore/patches)",
    )
    parser.add_argument(
        "--repo-url",
        help="Registry URL (default uses AETHERCORE_PATCHES_REPO_URL or built-in)",
    )
    parser.add_argument("--timeout", type=int, default=30, help="Network timeout in seconds")

    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list-remote", help="List patches from registry")
    sub.add_parser("list-installed", help="List installed patches")

    install = sub.add_parser("install", help="Install a patch")
    install.add_argument("patch_name")

    uninstall = sub.add_parser("uninstall", help="Uninstall a patch")
    uninstall.add_argument("patch_name")

    update = sub.add_parser("update", help="Update a patch")
    update.add_argument("patch_name")

    sync = sub.add_parser("sync", help="Sync (install/update) a patch")
    sync.add_argument("patch_name")

    return parser


def main():
    parser = _build_parser()
    args = parser.parse_args()

    patches_dir = _get_patches_dir(args.patches_dir)
    repo_url = _get_repo_url(args.repo_url)

    if args.command == "list-remote":
        result = list_remote_patches(repo_url, args.timeout)
    elif args.command == "list-installed":
        result = list_installed_patches(patches_dir)
    elif args.command == "install":
        result = install_patch(patches_dir, repo_url, args.patch_name, args.timeout)
    elif args.command == "uninstall":
        result = uninstall_patch(patches_dir, args.patch_name)
    elif args.command == "update":
        result = update_patch(patches_dir, repo_url, args.patch_name, args.timeout)
    elif args.command == "sync":
        result = sync_patch(patches_dir, repo_url, args.patch_name, args.timeout)
    else:
        result = {"error": f"Unknown command: {args.command}"}

    _print_json(result)
    if isinstance(result, dict) and "error" in result:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
