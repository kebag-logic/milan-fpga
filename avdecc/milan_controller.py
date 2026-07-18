#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""
milan_controller.py - minimal AVDECC controller to validate the Milan v1.2 HW
entity on silicon. Protocol-equivalent to what Hive / la_avdecc drive, but
self-contained (raw AF_PACKET, no external AVDECC stack) so it runs on any
Linux peer on the AVB segment.

Run on the measurement peer (amx-pw0), which shares the AVB switch with the
AX7101 entity:

    sudo python3 milan_controller.py <iface>            # full validation
    sudo python3 milan_controller.py <iface> --read-all # dump every descriptor

It sends AECP AEM/VU commands to the entity's unicast MAC and checks the
responses against the 5-descriptor Milan model (ENTITY, CONFIGURATION,
AVB_INTERFACE, AUDIO_UNIT, STREAM_OUTPUT), plus LOCK (granted) / ACQUIRE
(NOT_SUPPORTED) / getters / setters / MVU GET_MILAN_INFO.

The entity's MAC/EntityID are discovered from its ADP ENTITY_AVAILABLE.
"""
import argparse
import socket
import struct
import sys
import time

ETH_P_AVTP   = 0x22F0
ADP_MCAST    = bytes.fromhex("91e0f0010000")
SUBTYPE_ADP  = 0xFA
SUBTYPE_AECP = 0xFB

# AECP message_type
AEM_COMMAND, AEM_RESPONSE = 0, 1
VU_COMMAND, VU_RESPONSE   = 6, 7
# AEM command_type
CMD = dict(ACQUIRE=0, LOCK=1, ENTITY_AVAILABLE=2, READ_DESCRIPTOR=4,
           SET_CONFIGURATION=6, GET_CONFIGURATION=7,
           SET_STREAM_FORMAT=8, GET_STREAM_FORMAT=9,
           SET_NAME=16, GET_NAME=17, SET_SAMPLING_RATE=20, GET_SAMPLING_RATE=21,
           GET_AVB_INFO=39, GET_STREAM_INFO=15, GET_AS_PATH=40, GET_COUNTERS=41,
           SET_STREAM_INFO=14, START_STREAMING=34, STOP_STREAMING=35)
# descriptor_type
DESC = dict(ENTITY=0x0000, CONFIGURATION=0x0001, AUDIO_UNIT=0x0002,
            STREAM_OUTPUT=0x0006, AVB_INTERFACE=0x0009)
STATUS = {0: "SUCCESS", 1: "NOT_IMPLEMENTED", 2: "NO_SUCH_DESCRIPTOR",
          3: "ENTITY_LOCKED", 4: "ENTITY_ACQUIRED", 7: "BAD_ARGUMENTS",
          11: "NOT_SUPPORTED"}
MILAN_PROTOCOL_ID = bytes.fromhex("001bc50ac100")

npass = nfail = 0
def check(name, ok, detail=""):
    global npass, nfail
    if ok: npass += 1; print(f"  [ ok ] {name} {detail}")
    else:  nfail += 1; print(f"  [FAIL] {name} {detail}")


class Entity:
    def __init__(self, iface):
        self.iface = iface
        self.s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW,
                               socket.htons(ETH_P_AVTP))
        self.s.bind((iface, ETH_P_AVTP))
        self.s.settimeout(2.0)
        # Receive the AVDECC ADP multicast (91:E0:F0:01:00:00): a raw AF_PACKET
        # socket only gets frames the NIC accepts, so join promiscuous mode.
        ifindex = socket.if_nametoindex(iface)
        SOL_PACKET = getattr(socket, "SOL_PACKET", 263)
        PACKET_ADD_MEMBERSHIP, PACKET_MR_PROMISC = 1, 1
        mreq = struct.pack("iHH8s", ifindex, PACKET_MR_PROMISC, 0, b"")
        self.s.setsockopt(SOL_PACKET, PACKET_ADD_MEMBERSHIP, mreq)
        self.src = self.s.getsockname()[4][:6]
        self.ctlr_id = struct.unpack(">Q", self.src + b"\x00\x00")[0]
        self.seq = 0x1000
        self.mac = None
        self.eid = None

    # -- ADP discovery ------------------------------------------------------
    def discover(self, timeout=20.0):
        # send a global ENTITY_DISCOVER, then listen for ENTITY_AVAILABLE
        # ADPDU byte 1 = {sv,ver,msg_type}: ENTITY_DISCOVER = 2. (The old
        # code packed the 2 into byte 2 = valid_time, silently sending an
        # ENTITY_AVAILABLE with eid=0 - discovery only ever worked by
        # catching PERIODIC advertises, hence the flaky first runs.)
        adpdu = bytes([SUBTYPE_ADP, 0x02, 0x00, 0x00]) + b"\x00" * 64
        self._send(ADP_MCAST, adpdu)
        end = time.time() + timeout
        while time.time() < end:
            try:
                f = self.s.recv(2048)
            except socket.timeout:
                self._send(ADP_MCAST, adpdu); continue
            if len(f) < 16 or f[12:14] != struct.pack(">H", ETH_P_AVTP):
                continue
            if f[14] == SUBTYPE_ADP and (f[15] & 0x0F) == 0:  # ENTITY_AVAILABLE
                eid = struct.unpack(">Q", f[18:26])[0]
                # optional target filter (two-entity bench: pick the board)
                if getattr(self, "want_suffix", None) and \
                   not f"{eid:016x}".endswith(self.want_suffix):
                    continue
                self.mac = f[6:12]
                # ADPDU: subtype@14, sv/ver/msgtype@15, valid_time/cdl@16-17,
                # entity_id@18-25 (ADPDU bytes 4-11).
                self.eid = eid
                return True
        return False

    # -- ACMP transport (IEEE 1722.1 Clause 8; subtype 0xFC, all multicast) --
    def acmp(self, msg_type, tuid=0, seq_salt=0):
        self.seq = (self.seq + 1) & 0xFFFF
        seq = (self.seq + seq_salt) & 0xFFFF
        pkt = struct.pack(">BBH", 0xFC, msg_type & 0x0F, 44)
        pkt += b"\x00" * 8                                 # stream_id
        pkt += struct.pack(">Q", self.ctlr_id)             # controller
        pkt += struct.pack(">Q", self.eid)                 # talker
        pkt += b"\x00" * 8                                 # listener
        pkt += struct.pack(">HH", tuid, 0)                 # talker/listener uid
        pkt += b"\x00" * 6                                 # stream_dest_mac
        pkt += struct.pack(">HHHHH", 0, seq, 0, 0, 0)      # count/seq/flags/vlan/rsvd
        self._send(ADP_MCAST, pkt)
        end = time.time() + 1.5
        while time.time() < end:
            try:
                f = self.s.recv(2048)
            except socket.timeout:
                return None
            if len(f) < 70 or f[12:14] != struct.pack(">H", ETH_P_AVTP):
                continue
            if f[14] != 0xFC or (f[15] & 0x0F) != ((msg_type & 0x0F) | 1):
                continue
            if struct.unpack(">H", f[62:64])[0] != seq:
                continue
            return f
        return None

    # -- AECP transport -----------------------------------------------------
    def _send(self, dst, payload):
        self.s.send(dst + self.src + struct.pack(">H", ETH_P_AVTP) + payload)

    def _aecp(self, msg_type, cmd, spec, is_vu=False):
        self.seq = (self.seq + 1) & 0xFFFF
        if is_vu:
            body = MILAN_PROTOCOL_ID + struct.pack(">HH", cmd, 0) + spec
            cdl = 10 + len(body)
            hdr = struct.pack(">BBH", SUBTYPE_AECP, msg_type, (0 << 11) | cdl)
            pkt = hdr + struct.pack(">Q", self.eid) + struct.pack(">Q", self.ctlr_id) \
                  + struct.pack(">H", self.seq) + body
        else:
            cdl = 12 + len(spec)
            hdr = struct.pack(">BBH", SUBTYPE_AECP, msg_type, (0 << 11) | cdl)
            pkt = hdr + struct.pack(">Q", self.eid) + struct.pack(">Q", self.ctlr_id) \
                  + struct.pack(">H", self.seq) + struct.pack(">H", cmd & 0x7FFF) + spec
        want_seq = self.seq
        self._send(self.mac, pkt)
        end = time.time() + 1.5
        while time.time() < end:
            try:
                f = self.s.recv(2048)
            except socket.timeout:
                return None
            if len(f) < 38 or f[14] != SUBTYPE_AECP:
                continue
            mt = f[15] & 0x0F
            if mt not in (AEM_RESPONSE, VU_RESPONSE):
                continue
            rseq = struct.unpack(">H", f[34:36])[0]
            if rseq == want_seq:
                return f
        return None

    def read_descriptor(self, dtype, dindex=0):
        spec = struct.pack(">HHHH", 0, 0, dtype, dindex)   # cfg, reserved, type, index
        return self._aecp(AEM_COMMAND, CMD["READ_DESCRIPTOR"], spec)

    def aem(self, cmd, spec=b""):
        return self._aecp(AEM_COMMAND, CMD[cmd], spec)


def rstatus(f): return (f[16] >> 3) & 0x1F if f else -1
def rcdl(f):    return ((f[16] & 0x07) << 8) | f[17] if f and len(f) > 17 else -1
def cdl_ok(f):
    # IEEE 1722-2016 §5.4: control_data_length counts octets AFTER the stream_id
    # (target_entity_id) field, i.e. from wire offset 26. The pipewire AVB
    # reference (Hive-validated) matches: CDL = frame - 26. The on-wire frame is
    # the AECPDU padded up to the 60-byte Ethernet minimum, so
    # len == max(60, 26 + cdl). (Frames > 60 B pin cdl exactly; <= 60 B ones
    # can't be length-verified as padding hides the true cdl.)
    return bool(f) and len(f) > 26 and len(f) == max(60, 26 + rcdl(f))
def rcmd(f):    return ((f[36] & 0x7F) << 8) | f[37] if f else -1
def desc_payload(f): return f[42:] if f and len(f) > 42 else b""   # after cfg+reserved


def validate(e):
    print(f"\n== entity discovered: MAC {e.mac.hex(':')}  EID 0x{e.eid:016x} ==")

    print("\n[1] READ_DESCRIPTOR — the 5 Milan descriptors")
    r = e.read_descriptor(DESC["ENTITY"])
    check("ENTITY readable", rstatus(r) == 0, f"status={STATUS.get(rstatus(r))}")
    check("ENTITY control_data_length correct (spec §5.4, len-26)", cdl_ok(r),
          f"cdl={rcdl(r)} len-26={len(r)-26 if r else 0}")
    if r:
        d = desc_payload(r)
        eid = struct.unpack(">Q", d[4:12])[0]
        check("ENTITY.entity_id == ADP EID", eid == e.eid, f"0x{eid:016x}")
        cc = struct.unpack(">H", d[308:310])[0]
        check("ENTITY.configurations_count == 1", cc == 1, f"{cc}")
    for name in ("CONFIGURATION", "AUDIO_UNIT", "STREAM_OUTPUT", "AVB_INTERFACE"):
        r = e.read_descriptor(DESC[name])
        d = desc_payload(r)
        dt = struct.unpack(">H", d[0:2])[0] if len(d) >= 2 else -1
        check(f"{name} readable, type matches", rstatus(r) == 0 and dt == DESC[name],
              f"status={STATUS.get(rstatus(r))} type=0x{dt:04x}")
    r = e.read_descriptor(DESC["STREAM_OUTPUT"], 5)
    check("READ_DESCRIPTOR bad index -> NO_SUCH_DESCRIPTOR", rstatus(r) == 2,
          f"status={STATUS.get(rstatus(r))}")

    print("\n[2] ACQUIRE_ENTITY -> NOT_SUPPORTED (Milan)")
    r = e.aem("ACQUIRE", b"\x00" * 16)
    check("ACQUIRE answered NOT_SUPPORTED", rstatus(r) == 11 and rcmd(r) == 0,
          f"status={STATUS.get(rstatus(r))}")

    print("\n[3] LOCK_ENTITY -> SUCCESS, UNLOCK -> SUCCESS")
    r = e.aem("LOCK", b"\x00" * 12)   # flags=0 (LOCK)
    check("LOCK granted", rstatus(r) == 0, f"status={STATUS.get(rstatus(r))}")
    r = e.aem("LOCK", b"\x00\x00\x00\x01" + b"\x00" * 8)  # flags bit0 = UNLOCK
    check("UNLOCK granted", rstatus(r) == 0, f"status={STATUS.get(rstatus(r))}")

    print("\n[4] GET/SET_CONFIGURATION")
    r = e.aem("GET_CONFIGURATION")
    cc = struct.unpack(">H", r[40:42])[0] if r and len(r) > 42 else -1
    check("GET_CONFIGURATION -> config 0", rstatus(r) == 0 and cc == 0, f"cfg={cc}")
    r = e.aem("SET_CONFIGURATION", struct.pack(">HH", 0, 5))   # invalid
    check("SET_CONFIGURATION(5) -> BAD_ARGUMENTS", rstatus(r) == 7,
          f"status={STATUS.get(rstatus(r))}")

    print("\n[5] SET_NAME + read-back")
    nm = b"Hive Verified" + b"\x00" * (64 - 13)
    r = e.aem("SET_NAME", struct.pack(">HHHH", DESC["ENTITY"], 0, 0, 0) + nm)
    check("SET_NAME(ENTITY) -> SUCCESS", rstatus(r) == 0, f"status={STATUS.get(rstatus(r))}")
    r = e.read_descriptor(DESC["ENTITY"])
    newname = desc_payload(r)[48:48+13] if r else b""
    check("entity_name updated in ENTITY descriptor", newname == b"Hive Verified",
          newname.decode(errors="replace"))

    print("\n[6] SET_SAMPLING_RATE (96 kHz valid, 44.1 kHz invalid)")
    r = e.aem("SET_SAMPLING_RATE", struct.pack(">HH", DESC["AUDIO_UNIT"], 0) + bytes([0,1,0x77,0]))
    check("SET_SAMPLING_RATE(96k) -> SUCCESS", rstatus(r) == 0, f"status={STATUS.get(rstatus(r))}")
    r = e.aem("SET_SAMPLING_RATE", struct.pack(">HH", DESC["AUDIO_UNIT"], 0) + bytes([0,0,0xac,0x44]))
    check("SET_SAMPLING_RATE(44.1k) -> BAD_ARGUMENTS", rstatus(r) == 7,
          f"status={STATUS.get(rstatus(r))}")

    aecp_vlan = None
    print("\n[7] GET_STREAM_INFO (Milan fixed 56-byte payload)")
    r = e.aem("GET_STREAM_INFO", struct.pack(">HH", DESC["STREAM_OUTPUT"], 0))
    check("GET_STREAM_INFO -> SUCCESS", rstatus(r) == 0, f"status={STATUS.get(rstatus(r))}")
    check("GET_STREAM_INFO CDL == 68 (56+12, la_avdecc-strict)",
          rcdl(r) == 68 and cdl_ok(r), f"cdl={rcdl(r)} len={len(r) if r else 0}")
    if r and len(r) > 45:
        check("stream_info flags == 0xF6000000 (talker)",
              r[42:46] == bytes.fromhex("f6000000"), r[42:46].hex())
    if r and len(r) > 85:
        # live values (2026-07-14 talker SM): the advertised stream_id MUST
        # byte-match the AVTP frames = {station_mac, uid 0} - the old
        # entity_id here could never bind
        check("stream_id == {mac,0} (matches AVTP)",
              r[54:62] == bytes(e.mac) + b"\x00\x00", r[54:62].hex())
        check("dest_mac live (nonzero; vlan echoes the CSR - VID0 policy legal)",
              r[66:72] != b"\x00"*6,
              f"dmac={r[66:72].hex()} vlan={r[82:84].hex()}")
        aecp_vlan = r[82:84]

    print("\n[7b] SET_STREAM_INFO round-trip (Milan 5.4.2.9, ACC_LAT only)")
    def si_body(flags, lat, dtype=None):
        dt = DESC["STREAM_OUTPUT"] if dtype is None else dtype
        return (struct.pack(">HHI", dt, 0, flags) + b"\x00"*16 +
                struct.pack(">I", lat) + b"\x00"*28)
    r = e.aem("SET_STREAM_INFO", si_body(0x20000000, 1500000))
    check("SET(ACC_LAT=1.5ms) SUCCESS", rstatus(r) == 0,
          f"status={STATUS.get(rstatus(r))}")
    r = e.aem("GET_STREAM_INFO", struct.pack(">HH", DESC["STREAM_OUTPUT"], 0))
    check("GET reflects 1.5ms", r is not None and len(r) > 65 and
          r[62:66] == (1500000).to_bytes(4, "big"),
          r[62:66].hex() if r and len(r) > 65 else "-")
    r = e.aem("SET_STREAM_INFO", si_body(0x40000000, 7))   # STREAM_ID_VALID
    check("SET(other subcmd) -> NOT_SUPPORTED", rstatus(r) == 11,
          f"status={STATUS.get(rstatus(r))}")
    e.aem("SET_STREAM_INFO", si_body(0x20000000, 2000000))  # restore default
    r = e.aem("START_STREAMING", struct.pack(">HH", DESC["STREAM_OUTPUT"], 0))
    check("START_STREAMING -> NOT_SUPPORTED (input-only cmd)", rstatus(r) == 11,
          f"status={STATUS.get(rstatus(r))}")
    r = e.aem("STOP_STREAMING", struct.pack(">HH", DESC["STREAM_OUTPUT"], 0))
    check("STOP_STREAMING -> NOT_SUPPORTED (input-only cmd)", rstatus(r) == 11,
          f"status={STATUS.get(rstatus(r))}")

    print("\n[8] GET_AS_PATH (Milan-mandatory)")
    r = e.aem("GET_AS_PATH", struct.pack(">HH", 0, 0))
    check("GET_AS_PATH -> SUCCESS", rstatus(r) == 0, f"status={STATUS.get(rstatus(r))}")
    if r and len(r) > 49:
        cnt = int.from_bytes(r[40:42], "big")
        eui = r[42:50]
        mac = bytes(e.mac)
        exp = mac[:3] + b"\xff\xfe" + mac[3:]
        check("AS_PATH count==1, path[0]==EUI64(entity MAC)",
              cnt == 1 and eui == exp, f"count={cnt} path0={eui.hex()}")

    print("\n[9] ACMP (Milan v1.2 5.5 - PROBE_TX activation talker)")
    live_sid = bytes(e.mac) + b"\x00\x00"
    r = e.acmp(0)                        # CONNECT_TX == Milan PROBE_TX
    ok = r is not None
    check("PROBE_TX answered", ok, "timeout")
    if ok:
        check("PROBE_TX SUCCESS + count 0",
              (r[16] >> 3) == 0 and r[60:62] == b"\x00\x00",
              f"status={r[16]>>3} count={r[60:62].hex()}")
        check("PROBE_TX live stream_id {mac,0}", r[18:26] == live_sid,
              r[18:26].hex())
        check("PROBE_TX live dmac (vlan = CSR value, cross-checked vs AECP)",
              r[54:60] != b"\x00"*6 and (aecp_vlan is None or r[66:68] == aecp_vlan),
              f"dmac={r[54:60].hex()} vlan={r[66:68].hex()}")
    r = e.acmp(4)                        # GET_TX_STATE_COMMAND
    ok = r is not None
    check("GET_TX_STATE answered", ok, "timeout")
    if ok:
        check("GET_TX_STATE SUCCESS + live fields + count 0",
              (r[16] >> 3) == 0 and r[18:26] == live_sid and
              r[60:62] == b"\x00\x00",
              f"status={r[16]>>3} sid={r[18:26].hex()}")
    r = e.acmp(2)                        # DISCONNECT_TX_COMMAND
    check("DISCONNECT_TX SUCCESS + zeroed fields (Milan 5.5.4.2)",
          r is not None and (r[16] >> 3) == 0 and r[18:26] == b"\x00"*8,
          "timeout" if r is None else f"status={r[16]>>3}")
    r = e.acmp(12)                       # GET_TX_CONNECTION_COMMAND
    check("GET_TX_CONNECTION -> NOT_SUPPORTED (Milan 5.5.4.4)",
          r is not None and (r[16] >> 3) == 31,
          "timeout" if r is None else f"status={r[16]>>3}")

    print("\n[10] MVU GET_MILAN_INFO")
    r = e._aecp(VU_COMMAND, 0x0000, b"", is_vu=True)
    ok = r is not None and (r[15] & 0x0F) == VU_RESPONSE and r[36:42] == MILAN_PROTOCOL_ID
    check("MVU GET_MILAN_INFO answered", ok,
          f"proto={r[36:42].hex() if r else '-'}")
    check("MVU control_data_length correct (spec §5.4, len-26)", cdl_ok(r),
          f"cdl={rcdl(r)} len-26={len(r)-26 if r else 0}")
    if r:
        ver = struct.unpack(">I", r[46:50])[0]
        check("MILAN protocol_version == 1", ver == 1, f"{ver}")

    print(f"\n{'='*60}\nMilan entity validation: {npass} pass, {nfail} fail")
    return nfail == 0


def bind(iface, talker_sfx, listener_sfx):
    """USER bug 5 (2026-07-18): the controller MUST force the listener's
    channel count to the talker's before binding. Flow:
      1. discover both entities (ADP);
      2. GET_STREAM_FORMAT on the talker's STREAM_OUTPUT[0];
      3. SET_STREAM_FORMAT that exact u64 on the listener's STREAM_INPUT[0]
         (the fabric accepts any 1..8ch variant - adaptive listener);
      4. CONNECT_RX_COMMAND to the listener naming the talker.
    Without step 3 a talker format change strands the listener rejecting
    every frame as UNSUPPORTED (sound gone, lock impossible - user bug 6)."""
    tk = Entity(iface); tk.want_suffix = talker_sfx.lower()
    if not tk.discover():
        print("talker not discovered"); return False
    ls = Entity(iface); ls.want_suffix = listener_sfx.lower()
    if not ls.discover():
        print("listener not discovered"); return False

    r = tk.aem("GET_STREAM_FORMAT", struct.pack(">HH", 0x0006, 0))
    if rstatus(r) != 0:
        print(f"talker GET_STREAM_FORMAT: {STATUS.get(rstatus(r))}"); return False
    fmt = struct.unpack(">Q", r[44:52])[0]
    print(f"talker STREAM_OUTPUT[0] format {fmt:#018x} "
          f"({(fmt >> 22) & 0x3FF} ch)")

    r = ls.aem("SET_STREAM_FORMAT", struct.pack(">HHQ", 0x0005, 0, fmt))
    if rstatus(r) != 0:
        print(f"listener SET_STREAM_FORMAT: {STATUS.get(rstatus(r))}"); return False
    print("listener STREAM_INPUT[0] format matched")

    # CONNECT_RX_COMMAND: dst = ACMP multicast, listener + talker named
    pkt = struct.pack(">BBH", 0xFC, 6, 44)
    pkt += b"\x00" * 8
    pkt += struct.pack(">Q", ls.ctlr_id)
    pkt += struct.pack(">Q", tk.eid)
    pkt += struct.pack(">Q", ls.eid)
    pkt += struct.pack(">HH", 0, 0)
    pkt += b"\x00" * 6
    pkt += struct.pack(">HHHH", 0, 0x0B00, 0, 0)
    ls._send(ADP_MCAST, pkt)
    end = time.time() + 3.0
    while time.time() < end:
        try:
            f = ls.s.recv(2048)
        except socket.timeout:
            break
        if f[14] == 0xFC and (f[15] & 0x0F) == 7 \
           and struct.unpack(">Q", f[42:50])[0] == ls.eid:
            st = (f[16] >> 3) & 0x1F
            print(f"CONNECT_RX_RESPONSE status={st} "
                  f"({'SUCCESS' if st == 0 else STATUS.get(st, st)})")
            return st == 0
    print("CONNECT_RX: no response (listener SM may still bind+probe)")
    return True


def read_all(e):
    for name, dt in DESC.items():
        r = e.read_descriptor(dt)
        d = desc_payload(r)
        print(f"{name:14s} status={STATUS.get(rstatus(r),'?'):16s} "
              f"len={len(d):3d}  {d[:32].hex()}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("iface")
    ap.add_argument("--read-all", action="store_true")
    ap.add_argument("--eid", help="hex suffix of the target entity_id (two-entity bench)")
    ap.add_argument("--bind", nargs=2, metavar=("TALKER_SFX", "LISTENER_SFX"),
                    help="format-matched bind: talker fmt -> listener fmt -> CONNECT_RX")
    a = ap.parse_args()
    if a.bind:
        sys.exit(0 if bind(a.iface, a.bind[0], a.bind[1]) else 1)
    e = Entity(a.iface)
    if a.eid:
        e.want_suffix = a.eid.lower()
    print(f"controller MAC {e.src.hex(':')} on {a.iface}; discovering entity...")
    if not e.discover():
        print("no ENTITY_AVAILABLE seen — is the AX7101 up + ADP enabled?")
        sys.exit(2)
    if a.read_all:
        read_all(e); return
    ok = validate(e)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
