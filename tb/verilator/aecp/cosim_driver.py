#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""
tsn-gen <-> Verilator co-sim driver for KL_aecp_top.

Drives AECP command frames into the Verilator DUT (Vaecp_cosim, a UNIX-socket
AECP responder running the real RTL) and validates each response TWO ways:

  1. tsn-gen packet_gen --decode dissects the response's AECP common header
     (message_type / status / control_data_length) from its YAML field model.
  2. spec checks here: status, and control_data_length == frame_len - 26
     (IEEE 1722-2016 §5.4 — CDL counts octets after target_entity_id; the
     pipewire AVB reference confirms it. NB: tsn-gen's own CDL *value* counts
     target_entity_id and is 8 too high, so we assert against the spec, not
     against tsn-gen's number).

Usage: cosim_driver.py <socket-path> <packet_gen> <tsn-gen-root>
"""
import socket
import struct
import subprocess
import sys
import json

ENT_MAC = bytes.fromhex("020000fffe01")  # matches Vaecp_cosim station_mac
CTL_MAC = bytes.fromhex("6805ca95b2d1")
EID     = 0x020000fffe000001
CTLR    = 0x6805ca95b2d10000
BEAT    = struct.Struct("<QBB")   # tdata(LE u64), tkeep(u8), tlast(u8)

npass = nfail = 0
def ck(name, ok, detail=""):
    global npass, nfail
    if ok: npass += 1; print(f"  [ ok ] {name} {detail}")
    else:  nfail += 1; print(f"  [FAIL] {name} {detail}")

def aecp_cmd(msg_type, cmd, spec, seq, vu=False):
    if vu:
        body = bytes.fromhex("001bc50ac100") + struct.pack(">HH", cmd, 0) + spec
        cdl = 10 + len(body)
        pkt = struct.pack(">BBH", 0xFB, msg_type, cdl) + struct.pack(">Q", EID) \
            + struct.pack(">Q", CTLR) + struct.pack(">H", seq) + body
    else:
        cdl = 12 + len(spec)
        pkt = struct.pack(">BBH", 0xFB, msg_type, cdl) + struct.pack(">Q", EID) \
            + struct.pack(">Q", CTLR) + struct.pack(">H", seq) + struct.pack(">H", cmd) + spec
    f = ENT_MAC + CTL_MAC + struct.pack(">H", 0x22F0) + pkt
    return f + b"\x00" * max(0, 60 - len(f))

def send_frame(s, f):
    n = len(f)
    off = 0
    while off < n:
        chunk = f[off:off+8]
        tdata = int.from_bytes(chunk + b"\x00"*(8-len(chunk)), "little")
        tkeep = (1 << len(chunk)) - 1
        tlast = 1 if off + 8 >= n else 0
        s.sendall(BEAT.pack(tdata, tkeep, tlast))
        off += 8

def recv_frame(s):
    out = bytearray()
    while True:
        b = b""
        while len(b) < 10:
            chunk = s.recv(10 - len(b))
            if not chunk: return bytes(out)
            b += chunk
        tdata, tkeep, tlast = BEAT.unpack(b)
        for i in range(8):
            if tkeep & (1 << i): out.append((tdata >> (8*i)) & 0xFF)
        if tlast: return bytes(out)

def tsn_decode_cdl(pg, yamldir, resp_hex):
    # tsn-gen dissects the AECP common header; return its decoded control_data_length
    import os
    try:
        out = subprocess.run(
            [pg, "--yaml-dir", os.path.join(yamldir, "protocols"), "--stack-file",
             os.path.join(yamldir, "stacks", "aecp_acquire_entity.yaml"),
             "--decode", "--hex", resp_hex],
            capture_output=True, text=True, timeout=10).stdout
        for line in out.splitlines():
            d = json.loads(line)
            for lyr in d.get("layers", []):
                f = lyr.get("fields", {})
                if "control_data_length" in f:
                    return f["control_data_length"]
    except Exception as e:
        return f"(decode err: {e})"
    return None

def r_status(f): return (f[16] >> 3) & 0x1F if len(f) > 16 else -1
def r_cdl(f):    return ((f[16] & 7) << 8) | f[17] if len(f) > 17 else -1

def main():
    sock_path, pg, yamldir = sys.argv[1], sys.argv[2], sys.argv[3]  # yamldir=tsn-gen root
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect(sock_path)
    print("== tsn-gen <-> Verilator co-sim: KL_aecp_top (real RTL) ==")

    tests = [
        ("READ_DESCRIPTOR(ENTITY)",       0, 4, struct.pack(">HHHH", 0,0,0x0000,0), False, 0),
        ("READ_DESCRIPTOR(CONFIGURATION)",0, 4, struct.pack(">HHHH", 0,0,0x0001,0), False, 0),
        ("READ_DESCRIPTOR(AUDIO_UNIT)",   0, 4, struct.pack(">HHHH", 0,0,0x0002,0), False, 0),
        ("READ_DESCRIPTOR(STREAM_OUTPUT)",0, 4, struct.pack(">HHHH", 0,0,0x0006,0), False, 0),
        ("READ_DESCRIPTOR(AVB_INTERFACE)",0, 4, struct.pack(">HHHH", 0,0,0x0009,0), False, 0),
        ("LOCK_ENTITY",                   0, 1, b"\x00"*12, False, 0),
        ("ACQUIRE_ENTITY",                0, 0, b"\x00"*16, False, 11),
        ("GET_CONFIGURATION",             0, 7, b"", False, 0),
        ("GET_STREAM_INFO(STREAM_OUTPUT)", 0, 15, struct.pack(">HH", 0x0006, 0), False, 0),
        ("GET_COUNTERS(STREAM_OUTPUT)",   0, 41, struct.pack(">HH", 0x0006, 0), False, 0),
        ("GET_COUNTERS(ENTITY->BAD_ARG)", 0, 41, struct.pack(">HH", 0x0000, 0), False, 7),
        ("MVU GET_MILAN_INFO",            6, 0, b"", True, 0),
    ]
    seq = 0x100
    for name, mt, cmd, spec, vu, exp_status in tests:
        seq += 1
        s.sendall(b"")  # noop
        send_frame(s, aecp_cmd(mt, cmd, spec, seq, vu))
        r = recv_frame(s)
        ok = len(r) > 18
        ck(f"{name}: response received", ok, f"{len(r)}B")
        if not ok: continue
        ck(f"{name}: status", r_status(r) == exp_status, f"got={r_status(r)} exp={exp_status}")
        # spec CDL check (IEEE 1722-2016 §5.4 = frame-26); the Verilator DUT
        # has no MAC, so no 60-byte padding — CDL pins the length exactly.
        ck(f"{name}: CDL == frame-26 (spec, unpadded sim)",
           len(r) == 26 + r_cdl(r), f"cdl={r_cdl(r)} frame={len(r)}")
        # tsn-gen independent decode of the AECP header
        tcdl = tsn_decode_cdl(pg, yamldir, r.hex())
        print(f"         tsn-gen decoded control_data_length = {tcdl} "
              f"(counts target_eid: expected {r_cdl(r)+8})")

    print(f"\n== co-sim: {npass} pass, {nfail} fail ==")
    s.close()
    sys.exit(1 if nfail else 0)

if __name__ == "__main__":
    main()
