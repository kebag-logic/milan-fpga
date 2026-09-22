#!/usr/bin/env python3
"""R222-3: attribution map of every docs-workflow step at the candidate.

For each step of the three docs jobs at 72e16c61, each command line is matched
against (M) the manager's candidate2 41-command bank (commands exactly as
recorded in its spec) and (R) the commands this round ran on the combined tree
(receipts 08, 10a-c, 12-15). Lines that are tool installs, artifact uploads or
shell plumbing are labelled as such. Nothing here is executed.
Usage: 16_docs_workflow_attribution.py <candidate-clone> <evidence-bare-repo>
"""
import json
import subprocess
import sys
from pathlib import Path

import yaml

root = Path(sys.argv[1])
ev = sys.argv[2]
spec = json.loads(subprocess.run(
    ["git", "-C", ev, "show", "2102036d773acd885376a5b2f2d199b52040e7df:"
     "review-evidence/478-r1/candidate2/manager-builder-spec.json"],
    check=True, capture_output=True, text=True).stdout)
M = {" ".join(c) for c in spec["commands"]}
R = {
    "python3 scripts/docs_check.py", "python3 scripts/check_doc_style.py",
    "python3 scripts/check_doc_style.py --selftest", "python3 scripts/check_gptp_docs.py",
    "python3 scripts/check_gptp_docs.py --selftest", "python3 docs/DOC_MAP.gen.py --check",
    "python3 docs/DOC_MAP.gen.py --selftest", "python3 docs/diagrams/timesync_chain.gen.py --check",
    "python3 docs/diagrams/timesync_chain.gen.py --selftest", "python3 scripts/check_solution_docs.py",
    "python3 scripts/check_solution_docs.py --selftest",
    "python3 docs/diagrams/submodule_boundaries.gen.py --check",
    "python3 docs/diagrams/submodule_boundaries.gen.py --selftest",
    "python3 scripts/check_submodule_docs.py", "python3 scripts/check_submodule_docs.py --selftest",
    "python3 scripts/check_diagram_pngs.py", "python3 scripts/check_diagram_pngs.py --selftest",
    "python3 scripts/check_feature_status.py --self-test", "python3 scripts/check_feature_status.py",
    "python3 docs/traceability/gen_module_matrix.py --check", "python3 scripts/check_doc_paths.py",
    "python3 scripts/gen_toc.py --selftest", "python3 scripts/gen_toc.py --verify-anchors",
    "python3 scripts/gen_toc.py --check", "python3 scripts/check_archive.py",
    "python3 scripts/check_em_dash.py --selftest", "python3 scripts/check_py_idiom.py",
    "python3 scripts/check_hygiene.py --check", "python3 scripts/check_todo_ownership.py",
    "python3 scripts/ci_events.py --check", "python3 scripts/ci_events.py --selftest",
    "python3 avdecc/gen_aem_store.py --self-test",
    "python3 scripts/check_wire_accountability.py --self-test",
    "python3 scripts/check_baremetal_only.py --check", "python3 scripts/check_baremetal_only.py --selftest",
    "python3 scripts/pp_srcs.py --check --selftest", "python3 scripts/check_rtl_source_lists.py",
    "python3 scripts/check_rtl_source_lists.py --selftest", "python3 scripts/check_soc_sources.py",
    "python3 scripts/check_deploy_shape.py --self-test", "python3 scripts/check_entity_shape.py --self-test",
    "python3 sw/litex/iob_pack_selftest.py",
}
PARTIAL_R = {"python3 sw/builder/test_builder.py":
             "R: gate 36a's three arms and gate 32 only (full builder is M)"}
EQUIV = {'python3 scripts/check_em_dash.py --base "$base"':
         "R+M: --base 52711029 (= merge-base with dev, what a PR event derives)"}
PLUMB = ("set ", "case ", "if ", "fi", "esac", "echo ", "base=", "git fetch", "git cat-file",
         "pull_request)", "push)", "*)", ";;", "rm -rf .git", "exit ", "ver=", "sha256=", "url=",
         "curl ", "unzip ", "sudo ", "sv2v --version", '"$url"', "/usr/local/bin", "then",
         "else", "done", "for ", "do", "--output", "python3 -m pip install", "\\")
wf = yaml.safe_load((root / ".github/workflows/docs.yml").read_text())
tot = {"M": 0, "R": 0, "both": 0, "none": 0}
for job in ("docs-check", "wire-accountability", "docs-check-no-git"):
    steps = wf["jobs"][job]["steps"]
    print(f"== {job}: {len(steps)} steps")
    for i, s in enumerate(steps, 1):
        name = s.get("name") or s.get("uses")
        if "uses" in s:
            print(f"  {i:>2} {name}: action (hosted-only)")
            continue
        for ln in [l.strip() for l in s["run"].splitlines() if l.strip()]:
            if ln in EQUIV:
                tag = EQUIV[ln]
            elif ln in PARTIAL_R:
                tag = ("M + " if ln in M else "") + PARTIAL_R[ln]
            elif any(ln.startswith(p) for p in PLUMB):
                tag = "install/plumbing (not a gate)"
            else:
                m, r = ln in M, ln in R
                tag = {(True, True): "M+R", (True, False): "M", (False, True): "R",
                       (False, False): "NOT REPRODUCED on the candidate"}[(m, r)]
                tot["both" if m and r else "M" if m else "R" if r else "none"] += 1
            print(f"  {i:>2} {name}: {ln[:78]:<78} -> {tag}")
print(f"gate command lines: M+R {tot['both']}, M only {tot['M']}, R only {tot['R']}, "
      f"not reproduced {tot['none']}")
