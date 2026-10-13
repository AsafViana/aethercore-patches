#!/usr/bin/env sh
set -e

PYZ_PATH="${1:-}"

resolve_pyz() {
  if [ -n "$PYZ_PATH" ] && [ -f "$PYZ_PATH" ]; then
    printf '%s\n' "$PYZ_PATH"
    return 0
  fi
  script_dir="$(cd "$(dirname "$0")" && pwd)"
  default_pyz="$script_dir/../../dist/cli/aethercore-installer.pyz"
  if [ -f "$default_pyz" ]; then
    printf '%s\n' "$default_pyz"
    return 0
  fi
  return 1
}

pyz="$(resolve_pyz)" || {
  echo "PYZ not found. Pass path or build first." 1>&2
  exit 1
}

install_root="${XDG_DATA_HOME:-$HOME/.local/share}/aethercore-installer"
bin_dir="$HOME/.local/bin"

mkdir -p "$install_root" "$bin_dir"
cp "$pyz" "$install_root/aethercore-installer.pyz"

cat > "$bin_dir/aethercore-installer" <<'EOF'
#!/usr/bin/env sh
exec python3 "$HOME/.local/share/aethercore-installer/aethercore-installer.pyz" "$@"
EOF

chmod +x "$bin_dir/aethercore-installer"

echo "Installed to $install_root"
echo "Ensure \$HOME/.local/bin is in PATH, then run: aethercore-installer"
