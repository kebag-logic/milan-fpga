"""probe_mutants.py <tree> <out> <config> <interfaces> <set> [shard/of]

Reviewer probe: plant each defect alone into a private copy of the firmware tree of <tree> (a clean checkout of the
head under review), run the AECP App arm with the two tests the defects are aimed at, and report whether the run
fails and on which words. <set> is 'rows' (the PR's aecp_output_mutants.ROWS, checked by their own named words via
aecp_mutants.caught) or 'extra' (the reviewer's own defects, below, reported by the failures they produce)."""
import re
import shutil
import sys
from pathlib import Path

tree_root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree_root / "sw/firmware/ctrl/test"))
import aecp_arms  # noqa: E402
import aecp_mutants as am  # noqa: E402
import aecp_output_mutants as om  # noqa: E402
import fw_gtest  # noqa: E402
from ctrl_build import CTRL, ROOT, STACK, Tree  # noqa: E402

out, config, interfaces, which = Path(sys.argv[2]), ROOT / sys.argv[3], int(sys.argv[4]), sys.argv[5]
shard, of = (int(x) for x in (sys.argv[6] if len(sys.argv) > 6 else "0/1").split("/"))
FILTER = om.TEST + ":Core.TheRunningCheckObservesEveryStreamBriefly"
APP = "app/ctrl_app_aecp.c"
CMD = "aecp/aecp_commands.c"
EXTRA = (
    # aecp_stream_read no longer keeps the caller's brief: the map edit's check reads whole again
    ("rv-brief-not-kept", CMD, "\tout->brief = brief;\n", "\t(void)brief;\n"),
    # GET/SET_STREAM_INFO read brief: the completion never runs and the face's words are not read
    ("rv-stream-info-brief", CMD, "\tstruct aecp_stream_info info = {.brief = false};\n",
     "\tstruct aecp_stream_info info = {.brief = true};\n"),
    # the completion overwrites the face's flags instead of adding REGISTERING_FAILED to them
    ("rv-flags-overwritten", APP, "\tv->flags |= listening && !i->registered[index] ? 0x40u : 0u;\n",
     "\tv->flags = listening && !i->registered[index] ? 0x40u : 0u;\n"),
    # an Asking Failed Listener also raises MSRP_FAILURE_VALID (an output's Talker Failed bit), a wrong extra flag
    ("rv-failed-adds-msrp-failure-valid", APP, "\tv->flags |= listening && !i->registered[index] ? 0x40u : 0u;\n",
     "\tv->flags |= listening && !i->registered[index] ? 0x08000040u : 0u;\n"),
    # REGISTERING raised for a Listener on either interface (any interface's copy), not the output's own
    ("rv-listener-any-interface", APP, "\tbool listening = i != NULL && i->listener_present[index];\n",
     "\tbool listening = i != NULL && (c->app->srp->ifs[0].listener_present[index] || "
     "c->app->srp->ifs[MBX_N_IF - 1u].listener_present[index]);\n"),
    # the completion also runs for an undeclared output's brief read and every whole read (gate on the brief alone)
    ("rv-gate-brief-only", APP, "\t} else if (!v->brief && (v->flags & 0x10000000u) != 0u) {\n",
     "\t} else if (!v->brief && type == 6u) {\n"),
    # the gate reads STREAM_ID_VALID instead of STREAM_DEST_MAC_VALID (expected equivalent: the face sets both)
    ("rv-gate-stream-id-valid", APP, "\t} else if (!v->brief && (v->flags & 0x10000000u) != 0u) {\n",
     "\t} else if (!v->brief && (v->flags & 0x40000000u) != 0u) {\n"),
)

out.mkdir(parents=True, exist_ok=True)
src = out / "work/ctrl"
shutil.copytree(CTRL, src, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
shutil.copytree(CTRL.parent / "ctrl_nvm", src.parent / "ctrl_nvm", dirs_exist_ok=True,
                ignore=shutil.ignore_patterns("test", "__pycache__", "*.pyc"))
tree = Tree(src, out / "work/build", out / "work/reuse", fw_gtest.Build(jobs=4), STACK)
rows = [am.defect(*r) for r in om.ROWS] if which == "rows" else [am.defect(*r, ("-", "-")) for r in EXTRA]
rows = rows[shard::of]
bad = 0
for d in rows:
    target = src / d.path
    original = target.read_text()
    assert original.count(d.old) == 1, d.name
    target.write_text(original.replace(d.old, d.new))
    try:
        r = aecp_arms.core_arm(tree, config, interfaces, "app", FILTER)
    finally:
        target.write_text(original)
    words = sorted({re.sub(r"(: output [0-9]+.*|: [0-9]+|, declaration [0-9]+)$", "", m)
                    for m in re.findall(r"\[FAIL\] [A-Za-z.]+: ([^\n]*)", r.log)})
    if which == "rows":
        ok = all(am.caught(t, w, r) for t, w in d.checks)
        bad += not ok
        print(f"[{'ok' if ok else 'ESCAPED'}] {d.name} rc={r.rc} named={[w for _, w in d.checks]}", flush=True)
    else:
        print(f"[{'FAILS' if r.rc != 0 else 'SURVIVES'}] {d.name} rc={r.rc}", flush=True)
    for w in words:
        print(f"      fails: {w}", flush=True)
print(f"{config.stem} if{interfaces} {which} shard {shard}/{of}: {len(rows)} planted, {bad} escaped of named words",
      flush=True)
