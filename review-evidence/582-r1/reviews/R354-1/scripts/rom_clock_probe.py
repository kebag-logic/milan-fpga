#!/usr/bin/env python3
"""R354-1: replicate every gate-1b assertion that reads the gPTP ROM at head.

Run from sw/builder. Exits non-zero only if one of those assertions fails, so
under a mutant a zero exit means gate 1b's ROM checks would not detect it.
Prints the shipping-AX ROM SHA-256 so a survivor can be shown to change the
product image. Mirrors test_builder.py test_baremetal_profile_contract at
3baff441: the 1024-word length pin and the station-MAC and priority1 variants
(the fabric-clock variant was removed by this PR).
"""
import copy
import hashlib
import tempfile
from pathlib import Path

import os
import sys

import yaml
sys.path.insert(0, os.getcwd())
import endstation_builder as eb

CFG = Path("../../configs/endstation_ax7101_1x1_tdm8.yaml")


def rom(raw: dict, td: Path, tag: str) -> bytes:
    path = td / f"{tag}.yaml"
    path.write_text(yaml.safe_dump(raw))
    result = eb.build(path, td / tag, write_fragment=False)
    return Path(result["paths"]["gptp_ucode"]).read_bytes()


with tempfile.TemporaryDirectory() as tmp:
    td = Path(tmp)
    raw = yaml.safe_load(CFG.read_text())
    base = rom(raw, td, "base")
    assert len(base.splitlines()) == 1024, "ROM length pin"
    mac = copy.deepcopy(raw)
    mac["platform"]["mac_address"] = "02:00:00:00:00:03"
    assert rom(mac, td, "mac") != base, "station MAC did not reach ROM"
    p1 = copy.deepcopy(raw)
    p1["gptp"]["priority1"] = 247
    assert rom(p1, td, "p1") != base, "priority1 did not reach ROM"
    print("gate-1b ROM assertions: pass")
    print("shipping AX gptp_ucode sha256", hashlib.sha256(base).hexdigest())
