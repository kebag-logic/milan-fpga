#!/usr/bin/env python3
"""R312-2 probe: how many bytes does the product firmware's capture copy move?

Builds the committed host bench (sw/firmware/nvm_hosttest) from an
INSTRUMENTED copy of milan_baremetal.c held only in a scratch directory. The
instrumentation counts the bytes nvm_capture() stores into the private stage
and the records it copies, split by record id range, and prints them after
the copy loop. It then runs a blank boot followed by one commit (only
erased records, i.e. nothing materialized beyond what a blank board holds)
and applies section 18's own cost model to the counted bytes.

Usage: capture_copy_probe.py <repo root> <scratch dir> [config stems...]
No file in the repository is modified.
"""
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
SCRATCH = Path(sys.argv[2]).resolve()
STEMS = sys.argv[3:] or ["endstation_ax7101_1x1_tdm8", "endstation_ax7101_8x8"]
sys.path.insert(0, str(ROOT / "sw/firmware/nvm_hosttest"))
import test_nvm_firmware as t  # noqa: E402

STORE = "NVM_STG[KLJ2_HDR + i] = NVM_IMG[KLJ2_HDR + i];"
COPYDECL = "\t\tif (copy) {\n"
FENCE = '\t/* the copy\'s loads complete before the attest strobe leaves */\n'

src = (ROOT / "sw/firmware/milan_baremetal/milan_baremetal.c").read_text()
for needle in (STORE, COPYDECL, FENCE):
    assert src.count(needle) == 1, f"anchor not unique: {needle!r}"
src = src.replace("static struct nvm_cap nvm_capture(void)\n{",
                  "static unsigned int probe_bytes, probe_recs, probe_mapo, probe_open;\n"
                  "static struct nvm_cap nvm_capture(void)\n{", 1)
src = src.replace(STORE, STORE + " probe_bytes++;"
                  " if (rec.id >= 0x70u && rec.id < 0x80u) probe_mapo++;", 1)
src = src.replace(COPYDECL, "\t\tif (!copy) probe_open++;\n" + COPYDECL
                  + "\t\t\tprobe_recs++;\n", 1)
src = src.replace(FENCE, '\tprintf("PROBE copy bytes=%u records=%u mapo_bytes=%u open=%u\\n",'
                  " probe_bytes, probe_recs, probe_mapo, probe_open);\n"
                  "\tprobe_bytes = probe_recs = probe_mapo = probe_open = 0;\n" + FENCE, 1)

PROBE_RE = re.compile(r"PROBE copy bytes=(\d+) records=(\d+) mapo_bytes=(\d+) open=(\d+)")
rc = 0
for stem in STEMS:
    cfg = ROOT / "configs" / f"{stem}.yaml"
    work = SCRATCH / stem
    work.mkdir(parents=True, exist_ok=True)
    bench = t.make_bench(cfg, work, src)
    out, s, _boot = t.run(bench, "--boot", "--uart", "milan_nvm commit")
    hits = PROBE_RE.findall(out)
    if not hits or s.get("acks") != 1:
        print(f"{stem}: probe line or commit missing: acks={s.get('acks')} hits={hits}")
        rc = 1
        continue
    a, n, mapo, opened = (int(x) for x in hits[-1])
    instr = 6 * a + 50 * n
    ddr = 2 * a
    nominal = (10 * instr + 30 * ddr) * 1000 / 50_000_000
    doubled = (20 * instr + 60 * ddr) * 1000 / 50_000_000
    print(f"{stem}: capture copied {a} bytes over {n} records "
          f"({mapo} bytes in ids 0x70-0x7F), {opened} open records skipped; "
          f"acks={s.get('acks')}")
    print(f"{stem}: section-18 model on the copied bytes: nominal {nominal:.4f} ms "
          f"(margin {50 / nominal:.2f}x), doubled {doubled:.4f} ms "
          f"(margin {50 / doubled:.2f}x)")
sys.exit(rc)
