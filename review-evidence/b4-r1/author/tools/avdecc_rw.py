#!/usr/bin/env python3
"""Bench AECP/ACMP operations for the #451 retry (controller host, under sudo).

Reuses the read-only probe (avdecc_ro.py, staged beside this file) for the
socket, AECP and ACMP framing. Adds only the commands this task needs:
GET_AUDIO_MAP, ADD_AUDIO_MAPPINGS, REMOVE_AUDIO_MAPPINGS, and ACMP
CONNECT_RX / DISCONNECT_RX / GET_RX_STATE / GET_TX_STATE. One JSON object per
line on stdout. The caller holds the bench lock.

  census <iface>
  bind   <iface> <talker_eid> <talker_uid> <listener_eid> <listener_uid>
  unbind <iface> <talker_eid> <talker_uid> <listener_eid> <listener_uid>
  map    <iface> add|remove <desc_type> <desc_index> <n>   identity mappings c -> cluster c
  getmap <iface> <desc_type> <desc_index>
"""
import os
import struct
import sys

import avdecc_ro as ro

# IEEE 1722.1 AEM command codes: 0x002A is REBOOT and is never sent.
ro.READ_ONLY_AEM.update({0x002B: "GET_AUDIO_MAP", 0x002C: "ADD_AUDIO_MAPPINGS",
                         0x002D: "REMOVE_AUDIO_MAPPINGS"})
assert 0x002A not in ro.READ_ONLY_AEM
DUT = (bytes.fromhex("020000fffe000001"), bytes.fromhex("020000000001"))
PEER = (bytes.fromhex(os.environ["PEER_EID"]), bytes.fromhex(os.environ["PEER_MAC"]))
Z = bytes(8)


def aem(a, who, cmd, payload, what):
    target, mac = DUT if who == "dut" else PEER
    r = a.aem(target, mac, cmd, payload, timeout=1.0)
    ro.emit(dict(role=who, what=what, response=r))
    return r


def rx_state(a, who, i):
    eid = (DUT if who == "dut" else PEER)[0]
    r = a.acmp(10, Z, 0, eid, i, timeout=1.0)
    ro.emit(dict(role=who, what=f"rx-state-{i}", response=r))
    return r


def tx_state(a, who, i):
    eid = (DUT if who == "dut" else PEER)[0]
    r = a.acmp(4, eid, i, Z, 0, timeout=1.0)
    ro.emit(dict(role=who, what=f"tx-state-{i}", response=r))
    return r


def getmap(a, dtype, didx):
    return aem(a, "dut", 0x002B, struct.pack(">4H", dtype, didx, 0, 0), f"map-{dtype:#06x}-{didx}")


def census(a):
    for i in range(2):
        rx_state(a, "dut", i)
    for i in range(2):
        tx_state(a, "dut", i)
    for cmd, payload, what in [(0x17, "00240000", "clock"), (0x07, "00000000", "config"),
                               (0x15, "00020000", "sample-rate"), (0x27, "00090000", "avb")]:
        aem(a, "dut", cmd, bytes.fromhex(payload), what)
    for kind in (5, 6):
        for i in range(2):
            aem(a, "dut", 0x0009, struct.pack(">HH", kind, i), f"format-{kind}-{i}")
    for kind, i in [(5, 0), (6, 0)]:
        aem(a, "dut", 0x0004, struct.pack(">4H", 0, 0, kind, i), f"desc-{kind}-{i}")
    getmap(a, 0x000E, 0)
    getmap(a, 0x000F, 0)
    for i in range(10):
        rx_state(a, "peer", i)
    for i in range(4):
        tx_state(a, "peer", i)
    for cmd, payload, what in [(0x17, "00240000", "clock"), (0x15, "00020000", "sample-rate")]:
        aem(a, "peer", cmd, bytes.fromhex(payload), what)


def main():
    mode, iface = sys.argv[1], sys.argv[2]
    a = ro.Aecp(iface)
    ro.emit(dict(type="start", mode=mode, argv=sys.argv[1:]))
    try:
        if mode == "census":
            census(a)
        elif mode in ("bind", "unbind"):
            t, tu, l, lu = (bytes.fromhex(sys.argv[3]), int(sys.argv[4]),
                            bytes.fromhex(sys.argv[5]), int(sys.argv[6]))
            r = a.acmp(6 if mode == "bind" else 8, t, tu, l, lu, timeout=4.0)
            ro.emit(dict(what=mode, response=r))
            r = a.acmp(10, Z, 0, l, lu, timeout=1.0)
            ro.emit(dict(what="rx-state-after", response=r))
        elif mode == "map":
            op, dtype, didx, n = sys.argv[3], int(sys.argv[4], 0), int(sys.argv[5]), int(sys.argv[6])
            rows = b"".join(struct.pack(">4H", 0, c, c, 0) for c in range(n))
            cmd = 0x002C if op == "add" else 0x002D
            aem(a, "dut", cmd, struct.pack(">4H", dtype, didx, n, 0) + rows, f"map-{op}")
            getmap(a, dtype, didx)
        elif mode == "getmap":
            getmap(a, int(sys.argv[3], 0), int(sys.argv[4]))
        else:
            raise SystemExit(f"unknown mode {mode}")
    finally:
        a.sock.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
