#!/usr/bin/env python3
"""probe_leaks.py <checkout> <work>: reviewer-owned AS_CAPABLE leak plants for PR #966 (IEEE 1722.1-2021 7.4.40.2).

Each plant rewrites the one bit-0 override in sw/firmware/ctrl/aecp/aecp_face.c inside the campaign's own copy of
the tree (the checkout is never written) and is graded with the repository's own reader (aecp_mutants.caught) on
two words: it must FAIL with "AS_CAPABLE is the software gPTP owner's" and must NOT fail with "software gPTP keeps
the datapath's link flags" (so the new check, not the old one, catches it). The table's three software-gPTP face
rows and the plant-table drift control are re-run as well. Exit 0 only when every expectation holds."""
import json
import sys
from pathlib import Path

repo, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
only = sys.argv[3:]   # "baseline": the unplanted leg alone, reusing <work>/base
sys.path[:0] = [str(repo / "sw/firmware/ctrl/test"), str(repo / "sw/firmware/gtest")]
import aecp_face_mutants, aecp_mutants  # noqa: E401,E402
from ctrl_build import STACK, stack_pin  # noqa: E402

AVB = "Face.SoftwareGptpAvbKeepsTheDatapathsLinkAndClass"
NEW = "AS_CAPABLE is the software gPTP owner's"
LINK = "software gPTP keeps the datapath's link flags"
SITE = "out->flags = (uint8_t)((out->flags & ~1u) | (as_capable ? 1u : 0u));"
LEAKS = {
    # the datapath's bit wins outright: the owner's verdict ignored
    "rv-leak-datapath-wins": "out->flags = (uint8_t)((out->flags & ~1u) | (out->flags & 1u));",
    # the override removed entirely: the datapath's flags byte served as read
    "rv-leak-override-removed": "out->flags = (uint8_t)out->flags; (void)as_capable;",
    # the owner's verdict AND'd with the datapath's bit
    "rv-leak-and": "out->flags = (uint8_t)((out->flags & ~1u) | ((as_capable && (out->flags & 1u)) ? 1u : 0u));",
    # the owner's verdict OR'd with the datapath's bit, spelled differently from the table row
    "rv-leak-or-spelled": "out->flags = (uint8_t)((out->flags & ~1u) | ((as_capable || (out->flags & 1u)) ? 1u : 0u));",
    # the owner's verdict inverted (a non-leak control: must also be caught by the new words)
    "rv-owner-inverted": "out->flags = (uint8_t)((out->flags & ~1u) | (as_capable ? 0u : 1u));",
}
print(f"checkout {repo}; tsn-c-stack at {stack_pin(STACK.resolve())}", flush=True)
bad = 0
if not only:
    aecp_mutants.controls()          # the full table's drift control, with the new row in it
    print("controls: table drift and reader controls pass", flush=True)
    aecp_mutants.controls = lambda: None
    mine = tuple(aecp_mutants.defect(n, "aecp_face.c", SITE, v, (AVB, NEW)) for n, v in LEAKS.items())
    rows = tuple(aecp_mutants.defect(*r) for r in aecp_face_mutants.ROWS if r[0].startswith("face-software-gptp-"))
    aecp_mutants.DEFECTS = mine + rows
    escaped = aecp_mutants.campaign(work / "campaign", stack=STACK.resolve())
    bad += int(escaped)
    results = json.loads((work / "campaign/results.json").read_text())
    for r in results:
        log = (work / "campaign" / (r["name"] + ".log")).read_text()
        link = aecp_mutants.caught(AVB, LINK, aecp_mutants.Outcome(r["name"], 1, log))
        new = aecp_mutants.caught(AVB, NEW, aecp_mutants.Outcome(r["name"], 1, log))
        expect_link = r["name"] == "face-software-gptp-clears-link-flags"
        expect_new = r["name"].startswith("rv-") or r["name"] == "face-software-gptp-keeps-datapath-capable"
        ok = r["caught"] and (r["name"].endswith("path-refusal") or (link == expect_link and new == expect_new))
        bad += int(not ok)
        print(f"{'PASS' if ok else 'FAIL'} {r['name']}: caught={r['caught']} new-words-failed={new} "
              f"link-words-failed={link}", flush=True)
# the unplanted head: every Face.SoftwareGptp* test passes at one and two interfaces
import shutil  # noqa: E402
import aecp_arms, fw_gtest  # noqa: E401,E402
from ctrl_build import CTRL, ROOT, Tree  # noqa: E402
src = work / "base/ctrl"
shutil.rmtree(work / "base/ctrl", ignore_errors=True)
shutil.rmtree(work / "base/ctrl_nvm", ignore_errors=True)
shutil.copytree(CTRL, src, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
shutil.copytree(CTRL.parent / "ctrl_nvm", work / "base/ctrl_nvm", ignore=shutil.ignore_patterns("test", "__pycache__"))
tree = Tree(src, work / "base/build", work / "base/reuse", fw_gtest.Build(jobs=8), STACK.resolve())
for n in (1, 2):
    out = aecp_arms.core_arm(tree, ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml", n, "app", "Face.SoftwareGptp*")
    (work / f"baseline-if{n}.log").write_text(out.log)
    ok = out.rc == 0 and f"[       OK ] {AVB}" in out.log
    bad += int(not ok)
    print(f"{'PASS' if ok else 'FAIL'} baseline if{n}: rc={out.rc} {AVB} ok={ok}", flush=True)
print(f"probe-rc={int(bool(bad))}")
raise SystemExit(int(bool(bad)))
