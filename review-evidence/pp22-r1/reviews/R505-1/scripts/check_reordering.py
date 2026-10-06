#!/usr/bin/env python3
"""Prove exact byte moves, unchanged tracked scope, and declaration precedence."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

repo = Path(sys.argv[1]).resolve()
base = "e6a759deeb70b2d7de1b3336e9f080bc85d4f0a8"
head = "2139f3dc10161b456dfbd51d2f73a63f9164e041"
def git(*args):
    return subprocess.check_output(["git", "-C", str(repo), *args])

origin = "hdl/packet_engine/KL_pp_originator.sv"
rx = "hdl/packet_engine/KL_pp_rx_validator.sv"
assert git("diff", "--name-only", base, head).decode().splitlines() == [origin, rx]
assert git("rev-parse", f"{head}^" ).decode().strip() == base
assert git("rev-parse", f"{head}^{{tree}}").decode().strip() == "b7d98916ed833c26c7f7d713964b16c10c36daa3"
moves = {
    origin: (b"  logic                cancel_hit_w;\n  logic [IFL_AW_C-1:0] cancel_ix_w;\n\n", b"  logic [IFL_N_C-1:0]  cancel_work_w;\n"),
    rx: (b"  logic       fifo_ne_w, fifo_full_w, vq_ne_w, vq_full_w;\n", b"\n  assign acc_w  = rx_valid_i;\n"),
}
results = []
for path in [origin, rx]:
    old = git("show", f"{base}:{path}")
    new = git("show", f"{head}:{path}")
    block, anchor = moves[path]
    assert old.count(block) == new.count(block) == old.count(anchor) == 1
    expected = old.replace(block, b"")
    if path == rx:
        second = b"  logic       push_w, vd_push_w, vd_val_w, rd_fire_w, retire_w;\n"
        assert old.count(second) == new.count(second) == 1
        expected = expected.replace(second, b"")
        block += second
    expected = expected.replace(anchor, block + anchor)
    assert expected == new, path
    old_mode = git("ls-tree", base, "--", path).split()[0]
    new_mode = git("ls-tree", head, "--", path).split()[0]
    assert old_mode == new_mode == b"100644"
    declarations = []
    for line in block.decode().splitlines():
        if not line.strip():
            continue
        names = re.findall(r"\b[a-z][a-z0-9_]*_w\b", line)
        for name in names:
            hits = [(i + 1, row.strip()) for i, row in enumerate(new.decode().splitlines()) if re.search(r"\b" + name + r"\b", row)]
            assert hits[0][1].startswith("logic "), (path, name, hits[0])
            declarations.append({"name": name, "declaration_line": hits[0][0], "first_use_line": hits[1][0]})
    results.append({"path": path, "pure_byte_move": True, "mode": new_mode.decode(), "base_sha256": hashlib.sha256(old).hexdigest(), "head_sha256": hashlib.sha256(new).hexdigest(), "declarations": declarations})
print(json.dumps({"base": base, "head": head, "single_commit": True, "only_two_files_changed": True, "results": results}, indent=2))
