#!/usr/bin/env python3
"""Read-only GET_COUNTERS poller for the controller host (issue 529, A231).

Every <period_s> seconds for <seconds> seconds, sends GET_COUNTERS (0x0029)
for each <eid>=<mac>:<type>:<index> target and prints one JSON line per answer,
with the counters_valid mask and every valid quadlet decoded by name. It uses
avdecc_ro.Aecp (the #117 A200 reader, read-only allowlist) unchanged, so it
never registers for notifications and never changes entity state.

Its sequence ids start at 0x1000 so they cannot collide with a concurrently
running crf_bind_window.py, whose ids start at 0x4000 or above; avdecc_ro
matches responses on target, controller id, sequence id and message type.

usage: a231_counters_poll.py <iface> <seconds> <period_s> <eid>=<mac>:<type>:<index> [...]
  <type> is a descriptor type number (5 STREAM_INPUT, 6 STREAM_OUTPUT,
  9 AVB_INTERFACE, 0x24 CLOCK_DOMAIN, 0 ENTITY).
"""
import struct
import sys
import time

sys.path.insert(0, "/tmp/a231")
import avdecc_ro as ro  # noqa: E402

NAMES = {
    # IEEE 1722.1-2021 Table 7-157 (Milan keeps this layout for Stream Inputs)
    0x0005: ["MEDIA_LOCKED", "MEDIA_UNLOCKED", "STREAM_INTERRUPTED", "SEQ_NUM_MISMATCH",
             "MEDIA_RESET", "TIMESTAMP_UNCERTAIN", "TIMESTAMP_VALID", "TIMESTAMP_NOT_VALID",
             "UNSUPPORTED_FORMAT", "LATE_TIMESTAMP", "EARLY_TIMESTAMP", "FRAMES_RX"],
    # Milan v1.2 Table 5.17 (compact Stream Output layout)
    0x0006: ["STREAM_START", "STREAM_STOP", "MEDIA_RESET", "TIMESTAMP_UNCERTAIN", "FRAMES_TX"],
    # IEEE 1722.1-2021 AVB_INTERFACE counters
    0x0009: ["LINK_UP", "LINK_DOWN", "FRAMES_TX", "FRAMES_RX", "RX_CRC_ERROR", "GPTP_GM_CHANGED"],
    # IEEE 1722.1-2021 CLOCK_DOMAIN counters
    0x0024: ["LOCKED", "UNLOCKED"],
}


def decode_counters(payload_hex):
    b = bytes.fromhex(payload_hex)
    if len(b) < 8:
        return {}
    dtype, dindex, valid = struct.unpack(">HHI", b[:8])
    block = b[8:]
    names = NAMES.get(dtype, [])
    vals = {}
    nonzero_unclaimed = {}
    for bit in range(32):
        off = 4 * bit
        if off + 4 > len(block):
            break
        v = struct.unpack(">I", block[off:off + 4])[0]
        name = names[bit] if bit < len(names) else f"q{bit}"
        if valid & (1 << bit):
            vals[name] = v
        elif v:
            nonzero_unclaimed[name] = v
    return dict(descriptor_type=dtype, descriptor_index=dindex, counters_valid=f"{valid:#010x}",
                block_octets=len(block), counters=vals, nonzero_unclaimed=nonzero_unclaimed)


def main():
    iface, secs, period = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
    targets = []
    for spec in sys.argv[4:]:
        eid, rest = spec.split("=")
        mac, dtype, dindex = rest.rsplit(":", 2)
        targets.append((bytes.fromhex(eid), bytes.fromhex(mac.replace(":", "")),
                        int(dtype, 0), int(dindex, 0)))
    a = ro.Aecp(iface)
    a.seq = 0x1000
    ro.emit(dict(type="start", argv=sys.argv[1:], controller_eid=a.ceid.hex()))
    end = time.monotonic() + secs
    nxt = time.monotonic()
    rnd = 0
    while time.monotonic() < end:
        for eid, mac, dtype, dindex in targets:
            r = a.aem(eid, mac, 0x0029, struct.pack(">HH", dtype, dindex))
            r.update(type="counters", round=rnd, target=eid.hex(), req_type=dtype, req_index=dindex)
            if r.get("status") == "SUCCESS":
                r["decoded"] = decode_counters(r["payload"])
            ro.emit(r)
        rnd += 1
        nxt += period
        delay = nxt - time.monotonic()
        if delay > 0:
            time.sleep(min(delay, max(0.0, end - time.monotonic())))
    ro.emit(dict(type="done", rounds=rnd))
    return 0


if __name__ == "__main__":
    sys.exit(main())
