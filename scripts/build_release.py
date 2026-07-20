from __future__ import annotations

import json
import hashlib
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOCALIZATION_ROOT = PROJECT_ROOT / "translation"
OUTPUT_PATH = PROJECT_ROOT / "dist" / "craft-of-the-titans-1.30-zh-tw.zip"
CHECKSUM_PATH = OUTPUT_PATH.with_suffix(OUTPUT_PATH.suffix + ".sha256")

PACKAGE_DIRECTORIES = (
    (LOCALIZATION_ROOT / "betterquesting", Path("config/betterquesting")),
    (LOCALIZATION_ROOT / "enchiridion", Path("config/enchiridion")),
    (
        LOCALIZATION_ROOT / "BloodMagic" / "enchiridion",
        Path("config/BloodMagic/enchiridion"),
    ),
)

PACKAGE_DOCUMENTS = (
    (PROJECT_ROOT / "LICENSE.md", Path("LICENSE.md")),
    (PROJECT_ROOT / "THIRD_PARTY_NOTICES.md", Path("THIRD_PARTY_NOTICES.md")),
)


def package_files() -> list[tuple[Path, Path]]:
    files: list[tuple[Path, Path]] = []
    for source_directory, archive_directory in PACKAGE_DIRECTORIES:
        if not source_directory.is_dir():
            raise FileNotFoundError(f"Missing localization directory: {source_directory}")
        for source_path in sorted(source_directory.rglob("*.json")):
            archive_path = archive_directory / source_path.relative_to(source_directory)
            files.append((source_path, archive_path))
    return files


def main() -> None:
    json_files = package_files()
    if not json_files:
        raise RuntimeError("No localization JSON files were found")

    for source_path, _archive_path in json_files:
        json.loads(source_path.read_text(encoding="utf-8"))

    for source_path, _archive_path in PACKAGE_DOCUMENTS:
        if not source_path.is_file():
            raise FileNotFoundError(f"Missing release document: {source_path}")
        source_path.read_text(encoding="utf-8")

    files = [*json_files, *PACKAGE_DOCUMENTS]

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(OUTPUT_PATH, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for source_path, archive_path in files:
            archive.write(source_path, archive_path.as_posix())

    with ZipFile(OUTPUT_PATH) as archive:
        archived_files = archive.namelist()
        if len(archived_files) != len(files):
            raise RuntimeError("Release archive file count does not match the source files")
        expected_files = {archive_path.as_posix() for _, archive_path in files}
        if set(archived_files) != expected_files:
            raise RuntimeError("Release archive paths do not match the source files")
        for _source_path, archive_path in json_files:
            json.loads(archive.read(archive_path.as_posix()).decode("utf-8"))

    digest = hashlib.sha256(OUTPUT_PATH.read_bytes()).hexdigest()
    CHECKSUM_PATH.write_text(
        f"{digest}  {OUTPUT_PATH.name}\n", encoding="ascii"
    )
    size_mib = OUTPUT_PATH.stat().st_size / (1024 * 1024)
    print(
        f"Created {OUTPUT_PATH} with {len(json_files)} JSON files and "
        f"{len(PACKAGE_DOCUMENTS)} notices ({size_mib:.2f} MiB)"
    )
    print(f"SHA-256 {digest}")


if __name__ == "__main__":
    main()
