"""Gate table: the verifier's docs.yml rows with each log's last line, then the lane steps.
Usage: python3 -I gate_table.py <scratch logs dir> <verify.md> > gate_table.md"""
import re, sys
from pathlib import Path
logs = Path(sys.argv[1]); rows = Path(sys.argv[2]).read_text().splitlines()
def last(tag):
    for name in (f"{tag}.log", f"{tag}.log.tail"):
        p = logs / name
        if p.exists():
            ls = [l for l in p.read_text(errors="replace").splitlines() if l.strip()]
            return (ls[-1] if ls else "").replace("|", "/")[:150]
    return ""
print("| Job | Step | Name | rc | Last line |\n|---|---|---|---:|---|")
for r in rows:
    m = re.match(r"\| (\S+) \| (\S+) \| (.*) \| (0|NOT RUN|MISSING|BAD.*) \| (.*) \|$", r)
    if not m: continue
    job, sid, name, rc, rest = m.groups()
    tail = last(f"{job}__{sid}") if rc == "0" else rest
    print(f"| {job} | {sid} | {name} | {rc} | {tail} |")
LANE = [("inventory_check", "`docs_inventory.py --check`"),
        ("doc_style", "`check_doc_style.py` (its 24 current documents)"),
        ("style_merge_new", "check_doc_style's `analyze()` on all 11 pages the merge touched, at the merge and both parents: findings neither parent has"),
        ("style_merge_new_control", "the same with a planted 12-word sentence; must report it (negated)"),
        ("style_blocks_vs_dev", "changed-block probe, the branch's 4 pages against dev ac0a01e3"),
        ("behave", "`cd tests && behave --no-capture -f plain` (behave + PyYAML)"),
        ("diffcheck_mergebase", "`git diff --check ac0a01e3 HEAD` (merge base)"),
        ("diffcheck_oldbase", "`git diff --check 0a75aa77 HEAD` (round 6 base)"),
        ("em_dash_mergebase", "`check_em_dash.py --base ac0a01e3`"),
        ("reader_check_baseline", "AREA_BUDGET.md's reader: `pp_resource_gate.py check-baseline`"),
        ("reader_service_bounds", "MAILBOX_SPLIT.md's reader: `ctrl_service_bounds.arm_service_bounds`"),
        ("census_coverage", "`census_coverage.py` at the merge, against dev's `sw/litex/milan_soc.py`"),
        ("census_coverage_control", "`! census_coverage.py` against the round 1 page 3f8ed303 (must fail)")]
print("\n| Lane step | Command | rc | Last line |\n|---|---|---:|---|")
for sid, cmd in LANE:
    rc = (logs / f"lane__{sid}.rc").read_text().strip()
    print(f"| {sid} | {cmd} | {rc} | {last('lane__' + sid)} |")
