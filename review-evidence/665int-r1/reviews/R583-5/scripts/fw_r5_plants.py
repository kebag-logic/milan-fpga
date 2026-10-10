#!/usr/bin/env python3
"""Reviewer driver (R583-5): run the round-5 firmware plants of PR #704 and
independent reviewer plants against the gate's own arms, nothing else.

usage: fw_r5_plants.py REPO OUT [JOBS]

REPO is a checkout of the head under review (with third_party/lwSRP present);
OUT is a scratch directory. Every plant is a one-site text edit of a copy of
sw/firmware/ctrl; a plant counts as killed only if the named test fails with
the named words, by the gate's own `caught` predicates.
"""
import sys
from pathlib import Path

repo, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
jobs = int(sys.argv[3]) if len(sys.argv) > 3 else 4
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))

import ctrl_arms, ctrl_mutants, srp_mutants, srp_pub_mutants, fw_gtest  # noqa: E401,E402
from ctrl_build import CTRL, Tree, Refusal, Outcome  # noqa: E402
from ctrl_mutant import Mutant  # noqa: E402
from ctrl_reuse import cut_reuse  # noqa: E402

lwsrp = repo / "third_party/lwSRP"
B13 = ctrl_mutants.B13
SITE = "(void)mbx_pub_sink_binding(interface, sink, bound, started, stream_id != 0u);"
ARMS = {"acmp": ctrl_arms.arm_acmp, "acmpif2": ctrl_arms.arm_acmpif2}

# the author's round-5 ACMP plant, taken from the gate's own table
author = [m for m in ctrl_mutants.MUTANTS if m.name == "pub-acmp-adapter-sid-valid-always"]
assert len(author) == 1, "the round-5 ACMP plant is not in the table"
# reviewer plants: SID_VALID follows the binding or the started level, not the stream
mine = [
    Mutant("r583-sid-valid-follows-bound", "acmp/acmp_mbx.c", SITE,
           SITE.replace("stream_id != 0u", "bound"), "acmp", B13,
           "B13 the re-bound sink carries no stream_id to the datapath"),
    Mutant("r583-sid-valid-follows-started", "acmp/acmp_mbx.c", SITE,
           SITE.replace("stream_id != 0u", "started"), "acmp", B13,
           "B13 the started move carries no stream_id to the datapath"),
    Mutant("r583-sid-valid-stream-or-started", "acmp/acmp_mbx.c", SITE,
           SITE.replace("stream_id != 0u", "stream_id != 0u || started"), "acmp", B13,
           "B13 the started move carries no stream_id to the datapath"),
]

print(f"toolchain: {fw_gtest.toolchain()}", flush=True)
tree = Tree(CTRL, out / "checkout", out / "reuse", fw_gtest.Build(jobs=jobs))
cut_reuse(tree.reuse)
escaped = 0
base = ctrl_arms.arm_acmp(tree)
print(f"[{'ok' if base.rc == 0 else 'BAD'}] positive control: acmp arm on the unplanted tree rc={base.rc}", flush=True)
escaped += base.rc != 0
build = fw_gtest.Build(jobs=jobs)
for m in author + mine:
    t = Tree(ctrl_mutants.plant(m, out), out / "work" / "build", tree.reuse, build)
    missed = []
    for arm, test, needle in m.kills():
        try:
            o = ARMS[arm](t)
        except Refusal as exc:
            o = Outcome(arm, 2, f"refused: {exc}")
        if not ctrl_mutants.caught(test, needle, o):
            missed.append(f"{arm}:{test}:{needle}")
            print("\n".join(ln for ln in o.log.splitlines() if "[FAIL]" in ln)[:2000])
    print(f"[{'ok' if not missed else 'ESCAPED'}] acmp plant {m.name} {[k[0] for k in m.kills()]}"
          f"{'' if not missed else ' missed ' + '; '.join(missed)}", flush=True)
    escaped += bool(missed)

# SRP: the author's five round-5 defects at two and one interface(s), plus reviewer defects
r5 = tuple(d for d in srp_mutants.DEFECTS if d.name in srp_pub_mutants.ROUND5)
assert len(r5) == 5, r5
D = srp_mutants.Defect
FAILED = "PubTalkerDeclIsNotPublishedByACreationThatFails"
ADOPTED = "PubTalkerDeclHoldsAcrossADomainAdoption"
JOIN_FAIL = ("                         &value,true) != 0) {\n            return false;\n        }\n")
reviewer = (
    # a join refused part way publishes the sources already joined
    D("r583-partial-published-on-refusal", FAILED, JOIN_FAIL,
      JOIN_FAIL.replace("return false;", "(void)mbx_pub_talker_decl(i->index,declared);\n            return false;"),
      "publishes no Talker declaration"),
    # the adoption republishes TALKER_DECL one source short
    D("r583-adoption-one-source-short", ADOPTED, "    (void)declare_sources(i);\n    i->domain_owed = false;\n",
      "    (void)declare_sources(i);\n    (void)mbx_pub_talker_decl(i->index,(1u << CTRL_SRP_SOURCES) - 2u);\n"
      "    i->domain_owed = false;\n",
      "TALKER_DECL"),
    # the adoption republishes TALKER_DECL with source 0 dropped while the Domain is owed
    D("r583-adoption-drops-source-0", ADOPTED, srp_pub_mutants.DECLARED_PUBLISHED,
      "    (void)mbx_pub_talker_decl(i->index,i->domain_owed ? (declared & ~1u) : declared);\n",
      "TALKER_DECL"),
)
saved = srp_mutants.DEFECTS
try:
    for label, table, ifs in (("if2 author", r5, 2), ("if1 author", r5, 1), ("if2 reviewer", reviewer, 2)):
        srp_mutants.DEFECTS = table
        bad = srp_mutants.campaign(out / f"srp-{label.replace(' ', '-')}", lwsrp, jobs, ifs)
        print(f"[{'ESCAPED' if bad else 'ok'}] srp campaign {label}: {len(table)} defect(s)", flush=True)
        escaped += bool(bad)
finally:
    srp_mutants.DEFECTS = saved
print(f"fw_r5_plants: {escaped} escaped or failed control(s)")
sys.exit(1 if escaped else 0)
