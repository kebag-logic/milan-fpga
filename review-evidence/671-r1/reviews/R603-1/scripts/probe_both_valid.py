#!/usr/bin/env python3
"""Reviewer probe for PR #715 (issue #671): read faults with BOTH slots valid.

The head's check 13 always pairs one valid slot with a blank one. This probe
uses the head's own harness and helpers with two valid containers, the newer
at sequence S and the older at S-1 (different payloads in one record), both
orientations, and walks a read fault (one header byte or one record-area
byte, a different XOR on every faulty read) over the boot reads of either
slot. Per case it grades:

  W  the faulty boot's window decodes VD_OK and holds the newer or the older
     payload (what is loaded is what was judged);
  O  a held boot whose newer slot was UNREAD offers the older, cleanly read
     slot rather than nothing (the documented "the other is offered");
  S  after a change, the debounce commit and a clean reboot, the change
     survives, or the faulty boot HELD and the clean reboot restores the
     newer saved payload.

It also runs the stated limit once: slot B valid and A blank, B read as all
0xFF twice, which the rule must take for a blank slot (the change is then
lost on the clean reboot -- the limit both READMEs state, demonstrated, not
graded as a defect).

usage: probe_both_valid.py REPO CONFIG WORK [--plant NAME ...] [--head] [--jobs N]
"""
import argparse
import concurrent.futures as cf
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from probe_read_fault import PLANTS  # noqa: E402

SEQS = (0x5A5A5, 0x0)  # S; the older is S-1 mod 2**32 (0 is the wrap case)
WINDOWS = tuple((skip, count) for skip in range(6) for count in (1, 2, 3)) + ((0, 64),)
BYTES = (0x0, 0x40)    # the magic byte, and a record-area byte


def grade(repo: Path, cfg: Path, work: Path, label: str, text: str, limit: bool):
    sys.path.insert(0, str(repo / "sw/firmware/nvm_hosttest"))
    import test_nvm_firmware as t
    work.mkdir(parents=True, exist_ok=True)
    try:
        bench = t.make_bench(cfg, work, text)
    except SystemExit as e:
        return label, [f"BUILD EXIT: {str(e)[:400]}"], {}
    f = []
    stats = {"cases": 0, "held": 0, "held_offered_older": 0}
    rid = max(bench.frames)
    off = t.KLJ2_HDR + bench.offsets()[rid]
    plen = len(bench.frames[rid]) - t.REC_HDR
    lay = bench.donor.layout
    new_pl = bench.frames[rid][t.REC_HDR:]
    old_pl = bytes((0x11 + j) & 0xFF for j in range(plen))
    chg = t.frame_record(rid, bytes((0x40 + j) & 0xFF for j in range(plen)), lay)
    key = ("NAME", rid - 0x80)
    old_frames = dict(bench.frames)
    old_frames[rid] = t.frame_record(rid, old_pl, lay)

    def window(path: Path):
        vd, applied = t.klj2_decode(path.read_bytes()[:bench.img_len], bench.donor,
                                    bench.ident, bench.expect)
        return vd, (applied.get(key) if vd == t.VD_OK else None)

    w = work
    for newer in "ab":
        for s in SEQS:
            nw = bench.assemble(bench.frames, s)
            od = bench.assemble(old_frames, (s - 1) & 0xFFFF_FFFF)
            a, b = (nw, od) if newer == "a" else (od, nw)
            fa = t.slot_file(bench, "bv_a.bin", a)
            fb = t.slot_file(bench, "bv_b.bin", b)
            for target in "ab":
                for byte in BYTES:
                    for skip, count in WINDOWS:
                        stats["cases"] += 1
                        flt = ("--read-fault", f"{target}:{byte}:{skip}:{count}:8")
                        name = (f"newer {newer.upper()} at {s:#x}, fault {flt[1]}")
                        out0, s0, boot0 = t.run(bench, "--slot-a", fa, "--slot-b", fb, *flt,
                                                "--boot", "--dump-ddr", str(w / "bv_d0.bin"))
                        vd0, got0 = window(w / "bv_d0.bin")
                        held0 = t.HELD_LINE in out0
                        if boot0 is not None and boot0.group(5) != "-":
                            if got0 not in (new_pl, old_pl):
                                f.append(f"W {name}: the faulty boot offered "
                                         f"{boot0.group(5)} but its window reads "
                                         f"{t.VERDICT_NAME[vd0] if isinstance(t.VERDICT_NAME, (list, tuple, dict)) else vd0}"
                                         f" / {got0 and got0[:4].hex()}")
                        if held0:
                            stats["held"] += 1
                            # the newer slot unread: was the older one offered?
                            vnew = boot0 and boot0.group(1 if newer == "a" else 3)
                            vold = boot0 and boot0.group(3 if newer == "a" else 1)
                            if vold == "VD_OK" and boot0.group(5) == "-":
                                f.append(f"O {name}: held with the older slot read "
                                         f"cleanly, yet nothing was offered: {boot0.group(0)}")
                            elif boot0 and boot0.group(5) != "-" and vnew != "VD_OK":
                                stats["held_offered_older"] += 1
                        out, s1, _ = t.run(bench, "--slot-a", fa, "--slot-b", fb, *flt, "--boot",
                                           "--change", f"{off}:{chg.hex()}", "--idle-ms", "1500",
                                           "--dump-slot-a", str(w / "bv_a1.bin"),
                                           "--dump-slot-b", str(w / "bv_b1.bin"))
                        held = t.HELD_LINE in out
                        if held and (s1.get("erases") or s1.get("programs") or s1.get("acks")
                                     or s1.get("backed") or s1.get("hb")):
                            f.append(f"S {name}: the held writer persisted or claimed: {s1}")
                        _o2, _s2, boot2 = t.run(bench, "--slot-a", str(w / "bv_a1.bin"),
                                                "--slot-b", str(w / "bv_b1.bin"), "--boot",
                                                "--dump-ddr", str(w / "bv_d2.bin"))
                        _vd2, got2 = window(w / "bv_d2.bin")
                        want = new_pl if held else chg[t.REC_HDR:]
                        if got2 != want:
                            f.append(f"S {name}: {'held' if held else 'committed'}; the clean "
                                     f"reboot restored {got2 and got2[:4].hex()}, want "
                                     f"{want[:4].hex()}")
    if limit:
        golden = bench.assemble(bench.frames, 0x5A5A5)
        blank = b"\xff" * t.SLOT
        fa = t.slot_file(bench, "lim_a.bin", blank)
        fb = t.slot_file(bench, "lim_b.bin", golden)
        # reads: 0 the AEM image, 1-2 judge A (blank), 3-4 judge B
        out, s1, boot1 = t.run(bench, "--slot-a", fa, "--slot-b", fb, "--read-ff", "b:3:2",
                               "--boot", "--change", f"{off}:{chg.hex()}", "--idle-ms", "1500",
                               "--dump-slot-a", str(w / "lim_a1.bin"),
                               "--dump-slot-b", str(w / "lim_b1.bin"))
        _o2, _s2, boot2 = t.run(bench, "--slot-a", str(w / "lim_a1.bin"),
                                "--slot-b", str(w / "lim_b1.bin"), "--boot",
                                "--dump-ddr", str(w / "lim_d2.bin"))
        _vd, got = window(w / "lim_d2.bin")
        stats["limit_faulty_boot"] = boot1 and boot1.group(0)
        stats["limit_held"] = t.HELD_LINE in out
        stats["limit_clean_reboot"] = boot2 and boot2.group(0)
        stats["limit_change_survived"] = got == chg[t.REC_HDR:]
    return label, f, stats


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("repo", type=Path)
    ap.add_argument("config", type=Path)
    ap.add_argument("work", type=Path)
    ap.add_argument("--plant", action="append")
    ap.add_argument("--head", action="store_true")
    ap.add_argument("--jobs", type=int, default=3)
    a = ap.parse_args()
    head = (a.repo / "sw/firmware/milan_baremetal/milan_baremetal.c").read_text()
    jobs = [("head", head, True)] if a.head else []
    for name in a.plant or []:
        text = head
        for old, new in PLANTS[name]:
            if text.count(old) != 1:
                print(f"PLANT {name}: not applied")
                return 2
            text = text.replace(old, new)
        jobs.append((name, text, False))
    with cf.ProcessPoolExecutor(max_workers=a.jobs) as ex:
        futs = [ex.submit(grade, a.repo, a.config, a.work / lab, lab, txt, lim)
                for lab, txt, lim in jobs]
        for fu in cf.as_completed(futs):
            lab, out, stats = fu.result()
            print(f"=== {lab}: {len(out)} finding(s); {stats}")
            for x in out:
                print(f"  {x}")
            sys.stdout.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())
