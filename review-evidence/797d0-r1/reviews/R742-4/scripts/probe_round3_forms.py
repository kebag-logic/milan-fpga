#!/usr/bin/env python3
"""Replant the copy forms the round 3 report graded as misses, each on a page that holds no finding row.

Usage: probe_round3_forms.py <clone at the head>. Each arm appends one line to the page, requires --check to
refuse, regenerates, requires --check to pass, then reads the arm's row and the page's status. The clone is
restored after every arm.
"""
import re
import subprocess
import sys
from pathlib import Path

clone = Path(sys.argv[1]).resolve()
PAGE = "docs/guides/BOARD_DEPLOYMENT.md"
ARMS = (
    ("D0-001", "underscore emphasis", "_ADP, ACMP, AECP, MAAP and SRP default to bare-metal firmware._"),
    ("D0-001", "one word as an inline link", "ADP, ACMP, AECP, MAAP and SRP default to bare-metal [firmware](x.md)."),
    ("D0-001", "one word as a reference link", "ADP, ACMP, AECP, MAAP and SRP default to bare-metal [firmware][fw]."),
    ("D0-025", "sentence ended normally", "The protocol processor's NVM face is answered by a blank-flash responder."),
    ("D0-035", "sentence ended normally", "The AEM copy goes through the BIOS's `copy_image_from_flash_to_ram`."),
    ("D0-059", "sentence ended normally", 'Milan v1.2 5.3.8.2 is **not met by this build**.'),
    ("D0-002", "sentence ended normally", "Clock-source selection now reaches the media plane's wrapper."),
    # D0-040 records the same words earlier in the data file, so the copy row is its; D0-058 is held by that row.
    ("D0-040", "sentence with its marker", "**Nothing in this device persists a binding across a power cycle.**"),
    ("D0-047", "sentence ended normally", "What stays open is the write side."),
    ("D0-005", "sentence ended normally", "`media_tick_p` is a compile-time constant."),
    ("D0-062", "sentence ended normally", "The record below is the shipping option-on measurement."),
    ("D0-024", "sentence ended normally", "It was deleted 2026-08-13 with this repository's own AECP/AEM engine."),
    ("D0-036", "first sentence alone", "It is reachable with the standard quad read (`READ_1_1_4`, 0x6B)."),
    ("D0-036", "second sentence alone", '`mode="4x"` drives all four DQ.'),
)


def run(*args):
    return subprocess.run(args, cwd=clone, text=True, capture_output=True)


def restore():
    run("git", "reset", "-q", "--hard", "HEAD")
    run("git", "clean", "-qfdx")


GEN = ("python3", "-I", "scripts/docs_inventory.py")
restore()
print("baseline --check rc", run(*GEN, "--check").returncode)
good = 0
for ident, form, line in ARMS:
    restore()
    with (clone / PAGE).open("a", encoding="utf-8") as page:
        page.write("\n" + line + "\n")
    refused = run(*GEN, "--check").returncode
    wrote = run(*GEN, "--write").returncode
    passed = run(*GEN, "--check").returncode
    audit = (clone / "docs/DOCUMENTATION_AUDIT.md").read_text(encoding="utf-8")
    rows = re.findall(rf"^\| {ident} \| \[{re.escape(PAGE)}\]\([^)]*\) \| (\S+) ", audit, re.M)
    stale = bool(re.search(rf"^\| \[{re.escape(PAGE)}\]\([^)]*\) .*\| stale \|", audit, re.M))
    wanted = sum(1 for _ in (clone / PAGE).open(encoding="utf-8"))
    ok = refused == 1 and wrote == 0 and passed == 0 and rows == [str(wanted)] and stale
    good += ok
    print(f"{'PASS' if ok else 'FAIL'}\t{ident}\t{form}\tcheck_before={refused}\twrite={wrote}\tcheck_after={passed}"
          f"\trows={rows}\texpected_line={wanted}\tstale={stale}")
restore()
print(f"round 3 forms: {good}/{len(ARMS)} as expected; restored --check rc", run(*GEN, "--check").returncode)
sys.exit(0 if good == len(ARMS) else 1)
