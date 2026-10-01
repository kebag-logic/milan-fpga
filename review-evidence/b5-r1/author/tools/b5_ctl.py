#!/usr/bin/env python3
"""Bench AECP/ACMP operations for lane B5 (controller host, under sudo; the caller
holds the bench lock).

Reuses the read-only probe (avdecc_ro.py, staged beside this file) for the socket,
AECP and ACMP framing. Adds only what the lane's method needs:

  * GET_STREAM_FORMAT on both entities, and SET_STREAM_FORMAT on a STREAM_INPUT
    only (the binding rule: the listener adapts to the talker; a talker's format
    is never set, and the tool refuses it);
  * GET_AUDIO_MAP, and ADD/REMOVE_AUDIO_MAPPINGS on the DUT only (the first-light
    method's identity mappings);
  * ACMP CONNECT_RX / DISCONNECT_RX / GET_RX_STATE / GET_TX_STATE.

AEM command 0x002A is REBOOT and is never sent.

modes (one JSON object per line on stdout):
  census <iface> <peer_eid> <peer_mac>      read-only state of both entities
  descs  <iface> <peer_eid> <peer_mac>      read-only descriptor survey of the peer
  agent  <iface> <peer_eid> <peer_mac>      JSON command loop on stdin (see AGENT)

Every AEM and ACMP exchange carries the host's send and receive times (time.time()).
"""
import json
import struct
import sys
import time

import avdecc_ro as ro

ro.READ_ONLY_AEM.update({0x0008: "SET_STREAM_FORMAT", 0x002B: "GET_AUDIO_MAP",
                         0x002C: "ADD_AUDIO_MAPPINGS", 0x002D: "REMOVE_AUDIO_MAPPINGS"})
assert 0x002A not in ro.READ_ONLY_AEM
DUT = (bytes.fromhex("020000fffe000001"), bytes.fromhex("020000000001"))
Z = bytes(8)
STREAM_INPUT, STREAM_OUTPUT = 0x0005, 0x0006
ACMP = {"bind": 6, "unbind": 8, "rx": 10, "tx": 4}


class Ctl:
    def __init__(self, iface, peer_eid, peer_mac):
        self.a = ro.Aecp(iface)
        self.ent = {"dut": DUT, "peer": (bytes.fromhex(peer_eid), bytes.fromhex(peer_mac.replace(":", "")))}

    def aem(self, who, cmd, payload, what, timeout=1.0):
        target, mac = self.ent[who]
        t0 = time.time()
        r = self.a.aem(target, mac, cmd, payload, timeout=timeout)
        r.update(role=who, what=what, t_tx=round(t0, 6), t_rx=round(time.time(), 6))
        ro.emit(r)
        return r

    def acmp(self, kind, talker, tuid, listener, luid, what, timeout=1.0):
        t0 = time.time()
        r = self.a.acmp(ACMP[kind], talker, tuid, listener, luid, timeout=timeout)
        r.update(what=what, t_tx=round(t0, 6), t_rx=round(time.time(), 6))
        ro.emit(r)
        return r

    def eid(self, who):
        return self.ent[who][0]

    def rx_state(self, who, i):
        return self.acmp("rx", Z, 0, self.eid(who), i, f"rx-state-{who}-{i}")

    def tx_state(self, who, i):
        return self.acmp("tx", self.eid(who), i, Z, 0, f"tx-state-{who}-{i}")

    def get_fmt(self, who, dtype, idx):
        r = self.aem(who, 0x0009, struct.pack(">HH", dtype, idx), f"format-{who}-{dtype}-{idx}")
        if r.get("status") == "SUCCESS":
            r["format"] = r["payload"][8:24]
        return r

    def set_fmt(self, who, idx, fmt):
        # Listener only: the descriptor type is fixed to STREAM_INPUT.
        r = self.aem(who, 0x0008, struct.pack(">HH", STREAM_INPUT, idx) + bytes.fromhex(fmt),
                     f"set-format-{who}-input-{idx}")
        if r.get("status") == "SUCCESS":
            r["format"] = r["payload"][8:24]
        return r

    def getmap(self, who, dtype, didx, mapi=0):
        return self.aem(who, 0x002B, struct.pack(">4H", dtype, didx, mapi, 0), f"map-{who}-{dtype:#06x}-{didx}-{mapi}")

    def dut_map(self, op, dtype, didx, n):
        rows = b"".join(struct.pack(">4H", 0, c, c, 0) for c in range(n))
        cmd = 0x002C if op == "add" else 0x002D
        self.aem("dut", cmd, struct.pack(">4H", dtype, didx, n, 0) + rows, f"map-{op}")
        return self.getmap("dut", dtype, didx)


def census(c):
    for i in range(2):
        c.rx_state("dut", i)
    for i in range(2):
        c.tx_state("dut", i)
    for cmd, payload, what in [(0x17, "00240000", "clock"), (0x07, "00000000", "config"),
                               (0x15, "00020000", "sample-rate"), (0x27, "00090000", "avb")]:
        c.aem("dut", cmd, bytes.fromhex(payload), what)
    for kind in (STREAM_INPUT, STREAM_OUTPUT):
        for i in range(2):
            c.get_fmt("dut", kind, i)
    c.getmap("dut", 0x000E, 0)
    c.getmap("dut", 0x000F, 0)
    for i in range(10):
        c.rx_state("peer", i)
    for i in range(4):
        c.tx_state("peer", i)
    for cmd, payload, what in [(0x17, "00240000", "clock"), (0x07, "00000000", "config"),
                               (0x15, "00020000", "sample-rate")]:
        c.aem("peer", cmd, bytes.fromhex(payload), what)
    for i in range(10):
        c.get_fmt("peer", STREAM_INPUT, i)
    for i in range(4):
        c.get_fmt("peer", STREAM_OUTPUT, i)


def read_desc(c, who, cfg, dtype, idx):
    return c.aem(who, 0x0004, struct.pack(">4H", cfg, 0, dtype, idx), f"desc-{who}-{cfg}-{dtype:#06x}-{idx}")


def descs(c):
    ent = read_desc(c, "peer", 0, 0x0000, 0)
    cur = 0
    if ent.get("status") == "SUCCESS":
        b = bytes.fromhex(ent["payload"])[4:]
        cur = struct.unpack(">H", b[310:312])[0] if len(b) >= 312 else 0
    cfgd = read_desc(c, "peer", cur, 0x0001, cur)
    counts = {}
    if cfgd.get("status") == "SUCCESS":
        b = bytes.fromhex(cfgd["payload"])[4:]
        n = struct.unpack(">H", b[70:72])[0]
        off = struct.unpack(">H", b[72:74])[0]
        for k in range(n):
            t, cnt = struct.unpack(">HH", b[off + 4 * k: off + 4 * k + 4])
            counts[t] = cnt
    ro.emit(dict(type="counts", configuration=cur, counts={f"{k:#06x}": v for k, v in counts.items()}))
    # STREAM_INPUT, STREAM_OUTPUT, AUDIO_UNIT, STREAM_PORT_INPUT/OUTPUT, AUDIO_CLUSTER,
    # AUDIO_MAP, CLOCK_SOURCE, CLOCK_DOMAIN, AVB_INTERFACE, CONTROL (bounded per type)
    for t in (0x0005, 0x0006, 0x0002, 0x000E, 0x000F, 0x0010, 0x0014, 0x0024, 0x000A, 0x0009, 0x001A):
        for i in range(min(counts.get(t, 0), 64)):
            read_desc(c, "peer", cur, t, i)
    # The audio unit's children are not in the configuration's counts: walk them from
    # AUDIO_UNIT 0 (stream ports, then each port's clusters and maps), bounded.
    au = read_desc(c, "peer", cur, 0x0002, 0)
    if au.get("status") == "SUCCESS":
        b = bytes.fromhex(au["payload"])[4:]
        nin, bin_, nout, bout = struct.unpack(">4H", b[72:80])
        nein, bein, neout, beout = struct.unpack(">4H", b[80:88])
        ro.emit(dict(type="audio-unit", stream_in_ports=[nin, bin_], stream_out_ports=[nout, bout],
                     ext_in_ports=[nein, bein], ext_out_ports=[neout, beout]))
        for t, n, base in ((0x000E, nin, bin_), (0x000F, nout, bout), (0x0011, nein, bein), (0x0012, neout, beout)):
            for i in range(base, base + min(n, 16)):
                p = read_desc(c, "peer", cur, t, i)
                if t in (0x000E, 0x000F) and p.get("status") == "SUCCESS":
                    pb = bytes.fromhex(p["payload"])[4:]
                    ncl, bcl, nmp, bmp = struct.unpack(">4H", pb[12:20])
                    for k in range(bcl, bcl + min(ncl, 32)):
                        read_desc(c, "peer", cur, 0x0010, k)
                    for k in range(bmp, bmp + min(nmp, 32)):
                        read_desc(c, "peer", cur, 0x0014, k)
                    c.getmap("peer", t, i)


AGENT = """agent commands, one JSON object per line:
  {"op":"sync"}                                   reply with this host's time
  {"op":"fmt","who":"dut|peer","dir":"in|out","idx":i}
  {"op":"setfmt","who":"dut|peer","idx":i,"fmt":"<16 hex>"}   STREAM_INPUT only
  {"op":"bind|unbind","t":"<eid>","tu":u,"l":"<eid>","lu":u}  then GET_RX_STATE
  {"op":"rx|tx","who":"dut|peer","idx":i}
  {"op":"map","act":"add|remove|get","dtype":d,"didx":i,"n":n}  DUT only
  {"op":"counters","who":"dut|peer","dtype":d,"idx":i}
  {"op":"quit"}"""


def agent(c):
    ro.emit(dict(type="agent-ready"))
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        q = json.loads(line)
        op = q["op"]
        if op == "sync":
            ro.emit(dict(type="sync", n=q.get("n"), rt=time.time()))
            continue
        ro.emit(dict(type="req", req=q))
        if op == "fmt":
            c.get_fmt(q["who"], STREAM_INPUT if q["dir"] == "in" else STREAM_OUTPUT, int(q["idx"]))
        elif op == "setfmt":
            c.set_fmt(q["who"], int(q["idx"]), q["fmt"])
        elif op in ("bind", "unbind"):
            t, l = bytes.fromhex(q["t"]), bytes.fromhex(q["l"])
            c.acmp(op, t, int(q["tu"]), l, int(q["lu"]), op, timeout=4.0)
            c.acmp("rx", Z, 0, l, int(q["lu"]), "rx-state-after")
        elif op == "rx":
            c.rx_state(q["who"], int(q["idx"]))
        elif op == "tx":
            c.tx_state(q["who"], int(q["idx"]))
        elif op == "map":
            if q["act"] == "get":
                c.getmap("dut", int(q["dtype"]), int(q["didx"]))
            else:
                c.dut_map(q["act"], int(q["dtype"]), int(q["didx"]), int(q["n"]))
        elif op == "counters":
            c.aem(q["who"], 0x0029, struct.pack(">HH", int(q["dtype"]), int(q["idx"])),
                  f"counters-{q['who']}-{q['dtype']}-{q['idx']}")
        elif op == "quit":
            break
        else:
            ro.emit(dict(type="error", error=f"unknown op {op}"))
        ro.emit(dict(type="done", op=op))
    ro.emit(dict(type="agent-exit"))


def main():
    mode, iface, peid, pmac = sys.argv[1:5]
    c = Ctl(iface, peid, pmac)
    ro.emit(dict(type="start", mode=mode, argv=sys.argv[1:]))
    try:
        if mode == "census":
            census(c)
        elif mode == "descs":
            descs(c)
        elif mode == "agent":
            agent(c)
        else:
            raise SystemExit(f"unknown mode {mode}")
    finally:
        c.a.sock.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
