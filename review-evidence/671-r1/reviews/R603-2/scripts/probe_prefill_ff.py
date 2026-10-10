#!/usr/bin/env python3
"""Reviewer probe (R603-2), OUTSIDE #671's boot scope: a runtime read fault on
the capture's prefill (nvm_prefill_stage(), unchanged by PR #715), which
copies the authoritative slot from flash into the stage for every capture.

Slot A valid at 0x5A5A5, slot B blank. A clean boot (5 reads: the AEM image,
A's judgement, B's two, A's re-stage). One record is then reported OPEN by
the backend, another record is changed, and the debounce commits. The
reads after the boot that make the prefill are answered with slot A read as all 0xFF
(--read-ff a:5:IMG_LEN; the prefill opens one
mapping read per byte), the fault mode check 13 itself plants. A clean reboot
follows. The probe reports what the open record restores as.

Usage: probe_prefill_ff.py REPO_ROOT WORKDIR [--shape endstation_ax7101_1x1_tdm8]
Exit 0 when the probe ran (it reports, it does not grade).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("work")
    ap.add_argument("--shape", default="endstation_ax7101_1x1_tdm8")
    a = ap.parse_args()
    root = Path(a.root).resolve()
    sys.path.insert(0, str(root / "sw/firmware/nvm_hosttest"))
    import test_nvm_firmware as t  # noqa: E402

    work = Path(a.work).resolve()
    work.mkdir(parents=True, exist_ok=True)
    bench = t.make_bench(root / "configs" / f"{a.shape}.yaml", work / "bench", t.FIRMWARE.read_text())
    fr = t.fault_run(bench)
    rid = max(bench.frames)
    open_rid = rid - 1
    key_open = ("NAME", open_rid - 0x80)
    (work / "a0.bin").write_bytes(fr.containers[(0x5A5A5, False)])
    (work / "b0.bin").write_bytes(b"\xff" * t.SLOT)
    # nvm_prefill_stage() evaluates the mapping once per byte, so the
    # prefill is reads 5 .. 5 + img_len - 1
    for label, fault in (("control", ()), ("prefill_ff", ("--read-ff", f"a:5:{bench.img_len}"))):
        d = work / label
        d.mkdir(exist_ok=True)
        out, s, boot = t.run(bench, "--slot-a", str(work / "a0.bin"), "--slot-b", str(work / "b0.bin"),
                             *fault, "--boot", "--open-record", str(open_rid),
                             "--change", f"{fr.off}:{fr.changes[0].hex()}", "--idle-ms", "1500",
                             "--dump-slot-a", str(d / "a1.bin"), "--dump-slot-b", str(d / "b1.bin"))
        commits = [x for x in out.splitlines() if "commit" in x and x.startswith("Milan NVM")]
        out2, s2, boot2 = t.run(bench, "--slot-a", str(d / "a1.bin"), "--slot-b", str(d / "b1.bin"),
                                "--boot", "--dump-ddr", str(d / "ddr2.bin"))
        vd, applied = t.klj2_decode((d / "ddr2.bin").read_bytes()[:bench.img_len], bench.donor,
                                    bench.ident, bench.expect)
        print(f"--- {label}: faulty_reads={s.get('faulty_reads')} acks={s.get('acks')}; {commits}")
        print(f"    clean reboot: {boot2 and boot2.group(0)}")
        print(f"    changed record {fr.key}: "
              f"{'kept' if applied.get(fr.key) == fr.want[1][fr.key] else 'NOT kept'}; "
              f"open record {key_open}: saved {fr.want[0].get(key_open, b'')[:8].hex()}, "
              f"restored {(applied.get(key_open) or b'')[:8].hex() or 'nothing (erased record)'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
