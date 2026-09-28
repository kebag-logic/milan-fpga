#!/usr/bin/env python3
"""R369-3 disabled-writer probe (reviewer-owned, independent of the committed test).

Plants each rejected startup state WITHOUT editing the firmware source:
  identity: the host CSR model reports ID_MAGIC ^ 1 (harness copy edited);
  shape:    the generated header publishes MILAN_NVM_IMAGE_MAX 16, so the
            unmodified nvm_shape_consistent() refuses the record set.
Drives a long console sequence (empty, whitespace, unknown, every Milan
command, bad-argument forms) with and without idle time and requires no
heartbeat and no other backend strobe (hb, backed, stale, arms, starts,
acks, reloads all 0). Controls: the unmodified live boot must heartbeat,
and three firmware mutants must each be caught in the state they target:
  no-guard      : the nvm_started early return removed (both states);
  early-admit   : nvm_started = 1 moved above the shape check (shape);
  identity-admit: milan_init sets nvm_started before its identity return.
Usage: disabled_writer_probe.py REPO_ROOT WORKDIR [config ...]
"""
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
WORK = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(ROOT / "sw/firmware/nvm_hosttest"))
import test_nvm_firmware as nvm  # noqa: E402

LINES = ["", " ", "unknown_command", "help", "milan_status", "milan_nvm",
         "milan_nvm commit", "milan_nvm wipe", "milan_nvm bogus", "milan_gettime",
         "milan_settime", "milan_settime 1 0", "milan_utc", "milan_utc 1 0 37"]
ZERO = ("hb", "backed", "stale", "arms", "starts", "acks", "reloads")
FW = nvm.FIRMWARE.read_text()
HOST = nvm.HARNESS.read_text()
ORIG_HARNESS = nvm.HARNESS
ORIG_HEADER = nvm.constants_header


def once(old, new, text):
    if text.count(old) != 1:
        raise SystemExit(f"anchor not unique: {old!r}")
    return text.replace(old, new)


def bench(cfg, tag, state, fw_text):
    work = WORK / cfg.stem / tag / state
    work.mkdir(parents=True, exist_ok=True)
    nvm.HARNESS = ORIG_HARNESS
    nvm.constants_header = ORIG_HEADER
    if state == "identity":
        h = work / "nvm_host_idmismatch.c"
        text = once("csr[A_ID / 4] = ID_MAGIC;", "csr[A_ID / 4] = ID_MAGIC ^ 1u;", HOST)
        text = text.replace('#include "stubs/', f'#include "{ORIG_HARNESS.parent}/stubs/')
        h.write_text(text)
        nvm.HARNESS = h
    elif state == "shape":
        def hdr(*a, **k):
            return ORIG_HEADER(*a, **k).replace("#define MILAN_NVM_IMAGE_MAX 65536u",
                                                "#define MILAN_NVM_IMAGE_MAX 16u")
        nvm.constants_header = hdr
    b = nvm.make_bench(cfg, work, fw_text)
    nvm.HARNESS = ORIG_HARNESS
    nvm.constants_header = ORIG_HEADER
    return b


def drive(b, idle):
    args = ["--boot"]
    for ln in LINES * 2:
        args += ["--uart", ln]
        if idle:
            args += ["--idle-ms", str(idle)]
    raw, s, _ = nvm.run(b, *args)
    return raw, s


MARK = {"identity": "CSR identity mismatch", "shape": "persistence disabled"}


def grade_state(cfg, tag, state, fw_text):
    b = bench(cfg, tag, state, fw_text)
    bad = []
    for idle in (0, 300):
        raw, s = drive(b, idle)
        if state in MARK and MARK[state] not in raw:
            raise SystemExit(f"{cfg.stem} {tag} {state}: rejected state not reached")
        nz = {k: s[k] for k in ZERO if s[k] != 0}
        print(f"  {cfg.stem} {tag:<14} {state:<8} idle={idle:<3} lines={2*len(LINES)} "
              + " ".join(f"{k}={s[k]}" for k in ZERO) + f" erases={s['erases']} now_ms={s['now_ms']}")
        if nz:
            bad.append((idle, nz))
    return bad, s


def main():
    cfgs = [Path(c) for c in sys.argv[3:]] or sorted((ROOT / "configs").glob("endstation_*.yaml"))
    fails = []
    for cfg in cfgs:
        for state in ("identity", "shape"):
            bad, _ = grade_state(cfg, "head", state, FW)
            if bad:
                fails.append(f"{cfg.stem} head {state}: backend strobed {bad}")
        # live control: the admitted writer must heartbeat under the same lines
        b = bench(cfg, "head", "live", FW)
        raw, s = drive(b, 300)
        print(f"  {cfg.stem} head           live     hb={s['hb']} backed={s['backed']} stale={s['stale']}")
        if not (s["hb"] > 0 and s["backed"] == 1):
            fails.append(f"{cfg.stem} live control did not heartbeat")
    cfg = cfgs[0]
    mutants = {
        "no-guard": (once("\tif (!nvm_started)\n\t\treturn;\n", "", FW), ("identity", "shape")),
        "early-admit": (once("\tif (!nvm_shape_consistent()) {",
                             "\tnvm_started = 1;\n\tif (!nvm_shape_consistent()) {", FW), ("shape",)),
        "identity-admit": (once("\tif (id != MILAN_ID_MAGIC) {",
                                "\tnvm_started = 1;\n\tif (id != MILAN_ID_MAGIC) {", FW), ("identity",)),
    }
    for name, (text, states) in mutants.items():
        for state in states:
            bad, _ = grade_state(cfg, name, state, text)
            print(f"MUTANT {name} {state}: {'KILLED' if bad else 'SURVIVED'}")
            if not bad:
                fails.append(f"mutant {name} survived in {state}")
    for f in fails:
        print("FAIL:", f)
    print("RESULT:", "FAIL" if fails else "PASS", f"shapes={len(cfgs)}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
