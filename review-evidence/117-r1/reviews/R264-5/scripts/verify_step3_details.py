#!/usr/bin/env python3
"""Re-derive the Step 3 detail statements prior findings concerned, from the pinned raw files.

Usage: verify_step3_details.py <a202-packet-dir>

Reuses the timebase of verify_step3_cycles.py (own decoders). Per cycle:
  * dark window: last tap record after the off (either direction, and who
    sent it) and first record after the return;
  * holdover (CLKV_STAT bit 3) episodes after the off: consecutive sample
    count and first-set to first-clear span, and whether any sample while the
    grandmaster is absent has holdover set outside those episodes;
  * reaches asCapable: the DUT's completed Pdelay exchanges (DUT Pdelay_Req
    answered by Resp and Resp_Follow_Up) after the return, the second one's
    time, CLKV_STAT[16] rise time and PDELAY_NS at the rise;
  * LINKG_STAT 0x83 -> 0x03: delay after the last received (switch-sent)
    frame, and back to 0x83 relative to the first received frame;
and, over all tap captures, the interval between the bench switch's DHCP
DISCOVER frames (source MAC of the switch's gPTP frames).
"""
import os
import re
import struct
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verify_step3_cycles import offsets, tap  # noqa: E402

DUT = "020000fffe000001"


def console_full(path):
    samples, cur = [], None
    reads = []
    lines = open(path, errors="replace").read().split("\n")
    i = 0
    while i < len(lines):
        m = re.match(r"### (\S+)Z cmd='([^']*)'", lines[i])
        if m:
            t = datetime.fromisoformat(m.group(1)).replace(tzinfo=timezone.utc).timestamp()
            cmd = m.group(2)
            if cmd == "milan_status":
                cur = {"t": t}
                samples.append(cur)
            elif cmd.startswith("mem_read 0x90000774"):
                for j in range(i + 1, min(i + 5, len(lines))):
                    mm = re.match(r"0x90000774\s+(\S\S) (\S\S) (\S\S) (\S\S)", lines[j])
                    if mm:
                        reads.append((t, int("".join(reversed(mm.groups())), 16)))
                        break
            i += 1
            continue
        if cur is not None:
            for k, v in re.findall(r"(GPTP_GM|SYNC|ASCAPABLE|TU|CLKV_STAT|PDELAY_NS)=(\S+)", lines[i]):
                cur[k] = v
        i += 1
    return [s for s in samples if "CLKV_STAT" in s], reads


def main():
    pk = sys.argv[1]
    for c in range(1, 7):
        cdir = os.path.join(pk, f"bench/cycle{c}")
        offs = offsets(cdir)
        ps = open(os.path.join(cdir, "powerstrip.txt")).read()
        ps_host = [h for h in offs if h.endswith("pi")][0]
        srv = [h for h in offs if h.endswith("ubuntu-server")][0]
        t0 = float(re.search(r"T_OFF_CMD (\S+)", ps).group(1)) - offs[ps_host]
        smp, lg = console_full(os.path.join(cdir, "console.txt"))
        recs, _ = tap(os.path.join(cdir, f"tap-c{c}.pcap"))
        recs = [(t - offs[srv], p, et, pl) for t, p, et, pl in recs]
        before = [r for r in recs if t0 < r[0] < t0 + 10]
        after = [r for r in recs if r[0] > t0 + 10]
        last = before[-1]
        last_rx = max(r[0] for r in before if r[1] == 2)
        first_rx = min(r[0] for r in after if r[1] == 2)
        first_any = after[0][0]
        # holdover episodes after the off, until the DUT adopts the switch again
        hold = [(s["t"], int(s["CLKV_STAT"], 16) >> 3 & 1, s["GPTP_GM"]) for s in smp if s["t"] > t0]
        eps, cur = [], None
        for t, h, gm in hold:
            if h and cur is None:
                cur = [t, t, 1, gm]
            elif h:
                cur[1] = t
                cur[2] += 1
            elif cur is not None:
                eps.append((cur[0] - t0, t - cur[0], cur[2], cur[3]))
                cur = None
        gm_self_t = next(s["t"] for s in smp if s["t"] > t0 and s["GPTP_GM"] == DUT)
        gm_back_t = next(s["t"] for s in smp if s["t"] > gm_self_t and s["GPTP_GM"] != DUT)
        absent_hold = [t - t0 for t, h, _ in hold if gm_self_t <= t < gm_back_t and h]
        # the DUT's own completed Pdelay exchanges after the return
        reqs = [(t, pl) for t, p, et, pl in after if p == 3 and et == 0x88F7 and pl[0] & 0xF == 2]
        resp = {(pl[30:32], pl[44:54]): t for t, p, et, pl in after if p == 2 and et == 0x88F7 and pl[0] & 0xF == 3}
        fup = {(pl[30:32], pl[44:54]): t for t, p, et, pl in after if p == 2 and et == 0x88F7 and pl[0] & 0xF == 0xA}
        done = sorted(fup[(pl[30:32], pl[20:30])] for t, pl in reqs if (pl[30:32], pl[20:30]) in resp and (pl[30:32], pl[20:30]) in fup)
        rise = next(s for s in smp if s["t"] > t0 + 10 and int(s["CLKV_STAT"], 16) >> 16 & 1)
        prev = max(s["t"] for s in smp if s["t"] < rise["t"])
        lg_after = [(t, v) for t, v in lg if t > t0]
        drop = next(t for t, v in lg_after if v & 0x80 == 0)
        back = next(t for t, v in lg_after if t > drop and v & 0x80)
        back_prev = max(t for t, v in lg_after if t < back)
        print(f"cycle {c}: last record {last[0]-t0:.3f}s sent by {'DUT' if last[1]==3 else 'switch'}; first record after return {first_any-t0:.3f}s; dark {first_any-last[0]:.2f}s")
        print(f"   holdover episodes (start s, first-set->first-clear s, samples, GM at start): {[(round(a,2), round(b,2), n, g[-6:]) for a,b,n,g in eps]}")
        print(f"   holdover set while GM absent outside episodes: {[round(x,2) for x in absent_hold]}")
        print(f"   DUT Pdelay exchanges completed after return: first {done[0]-t0:.3f}s second {done[1]-t0:.3f}s; asCapable rise sample {rise['t']-t0:.3f}s (previous sample {prev-t0:.3f}s); rise - second {rise['t']-done[1]:.3f}s; second - first switch frame {done[1]-first_rx:.2f}s; PDELAY_NS at rise {rise.get('PDELAY_NS')}")
        print(f"   LINKG_STAT: first read with [7]=0 at {drop-t0:.2f}s, {drop-last_rx:.2f}s after last received frame; [7]=1 again at {back-t0:.2f}s (previous read {back_prev-t0:.2f}s), first received frame {first_rx-t0:.2f}s")
    # switch DHCP cadence
    import glob
    for path in sorted(glob.glob(os.path.join(pk, "bench/cycle*/tap-c*.pcap")))[:6]:
        recs, _ = tap(path)
        sw_mac = None
        for t, p, et, pl in recs:
            pass
        raw_recs = recs
        macs = {}
        for t, p, et, pl in raw_recs:
            if et == 0x0800 and len(pl) > 28 and pl[9] == 17 and struct.unpack(">H", pl[22:24])[0] == 67:
                macs.setdefault(p, []).append(t)
        for p, ts in macs.items():
            iv = [round(b - a, 2) for a, b in zip(ts, ts[1:])]
            print(f"{os.path.basename(path)}: DHCP to port 67 from tap port {p}: {len(ts)} frames, intervals {sorted(set(iv))[:6]}...")


if __name__ == "__main__":
    main()
