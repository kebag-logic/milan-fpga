"""External review probe driver: baseline + appended probe tests + selected plants.

Usage: python3 -I r702_6_probe.py <clone> <out> <probe_tests.cpp> [jobs] [noplants]
Works only in copies under <out>; never writes the clone.
"""
import json, shutil, sys
from pathlib import Path

clone, out, probe = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve()
jobs = int(sys.argv[4]) if len(sys.argv) > 4 else 16
noplants = len(sys.argv) > 5 and sys.argv[5] == "noplants"
sys.path.insert(0, str(clone / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(clone / "sw/firmware/gtest"))
import aecp_arms, aecp_mutants, fw_gtest  # noqa: E402
from ctrl_build import CTRL, ROOT, STACK, Tree, Refusal, Outcome, stack_pin  # noqa: E402

print("tsn-c-stack at", stack_pin(STACK.resolve()), flush=True)
out.mkdir(parents=True, exist_ok=True)
src = out / "work/ctrl"
shutil.copytree(CTRL, src, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
shutil.copytree(CTRL.parent / "ctrl_nvm", src.parent / "ctrl_nvm", dirs_exist_ok=True,
                ignore=shutil.ignore_patterns("test", "__pycache__", "*.pyc"))
here = out / "probe_here"
shutil.copytree(CTRL / "test", here, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
(here / "test_aecp.cpp").write_text((CTRL / "test/test_aecp.cpp").read_text() + probe.read_text())
aecp_arms.HERE = here
tree = Tree(src, out / "work/build", out / "work/reuse", fw_gtest.Build(jobs=jobs), STACK.resolve())
config = ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml"
receipts = {"baseline": {}, "plants": []}

for interfaces, mode in ((1, "core"), (2, "core"), (1, "app"), (2, "app")):
    r = aecp_arms.core_arm(tree, config, interfaces, mode, "*")
    (out / f"baseline-{mode}-if{interfaces}.log").write_text(r.log)
    probes = {t: (f"[       OK ] Core.{t} (" in r.log) for t in (
        "ReviewProbeOwnerUnlockWaitsAcrossExpiryThenTaken", "ReviewProbeOwnerUnlockWaitsAcrossExpiryThenFails",
        "ReviewProbeSystemIdReadWhileWaiting")}
    new = {t: (f"[       OK ] {t} (" in r.log) for t in (
        "Core.AnExpiredLockHoldsByItsOwnerUntilThePlatformAppliedItsRelease",
        "Core.ASystemIdChangeWhileOneWaitsIsRefusedAsEveryChangeIs",
        "Core.AWaitingChangeIsAnsweredOnTheInterfaceItCameIn",
        "Face.AWaitingChangeIsAnsweredWithinTheInProgressCadence")}
    failed = [l for l in r.log.splitlines() if l.startswith("[  FAILED  ]")]
    receipts["baseline"][f"{mode}-if{interfaces}"] = {"rc": r.rc, "probes_ok": probes, "new_tests_ok": new,
                                                      "failed_lines": failed[:40]}
    print(f"[baseline {mode} if{interfaces}] rc={r.rc} probes={probes} new={new} failed={len(failed)}", flush=True)

NEW = ["expired-lock-read-released", "expired-lock-owner-dropped", "expired-lock-not-read-by-acmp",
       "expired-lock-not-held-against-others", "expired-lock-owner-kept-once-notified",
       "system-id-refusal-not-implemented", "waiting-response-leaves-on-the-last-interface",
       "wait-bound-past-the-cadence", "wait-bound-past-the-cadence-with-its-service"]
D = aecp_mutants.defect
mine = [
    D("review-refusal-status-old-predicate", "aecp/aecp.c",
      "if (status == AECP_ENTITY_LOCKED && a->refusing && !aecp_other_lock(a)) {",
      "if (status == AECP_ENTITY_LOCKED && a->refusing && (!a->locked || a->lock_owner == a->requester)) {",
      ("Core.AnExpiredLockHoldsByItsOwnerUntilThePlatformAppliedItsRelease", "")),
    D("review-mvu-set-taken-while-refusing", "aecp/aecp.c",
      "if (set && a->refusing) {", "if (false) {",
      ("Core.ASystemIdChangeWhileOneWaitsIsRefusedAsEveryChangeIs", "")),
    D("review-available-owner-zero-while-released", "aecp/aecp_commands.c",
      "wire_put_be(out + 12, a->lock_owner, 8);", "wire_put_be(out + 12, a->locked ? a->lock_owner : 0u, 8);",
      ("Core.AnExpiredLockHoldsByItsOwnerUntilThePlatformAppliedItsRelease", "")),
    D("review-lock-reply-owner-zero-while-released", "aecp/aecp_commands.c",
      "wire_put_be(out + 4, a->lock_owner, 8);", "wire_put_be(out + 4, a->locked ? a->lock_owner : 0u, 8);",
      ("Core.AnExpiredLockHoldsByItsOwnerUntilThePlatformAppliedItsRelease", "")),
    D("review-mvu-refusal-reports-request", "aecp/aecp.c",
      "\t\t\t\t\tstatus = AECP_ENTITY_MISBEHAVING;\n\t\t\t\t} else if (set",
      "\t\t\t\t\tstatus = AECP_ENTITY_MISBEHAVING;\n\t\t\t\t\ta->system_id = wire_be64(p + 32);\n\t\t\t\t} else if (set",
      ("Core.ASystemIdChangeWhileOneWaitsIsRefusedAsEveryChangeIs", "")),
    D("review-wait-bound-111", "aecp/aecp.h", "#define AECP_WAIT_MS 100u", "#define AECP_WAIT_MS 111u",
      ("Face.AWaitingChangeIsAnsweredWithinTheInProgressCadence", "")),
]
by = {d.name: d for d in aecp_mutants.DEFECTS}
plants = [] if noplants else [by[n] for n in NEW] + mine
for d in plants:
    path = d.path if d.path.startswith(("aecp/", "app/", "mbx/")) or "/" in d.path else "aecp/" + d.path
    target = src / path
    original = target.read_text()
    count = original.count(d.old)
    if count != 1:
        receipts["plants"].append({"name": d.name, "caught": False, "error": f"sites={count}"})
        print(f"[SITE {count}] {d.name}", flush=True)
        continue
    target.write_text(original.replace(d.old, d.new))
    try:
        selected = ":".join(t for t, _ in d.checks)
        r = aecp_arms.core_arm(tree, config, 2, "app", selected)
        ok = all(aecp_mutants.caught(t, w, r) for t, w in d.checks)
        (out / (d.name + ".log")).write_text(r.log)
    except Refusal as e:
        ok = False
        (out / (d.name + ".log")).write_text(str(e))
    finally:
        target.write_text(original)
    receipts["plants"].append({"name": d.name, "path": path, "checks": list(d.checks), "caught": ok})
    print(f"[{'ok' if ok else 'ESCAPED'}] {d.name}", flush=True)
(out / "results.json").write_text(json.dumps(receipts, indent=2) + "\n")
