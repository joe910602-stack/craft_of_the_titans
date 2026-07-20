from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
ORIGINAL_ROOT = PROJECT_ROOT / "original"
TRANSLATION_ROOT = PROJECT_ROOT / "translation"


def run(command: list[str]) -> None:
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    subprocess.run(command, cwd=PROJECT_ROOT, env=environment, check=True)


def compare_structure(source: Any, target: Any, path: str = "$") -> None:
    if type(source) is not type(target):
        raise RuntimeError(f"Type differs at {path}")
    if isinstance(source, dict):
        if source.keys() != target.keys():
            raise RuntimeError(f"Object keys differ at {path}")
        for key in source:
            compare_structure(source[key], target[key], f"{path}.{key}")
    elif isinstance(source, list):
        if len(source) != len(target):
            raise RuntimeError(f"List length differs at {path}")
        for index, (source_item, target_item) in enumerate(zip(source, target)):
            compare_structure(source_item, target_item, f"{path}[{index}]")
    elif not isinstance(source, str) and source != target:
        raise RuntimeError(f"Non-text value differs at {path}")


def enchiridion_pairs() -> list[tuple[Path, Path]]:
    pairs: list[tuple[Path, Path]] = []
    for relative_root in (Path("enchiridion"), Path("BloodMagic/enchiridion")):
        source_root = ORIGINAL_ROOT / relative_root
        for relative_directory in (Path("books"), Path("templates")):
            for source_path in sorted((source_root / relative_directory).glob("*.json")):
                target_path = TRANSLATION_ROOT / source_path.relative_to(ORIGINAL_ROOT)
                if not target_path.is_file():
                    raise FileNotFoundError(f"Missing translation: {target_path}")
                pairs.append((source_path, target_path))
    return pairs


def main() -> None:
    python = sys.executable
    audit = SCRIPT_DIR / "audit_quest_translations.py"
    for option in ("--books", "--format", "--newline"):
        run([python, str(audit), option])

    translation_files = sorted(TRANSLATION_ROOT.rglob("*.json"))
    if not translation_files:
        raise RuntimeError("No translated JSON files were found")
    for path in translation_files:
        json.loads(path.read_text(encoding="utf-8"))

    pairs = enchiridion_pairs()
    for source_path, target_path in pairs:
        raw_target = target_path.read_bytes()
        if any(byte >= 128 for byte in raw_target):
            raise RuntimeError(
                f"Enchiridion translation is not ASCII Unicode-escaped: {target_path}"
            )
        source = json.loads(source_path.read_text(encoding="utf-8"))
        target = json.loads(raw_target.decode("ascii"))
        compare_structure(source, target)

    run([python, str(SCRIPT_DIR / "build_release.py")])
    print(
        f"Validation passed: {len(translation_files)} translated JSON files; "
        f"{len(pairs)} Enchiridion source/translation pairs"
    )


if __name__ == "__main__":
    main()
