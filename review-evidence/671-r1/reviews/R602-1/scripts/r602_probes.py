#!/usr/bin/env python3
"""R602-1 reviewer probes for #671 / PR #715, on the firmware host model.

Usage: r602_probes.py <clone root> <work dir> <config stem> <probe> [<firmware.c>]

Imports the clone's own sw/firmware/nvm_hosttest/test_nvm_firmware.py (the
head harness) and drives it. <probe> is one of:
  base_repro   grade checks 13/14 (grade_read_faults, grade_refused_generation)
               against the firmware text given as the fifth argument (the base
               firmware): the #671 loss must be reported.
  plants       apply every READ_FAULT_MUTATIONS plant to the head firmware and
               grade checks 13/14 on this shape; each must be caught by its
               named words.
  scenarios    reviewer scenarios on the head firmware: both slots valid with
               the newer one faulted, a faulted re-stage that falls back to the
               other valid slot, the boot line's read-fault counter, and a
               fault on the header's length word (bytes per read).
Prints one line per observation and exits 0; the caller judges the lines.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
WORK = Path(sys.argv[2]).resolve()
CFG = ROOT / "configs" / f"{sys.argv[3]}.yaml"
PROBE = sys.argv[4]
sys.path.insert(0, str(ROOT / "sw/firmware/nvm_hosttest"))
import test_nvm_firmware as t  # noqa: E402
from nvm_contract import KLJ2_HDR, REC_HDR  # noqa: E402
from nvm_klj2 import frame_record, klj2_decode  # noqa: E402

HEAD_FW = (ROOT / "sw/firmware/milan_baremetal/milan_baremetal.c").read_text()


def bench_for(text: str, sub: str):
    w = WORK / sub
    w.mkdir(parents=True, exist_ok=True)
    return t.make_bench(CFG, w, text)


def payload(b, ddr: Path):
    rid = max(b.frames)
    vd, applied = klj2_decode(ddr.read_bytes()[:b.img_len], b.donor, b.ident, b.expect)
    return applied.get(("NAME", rid - 0x80)) if vd == t.VD_OK else None


def new_rec(b, base):
    rid = max(b.frames)
    plen = len(b.frames[rid]) - REC_HDR
    return frame_record(rid, bytes((base + j) & 0xFF for j in range(plen)), b.donor.layout)


def rec_off(b):
    return KLJ2_HDR + b.offsets()[max(b.frames)]


def base_repro():
    fw = Path(sys.argv[5]).read_text()
    b = bench_for(fw, "base")
    for g in (t.grade_read_faults, t.grade_refused_generation):
        got = g(b)
        lost = [x for x in got if "lost on the clean reboot" in x]
        print(f"BASE {CFG.stem} {g.__name__}: {len(got)} finding(s), "
              f"{len(lost)} 'lost on the clean reboot'")
        for x in got[:4]:
            print(f"BASE   e.g. {x[:300]}")


def plants():
    for label, (pairs, words) in t.READ_FAULT_MUTATIONS.items():
        text = HEAD_FW
        ok = True
        for old, new in pairs:
            if text.count(old) != 1:
                ok = False
                break
            text = text.replace(old, new)
        if not ok:
            print(f"PLANT {CFG.stem} {label}: DID NOT MATCH")
            continue
        b = bench_for(text, f"plant_{label}")
        got = []
        for g in t.READ_FAULT_GRADES:
            got += g(b)
        named = [x for x in got if words in x]
        print(f"PLANT {CFG.stem} {label}: {'CAUGHT' if named else 'NOT CAUGHT'} "
              f"named={len(named)} total={len(got)} words={words!r}")
        if named:
            print(f"PLANT   first: {named[0][:300]}")


def scenarios():
    # instrument a COPY: print the bytes each slot read delivered
    probe_fw = HEAD_FW.replace(
        "\t\trd.digest = nvm_crc32(NVM_STG, rd.bytes);\n\treturn rd;\n}",
        "\t\trd.digest = nvm_crc32(NVM_STG, rd.bytes);\n"
        "\tprintf(\"PROBE slot read bytes=%lu vd=%u\\n\", (unsigned long)rd.bytes, rd.vd);\n"
        "\treturn rd;\n}")
    assert probe_fw != HEAD_FW
    b = bench_for(probe_fw, "scen")
    w = b.work
    blank = b"\xff" * t.SLOT
    n1, n2 = new_rec(b, 0x40), new_rec(b, 0x21)
    off = rec_off(b)
    rid = max(b.frames)
    saved = b.frames[rid][REC_HDR:]

    def boot(a, bb, *extra, tag):
        out, s, bl = t.run(b, "--slot-a", t.slot_file(b, f"{tag}_a.bin", a),
                           "--slot-b", t.slot_file(b, f"{tag}_b.bin", bb), *extra,
                           "--boot", "--change", f"{off}:{n1.hex()}", "--idle-ms", "1500",
                           "--dump-slot-a", str(w / f"{tag}_a1"), "--dump-slot-b", str(w / f"{tag}_b1"))
        out2, s2, bl2 = t.run(b, "--slot-a", str(w / f"{tag}_a1"), "--slot-b", str(w / f"{tag}_b1"),
                              "--boot", "--dump-ddr", str(w / f"{tag}_ddr"))
        return out, s, bl, out2, s2, bl2, payload(b, w / f"{tag}_ddr")

    def line(bl):
        return bl.group(0) if bl else None

    # S1: both valid; the newer slot faulted for the whole boot
    for newer in "ab":
        for seq in (2, 0x80000000, 0xFFFFFFFF, 0):
            older_seq = (seq - 1) & 0xFFFFFFFF
            g_new = b.assemble(b.frames, seq)
            # the older container carries a different value in the record
            older_frames = dict(b.frames)
            older_frames[rid] = new_rec(b, 0x70)
            g_old = b.assemble(older_frames, older_seq)
            a, bb = (g_new, g_old) if newer == "a" else (g_old, g_new)
            out, s, bl, out2, s2, bl2, got = boot(a, bb, "--read-fault", f"{newer}:0:0:64",
                                                  tag=f"s1{newer}{seq:x}")
            held = t.HELD_LINE in out
            print(f"S1 {CFG.stem} newer={newer} seq={seq:#x} older={older_seq:#x} faulted=newer: "
                  f"held={held} erases={s.get('erases')} programs={s.get('programs')} acks={s.get('acks')} "
                  f"backed={s.get('backed')} hb={s.get('hb')} boot_reads={s.get('boot_reads')} | "
                  f"reboot offered={bl2 and bl2.group(5)} restored_newer={got == saved} | {line(bl)}")
    # S2: both valid; only the re-stage of the picked (newer) slot is faulted,
    # so the pick falls back to the older valid slot
    for newer in "ab":
        seq = 0x5A5A5
        g_new = b.assemble(b.frames, seq)
        older_frames = dict(b.frames)
        older_frames[rid] = new_rec(b, 0x70)
        g_old = b.assemble(older_frames, seq - 1)
        a, bb = (g_new, g_old) if newer == "a" else (g_old, g_new)
        # clean boot first, to learn the read indices
        out, s, bl = t.run(b, "--slot-a", t.slot_file(b, "s2c_a.bin", a),
                           "--slot-b", t.slot_file(b, "s2c_b.bin", bb), "--boot")
        print(f"S2 {CFG.stem} newer={newer} clean boot_reads={s.get('boot_reads')} | {line(bl)}")
        # reads: 0 AEM, 1 judge A, 2 judge B, 3.. re-stage of the pick
        out, s, bl, out2, s2, bl2, got = boot(a, bb, "--read-fault", f"{newer}:0:3:3",
                                              tag=f"s2{newer}")
        loaded = None
        print(f"S2 {CFG.stem} newer={newer} restage faulted x3: held={t.HELD_LINE in out} "
              f"faulty_reads={s.get('faulty_reads')} erases={s.get('erases')} acks={s.get('acks')} "
              f"backed={s.get('backed')} | {line(bl)} | reboot offered={bl2 and bl2.group(5)} "
              f"restored_newer={got == saved}")
    # S3: the boot line's read-fault counter after one faulty read that heals
    g = b.assemble(b.frames, 0x5A5A5)
    for skip, label in ((1, "first judgement read of A"), (2, "second read of A")):
        out, s, bl = t.run(b, "--slot-a", t.slot_file(b, "s3_a.bin", g),
                           "--slot-b", t.slot_file(b, "s3_b.bin", blank),
                           "--read-fault", f"a:0:{skip}:1", "--boot")
        import re
        m = re.search(r"read faults=(\d+) unread=(\d+)", out)
        print(f"S3 {CFG.stem} one faulty read at index {skip} ({label}): faulty_reads={s.get('faulty_reads')} "
              f"boot line read faults={m and m.group(1)} unread={m and m.group(2)}")
    # S4: a fault on the length word (byte 17) of a valid slot, three reads
    img_len = b.img_len
    hi = (img_len >> 8) & 0xFF
    xor = hi ^ 0xFF   # the first faulty read makes byte 17 0xFF
    out, s, bl = t.run(b, "--slot-a", t.slot_file(b, "s4_a.bin", g),
                       "--slot-b", t.slot_file(b, "s4_b.bin", blank),
                       "--read-fault", f"a:17:1:3:{xor}", "--boot")
    reads = [ln for ln in out.splitlines() if ln.startswith("PROBE slot read")]
    total = sum(int(ln.split("bytes=")[1].split()[0]) for ln in reads)
    print(f"S4 {CFG.stem} img_len={img_len} length-word fault x3 on A: held={t.HELD_LINE in out} "
          f"refusal reads={reads} refusal bytes={total} ({total / img_len:.2f} containers) | {line(bl)}")


#: reviewer plants beyond the suite's four: label -> (old, new)
EXTRA_PLANTS = {
    # a re-stage that never reads back no longer marks its slot UNREAD, so
    # the writer goes live after offering the other slot (or the blank image)
    "restage_fail_not_unread": (
        "\t\tnvm_unread |= (chosen == NVM_SLOT_A) ? 1u : 2u;\n\t\tif (chosen == NVM_SLOT_A) {\n",
        "\t\tif (chosen == NVM_SLOT_A) {\n"),
}


def extra_plants():
    """Grade checks 13/14 on each reviewer plant, then show what the plant
    does to the saved state in a restage-only fault window (A valid, B blank:
    reads 0 AEM, 1 judge A, 2-3 judge B, 4-6 re-stage A)."""
    for label, (old, new) in EXTRA_PLANTS.items():
        assert HEAD_FW.count(old) == 1, label
        b = bench_for(HEAD_FW.replace(old, new), f"xplant_{label}")
        got = []
        for g in t.READ_FAULT_GRADES:
            got += g(b)
        print(f"XPLANT {CFG.stem} {label}: checks 13/14 give {len(got)} finding(s)")
        for x in got[:3]:
            print(f"XPLANT   {x[:300]}")
        w = b.work
        golden = b.assemble(b.frames, 0x5A5A5)
        n1 = new_rec(b, 0x40)
        out, s, bl = t.run(b, "--slot-a", t.slot_file(b, "x_a.bin", golden),
                           "--slot-b", t.slot_file(b, "x_b.bin", b"\xff" * t.SLOT),
                           "--read-fault", "a:0:4:3", "--boot",
                           "--change", f"{rec_off(b)}:{n1.hex()}", "--idle-ms", "1500",
                           "--dump-slot-a", str(w / "x_a1"), "--dump-slot-b", str(w / "x_b1"))
        t.run(b, "--slot-a", str(w / "x_a1"), "--slot-b", str(w / "x_b1"), "--boot",
              "--dump-ddr", str(w / "x_ddr"))
        vd, applied = klj2_decode((w / "x_ddr").read_bytes()[:b.img_len], b.donor, b.ident, b.expect)
        _, golden_applied = klj2_decode(golden, b.donor, b.ident, b.expect)
        rid = max(b.frames)
        kept = sum(1 for k, v in golden_applied.items()
                   if k != ("NAME", rid - 0x80) and applied.get(k) == v)
        others = sum(1 for k in golden_applied if k != ("NAME", rid - 0x80))
        print(f"XPLANT {CFG.stem} {label}: restage-only fault a:0:4:3 -> held={t.HELD_LINE in out} "
              f"erases={s.get('erases')} acks={s.get('acks')} | {bl and bl.group(0)} | after reboot: "
              f"changed record survived={applied.get(('NAME', rid - 0x80)) == n1[REC_HDR:]}, "
              f"other saved records kept {kept}/{others}")


{"base_repro": base_repro, "plants": plants, "scenarios": scenarios,
 "extra_plants": extra_plants}[PROBE]()
