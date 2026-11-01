"""Exercise the inline-markup neutraliser and scan the real tree for the ten recorded forms.

usage: python3 -I markup_and_forms.py <repo-root>
Part 1 puts every delimiter run at every position of each spelling; a delimiter that renders as
markup must still leave a finding. Part 2 is independent of the gate: it normalises each Current
page and looks for each unit-bearing constant in the ten recorded forms, with each form's wider
family (other spelled units, other entities, any HTML tag, any link).
"""
import importlib.util
import re
import sys
import types
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("check_docs", ROOT / "scripts/check_docs.py")
checker = importlib.util.module_from_spec(spec)
sys.path.insert(0, str(ROOT))
spec.loader.exec_module(checker)

fixture = types.SimpleNamespace(SYNC_RTO_MS_C=375, CEASE_MS_C=300_000, STEP_LINKUP_NS_C=20_000, RATE_PPM_C=200)
table = (f"{checker.CONSTANTS_HEADING}\n\n| Constant | Value | Meaning |\n|---|---:|---|\n"
         "| `SYNC_RTO_MS_C` | 375 | syncReceiptTimeout, ms |\n"
         "| `CEASE_MS_C` | 300,000 | Cease countdown, ms |\n"
         "| `STEP_LINKUP_NS_C` | 20,000 | Step threshold, ns |\n"
         "| `RATE_PPM_C` | 200 | Rate bound, ppm |\n")
SPELLINGS = ("375 ms", "375-ms", "375ms", "300,000 ms", "300 s", "5 minutes", "5-minute", "5min", "five minutes",
             "five-minute", "20,000 ns", "20 us", "200 ppm")
RUNS = ("*", "**", "***", "_", "__", "`", "``", "_**", "**_")


def caught(text):
    return bool(checker.copy_findings({"docs/GUIDE.md": text}, table, fixture))


def part_one():
    total = escaped = 0
    samples = []
    for spelling in SPELLINGS:
        # Wrap each substring at word edges, and each position inside the spelling.
        for start in range(len(spelling) + 1):
            for end in range(start, len(spelling) + 1):
                for run in RUNS:
                    closing = run[::-1]
                    text = f"A {spelling[:start]}{run}{spelling[start:end]}{closing}{spelling[end:]} watch."
                    total += 1
                    if not caught(text):
                        # An underscore between word characters delimits nothing in CommonMark.
                        between = re.search(r"(?<=\w)_+(?=\w)", text)
                        if between:
                            continue
                        escaped += 1
                        if len(samples) < 20:
                            samples.append(text)
    print(f"markup product: {total} documents, {escaped} escapes outside intraword underscores")
    for text in samples:
        print("  ", repr(text))


FORMS = {
    "decimal_seconds": r"(?<![\d.])0?\.(?:375|125|\d*[1-9]\d*)\s*s(?:ec(?:ond)?s?)?\b",
    "spelled_unit": r"\b{v}[\s-]*(?:milli|micro|nano)?seconds?\b|\b{v}[\s-]*parts per million\b",
    "link_on_value": r"\[{v}\]\([^)]*\)\s*(?:ms|ns|us|ppm|s|min)",
    "html_on_value": r"<[a-zA-Z][^>]*>\s*{v}\s*</[a-zA-Z]+>\s*(?:ms|ns|us|ppm|s|min)",
    "html_entity": r"\b{v}&[#a-zA-Z0-9]+;\s*(?:ms|ns|us|ppm|s|min)",
    "strikethrough": r"~+{v}~+\s*(?:ms|ns|us|ppm|s|min)",
}


def unit_values(constants_text):
    values = []
    for line in constants_text.splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 3 and re.fullmatch(r"[\d,]+", cells[1] or "x"):
            found = checker.UNIT_CELL_RE.search(cells[2])
            if found:
                values.append((cells[0], int(cells[1].replace(",", "")), found.group(1)))
    return values


def part_two():
    pages = checker.current_pages() if hasattr(checker, "current_pages") else None
    if pages is None:
        pages = [p for p in checker.markdown_files() if "docs/history" not in p.as_posix()] if hasattr(checker, "markdown_files") else [
            p for p in sorted(ROOT.rglob("*.md")) if "docs/history" not in p.as_posix()]
    constants = (ROOT / checker.CONSTANTS_PAGE).read_text(encoding="utf-8")
    home = "\n".join(checker.section_lines(constants, checker.CONSTANTS_HEADING))
    values = unit_values(home)
    print(f"{len(pages)} current pages; {len(values)} unit-bearing rows: " + ", ".join(f"{n} {v} {u}" for n, v, u in values))
    hits = 0
    for page in pages:
        text = Path(page).read_text(encoding="utf-8")
        relative = Path(page).resolve().relative_to(ROOT).as_posix()
        kept = checker.unfenced_lines(text)
        if relative == checker.CONSTANTS_PAGE:
            inside, filtered = False, []
            for number, line in kept:
                if line.startswith("## "):
                    inside = line.strip() == checker.CONSTANTS_HEADING
                if not inside:
                    filtered.append((number, line))
            kept = filtered
        body = "\n".join(line for _, line in kept)
        for form, pattern in FORMS.items():
            spellings = {f"{v}" for _, v, _ in values} | {f"{v:,}" for _, v, _ in values}
            spellings |= {f"{v // 1000}" for _, v, u in values if v % 1000 == 0}
            for text_value in sorted(spellings):
                if form == "decimal_seconds":
                    regex = rf"(?<![\d.])0?\.(?:{int(text_value):03d})\s*s(?:ec(?:ond)?s?)?\b" if text_value.isdigit() and int(text_value) < 1000 else None
                else:
                    regex = pattern.replace("{v}", re.escape(text_value))
                if regex is None:
                    continue
                for found in re.finditer(regex, body):
                    hits += 1
                    print(f"  {relative}: {form}: {found.group(0)!r}")
        # Wrapped line: value at the end of one line, unit starting the next.
        for (_, first), (_, second) in zip(kept, kept[1:]):
            for _, value, unit in values:
                for text_value in {f"{value}", f"{value:,}"}:
                    if re.search(rf"(?<![\d.,]){re.escape(text_value)}[`*_]*\s*$", first) and re.match(rf"\s*[`*_]*{unit}\b", second):
                        hits += 1
                        print(f"  {relative}: wrapped: {first.strip()[-30:]!r} / {second.strip()[:30]!r}")
        # Indented heading anywhere on a page, and any raw HTML block opening.
        for number, line in kept:
            if re.match(r" {1,3}#{1,6} ", line):
                hits += 1
                print(f"  {relative}:{number}: indented heading {line!r}")
            if re.match(r" {0,3}<(?!!--)[a-zA-Z/?!]", line):
                print(f"  {relative}:{number}: raw HTML start {line[:60]!r} (information)")
    print(f"form hits: {hits}")


part_one()
part_two()
