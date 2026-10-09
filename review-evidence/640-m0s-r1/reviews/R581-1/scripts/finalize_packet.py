#!/usr/bin/env python3
"""Finalize this review's report and explicit publication inventory."""
import hashlib
import json
from pathlib import Path
import sys

p = Path(sys.argv[1]).resolve()
s = json.loads((p / "receipts/public-state-final.json").read_text())
assert s["review_audit"] == {"conversation_count": 2, "reviews_count": 0,
                            "inline_review_comments_count": 0,
                            "conversation_ids": [6087087303, 6087161464]}
assert (p / "receipts/integrity-before.json").read_bytes() == (p / "receipts/integrity-after.json").read_bytes()
envelope = json.loads((p / "receipts/resource-envelope.json").read_text())
text = (p / "receipts/independent-verdict.md").read_text()
text = text.replace(
    "Independent verdict and ledger frozen before reading prior public findings. Audit follows in the final report.",
    "Prior public findings: none. After freezing the independent verdict and ledger, the conversation, review and inline-review endpoints were read. The only two comments are the internal and external review starts (6087087303 and 6087161464); there are zero reviews and zero inline review comments. Nothing remains to resolve or retain. `receipts/prior-findings-audit.json` binds this audit to the pre-audit verdict.")
hosted = """Hosted snapshot at 2026-10-09 19:00:17 UTC: all inspected runs name this exact head. `docs-check-no-git`, `wire-accountability`, `bdd-conformance`, `verilator-lint`, one simulation shard and all four portability shards completed successfully with executed steps. `docs-check`, `elaborate`, firmware checks, fast elaboration and four simulation shards were still running. The `rtl-fast`, `verilator-suites` and `yosys-portability` aggregate verdicts were not yet emitted in the snapshot. The physical gPTP job was skipped with zero executed steps. Neither a skipped context nor an unfinished aggregate is execution proof. No required job in this snapshot has a failure conclusion, but the required hosted acceptance is still pending. [Fast workflow](https://github.com/kebag-logic/milan-fpga/actions/runs/37974767370), [full workflow](https://github.com/kebag-logic/milan-fpga/actions/runs/37974767359), [documentation](https://github.com/kebag-logic/milan-fpga/actions/runs/37974767534), and [elaboration](https://github.com/kebag-logic/milan-fpga/actions/runs/37974767558) are preserved in `receipts/public-state-final.json` and the raw final hosted receipts. Hosted and local-workflow acceptance remain with the manager."""
text = text.replace("Hosted checks remain in progress in the inspected exact-head snapshot. Final snapshot follows in REPORT.md; no hosted acceptance is asserted.", hosted)
text = text.replace(
    "The unit memory ceiling is 12 GiB; the current sampled peak is below 2 GiB, with no out-of-memory event.",
    f"The unit memory ceiling is 12 GiB; the recorded peak was {int(envelope['memory.peak']):,} bytes, with zero limit-hit or out-of-memory events (`receipts/resource-envelope.json`).")
for old, new in (
    ("recipe:259; resource gate:278/731; plan:634", "syn/ooc/pp_baseline.py:259; syn/ooc/pp_resource_gate.py:278; docs/design/MARK_II_AREA_PLAN.md:634"),
    ("placement:18/34/88; SoC:2549; datapath:8003; pinned processor top:1918", "syn/ooc/pp_placement.py:18; sw/litex/milan_soc.py:2549; hdl/milan/milan_datapath.sv:8003; protocol-processor/hdl/top/protocol_processor_top.sv:1918"),
    ("placement:51/63; recipe:154; gate:297/323; resource.log; independent-probes.log", "syn/ooc/pp_placement.py:63; syn/ooc/pp_baseline.py:154; syn/ooc/pp_resource_gate.py:297; receipts/resource.log; receipts/independent-probes.log"),
    ("placement selftest:55/73/156; both mutation drivers; OOC suite; checks.json; independent probe script", "syn/ooc/pp_placement_selftest.py:55; syn/ooc/pp_baseline_mutants.py:13; syn/ooc/pp_resource_gate_mutants.py:283; receipts/checks.json; scripts/independent_probes.py"),
    ("recipe document:183; plan:634; area budget:358; PR body; public author packet; documentation receipts", "docs/testing/PP_SHADOW_BASELINE_RECIPE.md:183; docs/design/MARK_II_AREA_PLAN.md:634; docs/design/AREA_BUDGET.md:358; PR body; receipts/public-author/HANDOFF.md"),
):
    text = text.replace(old, new)
assert text.startswith("[R581] POSITIVE - exact head bc89f84e6757f8fcddf21958e99f40f17bc0ee1e\n")
assert text.endswith("R581-1 FINISHED\n")
assert not any(word in text for word in ("SKELETON", "OOC_RESULT", "PRIOR_AUDIT", "HOSTED_SNAPSHOT", "RESOURCE_ENVELOPE"))
(p / "REPORT.md").write_text(text)

# Initial API snapshots stay unpublished; final raw snapshots and execution receipts are listed.
files = set((p / "scripts").glob("*.py"))
files.update((p / "receipts").glob("*.log"))
files.update((p / "receipts").glob("*.rc"))
files.update((p / "receipts").glob("final-hosted-*.json"))
files.update((p / "receipts/public-author").glob("*"))
for name in ("checks.json", "independent-verdict.md", "integrity-before.json", "integrity-after.json",
             "public-evidence-manifest.json", "public-state-final.json", "prior-findings-audit.json",
             "resource-envelope.json", "scoped-executable.txt", "source.diff"):
    files.add(p / "receipts" / name)
files.add(p / "REPORT.md")
lines = []
for path in sorted(files):
    assert path.is_file() and "scratch" not in path.relative_to(p).parts
    lines.append(hashlib.sha256(path.read_bytes()).hexdigest() + "  " + path.relative_to(p).as_posix())
(p / "MANIFEST.sha256").write_text("\n".join(lines) + "\n")
print(f"Final report and {len(lines)} publication entries written.")
print("Exact tracked bytes, modes, index and required gitlinks remain unchanged.")
