#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Byte-for-byte cross-check: the offline AECP model's MVU answers against the
frames the pinned protocol processor's tb/pp_top M-section expects.

Usage: python3 -B xcheck_pp_top_mvu.py <milan-fpga checkout at the reviewed head>

The pp_top `aecp_frame()` builder (tb/pp_top/sim_main.cpp) is restated here,
including its `aem_like` u-bit rule, with pp_top's own identity constants, so
each model response can be compared to the exact `want` frame pp_top grades
the RTL against. Cases the pinned pp_top does not carry (MVU 0x0001, 0x0003,
0x0004, non-VU message types carrying the Milan protocol_id, and each Table
5.18 command in its own Milan v1.2 Figure shape) are compared against the
echo the engine source produces for them (KL_aecp_engine.sv: only
`mvu_get_milan_info_w` leaves the NOT_IMPLEMENTED echo).
Exit 0 when every case matches, 1 otherwise.
"""
import struct
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
sys.path.insert(0, str(root / "tests" / "steps"))
import aecp_engine_model as m  # noqa: E402
from aecp_engine_steps import SERVED, SERVED_MVU  # noqa: E402

# tb/pp_top/sim_main.cpp identity constants
OWN_MAC = 0x0A0B0C0D0E0F
EID = 0x123456789ABCDEF0
CTLR_MAC = 0x0202DEADBEEF
CTLR_EID = 0x7777000000000042
MVU_PID_HI = 0x001B
MVU_PID_LO = 0xC50AC100
MVU_INFO = 0x0000
VU_COMMAND, VU_RESPONSE = 6, 7
SUCCESS, NOT_IMPLEMENTED = 0, 1


def be(v, n):
    return v.to_bytes(n, "big")


def aecp_frame(da, sa, mt, status, target, ctlr, seq, cmd_type, payload):
    """tb/pp_top/sim_main.cpp aecp_frame(), pad60 = true."""
    f = bytearray(38 + len(payload))
    f[0:6] = be(da, 6)
    f[6:12] = be(sa, 6)
    f[12:14] = be(0x22F0, 2)
    f[14] = 0xFB
    f[15] = mt & 0x0F
    cdl = 12 + len(payload)
    f[16] = ((status & 0x1F) << 3) | ((cdl >> 8) & 0x07)
    f[17] = cdl & 0xFF
    f[18:26] = be(target, 8)
    f[26:34] = be(ctlr, 8)
    f[34:36] = be(seq, 2)
    aem_like = mt in (0, 1)
    f[36:38] = be(cmd_type & 0x7FFF if aem_like else cmd_type, 2)
    f[38:38 + len(payload)] = payload
    if len(f) < 60:
        f += bytes(60 - len(f))
    return bytes(f)


def mvu_cmd_pl(pid_lo, ct, nbytes):
    p = bytearray(nbytes)
    if nbytes >= 4:
        p[0:4] = be(pid_lo, 4)
    if nbytes >= 6:
        p[4:6] = be(ct, 2)
    return bytes(p)


INFO_PL = (be(MVU_PID_LO, 4) + be(MVU_INFO, 2) + be(0, 2) + be(1, 4)
           + be(0, 4) + be(0, 4))

model = m.AecpEngineModel(SERVED, m.DescriptorImage(), entity_id=EID,
                          own_mac=be(OWN_MAC, 6), mvu_served=SERVED_MVU)

cases = []


def case(name, mt, hi, cmd_pl, want_status, want_pl, seq):
    cmd = aecp_frame(OWN_MAC, CTLR_MAC, mt, 0, EID, CTLR_EID, seq, hi, cmd_pl)
    want = aecp_frame(CTLR_MAC, OWN_MAC, mt | 1, want_status, EID, CTLR_EID,
                      seq, hi, want_pl)
    got = model.deliver(cmd)
    ok = got == want
    cases.append((name, ok, got, want))


# ---- pp_top M-section, verbatim shapes -------------------------------------
case("M1 GET_MILAN_INFO byte-exact", VU_COMMAND, MVU_PID_HI,
     mvu_cmd_pl(MVU_PID_LO, MVU_INFO, 8), SUCCESS, INFO_PL, 0xC001)
case("M3 foreign 12-bit protocol id", VU_COMMAND, MVU_PID_HI,
     mvu_cmd_pl(0xC50AC101, MVU_INFO, 8), NOT_IMPLEMENTED,
     mvu_cmd_pl(0xC50AC101, MVU_INFO, 8), 0xC002)
case("M4 GET_SYSTEM_UNIQUE_ID 0x0002", VU_COMMAND, MVU_PID_HI,
     mvu_cmd_pl(MVU_PID_LO, 0x0002, 8), NOT_IMPLEMENTED,
     mvu_cmd_pl(MVU_PID_LO, 0x0002, 8), 0xC003)
case("M5 r = 1", VU_COMMAND, MVU_PID_HI, mvu_cmd_pl(MVU_PID_LO, 0x8000, 8),
     NOT_IMPLEMENTED, mvu_cmd_pl(MVU_PID_LO, 0x8000, 8), 0xC004)
junk = bytearray(mvu_cmd_pl(MVU_PID_LO, MVU_INFO, 8))
junk[6], junk[7] = 0xDE, 0xAD
case("M5b junk reserved still served, reserved 0", VU_COMMAND, MVU_PID_HI,
     bytes(junk), SUCCESS, INFO_PL, 0xC005)
case("M6 truncated (6 payload octets)", VU_COMMAND, MVU_PID_HI,
     mvu_cmd_pl(MVU_PID_LO, MVU_INFO, 6), NOT_IMPLEMENTED,
     mvu_cmd_pl(MVU_PID_LO, MVU_INFO, 6), 0xC006)
for hi, lo, what in [
        (0xFF1B, 0xC50AC100, "M8 foreign @22"),
        (0x00FF, 0xC50AC100, "M8 foreign @23"),
        (0x001B, 0xFF0AC100, "M8 foreign @24"),
        (0x001B, 0xC5FFC100, "M8 foreign @25"),
        (0x001B, 0xC50AFF00, "M8 foreign @26"),
        (0x001B, 0xC50AC1FF, "M8 foreign @27"),
        (0x001B, 0xC50AC101, "M8 one bit in the last octet"),
        (0xFC1B, 0xC50AC100, "M8b OUI bit 7 set (0xFC)"),
        (0x801B, 0xC50AC100, "M8b OUI bit 7 only (0x80)")]:
    pl = mvu_cmd_pl(lo, MVU_INFO, 8)
    case(what, VU_COMMAND, hi, pl, NOT_IMPLEMENTED, pl, 0xC010)

# ---- beyond the pinned pp_top: engine-source echo --------------------------
for ct in (0x0001, 0x0003, 0x0004):
    pl = mvu_cmd_pl(MVU_PID_LO, ct, 8)
    case("MVU %#06x in the Figure 5.3 shape (feature row)" % ct, VU_COMMAND,
         MVU_PID_HI, pl, NOT_IMPLEMENTED, pl, 0xC020 + ct)
case("7-octet GET_MILAN_INFO (feature row, cdl 19)", VU_COMMAND, MVU_PID_HI,
     mvu_cmd_pl(MVU_PID_LO, MVU_INFO, 7), NOT_IMPLEMENTED,
     mvu_cmd_pl(MVU_PID_LO, MVU_INFO, 7), 0xC030)
padded = mvu_cmd_pl(MVU_PID_LO, MVU_INFO, 16)
case("GET_MILAN_INFO carrying 8 extra octets (cdl 28) still served",
     VU_COMMAND, MVU_PID_HI, padded, SUCCESS, INFO_PL, 0xC031)
for mt in (2, 4, 8, 10, 12, 14):
    pl = mvu_cmd_pl(MVU_PID_LO, MVU_INFO, 8)
    case("message_type %d carrying the Milan protocol_id is echoed" % mt, mt,
         MVU_PID_HI, pl, NOT_IMPLEMENTED, pl, 0xC040 + mt)
# Each Table 5.18 command in its OWN Milan v1.2 figure shape (5.5/5.3/5.6/5.7)
suid = mvu_cmd_pl(MVU_PID_LO, 0x0001, 8) + be(0x0123456789ABCDEF, 8)
case("SET_SYSTEM_UNIQUE_ID, Figure 5.5 (cdl 28)", VU_COMMAND, MVU_PID_HI,
     suid, NOT_IMPLEMENTED, suid, 0xC051)
smcri = (be(MVU_PID_LO, 4) + be(0x0003, 2) + be(0, 2)
         + bytes((0x01, 0, 0x80, 0x70)) + be(0, 4)
         + b"DEFAULT".ljust(64, b"\0"))
case("SET_MEDIA_CLOCK_REFERENCE_INFO, Figure 5.6 (cdl %d)"
     % (12 + len(smcri)), VU_COMMAND, MVU_PID_HI, smcri, NOT_IMPLEMENTED,
     smcri, 0xC053)
gmcri = be(MVU_PID_LO, 4) + be(0x0004, 2) + be(0, 2)
case("GET_MEDIA_CLOCK_REFERENCE_INFO, Figure 5.7 (cdl 20)", VU_COMMAND,
     MVU_PID_HI, gmcri, NOT_IMPLEMENTED, gmcri, 0xC054)

bad = 0
for name, ok, got, want in cases:
    print("%-4s %s" % ("OK" if ok else "FAIL", name))
    if not ok:
        bad += 1
        print("     got  %s" % (got.hex() if got else None))
        print("     want %s" % want.hex())
print("M1 want frame: %s" % cases[0][3].hex())
print("%d cases, %d mismatches" % (len(cases), bad))
sys.exit(1 if bad else 0)
