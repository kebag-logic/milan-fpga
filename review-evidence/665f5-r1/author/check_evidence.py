"""Audit sizing artifacts and exercise two refusal controls, without running firmware."""
import argparse
import hashlib
import json
import os
import re
import struct
import subprocess
import sys
from pathlib import Path

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument("--root", type=Path, required=True)
ap.add_argument("--scratch", type=Path, required=True)
a = ap.parse_args()
root, scratch = a.root.resolve(), a.scratch.resolve()
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
import ctrl_image

cc = os.environ["MILAN_RV32_CC"]
tool = cc.removesuffix("gcc")
runtime = scratch / "runtime-freestanding"
required_store = {"nvm_store_boot", "nvm_store_service", "nvm_stage", "nvm_payload", "nvm_chunk"}
records = []
for shape in ("1x1_tdm8", "8x8"):
    for interfaces in (1, 2):
        for prefix in ("base-final", "store"):
            name = f"{prefix}-{shape}-if{interfaces}"
            work = scratch / name
            elf = work / "ctrl_app.elf"
            report = json.loads((work / "size.json").read_text())
            inputs = [str(p) for p in sorted(work.glob("*.o"))]
            inputs += [str(runtime / n) for n in ("libc.a", "libcompiler_rt.a")]
            findings, audit = ctrl_image.audit(tool, elf, inputs)
            linked_findings, linked_audit = ctrl_image.audit(tool, elf, [])
            assert not linked_findings, (name, linked_findings)
            symbols = ctrl_image.symbol_sizes(tool, elf)
            store_symbols = {n: symbols[n][1] for n in sorted(required_store & symbols.keys())}
            assert set(store_symbols) == (required_store if prefix == "store" else set())
            size_text = subprocess.check_output([tool + "size", "-A", str(elf)], text=True)
            sections = {n: (int(s), int(addr)) for n, s, addr in
                        re.findall(r"^(\.\S+)\s+(\d+)\s+(\d+)", size_text, re.M)}
            names = (".text", ".rodata", ".data", ".bss", ".stack")
            sizes = {n: sections.get(n, (0, 0))[0] for n in names}
            span = max(sections[n][0] + sections[n][1] for n in names if n in sections) - sections[".text"][1]
            assert sizes == {n: report["sections"].get(n, 0) for n in names}
            assert span == report["ram_span"]
            assert sum(sizes.values()) == report["ram_sections"]
            artifacts = []
            for artifact in report["artifacts"]:
                p = runtime / artifact["name"] if artifact["name"].endswith(".a") else work / artifact["name"]
                observed = {"name": artifact["name"], "size": p.stat().st_size,
                            "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
                assert observed == artifact
                artifacts.append(observed)
            records.append({"case": name, "sections": sizes, "span": span,
                            "four_sections": sum(sizes.values()) - sizes[".stack"],
                            "static_storage_within_bss": report["static_storage"],
                            "store_symbols": store_symbols, "linked_audit": linked_audit,
                            "all_input_findings": findings,
                            "artifacts": artifacts})

base = scratch / "base-final-8x8-if2/ctrl_app.elf"
store = scratch / "store-8x8-if2/ctrl_app.elf"
baseline_symbols = ctrl_image.symbol_sizes(tool, base)
assert required_store - baseline_symbols.keys() == required_store
corrupt = bytearray(store.read_bytes())
struct.pack_into("<I", corrupt, 36, 1)
assert any("e_flags" in item for item in ctrl_image.header_findings(corrupt))
largest = next(r for r in records if r["case"] == "store-8x8-if2")
assert largest["four_sections"] > 128 * 1024
result = {"head": "5603c353137e90c1fa95429f6d00ef7a2298d9ee",
          "compiler": ctrl_image.identity(cc), "cases": records,
          "controls": [
              {"plant": "Substitute the baseline ELF for a store-composed ELF",
               "result": "Rejected: all five required saved-state symbols are absent"},
              {"plant": "Set RVC in a copy of the ELF header e_flags",
               "result": "Rejected by the existing RV32I header check"}],
          "disposition": "STOP: largest two-interface four-section sum exceeds 131072 bytes"}
(scratch / "evidence.json").write_text(json.dumps(result, indent=2) + "\n")
print(f"PASS: {len(records)} retained-image audits; 2 planted controls rejected; sizing disposition STOP")
failed = [r for r in records if r["all_input_findings"]]
for record in failed:
    print(f"REFUSED all-input closure: {record['case']}: {record['all_input_findings']}")
raise SystemExit(1 if failed else 0)
