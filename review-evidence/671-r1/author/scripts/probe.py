"""Scratch probe: the #671 scenario on a given firmware text (not part of the tree)."""
import sys, subprocess, tempfile
from pathlib import Path
ROOT = Path(sys.argv[1]); FW = Path(sys.argv[2]); CFG = ROOT / "configs" / sys.argv[3]
sys.path.insert(0, str(ROOT / "sw/firmware/nvm_hosttest"))
import test_nvm_firmware as t
from nvm_contract import KLJ2_HDR, REC_HDR
from nvm_klj2 import frame_record, klj2_decode
work = Path(tempfile.mkdtemp(prefix="probe.", dir="$VALIDATION_STORAGE/671-a592/tmp"))
b = t.make_bench(CFG, work, FW.read_text())
def scenario(valid, seq, fault):
    golden = b.assemble(b.frames, seq)
    blank = b"\xff" * t.SLOT
    rid = max(b.frames)
    new = frame_record(rid, bytes((0x40 + j) & 0xFF for j in range(len(b.frames[rid]) - REC_HDR)), b.donor.layout)
    off = KLJ2_HDR + b.offsets()[rid]
    a, bb = (golden, blank) if valid == "a" else (blank, golden)
    sa, sb = t.slot_file(b, "sa.bin", a), t.slot_file(b, "sb.bin", bb)
    out, s, boot = t.run(b, "--slot-a", sa, "--slot-b", sb, *fault, "--boot",
                         "--change", f"{off}:{new.hex()}", "--idle-ms", "1500",
                         "--dump-slot-a", str(work / "a1"), "--dump-slot-b", str(work / "b1"))
    out2, s2, boot2 = t.run(b, "--slot-a", str(work / "a1"), "--slot-b", str(work / "b1"), "--boot",
                            "--dump-ddr", str(work / "ddr"))
    vd, applied = klj2_decode((work / "ddr").read_bytes()[:b.img_len], b.donor, b.ident, b.expect)
    survived = applied.get(("NAME", rid - 0x80)) == new[REC_HDR:]
    held = "HELD" in out
    print(f"valid={valid} seq={seq:#x} fault={' '.join(fault)}: boot1 [{boot.group(0) if boot else None}] "
          f"erases={s.get('erases')} acks={s.get('acks')} boot_reads={s.get('boot_reads')} faulty={s.get('faulty_reads')} held={held} | "
          f"reboot [{boot2.group(0) if boot2 else None}] survived={survived}")
for valid in ("a", "b"):
    for seq in (1, 0x5A5A5, 0x80000000, 0xFFFFFFFF):
        sl = valid
        scenario(valid, seq, ["--read-fault", f"{sl}:0:0:64"])
        scenario(valid, seq, ["--read-fault", f"{sl}:0x0b:0:2:0x80"])
