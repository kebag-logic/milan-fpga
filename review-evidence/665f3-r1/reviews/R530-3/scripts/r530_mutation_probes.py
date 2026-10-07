#!/usr/bin/env python3
"""[R530] R530-3 reviewer-planted defects in acmp.c, each run against the head's `acmp` arm
(ctrl_arms.arm_acmp) in a copy of the ctrl tree. usage: r530_mutation_probes.py ROOT WORKDIR"""
import pathlib, shutil, sys
root, work = pathlib.Path(sys.argv[1]).resolve(), pathlib.Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / 'sw/firmware/ctrl/test'))
import ctrl_arms, ctrl_build as b, fw_gtest  # noqa: E402
SENT = "\tif (sent == SENT) {\n\t\tno_resp_from_send(a, s);\n"
SM = "sm_timer(a, s, ACMP_TIMER_NO_RESP, ACMP_TMR_NO_RESP_MS);"
MUTANTS = [
    ("owed-probe-sets-no-timer-kind", "\t\ts->timer = ACMP_TIMER_NO_RESP;\n\t\ts->timer_held = true;\n",
     "\t\ts->timer_held = true;\n"),
    ("no-resp-from-send-keeps-the-cached-clock", "\ta->now_read = false;\n\tsm_timer(a, s, ACMP_TIMER_NO_RESP",
     "\tsm_timer(a, s, ACMP_TIMER_NO_RESP"),
    ("duplicate-only-from-the-cached-clock", SENT,
     "\tif (sent == SENT) {\n\t\tif (s->probe_retried) { " + SM + " } else { no_resp_from_send(a, s); }\n"),
    ("initial-only-from-the-cached-clock", SENT,
     "\tif (sent == SENT) {\n\t\tif (!s->probe_retried) { " + SM + " } else { no_resp_from_send(a, s); }\n"),
    ("poll-timer-from-a-clock-read-before-its-send",
     "\tif (a->owed_count != 0u) {\n\t\tconst struct acmp_owed *o = &a->owed[a->owed_head];\n",
     "\tif (a->owed_count != 0u) {\n\t\t(void)now(a);\n\t\tconst struct acmp_owed *o = &a->owed[a->owed_head];\n"),
    ("taken-probe-199ms", SENT, "\tif (sent == SENT) {\n\t\tno_resp_from_send(a, s);\n\t\ts->timer_deadline -= 1u;\n"),
    ("lost-probe-rereads-the-clock (expected equivalent)", "\t} else {\n\t\t" + SM + "\n\t\ta->probes_lost++;",
     "\t} else {\n\t\tno_resp_from_send(a, s);\n\t\ta->probes_lost++;"),
]
# the poll mutant needs probe_left to keep the pre-send read: plant both edits
EXTRA = {"poll-timer-from-a-clock-read-before-its-send":
         ("\tif (s->timer_held && wire_be16(o->frame + O_SEQ) == s->probe_seq) {\n\t\tno_resp_from_send(a, s);",
          "\tif (s->timer_held && wire_be16(o->frame + O_SEQ) == s->probe_seq) {\n\t\t" + SM)}
results = []
for name, old, new in MUTANTS:
    slug = name.split(' ')[0]
    copy = work / slug / 'ctrl'
    if copy.exists():
        shutil.rmtree(copy)
    shutil.copytree(b.CTRL, copy, ignore=shutil.ignore_patterns('__pycache__'))
    f = copy / 'acmp/acmp.c'
    text = f.read_text()
    edits = [(old, new)] + ([EXTRA[name]] if name in EXTRA else [])
    for o, n in edits:
        assert text.count(o) == 1, (name, text.count(o))
        text = text.replace(o, n)
    f.write_text(text)
    tree = b.Tree(copy, work / slug / 'out', work / 'reuse', fw_gtest.Build(jobs=4))
    out = ctrl_arms.arm_acmp(tree)
    fails = [ln for ln in out.log.splitlines() if '[  FAILED  ]' in ln and ' ms)' in ln]
    verdict = 'CAUGHT' if out.rc != 0 else 'SURVIVED'
    results.append((name, verdict, out.rc, fails))
    print(f"[{verdict}] {name}: rc={out.rc}", *(f"\n    {x.strip()}" for x in fails[:6]), flush=True)
sys.exit(0)
