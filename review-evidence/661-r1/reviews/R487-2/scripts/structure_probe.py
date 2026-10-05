#!/usr/bin/env python3
"""Check clean re-merge, source delta, port contract and public-body hygiene."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

root, packet = (Path(arg).resolve() for arg in sys.argv[1:])
sys.path.insert(0, str(root / "scripts"))
from sv_ports import declarations


def git(*args):
    return subprocess.check_output(["git", "-C", str(root), *args])


head = git("rev-parse", "HEAD").decode().strip()
parents = git("rev-parse", "HEAD^1", "HEAD^2").decode().splitlines()
tree = git("rev-parse", "HEAD^{tree}").decode().strip()
remerge = git("merge-tree", "--write-tree", *parents).decode().splitlines()[0]
assert remerge == tree
assert parents[1] == "fa450d301805881ad713b67521477bf042ddadfd"
rtl = git("diff", "--name-only", "42f65447", "HEAD", "--", "hdl").decode().splitlines()
assert rtl == ["hdl/milan/KL_nvm_backend.sv"]
assert not git("diff", "42f65447", "HEAD", "--", "protocol-processor", "gptp-processor",
               "third_party/verilog-axis", "sw/litex/milan_soc.py", "sw/firmware",
               "syn/ooc/pp_resource_gate.py", "syn/ooc/pp_resource_baseline.json")
pin = git("rev-parse", "HEAD:protocol-processor").decode().strip()
old_pin = git("rev-parse", "506d91db:protocol-processor").decode().strip()
ports = {}
for revision in (old_pin, pin):
    text = subprocess.check_output(["git", "-C", str(root / "protocol-processor"),
                                    "show", revision + ":hdl/top/protocol_processor_top.sv"], text=True)
    ports[revision] = sorted(name for module, name, doc, multi, kind in declarations(text)
                             if module == "protocol_processor_top" and kind == "port")
assert ports[old_pin] == ports[pin] and len(ports[pin]) == 212
pr = json.loads((packet / "receipts/pr-body.json").read_text())
body = pr["body"]
assert pr["head"]["sha"] == head
assert "its 212 ports" in body
assert "exception is retired" in body and "139 checks / 0 failures" in body
account_pattern = r"\b" + "".join(map(chr, (97, 108, 101, 120))) + r"\b"
for pattern in (r"/(?:home|data|root|tmp|Users)/", r"\bsudo\b", account_pattern):
    assert not re.search(pattern, body), pattern
old_baseline = json.loads(git("show", "506d91db:syn/ooc/pp_resource_baseline.json"))
new_baseline = json.loads((root / "syn/ooc/pp_resource_baseline.json").read_text())
print(json.dumps({"head": head, "tree": tree, "parents": parents, "clean_remerge_tree": remerge,
                  "merge_tree_equal": True, "round2_rtl_delta": rtl,
                  "round2_pins_soc_firmware_resource_gate_and_baseline_unchanged": True,
                  "processor_ports": {p: len(names) for p, names in ports.items()},
                  "processor_port_names_unchanged": True,
                  "pr_body_sha256": hashlib.sha256(body.encode()).hexdigest(),
                  "pr_body_hygiene_and_count": "PASS",
                  "pr_body_updated_at": pr["updated_at"]}, indent=2))
