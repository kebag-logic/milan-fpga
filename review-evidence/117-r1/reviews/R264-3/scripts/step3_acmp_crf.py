#!/usr/bin/env python3
"""Cycles 4-6: ACMP CONNECT_TX commands reaching the DUT and CRF tu edges.

Usage: step3_acmp_crf.py ARCHIVE_ROOT
Reuses the timebase of step3_recheck.py (same directory).
"""
import os, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import step3_recheck as s3


def avtp(fr):
    et = struct.unpack(">H", fr[12:14])[0]
    p = fr[14:]
    if et == 0x8100:
        et = struct.unpack(">H", fr[16:18])[0]
        p = fr[18:]
    if et != 0x22F0 or len(p) < 2:
        return None
    return p


root = sys.argv[1]
for c in (4, 5, 6):
    cdir = os.path.join(root, "bench-a202", "bench", f"cycle{c}")
    offs = s3.offsets(cdir)
    t0, _ = s3.t_off(cdir, offs)
    recs, _ = s3.tap(os.path.join(cdir, f"tap-c{c}.pcap"))
    srv = s3.host(offs, "ubuntu-server")
    ctx, crf = [], []
    for r in recs:
        r["t"] = r["srv"] - srv - t0
        p = avtp(r["fr"])
        if p is None:
            continue
        if p[0] == 0xFC and r["port"] == 2 and (p[1] & 0x0F) == 0:
            ctx.append(r["t"])
        if p[0] == 0x04 and r["port"] == 3:
            crf.append((r["t"], p[1] & 0x01))
    loss_ctx = [t for t in ctx if 0 < t < 40.4]
    after = [t for t in ctx if t > 30]
    tu1 = [t for t, tu in crf if tu == 1]
    pre_end = max(t for t, _ in crf if t < 10)
    post = [(t, tu) for t, tu in crf if t > 30]
    print(f"CYCLE {c} connect_tx_total={len(ctx)} connect_tx_between_0_and_40.4s={len(loss_ctx)} "
          f"first_connect_tx_after_return={after[0]:.2f} first_crf_after_return={post[0][0]:.2f} "
          f"post_return_tu1={sum(tu for _, tu in post)} first_tu1={tu1[0]:.2f} tu1_count_at_loss={len([t for t in tu1 if t < 10])} "
          f"emission_end={pre_end:.2f}")
