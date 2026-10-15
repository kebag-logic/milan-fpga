#!/usr/bin/env python3
"""Read-only AVDECC probe for the controller host (issue 117, A200).

Runs under sudo on the controller host. It joins the AVDECC multicast group
91:E0:F0:01:00:00 on the given interface for the life of the socket (the
membership ends when the process exits) and prints one JSON object per line.

Modes:
  discover <iface> <seconds>
      Send one ADP ENTITY_DISCOVER (entity_id 0) and collect ENTITY_AVAILABLE
      advertisements for <seconds>.
  aem <iface> <target_eid> <target_mac> <cmd> <payload_hex> [<cmd> <payload_hex> ...]
      Send each AEM command in turn and print the matched response. Only the
      read-only commands in READ_ONLY_AEM are accepted.
  acmp <iface> <get_rx_state|get_tx_state> <talker_eid> <talker_uid> <listener_eid> <listener_uid>
      Send one read-only ACMP state query (control_data_length 44).
  watch <iface> <seconds> <period_s> <eid>=<mac> [<eid>=<mac> ...]
      Poll GET_AVB_INFO (AVB_INTERFACE 0) and GET_AS_PATH (index 0) on every
      named entity every <period_s> seconds for <seconds>, and log every ADP
      advertisement seen meanwhile (so GM identity changes in ADP are timed).

AECP control_data_length is the number of octets after target_entity_id
(12 + command payload); ACMP control_data_length is 44.
"""
import json
import os
import select
import socket
import struct
import sys
import time

ETH_P_ALL = 0x0003
ETH_AVTP = 0x22F0
AVDECC_MC = bytes.fromhex("91e0f0010000")
SOL_PACKET = 263
PACKET_ADD_MEMBERSHIP = 1
PACKET_MR_MULTICAST = 0

READ_ONLY_AEM = {
    0x0004: "READ_DESCRIPTOR", 0x0007: "GET_CONFIGURATION", 0x0009: "GET_STREAM_FORMAT",
    0x000F: "GET_STREAM_INFO", 0x0011: "GET_NAME", 0x0015: "GET_SAMPLING_RATE",
    0x0017: "GET_CLOCK_SOURCE", 0x0019: "GET_CONTROL", 0x0027: "GET_AVB_INFO",
    0x0028: "GET_AS_PATH", 0x0029: "GET_COUNTERS",
}
AEM_STATUS = {0: "SUCCESS", 1: "NOT_IMPLEMENTED", 2: "NO_SUCH_DESCRIPTOR", 3: "ENTITY_LOCKED",
              4: "ENTITY_ACQUIRED", 5: "NOT_AUTHENTICATED", 6: "AUTHENTICATION_DISABLED",
              7: "BAD_ARGUMENTS", 8: "NO_RESOURCES", 9: "IN_PROGRESS", 10: "ENTITY_MISBEHAVING",
              11: "NOT_SUPPORTED", 12: "STREAM_IS_RUNNING"}
ACMP_READ_ONLY = {"get_tx_state": 4, "get_rx_state": 10}


def emit(obj):
    obj.setdefault("t", round(time.time(), 6))
    print(json.dumps(obj, separators=(",", ":")), flush=True)


def open_sock(iface):
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_ALL))
    s.bind((iface, ETH_P_ALL))
    ifindex = socket.if_nametoindex(iface)
    mreq = struct.pack("iHH8s", ifindex, PACKET_MR_MULTICAST, 6, AVDECC_MC + b"\x00\x00")
    s.setsockopt(SOL_PACKET, PACKET_ADD_MEMBERSHIP, mreq)
    return s


def iface_mac(iface):
    with open(f"/sys/class/net/{iface}/address") as f:
        return bytes.fromhex(f.read().strip().replace(":", ""))


def eth(dst, src, payload):
    return dst + src + struct.pack(">H", ETH_AVTP) + payload


def frames(sock, deadline):
    while True:
        rem = deadline - time.monotonic()
        if rem <= 0:
            return
        r, _, _ = select.select([sock], [], [], rem)
        if not r:
            return
        fr = sock.recv(65535)
        if len(fr) >= 18 and struct.unpack(">H", fr[12:14])[0] == ETH_AVTP:
            yield fr


def parse_adp(fr):
    p = fr[14:]
    if len(p) < 68 or p[0] != 0xFA or (p[1] & 0x0F) != 0:
        return None
    return dict(src=fr[6:12].hex(":"), entity_id=p[4:12].hex(), model_id=p[12:20].hex(),
                entity_caps=f"{struct.unpack('>I', p[20:24])[0]:#010x}",
                talker_sources=struct.unpack(">H", p[24:26])[0],
                listener_sinks=struct.unpack(">H", p[28:30])[0],
                controller_caps=f"{struct.unpack('>I', p[32:36])[0]:#010x}",
                available_index=struct.unpack(">I", p[36:40])[0], gptp_gm=p[40:48].hex(),
                gptp_domain=p[48], cfg=struct.unpack(">H", p[52:54])[0],
                interface_index=struct.unpack(">H", p[56:58])[0])


class Aecp:
    def __init__(self, iface):
        self.iface = iface
        self.sock = open_sock(iface)
        self.src = iface_mac(iface)
        self.ceid = self.src[:3] + b"\xff\xfe" + self.src[3:]
        self.seq = (int(time.time() * 1000) & 0x7FFF) | 0x4000

    def aem(self, target, mac, cmd, payload, timeout=1.5, on_other=None):
        if cmd not in READ_ONLY_AEM:
            raise SystemExit(f"refused: AEM command {cmd:#06x} is not in the read-only allowlist")
        self.seq = (self.seq + 1) & 0xFFFF
        seq = self.seq
        body = self.ceid + struct.pack(">HH", seq, cmd & 0x7FFF) + payload
        pdu = struct.pack(">BBH", 0xFB, 0x00, 12 + len(payload)) + target + body
        t_tx = time.time()
        self.sock.send(eth(mac, self.src, pdu))
        for fr in frames(self.sock, time.monotonic() + timeout):
            p = fr[14:]
            if (p[0] == 0xFB and (p[1] & 0x0F) == 1 and p[4:12] == target
                    and p[12:20] == self.ceid and struct.unpack(">H", p[20:22])[0] == seq):
                st = p[2] >> 3
                cdl = struct.unpack(">H", p[2:4])[0] & 0x7FF
                return dict(cmd=READ_ONLY_AEM[cmd], seq=seq, status=AEM_STATUS.get(st, st),
                            cdl=cdl, rtt_ms=round((time.time() - t_tx) * 1e3, 3),
                            payload=p[24:12 + cdl].hex())
            if on_other is not None:
                on_other(fr)
        return dict(cmd=READ_ONLY_AEM[cmd], seq=seq, status="TIMEOUT")

    def acmp(self, mt, talker, tuid, listener, luid, timeout=3.0):
        self.seq = (self.seq + 1) & 0xFFFF
        seq = self.seq
        body = (self.ceid + talker + listener + struct.pack(">HH", tuid, luid) + b"\x00" * 6
                + struct.pack(">HHHHH", 0, seq, 0, 0, 0))
        assert len(body) == 44
        pdu = struct.pack(">BBH", 0xFC, mt, 44) + b"\x00" * 8 + body
        self.sock.send(eth(AVDECC_MC, self.src, pdu))
        for fr in frames(self.sock, time.monotonic() + timeout):
            p = fr[14:]
            if p[0] == 0xFC and (p[1] & 0x0F) == mt + 1 and struct.unpack(">H", p[48:50])[0] == seq \
                    and p[12:20] == self.ceid:
                return dict(status=p[2] >> 3, stream_id=p[4:12].hex(), controller=p[12:20].hex(),
                            talker=p[20:28].hex(), listener=p[28:36].hex(),
                            talker_uid=struct.unpack(">H", p[36:38])[0],
                            listener_uid=struct.unpack(">H", p[38:40])[0], dmac=p[40:46].hex(),
                            conn_count=struct.unpack(">H", p[46:48])[0],
                            flags=f"{struct.unpack('>H', p[50:52])[0]:#06x}",
                            vlan=struct.unpack(">H", p[52:54])[0])
        return dict(status="TIMEOUT")


def decode_avb_info(pl):
    b = bytes.fromhex(pl)
    if len(b) < 16:
        return {}
    return dict(gm=b[4:12].hex(), pdelay_ns=struct.unpack(">I", b[12:16])[0], domain=b[16],
                flags=f"{b[17]:#04x}", as_capable=b[17] & 1, gptp_enabled=(b[17] >> 1) & 1,
                srp_enabled=(b[17] >> 2) & 1)


def decode_as_path(pl):
    b = bytes.fromhex(pl)
    if len(b) < 4:
        return {}
    n = struct.unpack(">H", b[2:4])[0]
    return dict(count=n, path=[b[4 + 8 * i:12 + 8 * i].hex() for i in range(n)])


def main():
    mode, iface = sys.argv[1], sys.argv[2]
    a = Aecp(iface)
    emit(dict(type="start", mode=mode, argv=sys.argv[1:], controller_eid=a.ceid.hex()))
    if mode == "discover":
        secs = float(sys.argv[3])
        disc = struct.pack(">BBH", 0xFA, 0x02, 56) + b"\x00" * 64
        a.sock.send(eth(AVDECC_MC, a.src, disc))
        seen = {}
        for fr in frames(a.sock, time.monotonic() + secs):
            e = parse_adp(fr)
            if e:
                seen.setdefault(e["entity_id"], 0)
                seen[e["entity_id"]] += 1
                emit(dict(type="adp", **e))
        emit(dict(type="done", entities=seen))
    elif mode == "aem":
        target = bytes.fromhex(sys.argv[3])
        mac = bytes.fromhex(sys.argv[4].replace(":", ""))
        rest = sys.argv[5:]
        for i in range(0, len(rest), 2):
            cmd = int(rest[i], 0)
            payload = bytes.fromhex(rest[i + 1])
            r = a.aem(target, mac, cmd, payload)
            r.update(type="aem", target=target.hex(), req=payload.hex())
            if r.get("status") == "SUCCESS" and cmd == 0x0027:
                r["decoded"] = decode_avb_info(r["payload"])
            if r.get("status") == "SUCCESS" and cmd == 0x0028:
                r["decoded"] = decode_as_path(r["payload"])
            emit(r)
    elif mode == "acmp":
        mt = ACMP_READ_ONLY[sys.argv[3]]
        r = a.acmp(mt, bytes.fromhex(sys.argv[4]), int(sys.argv[5]),
                   bytes.fromhex(sys.argv[6]), int(sys.argv[7]))
        emit(dict(type="acmp", query=sys.argv[3], **r))
    elif mode == "watch":
        secs, period = float(sys.argv[3]), float(sys.argv[4])
        targets = []
        for spec in sys.argv[5:]:
            e, m = spec.split("=")
            targets.append((bytes.fromhex(e), bytes.fromhex(m.replace(":", ""))))

        def other(fr):
            e = parse_adp(fr)
            if e:
                emit(dict(type="adp", **e))

        end = time.monotonic() + secs
        nxt = time.monotonic()
        while time.monotonic() < end:
            for tgt, mac in targets:
                r = a.aem(tgt, mac, 0x0027, struct.pack(">HH", 0x0009, 0), timeout=0.8, on_other=other)
                if r.get("status") == "SUCCESS":
                    r["decoded"] = decode_avb_info(r["payload"])
                r.update(type="avb_info", target=tgt.hex())
                emit(r)
                r = a.aem(tgt, mac, 0x0028, struct.pack(">HH", 0, 0), timeout=0.8, on_other=other)
                if r.get("status") == "SUCCESS":
                    r["decoded"] = decode_as_path(r["payload"])
                r.update(type="as_path", target=tgt.hex())
                emit(r)
            nxt += period
            for fr in frames(a.sock, max(nxt, time.monotonic())):
                other(fr)
        emit(dict(type="done"))
    else:
        raise SystemExit(f"unknown mode {mode}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
