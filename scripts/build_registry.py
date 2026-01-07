#!/usr/bin/env python3
import json
import os
import sys
import zipfile
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List

import yaml  # PyYAML


REPO_USER = os.environ.get("AETHERCORE_REPO_USER", "SEU_USER")
REPO_NAME = os.environ.get("AETHERCORE_REPO_NAME", "aethercore-patches")
BRANCH = os.environ.get("AETHERCORE_REPO_BRANCH", "main")


ROOT = Path(__file__).resolve().parents[1]
PATCHES_DIR = ROOT / "patches"
DIST_DIR = ROOT / "dist"
GENERATED_DIR = ROOT / "generated"


@dataclass
class RemotePatch:
    name: str
    version: str
    description: str
    download_url: str


def log(msg: str) -> None:
    print(f"[build_registry] {msg}")


def fail(msg: str) -> None:
    log(f"FATAL: {msg}")
    sys.exit(1)


def load_manifest(path: Path) -> dict:
    try:
        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if not isinstance(data, dict):
            raise ValueError("manifest.yaml não é um objeto YAML válido")
        return data
    except Exception as e:
        fail(f"Erro lendo manifest {path}: {e}")


def read_description(patch_dir: Path, manifest: dict) -> str:
    # 1) Se tiver campo description no manifest, usa.
    desc = manifest.get("description")
    if isinstance(desc, str) and desc.strip():
        return desc.strip()

    # 2) Tenta pegar primeira linha não vazia do README.md
    readme = patch_dir / "README.md"
    if readme.exists():
        try:
            with readme.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        return line
        except Exception as e:
            log(f"Aviso: não foi possível ler descrição do {readme}: {e}")

    # 3) Fallback
    return f"Patch {manifest.get('name', 'desconhecido')}"


def build_zip_for_patch(patch_dir: Path, name: str, version: str) -> Path:
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    zip_name = f"{name}-{version}.zip"
    zip_path = DIST_DIR / zip_name

    log(f"Empacotando {patch_dir} -> {zip_path}")

    # Remove zip antigo se existir (para evitar lixo)
    if zip_path.exists():
        zip_path.unlink()

    # Cria zip com estrutura relativa à pasta patches/
    # Ex.: patches/notes_patch/...
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(patch_dir):
            root_path = Path(root)
            for file in files:
                file_path = root_path / file
                rel_path = file_path.relative_to(ROOT)
                zf.write(file_path, rel_path.as_posix())

    return zip_path


def build_remote_patch(patch_dir: Path) -> RemotePatch:
    manifest_path = patch_dir / "manifest.yaml"
    if not manifest_path.exists():
        fail(f"manifest.yaml não encontrado em {patch_dir}")

    manifest = load_manifest(manifest_path)

    name = manifest.get("name")
    version = manifest.get("version")

    if not isinstance(name, str) or not name.strip():
        fail(f"Campo 'name' inválido no manifest {manifest_path}")
    if not isinstance(version, str) or not version.strip():
        fail(f"Campo 'version' inválido no manifest {manifest_path}")

    name = name.strip()
    version = version.strip()

    description = read_description(patch_dir, manifest)

    # Gera zip
    zip_path = build_zip_for_patch(patch_dir, name, version)

    # Monta URL para raw.githubusercontent
    download_url = (
        f"https://raw.githubusercontent.com/"
        f"{REPO_USER}/{REPO_NAME}/{BRANCH}/"
        f"{zip_path.relative_to(ROOT).as_posix()}"
    )

    return RemotePatch(
        name=name,
        version=version,
        description=description,
        download_url=download_url,
    )


def discover_patches() -> List[RemotePatch]:
    if not PATCHES_DIR.exists():
        fail(f"Pasta de patches não encontrada: {PATCHES_DIR}")

    patches: List[RemotePatch] = []

    for item in PATCHES_DIR.iterdir():
        if not item.is_dir():
            continue
        # Ignora diretórios ocultos ou vazios
        if item.name.startswith("."):
            continue

        log(f"Processando patch: {item.name}")
        try:
            rp = build_remote_patch(item)
            patches.append(rp)
        except SystemExit:
            # fail() já logou e deu exit; apenas propaga
            raise
        except Exception as e:
            fail(f"Erro processando patch {item}: {e}")

    if not patches:
        log("Aviso: nenhum patch encontrado em patches/")

    return patches


def write_patches_json(patches: List[RemotePatch]) -> None:
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    out_path = GENERATED_DIR / "patches.json"

    data = [asdict(p) for p in patches]

    tmp_path = out_path.with_suffix(".json.tmp")

    log(f"Gravando {out_path} ({len(patches)} patches)")

    try:
        with tmp_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        tmp_path.replace(out_path)
    except Exception as e:
        fail(f"Erro escrevendo {out_path}: {e}")


def main() -> None:
    log(f"ROOT = {ROOT}")
    patches = discover_patches()
    write_patches_json(patches)
    log("Concluído com sucesso.")


if __name__ == "__main__":
    main()
