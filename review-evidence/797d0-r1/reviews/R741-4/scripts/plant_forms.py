#!/usr/bin/env python3
"""Plant copy forms of real recorded statements on new pages in a disposable clone and grade the generator's rows."""
import re, subprocess, sys
from pathlib import Path
root = Path(sys.argv[1]); inv = [sys.executable, "-I", "scripts/docs_inventory.py"]
P = (  # label, finding, text, expected row
 ("underscore-whole", "D0-063", "_The processor answers four Stream Input fields itself._", True),
 ("underscore-double-part", "D0-065", "__Never add__ a second source for the processor's four fields.", True),
 ("underscore-around-code", "D0-064", "_`milan_datapath`_ answers every other word and every validity flag.", True),
 ("underscore-star-mixed", "D0-063", "**_The processor answers_** four Stream Input fields itself.", True),
 ("link-inline-title", "D0-063", 'The processor answers [four Stream Input](a.md#x "t") fields itself.', True),
 ("link-reference", "D0-065", "Never add [a second source][ref] for the processor's four fields.", True),
 ("link-wrapped", "D0-065", "Never add [a second\nsource](a.md) for the\nprocessor's four fields.", True),
 ("link-image", "D0-063", "The processor answers ![four Stream Input](a.png) fields itself.", True),
 ("end-comma", "D0-063", "The processor answers four Stream Input fields itself, and nothing else.", True),
 ("end-semicolon", "D0-063", "The processor answers four Stream Input fields itself; the rest pass.", True),
 ("end-colon", "D0-063", "The processor answers four Stream Input fields itself: see below.", True),
 ("end-none", "D0-063", "- The processor answers four Stream Input fields itself", True),
 ("quote-ends-comma", "D0-036", 'reachable with the standard quad read (`READ_1_1_4`, 0x6B). `mode="4x"` drives all four DQ.', True),
 ("also-D0-002", "D0-002", "Now, clock-source selection now reaches the media plane's wrapper.", True),
 ("also-D0-005", "D0-005", "Here `media_tick_p` is a compile-time constant.", True),
 ("also-D0-024", "D0-024", "It was deleted 2026-08-13 with this repository's own AECP/AEM engine.", True),
 ("also-D0-025", "D0-025", "Here the protocol processor's NVM face is answered by a blank-flash responder.", True),
 ("also-D0-035", "D0-035", "The AEM copy goes through the BIOS's `copy_image_from_flash_to_ram`.", True),
 ("also-D0-036a", "D0-036", "It is reachable with the standard quad read (`READ_1_1_4`, 0x6B).", True),
 ("also-D0-036b", "D0-036", '`mode="4x"` drives all four DQ.', True),
 ("also-D0-047", "D0-047", "What stays open is the write side.", True),
 # D0-040 records the same words; the row for the page may stand under either, and one row suffices.
 ("also-D0-058", ("D0-040", "D0-058"), "Nothing in this device persists a binding across a power cycle.", True),
 ("also-D0-059", "D0-059", "The clause is not met by this build.", True),
 ("also-D0-062", "D0-062", "The record below is the shipping option-on measurement.", True),
 ("no-inner-underscore", "D0-063", "The processor answers four Stream_Input fields itself.", False),
 ("no-longer-word", "D0-063", "The processor answers four Stream Input fields itselfish.", False),
 ("no-unrelated-link", "D0-063", "See [the processor](a.md) in the guide.", False),
 ("no-blank-line-split", "D0-065", "Never add a second source\n\nfor the processor's four fields.", False),
)
assert subprocess.run(inv + ["--check"], cwd=root).returncode == 0
names = []
for n, (label, ident, text, want) in enumerate(P):
    name = f"docs/guides/PROBE_{n:02d}.md"
    # Two wrapped links above the plant: a row's line must still be the plant's own.
    (root / name).write_text(f"# Probe {label}\n\nSee [a\nwrapped](x.md) link and [b\nc][d].\n\n{text}\n", encoding="utf-8")
    names.append(name)
subprocess.check_call(["git", "add", *names], cwd=root)
print("--check after planting rc=", subprocess.run(inv + ["--check"], cwd=root, capture_output=True).returncode, "(1 expected)")
subprocess.check_call(inv + ["--write"], cwd=root, stdout=subprocess.DEVNULL)
print("--check after --write rc=", subprocess.run(inv + ["--check"], cwd=root, capture_output=True).returncode, "(0 expected)")
page = (root / "docs/DOCUMENTATION_AUDIT.md").read_text(encoding="utf-8")
bad = 0
for n, (label, ident, text, want) in enumerate(P):
    name = f"docs/guides/PROBE_{n:02d}.md"
    rows = re.findall(rf"^\| (D0-\d+) \| \[{re.escape(name)}\]\([^)]*\) \| (\d+) \|", page, re.M)
    inv_row = re.search(rf"^\|[^\n]*{re.escape(name)}[^\n]*$", page, re.M).group(0)
    stale = "stale" in inv_row.lower()
    ids = ident if isinstance(ident, tuple) else (ident,)
    hit = any(r[0] in ids for r in rows)
    ok = hit == want and stale == want and (not want or all(r[1] == "7" for r in rows if r[0] in ids) )
    bad += not ok
    print(f"{'OK ' if ok else 'BAD'} {label:24} want_row={want!s:5} rows={rows} stale={stale}")
print("wrong:", bad, "of", len(P))
