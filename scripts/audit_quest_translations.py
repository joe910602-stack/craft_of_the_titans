from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from collections import Counter
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
CACHE_PATH = SCRIPT_DIR / "quest_zh_tw_cache.json"
PROJECT_ROOT = SCRIPT_DIR.parent
ORIGINAL_ROOT = PROJECT_ROOT / "original"
TRANSLATION_ROOT = PROJECT_ROOT / "translation"
BOOK_PAIRS = (
    (
        ORIGINAL_ROOT / "betterquesting" / "DefaultQuests.json",
        TRANSLATION_ROOT / "betterquesting" / "DefaultQuests.json",
    ),
    (
        ORIGINAL_ROOT / "betterquesting" / "resources" / "craftofthetitans" / "DefaultQuests.json",
        TRANSLATION_ROOT / "betterquesting" / "resources" / "craftofthetitans" / "DefaultQuests.json",
    ),
)
FORMAT_CODE = re.compile(r"§[0-9A-FK-ORa-fk-or]")
URL = re.compile(
    r"(?:https?://|www\.)[^\s，。；）]+|"
    r"(?:[A-Za-z0-9-]+\.)+(?:com|net|org|io|wiki)(?:/[^\s，。；）]*)?",
    re.IGNORECASE,
)
ASCII_WORD = re.compile(r"[A-Za-z][A-Za-z0-9'’+./_-]*")
CJK = re.compile(r"[\u3400-\u9fff]")
BILINGUAL_GLOSS = re.compile(
    r"[A-Za-z][A-Za-z0-9'’+./_-]*(?: +[A-Za-z0-9][A-Za-z0-9'’+./_-]*)*"
    r"[（(][^）)\n]*[\u3400-\u9fff][^）)\n]*[）)]"
)
NON_GLOSS_IDENTIFIERS = {"IC2", "EU", "RF", "GP", "LP", "XP", "GUI", "JEI", "NEI"}


def normalized_words(text: str) -> set[str]:
    text = URL.sub("", text)
    return {word.casefold() for word in ASCII_WORD.findall(text)}


def visible_fields(value, path="$"):
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if key in {"name", "desc"} and isinstance(child, str):
                yield child_path, child
            yield from visible_fields(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from visible_fields(child, f"{path}[{index}]")



def audit_books(cache: dict[str, str]) -> None:
    mismatch_count = 0
    uncached_english_count = 0
    for source_path, target_path in BOOK_PAIRS:
        source = json.loads(source_path.read_text(encoding="utf-8"))
        target = json.loads(target_path.read_text(encoding="utf-8"))
        file_mismatches = 0
        file_uncached = 0
        for collection, id_field in (("questDatabase", "questID"), ("questLines", "lineID")):
            source_entries = {entry[id_field]: entry for entry in source.get(collection, [])}
            target_entries = {entry[id_field]: entry for entry in target.get(collection, [])}
            if set(source_entries) != set(target_entries):
                raise RuntimeError(f"Entry IDs differ: {source_path} -> {target_path} ({collection})")
        source_fields = dict(visible_fields(source))
        target_fields = dict(visible_fields(target))
        if source_fields.keys() != target_fields.keys():
            raise RuntimeError(f"Visible field paths differ: {source_path} -> {target_path}")
        for path, source_value in source_fields.items():
            target_value = target_fields[path]
            if source_value in cache and target_value != cache[source_value]:
                file_mismatches += 1
                print(
                    f"MISMATCH {target_path} {path}: {source_value!r} -> "
                    f"expected {cache[source_value]!r}, got {target_value!r}"
                )
            elif (
                source_value not in cache
                and ASCII_WORD.search(source_value)
                and not CJK.search(target_value)
                and not source_value.startswith("ability.abilities.")
            ):
                visible = FORMAT_CODE.sub("", target_value).strip()
                if visible not in {
                    "FUS RO DAH!",
                    "O-oooooooooo AAAAE-A-A-I-A-U-JO-oooooooooooo AAE-O-A-A-U-U-A-E-eee-ee-eee AAAAE-A-E-I-E-A-JO-ooo-oo-oo-oo EEEEO-A-AAA-AAAA",
                    "O-oooooooooo AAAAE-A-A-I-A-U- JO-oooooooooooo AAE-O-A-A-U-U-A- E-eee-ee-eee AAAAE-A-E-I-E-A- JO-ooo-oo-oo-oo EEEEO-A-AAA-AAAA",
                }:
                    file_uncached += 1
                    print(
                        f"UNCACHED {source_path} {path}: "
                        f"{source_value!r} -> {target_value!r}"
                    )
        mismatch_count += file_mismatches
        uncached_english_count += file_uncached
        print(f"BOOK {target_path}: mismatches={file_mismatches}, uncached_english={file_uncached}")
    print(f"book_cache_mismatches={mismatch_count}")
    print(f"book_uncached_english={uncached_english_count}")

def main() -> None:
    cache: dict[str, str] = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    if "--books" in sys.argv:
        audit_books(cache)
        return

    pure_english: list[tuple[str, str]] = []
    format_mismatches: list[tuple[str, str]] = []
    newline_mismatches: list[tuple[str, str]] = []
    missing_urls: list[tuple[str, str]] = []
    bilingual: list[tuple[str, str]] = []
    added_english: list[tuple[str, str, list[str]]] = []
    targets: defaultdict[str, list[str]] = defaultdict(list)

    for source, target in cache.items():
        targets[target].append(source)
        visible = FORMAT_CODE.sub("", URL.sub("", target)).strip()
        if visible and not CJK.search(visible) and ASCII_WORD.search(visible):
            pure_english.append((source, target))
        if FORMAT_CODE.findall(source) != FORMAT_CODE.findall(target):
            format_mismatches.append((source, target))
        if source.count("\n") != target.count("\n"):
            newline_mismatches.append((source, target))
        source_urls = URL.findall(source)
        if any(url not in target for url in source_urls):
            missing_urls.append((source, target))
        glosses = []
        for match in BILINGUAL_GLOSS.finditer(target):
            head = re.split(r"[（(]", match.group(0), maxsplit=1)[0]
            if match.start() > 0 and target[match.start() - 1] == "§":
                continue
            if head in NON_GLOSS_IDENTIFIERS or re.fullmatch(r"[A-Za-z]+\d+", head):
                continue
            glosses.append(match.group(0))
        if glosses:
            bilingual.append((source, target))
        new_words = sorted(normalized_words(target) - normalized_words(source))
        if new_words:
            added_english.append((source, target, new_words))

    duplicate_targets = [
        (target, sources)
        for target, sources in targets.items()
        if len(sources) > 1 and len(target) >= 4
    ]

    if "--format" in sys.argv:
        print(f"format_mismatches={len(format_mismatches)}")
        for source, target in format_mismatches:
            print(f"SOURCE: {source!r}")
            print(f"TARGET: {target!r}")
            print(f"CODES: {FORMAT_CODE.findall(source)!r} -> {FORMAT_CODE.findall(target)!r}")
            print(f"NEWLINES: {source.count(chr(10))} -> {target.count(chr(10))}")
        return

    if "--newline" in sys.argv:
        print(f"newline_mismatches={len(newline_mismatches)}")
        for source, target in newline_mismatches:
            print(f"SOURCE: {source!r}")
            print(f"TARGET: {target!r}")
            print(f"NEWLINES: {source.count(chr(10))} -> {target.count(chr(10))}")
        return

    if "--added-words" in sys.argv:
        counts = Counter(word for _source, _target, words in added_english for word in words)
        for word, count in counts.most_common():
            print(f"{count:3} {word}")
        return

    if "--english-segments" in sys.argv:
        segments = Counter()
        for target in cache.values():
            cleaned = URL.sub("", FORMAT_CODE.sub("", target))
            for segment in re.findall(r"[A-Za-z][A-Za-z0-9'’+./_-]*(?: +[A-Za-z0-9][A-Za-z0-9'’+./_-]*)*", cleaned):
                segments[segment.strip()] += 1
        for segment, count in segments.most_common():
            print(f"{count:3} {segment}")
        return

    if "--duplicates" in sys.argv:
        print(f"duplicate_long_targets={len(duplicate_targets)}")
        for index, (target, sources) in enumerate(duplicate_targets, start=1):
            print(f"DUPLICATE {index}: {target!r}")
            for source in sources:
                print(f"  SOURCE: {source!r}")
        return

    print(f"entries={len(cache)}")
    print(f"pure_english={len(pure_english)}")
    for source, target in pure_english:
        print(f"  PURE {source!r} -> {target!r}")
    print(f"format_mismatches={len(format_mismatches)}")
    for source, target in format_mismatches:
        print(f"  FORMAT {FORMAT_CODE.findall(source)} -> {FORMAT_CODE.findall(target)} :: {source[:100]!r}")
    print(f"newline_mismatches={len(newline_mismatches)}")
    for source, target in newline_mismatches:
        print(f"  NEWLINE {source.count(chr(10))} -> {target.count(chr(10))} :: {source[:100]!r}")
    print(f"missing_urls={len(missing_urls)}")
    for source, target in missing_urls:
        print(f"  URL {URL.findall(source)!r} :: {target[:140]!r}")
    print(f"bilingual_glosses={len(bilingual)}")
    for source, target in bilingual:
        print(f"  GLOSS {source[:100]!r} -> {target[:180]!r}")
    print(f"added_english={len(added_english)}")
    for source, target, words in added_english:
        print(f"  ADDED {words!r} :: {source[:100]!r} -> {target[:180]!r}")
    print(f"duplicate_long_targets={len(duplicate_targets)}")
    for target, sources in duplicate_targets:
        print(f"  DUP {len(sources)} sources -> {target[:180]!r}")
        for source in sources:
            print(f"    {source[:160]!r}")


if __name__ == "__main__":
    main()
