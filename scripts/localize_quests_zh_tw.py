from __future__ import annotations

import argparse
import concurrent.futures
import ctypes
import json
import os
import pathlib
import re
import threading
import time
from typing import Any

import requests

from quest_terminology_zh_tw import polish_quest_terminology, polish_quest_translation


SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
TRANSLATE_URL = "https://clients5.google.com/translate_a/t"
FIELD_NAMES = ("name", "desc")
PROPER_NAMES = (
    "Craft of the Titans",
    "Craft Of The Titans",
    "Better Questing",
    "Cooking for Blockheads",
    "Cooking For Blockheads",
    "Immersive Engineering",
    "Actually Additions",
    "Mystical Agriculture",
    "IndustrialCraft 2",
    "Industrial Craft 2",
    "Industrial Craft",
    "Extra Utilities 2",
    "Extra Utilities",
    "Draconic Evolution",
    "Extreme Reactors",
    "Refined Storage",
    "Storage Drawers",
    "Blood Arsenal",
    "Blood Magic",
    "Ars Magica 2",
    "Ars Magicka 2",
    "Ars Magica",
    "Ars Magicka",
    "AbyssalCraft",
    "EnderIO",
    "MineCraft",
    "Minecraft",
    "Botania",
    "The Beneath",
)
TOKEN_PATTERN = re.compile(
    r"(?:https?://|www\.)\S+|"
    r"(?:[A-Za-z0-9-]+\.)+(?:com|net|org|io|wiki)(?:/\S*)?|"
    r"§[0-9A-FK-ORa-fk-or]|"
    r"\n"
)
PLACEHOLDER_PATTERN = re.compile(r"\s*ZXQPH(\d{5})QXZ\s*", re.IGNORECASE)
CJK_PATTERN = re.compile(r"[\u3400-\u9fff]")
_thread_local = threading.local()


def get_session() -> requests.Session:
    session = getattr(_thread_local, "session", None)
    if session is None:
        session = requests.Session()
        session.headers["User-Agent"] = "Mozilla/5.0 quest-localizer/1.0"
        _thread_local.session = session
    return session


def protect_text(text: str) -> tuple[str, list[str]]:
    protected: list[str] = []

    def placeholder(value: str) -> str:
        index = len(protected)
        protected.append(value)
        return f"ZXQPH{index:05d}QXZ"

    # Longest first prevents a short proper name from matching inside a long one.
    result = text
    for proper_name in sorted(PROPER_NAMES, key=len, reverse=True):
        result = re.sub(
            re.escape(proper_name),
            lambda match: placeholder(match.group(0)),
            result,
            flags=re.IGNORECASE,
        )
    result = TOKEN_PATTERN.sub(lambda match: placeholder(match.group(0)), result)
    return result, protected


def restore_text(text: str, protected: list[str]) -> str:
    found = [int(match.group(1)) for match in PLACEHOLDER_PATTERN.finditer(text)]
    if sorted(found) != list(range(len(protected))):
        raise ValueError(
            f"Placeholder mismatch: expected {len(protected)}, got {found!r} in {text!r}"
        )

    def restore(match: re.Match[str]) -> str:
        return protected[int(match.group(1))]

    return PLACEHOLDER_PATTERN.sub(restore, text)


def polish_translation(text: str) -> str:
    text = to_traditional_chinese(text)
    replacements = (
        ("右鍵單擊", "按右鍵"),
        ("右鍵點擊", "按右鍵"),
        ("左鍵單擊", "按左鍵"),
        ("左鍵點擊", "按左鍵"),
        ("鼠標", "滑鼠"),
        ("視頻", "影片"),
        ("信息", "資訊"),
        ("文件夾", "資料夾"),
        ("服務器", "伺服器"),
        ("互聯網", "網路"),
        ("加載", "載入"),
        ("保存", "儲存"),
        ("生物群落", "生態域"),
        ("下界", "地獄"),
        ("末地", "終界"),
        ("主世界", "主世界"),
        ("鵝卵石", "鵝卵石"),
        ("熔巖", "熔岩"),
        ("工作臺", "工作台"),
    )
    for old, new in replacements:
        text = text.replace(old, new)
    return polish_quest_terminology(text)


def to_traditional_chinese(text: str) -> str:
    """Normalize occasional Simplified Chinese output using the Windows NLS API."""
    if os.name != "nt" or not text:
        return text
    lcmap_string_ex = ctypes.windll.kernel32.LCMapStringEx
    traditional_chinese = 0x04000000
    required = lcmap_string_ex(
        "zh-TW", traditional_chinese, text, len(text), None, 0, None, None, 0
    )
    if not required:
        return text
    buffer = ctypes.create_unicode_buffer(required)
    written = lcmap_string_ex(
        "zh-TW",
        traditional_chinese,
        text,
        len(text),
        buffer,
        required,
        None,
        None,
        0,
    )
    return buffer[:written] if written else text


def translate_segment(source: str) -> str:
    if not source or not re.search(r"[A-Za-z]", source):
        return source
    prepared, protected = protect_text(source)
    response = get_session().get(
        TRANSLATE_URL,
        params={
            "client": "dict-chrome-ex",
            "sl": "en",
            "tl": "zh-TW",
            "dt": "t",
            "q": prepared,
        },
        timeout=45,
    )
    response.raise_for_status()
    payload = response.json()
    if isinstance(payload, list) and payload and isinstance(payload[0], str):
        translated = payload[0]
    else:
        translated = "".join(part[0] for part in payload[0] if part and part[0])
    if not translated:
        raise ValueError(f"Empty translation for {source!r}")
    return polish_translation(restore_text(translated, protected))


def preserve_outer_whitespace(source: str, target: str) -> str:
    """Keep leading and trailing whitespace exactly as it appears in the source."""
    leading = re.match(r"^\s*", source).group(0)
    trailing = re.search(r"\s*$", source).group(0)
    return leading + target.strip() + trailing


def translate_once(source: str) -> str:
    return preserve_outer_whitespace(source, translate_segment(source))


class RateLimitError(RuntimeError):
    """Raised when the translation service asks the caller to stop sending work."""


def translate_with_retry(source: str, stop_on_rate_limit: bool = False) -> str:
    last_error: Exception | None = None
    for attempt in range(6):
        try:
            translated = translate_once(source)
            time.sleep(1.5)
            return translated
        except Exception as error:  # Network and malformed-response retries share a backoff.
            last_error = error
            status = getattr(getattr(error, "response", None), "status_code", None)
            if status == 429 and stop_on_rate_limit:
                raise RateLimitError("Translation service rate limited (HTTP 429)") from error
            time.sleep(30 if status == 429 else min(2**attempt, 20))
    raise RuntimeError(
        f"Unable to translate a {len(source)}-character string; last error: {last_error!r}"
    ) from last_error


def visible_text_fields(data: Any):
    """Yield every user-visible name/description field, including nested tasks."""
    if isinstance(data, dict):
        for field, value in data.items():
            if field in FIELD_NAMES and isinstance(value, str):
                yield data, field
            yield from visible_text_fields(value)
    elif isinstance(data, list):
        for value in data:
            yield from visible_text_fields(value)


def is_untranslated_visible_text(value: Any) -> bool:
    return (
        isinstance(value, str)
        and bool(re.search(r"[A-Za-z]", value))
        and not CJK_PATTERN.search(value)
    )


def atomic_write_json(path: pathlib.Path, data: Any) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    os.replace(temporary, path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", type=pathlib.Path)
    parser.add_argument(
        "--cache",
        type=pathlib.Path,
        default=SCRIPT_DIR / "quest_zh_tw_cache.json",
    )
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--sample", type=int, default=0)
    parser.add_argument(
        "--apply-cache",
        action="store_true",
        help="Apply completed cached translations without making network requests.",
    )
    parser.add_argument(
        "--stop-on-rate-limit",
        action="store_true",
        help="Translate sequentially and stop immediately on the first HTTP 429 response.",
    )
    args = parser.parse_args()

    original_text = args.target.read_text(encoding="utf-8")
    data = json.loads(original_text)
    fields = list(visible_text_fields(data))
    sources = sorted(
        {
            container[field]
            for container, field in fields
            if is_untranslated_visible_text(container.get(field))
        },
        key=lambda value: (len(value), value),
    )
    cache: dict[str, str] = {}
    if args.cache.exists():
        cache = json.loads(args.cache.read_text(encoding="utf-8"))
        normalized_cache = {
            source: preserve_outer_whitespace(
                source, polish_quest_translation(source, polish_translation(target))
            )
            for source, target in cache.items()
        }
        if normalized_cache != cache:
            cache = normalized_cache
            atomic_write_json(args.cache, cache)
    # Exact translations reviewed by hand live in the terminology module. Seed
    # them into the cache so newly discovered quest-book variants stay offline.
    for source in sources:
        reviewed = preserve_outer_whitespace(
            source, polish_quest_translation(source, source)
        )
        if reviewed != source:
            cache[source] = reviewed
    atomic_write_json(args.cache, cache)
    uncached = [source for source in sources if source not in cache]
    pending = [] if args.apply_cache else list(uncached)
    if args.sample:
        pending = pending[: args.sample]

    print(
        f"Visible text fields: {len(fields)}; unique English strings: {len(sources)}; "
        f"cached: {len(sources) - len(uncached)}; pending: {len(pending)}; "
        f"uncached: {len(uncached)}",
        flush=True,
    )
    completed_since_save = 0
    errors: list[tuple[str, Exception]] = []
    rate_limited = False
    if args.stop_on_rate_limit:
        total = len(pending)
        for completed, source in enumerate(pending, start=1):
            try:
                cache[source] = translate_with_retry(source, stop_on_rate_limit=True)
            except RateLimitError as error:
                atomic_write_json(args.cache, cache)
                print(
                    f"RATE_LIMITED after {completed - 1}/{total}: {error}; cache saved",
                    flush=True,
                )
                rate_limited = True
                break
            except Exception as error:
                errors.append((source, error))
                print(f"Translation error {len(errors)}: {error}", flush=True)
                continue
            completed_since_save += 1
            if completed_since_save >= 20 or completed == total:
                atomic_write_json(args.cache, cache)
                completed_since_save = 0
            if completed == 1 or completed % 25 == 0 or completed == total:
                print(f"Translated {completed}/{total}", flush=True)
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
            future_to_source = {
                executor.submit(translate_with_retry, source): source for source in pending
            }
            total = len(future_to_source)
            for completed, future in enumerate(
                concurrent.futures.as_completed(future_to_source), start=1
            ):
                source = future_to_source[future]
                try:
                    cache[source] = future.result()
                except Exception as error:
                    errors.append((source, error))
                    print(f"Translation error {len(errors)}: {error}", flush=True)
                    continue
                completed_since_save += 1
                if completed_since_save >= 20 or completed == total:
                    atomic_write_json(args.cache, cache)
                    completed_since_save = 0
                if completed == 1 or completed % 25 == 0 or completed == total:
                    print(f"Translated {completed}/{total}", flush=True)

    if errors:
        atomic_write_json(args.cache, cache)
        raise RuntimeError(f"Translation failed for {len(errors)} strings")

    if args.sample:
        for source in pending:
            print("\nEN:", source)
            print("ZH:", cache[source])
        return

    missing = [source for source in sources if source not in cache]
    if missing and not (args.apply_cache or rate_limited):
        raise RuntimeError(f"Cache is incomplete: {len(missing)} strings missing")
    for container, field in fields:
        value = container.get(field)
        if value in cache:
            container[field] = cache[value]
        elif isinstance(value, str):
            container[field] = polish_translation(value)
    atomic_write_json(args.target, data)
    # A second parse catches truncated or incorrectly encoded output immediately.
    json.loads(args.target.read_text(encoding="utf-8"))
    print(
        f"Wrote localized quest book: {args.target}; untranslated unique strings: {len(missing)}",
        flush=True,
    )
    if rate_limited:
        raise SystemExit(75)


if __name__ == "__main__":
    main()
