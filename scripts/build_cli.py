#!/usr/bin/env python3
import argparse
import zipapp
from pathlib import Path


def build_cli(output_path, source_dir):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    zipapp.create_archive(
        source_dir,
        output_path,
        main="aethercore_installer_cli:main",
        interpreter="/usr/bin/env python3",
    )


def main():
    parser = argparse.ArgumentParser(description="Build the AetherCore installer CLI")
    parser.add_argument(
        "--output",
        default="dist/cli/aethercore-installer.pyz",
        help="Output .pyz file path",
    )
    parser.add_argument(
        "--source",
        default="cli",
        help="Source directory containing the CLI module",
    )
    args = parser.parse_args()

    output_path = Path(args.output).resolve()
    source_dir = Path(args.source).resolve()
    if not source_dir.exists():
        raise SystemExit(f"Source dir not found: {source_dir}")

    build_cli(output_path, source_dir)
    print(f"Built: {output_path}")


if __name__ == "__main__":
    main()
