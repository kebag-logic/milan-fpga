#!/usr/bin/env python3
"""Reviewer probe (R603-2): a boot read fault on the WRITER RESTART WITHOUT A
FABRIC RESET (the re-attach path of nvm_boot()), which check 13 never boots.

The PR's host harness (sw/firmware/nvm_hosttest/nvm_host.c) is copied into a
scratch directory and given two probe-only options: --restart, the CPU-only
reset tb/verilator/nvm_cosim/run_cases.py already models (every writer static
back to its initial value, then nvm_boot() again, the fabric model kept), and
--read-fault-now, a --read-fault whose SKIP counts from the current read.
Nothing in the source tree is modified.

Scenario, per firmware (the exact head, and the head with the re-attach
branch's nvm_go_live() replaced by `nvm_ready = 1`):
  slot A blank, slot B valid at 0x5A5A5; a clean cold boot; then slot B's
  magic byte faulted on every read of the restart's judgement (differing
  bytes each time, so B is UNREAD); the restart; a real change; the debounce;
  then a clean cold boot from the slots the run left.
A control runs the same restart with no fault.

Usage: probe_reattach.py REPO_ROOT WORKDIR [--shape endstation_ax7101_1x1_tdm8]
Exit 0 when every expectation below holds, 1 otherwise.
"""
from __future__ import annotations

import argparse
import struct
import subprocess
import sys
from pathlib import Path

HARNESS_PATCH_ANCHOR = '\t\telse if (strcmp(a, "--erase-ms") == 0 && v)\n'
HARNESS_PATCH = (
    '\t\telse if (strcmp(a, "--read-fault-now") == 0 && v) {\n'
    '\t\t\tarm_read_fault(v, RF_XOR);\n'
    '\t\t\trf.skip += reads;\n'
    '\t\t} else if (strcmp(a, "--restart") == 0) {\n'
    '\t\t\tnvm_host_writer_restart();\n'
    '\t\t\tsettle();\n'
    '\t\t\tprintf("HOST restarted\\n");\n'
    '\t\t\ttakes = 0;\n'
    '\t\t}\n'
)
MAIN_ANCHOR = "int main(int argc, char **argv)\n"
REATTACH_OLD = "\t\tnvm_publish(verdict);\n\t\tnvm_go_live();\n\t\tprintf(\"Milan NVM: writer restarted"
REATTACH_NEW = "\t\tnvm_publish(verdict);\n\t\tnvm_ready = 1;\n\t\tprintf(\"Milan NVM: writer restarted"


def build(t, rc, bench, text: str, work: Path) -> Path:
    work.mkdir(parents=True, exist_ok=True)
    (work / "generated").mkdir(exist_ok=True)
    (work / "generated/soc.h").write_text((bench.work / "generated/soc.h").read_text())
    harness = t.HARNESS.read_text()
    assert harness.count(HARNESS_PATCH_ANCHOR) == 1 and harness.count(MAIN_ANCHOR) == 1
    harness = harness.replace(HARNESS_PATCH_ANCHOR, HARNESS_PATCH + HARNESS_PATCH_ANCHOR)
    harness = harness.replace(MAIN_ANCHOR, "void nvm_host_writer_restart(void);\n\n" + MAIN_ANCHOR)
    (work / "nvm_host_probe.c").write_text(harness)
    fw = t.FENCE_RE.sub("(void)0;", text) + rc.host_restart(text)
    (work / "milan_baremetal.c").write_text(fw)
    common = ["gcc", "-std=gnu11", "-O1", "-g", "-Wall", "-Wextra", "-Werror", f"-I{work}", f"-I{t.STUBS}", f"-I{t.HERE}"]
    defs = [f"-DNVM_HOST_JOURNAL_OFFSET=0x{t.JOURNAL:x}u", f"-DNVM_HOST_AEM_OFFSET=0x{t.AEM_OFFSET:x}u",
            f"-DNVM_HOST_IMAGE_OFF=0x{t.IMAGE_OFF:x}u"]
    for cmd in (common + defs + ["-c", str(work / "nvm_host_probe.c"), "-o", str(work / "host.o")],
                common + ["-Wno-format", "-c", str(work / "milan_baremetal.c"), "-o", str(work / "fw.o")],
                ["gcc", str(work / "host.o"), str(work / "fw.o"), "-o", str(work / "fw")]):
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode:
            raise SystemExit(f"probe build failed: {' '.join(cmd)}\n{r.stderr}")
    return work / "fw"


def go(binary: Path, work: Path, *args: str) -> tuple[str, dict]:
    r = subprocess.run([str(binary), *args], capture_output=True, text=True, cwd=work, timeout=600)
    if r.returncode:
        raise SystemExit(f"harness failed {r.returncode}: {args}\n{r.stdout}\n{r.stderr}")
    s = {}
    for line in r.stdout.splitlines():
        if line.startswith("HOST hb="):
            s = {k: int(v) for k, v in (kv.split("=") for kv in line[5:].split())}
    return r.stdout, s


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("work")
    ap.add_argument("--shape", default="endstation_ax7101_1x1_tdm8")
    a = ap.parse_args()
    root = Path(a.root).resolve()
    sys.path.insert(0, str(root / "sw/firmware/nvm_hosttest"))
    sys.path.insert(0, str(root / "tb/verilator/nvm_cosim"))
    import test_nvm_firmware as t  # noqa: E402
    import run_cases as rc  # noqa: E402

    work = Path(a.work).resolve()
    work.mkdir(parents=True, exist_ok=True)
    text = t.FIRMWARE.read_text()
    assert text.count(REATTACH_OLD) == 1
    bench = t.make_bench(root / "configs" / f"{a.shape}.yaml", work / "bench", text)
    fr = t.fault_run(bench)
    seq = 0x5A5A5
    b_slot = fr.containers[(seq, False)]
    (work / "a0.bin").write_bytes(b"\xff" * t.SLOT)
    (work / "b0.bin").write_bytes(b_slot)
    change = f"{fr.off}:{fr.changes[0].hex()}"
    want_change = fr.changes[0][t.REC_HDR:]
    ok = True
    print(f"shape {a.shape}; slot A blank, slot B valid at {seq:#x}; change at image offset {fr.off}")
    for label, fw_text in (("head", text), ("p_reattach_goes_live", text.replace(REATTACH_OLD, REATTACH_NEW))):
        binary = build(t, rc, bench, fw_text, work / label)
        for fault in (True, False):
            tag = f"{label}/{'fault' if fault else 'control'}"
            d = work / label / ("fault" if fault else "control")
            d.mkdir(exist_ok=True)
            opts = ["--slot-a", str(work / "a0.bin"), "--slot-b", str(work / "b0.bin"), "--boot",
                    "--idle-ms", "100"]
            if fault:
                opts += ["--read-fault-now", "b:0:0:5"]
            opts += ["--restart", "--change", change, "--idle-ms", "3000",
                     "--dump-slot-a", str(d / "a1.bin"), "--dump-slot-b", str(d / "b1.bin")]
            out, s = go(binary, d, *opts)
            restart = out.split("HOST booted", 1)[1]
            lines = [x for x in restart.splitlines() if x.startswith("Milan NVM") or x.startswith("HOST")]
            print(f"--- {tag}: restart transcript")
            for x in lines:
                print("   ", x)
            out2, s2 = go(binary, d, "--slot-a", str(d / "a1.bin"), "--slot-b", str(d / "b1.bin"),
                          "--boot", "--dump-ddr", str(d / "ddr2.bin"))
            boot2 = t.BOOT_RE.search(out2)
            got = t.restored(bench, d / "ddr2.bin", fr.want[1], fr.key)[0]
            a1 = (d / "a1.bin").read_bytes()[:bench.img_len]
            a1_seq = struct.unpack_from("<I", a1, 8)[0] if bench.verdict(a1) == t.VD_OK else None
            survived = got == want_change
            held = t.HELD_LINE in restart
            print(f"    after the restart: held={held} erases={s.get('erases')} programs={s.get('programs')} "
                  f"acks={s.get('acks')} backed={s.get('backed')} dirty={s.get('dirty')}; slot A now "
                  f"{'seq %#x' % a1_seq if a1_seq is not None else 'not a valid container'}")
            print(f"    clean reboot: {boot2 and boot2.group(0)}")
            print(f"    the change {'SURVIVED' if survived else 'was LOST'} the clean reboot")
            if label == "head" and fault:
                exp = held and s.get("programs") == 0 and s.get("acks") == 0 and s.get("backed") == 0
            elif fault:
                exp = (not held) and s.get("acks") == 1 and not survived
            else:
                exp = (not held) and s.get("acks") == 1 and survived
            print(f"    EXPECTATION {'MET' if exp else 'NOT MET'} for {tag}")
            ok &= bool(exp)
    print("probe_reattach: " + ("every expectation met" if ok else "an expectation was NOT met"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
