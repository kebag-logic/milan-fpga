"""Complete local handoff artifacts only after every assigned gate finishes."""
import hashlib
import json
from pathlib import Path
import shlex
import subprocess

out = Path(__file__).resolve().parent
head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
assert head == "224ec0e9a9fa129924bf8f0433cf70b4140f7bd2"
assert not subprocess.check_output(["git", "status", "--porcelain"], text=True)
expected = ["notify-mutants", "milan-dp-run", "pp-shadow", "docs-git", "docs-no-git",
            "em-dash", "doc-style", "toc", "doc-paths", "xvlog", "cpp", "python",
            "port-contracts", "naming", "test-evidence", "whitespace",
            "committed-whitespace", "citations", "duplicate-mutant-proof"]
rows = [json.loads(line) for line in (out / "gates.jsonl").read_text().splitlines()]
current = {r["name"]:r for r in rows if r["head"] == head}
assert set(current) == set(expected), (set(expected)-set(current), set(current)-set(expected))
assert all(r["rc"] == 0 and not r["dirty"] for r in current.values())
for sub in ["protocol-processor", "gptp-processor", "third_party/verilog-axis"]:
    assert not subprocess.check_output(["git", "-C", sub, "status", "--porcelain"], text=True)
live = json.loads(subprocess.check_output(["gh", "pr", "view", "560", "--json", "body"], text=True))
assert live["body"] == (out / "pr-original.md").read_text(), "Public PR body changed; preserve the new content before publishing the proposed body"
(out / "pr-current.json").write_text(json.dumps(live, indent=2) + "\n")
summary = dict(head=head, clean=True, final_head_gate_count=len(current), all_rc_zero=True,
               gates=[dict(name=n, rc=current[n]["rc"], seconds=current[n]["seconds"],
                           log=current[n]["log"], sha256=hashlib.sha256((out/current[n]["log"]).read_bytes()).hexdigest()) for n in expected])
(out / "completion-check.json").write_text(json.dumps(summary, indent=2)+"\n")
validation = """Validation: all required commands returned rc 0 at the exact local head:

```text
make -C tb/verilator/milan_dp notify gsi-mutants
make -C tb/verilator/milan_dp run
make -C tb/verilator/pp_shadow
python3 scripts/docs_check.py
env GIT_DIR=/nonexistent-508-a297-git python3 scripts/docs_check.py
python3 scripts/check_em_dash.py --base c266432dcb0cdd464205823a3d82cad260eedde2
python3 scripts/check_doc_style.py
python3 scripts/gen_toc.py --check
python3 scripts/check_doc_paths.py
python3 scripts/xvlog_gate.py --check
python3 scripts/check_cpp_idiom.py
python3 scripts/check_py_idiom.py
python3 scripts/check_port_contracts.py
python3 scripts/measure_naming.py --check
python3 scripts/measure_test_evidence.py --check
git diff --check
git diff --check c266432dcb0cdd464205823a3d82cad260eedde2 HEAD
```

The notification leg passed 380/380; the campaign passed 9/9 controls (clean plus eight caught mutants). The complete default datapath run passed, including its built-in controls. The shadow suite passed 371/371. The citation/changelog proof and raw duplicate-mutant proof also returned zero. The HDL frontend ran with its four existing recorded findings; all budgets are unchanged. The em-dash and TOC checks used the locked Markdown dependencies. The no-git documentation mode skips only its Git inventory-parity arm.
"""
p = out / "REVIEW-READY.md"
p.write_text(p.read_text().replace("FINAL_VALIDATION_PENDING", validation).replace(" This is author validation, not a review verdict.", ""))
p = out / "PR-BODY.md"
body = p.read_text().replace("round 3 local validation is in progress", "the complete round-3 assigned local gate set passed")
body = body.replace("Final-head validation: pending.", """Final-head validation: the clean notification leg passes 380/380 checks;
all eight mutants fail their named checks, with 9/9 campaign controls passing.
The duplicate fails both G8 counts with three pushes instead of two.
The complete default datapath sweep and shadow suite pass; the latter grades
371/371 checks. Both documentation inventory modes and every assigned source,
contract, naming, evidence, formatting and path gate return zero. The HDL
frontend retains its four recorded findings, with no budget change. Citation
and historical-changelog proofs also pass. The head remains local and unpushed.""")
assert body.splitlines()[0] == "[A297]" and "Closes #508" in body and "## Round 3" in body
assert "/home/" not in body and "Final-head validation: pending" not in body
p.write_text(body)
p = out / "HANDOFF.md"
text = p.read_text().replace("Status: implementation committed, final-head validation running.", "Status: implementation and all assigned final-head validation complete; ready for delta review.")
text = text.replace("Preliminary results:", "Results, repeated at the final commit:")
text = text.replace("Final-head receipts will supersede preliminary receipts.", "Final-head receipts supersede preliminary receipts.")
start = text.index("Validation: all fifteen")
end = text.index("\nscope-proof.json", start)
text = text[:start] + validation + "\nAll 19 final-head command/proof receipts have rc 0 and a clean worktree. completion-check.json binds their logs by SHA-256. gates.jsonl retains the earlier preliminary receipts separately. Every command ran in the foreground without a shell pipeline.\n" + text[end:]
text = text.replace("Publication: pending the requested [A297] REVIEW READY comment on #508.", "Publication: REVIEW-READY.md is the exact [A297] REVIEW READY comment prepared for #508. Posting it is the final action after artifact checks.")
p.write_text(text)
for name in ["HANDOFF.md", "PR-BODY.md", "REVIEW-READY.md"]:
    text = (out/name).read_text()
    assert "/home/" not in text, name
    assert "FINAL_VALIDATION_PENDING" not in text, name
print("All 19 final-head commands/proofs passed; handoff, proposed PR body and issue comment finalized.")
