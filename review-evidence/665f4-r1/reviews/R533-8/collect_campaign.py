#!/usr/bin/env python3
"""Retain the six assigned plants' failed observables at both interface counts."""
import hashlib
import json
from pathlib import Path
import re

packet = Path(__file__).resolve().parent
checkout = Path.cwd()
receipts = packet / "receipts"
record = json.loads((receipts / "ctrl-campaign.json").read_text())
assert record["rc"] == 0
log = (receipts / "ctrl-campaign.log").read_text()
assert "test_ctrl_firmware: PASS" in log
assert "[ESCAPED]" not in log
assert len(re.findall(r"^\[ok\] mutant ", log, re.M)) == 469
expected = {
    "four-way-srp-irq-missing": "U6 exact four-channel receive and event interrupt mask",
    "four-way-srp-wake-missing": "U6 idle loop wakes for SRP alone",
    "four-way-acmp-enable-lost": "U6 four receive channels and no others",
    "four-way-unbound-irq-enabled": "U6 exact four-channel receive and event interrupt mask",
    "four-way-bound-drops-srp": "F6 four modules count each shared event record once",
    "four-way-bound-duplicates-events": "F6 four modules count each shared event record once",
}
published = []
for interfaces, folder, count in ((2, "srp-mutants", 108), (1, "srp-if1-mutants", 6)):
    root = packet / "scratch/ctrl-campaign" / folder
    assert len(list(root.glob("*.log"))) == count
    dest = receipts / f"four-way-if{interfaces}"
    dest.mkdir(exist_ok=True)
    for name, needle in expected.items():
        raw = (root / (name + ".log")).read_bytes()
        data = raw.decode()
        lines = [line.strip() for line in data.splitlines()
                 if "[FAIL] AcmpMailbox." in line and needle in line]
        assert lines, (interfaces, name, needle)
        assert "RESULT: FAIL" in data
        normalized = (data.replace(str(packet), "$PACKET")
                      .replace(str(checkout), "$CHECKOUT")
                      .replace(str(Path.home()), "$USER_HOME"))
        out = dest / (name + ".log")
        out.write_text(normalized)
        published.append({"interfaces": interfaces, "plant": name,
                          "failed_observable": lines,
                          "receipt": str(out.relative_to(packet)),
                          "raw_sha256": hashlib.sha256(raw).hexdigest(),
                          "published_sha256": hashlib.sha256(out.read_bytes()).hexdigest()})
print(json.dumps({"control_plants": 469, "srp_if2_plants": 108,
                  "srp_if1_additional_plants": 6, "four_way": published}, indent=2))
