#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Planted controls for the register reference freshness gate (#797).

Each control copies the generator's inputs and outputs into a temporary tree,
plants one defect and runs the same `--check` entry the docs workflow calls on
that tree. A fresh copy must pass; every planted defect must fail with the
expected exit status and message. The controls are the gate's own evidence:
a renamed RTL field, a changed reset value, a new address, a hand edit, a
missing or extra diagram, an edited SoC extract and descriptions the RTL
cannot back.
"""

from __future__ import annotations

import contextlib
import io
import json
import re
import shutil
import tempfile
from collections.abc import Callable
from pathlib import Path

from register_page import DESCRIPTIONS, DIAGRAM_DIR, PAGE, SOC
from register_rtl import CSR_INCLUDE_DIR, DATAPATH, ETH_PKG, ROOT, RTL, SHAPE_INCLUDE_DIR

LEDGER = "docs/reference/milan_feature_status.json"
Entry = Callable[..., int]


def copy_inputs(dst: Path) -> None:
    """The files the generator reads and writes, copied under `dst`."""
    shape = json.loads((ROOT / SOC).read_text(encoding="utf-8"))["shape"]
    files = [RTL, DATAPATH, ETH_PKG, DESCRIPTIONS, SOC, LEDGER, PAGE, "docs/diagrams/README.md"]
    for include_dir in (CSR_INCLUDE_DIR, SHAPE_INCLUDE_DIR.format(shape=shape)):
        files += [p.relative_to(ROOT).as_posix() for p in (ROOT / include_dir / "gen").glob("*.svh")]
    files += [p.relative_to(ROOT).as_posix() for p in (ROOT / DIAGRAM_DIR).rglob("*") if p.is_file()]
    for rel in files:
        (dst / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / rel, dst / rel)


def edit(root: Path, rel: str, change: Callable[[str], str]) -> None:
    """Apply one text change to a copied file, refusing a change that does nothing."""
    path = root / rel
    before = path.read_text(encoding="utf-8")
    after = change(before)
    if after == before:
        raise AssertionError(f"planted change to {rel} changed nothing")
    path.write_text(after, encoding="utf-8")


def undescribed_port(root: Path) -> str:
    """An output port that names a stored field the descriptions do not key."""
    desc = json.loads((root / DESCRIPTIONS).read_text(encoding="utf-8"))
    described = {f for r in desc["registers"].values() for f in r.get("fields", {})}
    text = (root / RTL).read_text(encoding="utf-8")
    for port in ("o_tcam_wr_action", "o_mcsrv_ps_invert", "o_tone_att", "o_maap_seed_offset"):
        if port in text and port[2:].upper() not in described:
            return port
    raise AssertionError("every candidate port has a description; pick another")


def plant_field(desc: dict) -> dict:
    """The descriptions with one field key the RTL does not have."""
    desc["registers"]["ETH_GUARD"]["fields"]["PLANTED_FIELD"] = "no such field"
    return desc


def controls(entry: Entry) -> list[tuple[str, Callable[[Path], None], int, str]]:
    """(name, plant, expected exit status, text the output must carry)."""
    rtl_rename = lambda r: edit(r, RTL, lambda t: re.sub(  # noqa: E731
        r"\b" + undescribed_port(r) + r"\b", undescribed_port(r) + "_renamed", t))
    return [
        ("fresh copy", lambda r: None, 0, "fresh"),
        ("RTL field rename (output port of an undescribed field)", rtl_rename, 1, f"STALE {PAGE}"),
        ("RTL field rename of a described field",
         lambda r: edit(r, RTL, lambda t: re.sub(r"\bo_eth_guard\b", "o_eth_lock", t)), 2,
         "describes field ETH_GUARD.ETH_GUARD"),
        ("reset value change in csr_default",
         lambda r: edit(r, RTL, lambda t: re.sub(r"(A_MAC_IFG\[10:0\]:\s*csr_default = )32'h0C;",
                                                 r"\g<1>32'h0D;", t)), 1, f"STALE {PAGE}"),
        ("reset value change in the reset block",
         lambda r: edit(r, RTL, lambda t: t.replace("eth_guard <= 1'b1;", "eth_guard <= 1'b0;", 1)), 1,
         f"STALE {PAGE}"),
        ("unlock key change in the ETH_GUARD write decode",
         lambda r: edit(r, RTL, lambda t: t.replace("(s_axi_wdata != 32'h554E_4C4B)",
                                                    "(s_axi_wdata != 32'h554E_4C4C)")), 1,
         f"STALE {PAGE}"),
        ("new RTL address inside a module",
         lambda r: edit(r, RTL, lambda t: t.replace(
             "A_GPTP_LAT   = 'h7F0;",
             "A_GPTP_LAT   = 'h7F0;\n  localparam [ADDR_WIDTH-1:0] A_PLANTED = 'h7F4;", 1)),
         1, f"STALE {PAGE}"),
        ("new RTL address outside every module",
         lambda r: edit(r, RTL, lambda t: t.replace(
             "A_GPTP_LAT   = 'h7F0;",
             "A_GPTP_LAT   = 'h7F0;\n  localparam [ADDR_WIDTH-1:0] A_PLANTED = 'hA00;", 1)),
         2, "has no module"),
        ("hand edit of the page",
         lambda r: edit(r, PAGE, lambda t: t.replace("[reset = 0x00000001]", "[reset = 0x00000000]", 1)), 1,
         f"STALE {PAGE}"),
        ("deleted register diagram",
         lambda r: next((r / DIAGRAM_DIR).rglob("*.svg")).unlink(), 1, "STALE docs/diagrams/regmap/"),
        ("extra stale diagram",
         lambda r: (r / DIAGRAM_DIR / "planted.svg").write_text("<svg/>\n", encoding="utf-8"), 1,
         "planted.svg (not generated)"),
        ("edited WaveDrom source",
         lambda r: edit(r, f"{DIAGRAM_DIR}/guard.json", lambda t: t.replace('"R/W-1h"', '"R/W-0"')), 1,
         f"STALE {DIAGRAM_DIR}/guard.json"),
        ("edited SoC extract",
         lambda r: edit(r, SOC, lambda t: t.replace('"origin": 4026537984', '"origin": 4026540032', 1)), 1,
         f"STALE {PAGE}"),
        ("description of a register the RTL lacks",
         lambda r: edit(r, DESCRIPTIONS, lambda t: t.replace('"registers": {', '"registers": {"PLANTED": {},', 1)),
         2, "describes register PLANTED"),
        ("description of a field the RTL lacks",
         lambda r: edit(r, DESCRIPTIONS, lambda t: json.dumps(plant_field(json.loads(t)), indent=2) + "\n"), 2,
         "describes field ETH_GUARD.PLANTED_FIELD"),
        ("description breaking the prose rules",
         lambda r: edit(r, DESCRIPTIONS, lambda t: t.replace(
             '"The Ethernet guard kill switch."',
             '"The Ethernet guard kill switch, which is described here in far more words than allowed."', 1)),
         2, "breaks the documentation rules"),
    ]


def run(entry: Entry, root: Path) -> tuple[int, str]:
    """The workflow's `--check` on `root`: exit status and output."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = entry(["--check"], root=root)
    return rc, buf.getvalue()


def selftest(entry: Entry) -> int:
    """Run every control; 0 when each verdict is the expected one."""
    failures = 0
    names = controls(entry)
    for name, plant, want_rc, want_text in names:
        with tempfile.TemporaryDirectory(prefix="regref-selftest-") as tmp:
            root = Path(tmp)
            copy_inputs(root)
            try:
                plant(root)
            except (AssertionError, StopIteration) as exc:
                rc, out = -1, f"the plant itself failed: {exc}"
            else:
                rc, out = run(entry, root)
        ok = rc == want_rc and want_text in out
        failures += not ok
        print(f"  {'ok  ' if ok else 'FAIL'} {name}: rc {rc} (want {want_rc})"
              + ("" if ok else f"\n       output: {' '.join(out.split())[:300]}"))
    print(f"register reference selftest: {'OK' if not failures else 'FAIL'} "
          f"({len(names) - failures}/{len(names)} controls)")
    return 1 if failures else 0
