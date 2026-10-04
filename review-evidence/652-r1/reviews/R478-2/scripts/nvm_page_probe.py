#!/usr/bin/env python3
"""Run check_nvm_record_space.py's real check (no --mutate) from the review
clone with one edit applied IN MEMORY to the design page's text through the
gate's own SEAM.ALLOCATION_PAGE_EDIT; the clone's files are never written.
Usage: nvm_page_probe.py <clone> <case>   (cases listed in CASES)
Prints the gate's findings and CHECK rc=<rc>; rc 1 means the edit was caught."""
import sys
from pathlib import Path

USER = "| `0x80` .. `0xFF` | user name | 128 | name ordinal | 39 | **107** |"
RECORDS = "| **records** | | | | **54** | **164** |"
HIGHEST = "| **highest id** | | | | `0xA6` | `0xEA` |"
RESERVED = "| `0x1A` .. `0x1F` | reserved | 6 | -- | -- | -- |"
CFG = "| `0x00` | configuration index | 1 | -- | 1 | 1 |"
CASES = {
    "control-unedited": (None, None),
    "user-row-short": (USER, USER.rsplit(" **107** |", 1)[0]),
    "user-row-long": (USER, USER + " **107** |"),
    "user-row-blank-8x8": (USER, USER.replace("**107**", "")),
    "user-row-middle-cell-lost": (USER, USER.replace(" name ordinal |", "")),
    "records-row-short": (RECORDS, RECORDS.rsplit(" **164** |", 1)[0]),
    "highest-row-short": (HIGHEST, HIGHEST.rsplit(" `0xEA` |", 1)[0]),
    "cfg-row-short": (CFG, CFG[:-4]),
    "records-row-deleted": (RECORDS + "\n", ""),
    "highest-row-deleted": (HIGHEST + "\n", ""),
    "reserved-row-deleted": (RESERVED + "\n", ""),
    "user-row-deleted": (USER + "\n", ""),
}
clone, case = Path(sys.argv[1]).resolve(), sys.argv[2]
old, new = CASES[case]
sys.path.insert(0, str(clone / "scripts"))
import check_nvm_record_space as gate  # noqa: E402
if old is not None:
    def edit(page, old=old, new=new):
        assert page.count(old) == 1, f"anchor occurs {page.count(old)} times"
        return page.replace(old, new)
    gate.SEAM.ALLOCATION_PAGE_EDIT = edit
sys.argv = [str(clone / "scripts/check_nvm_record_space.py"), "--quiet"]
rc = gate.main()
print(f"CHECK rc={rc}")
