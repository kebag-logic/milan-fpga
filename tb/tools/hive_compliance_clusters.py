#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""hive_compliance_clusters.py - the CLUSTER/MAP half of the Hive-grade checks.

    sudo ./hive_compliance_clusters.py --iface enp6s0 \
         --target-eid 020000FFFE000001 --target-mac 02:00:00:00:00:01
    sudo ./hive_compliance_clusters.py --iface enp6s0 \
         --target-eid 3CC0C60102030000 --target-mac 3c:c0:c6:01:02:03

RUN IT AGAINST BOTH DEVICES, EVERY ROUND. A check that only ever passes
proves as little as one that only ever fails. The Milan-validated test device
(3CC0C60102030000) is the calibration oracle: if a check here fails on the
peer, the check is wrong until the clause proves otherwise - that is the C1
lesson, where the first rule ("a non-success response echoes the COMMAND")
was an invention the reference device refuted.

These are C5-C9, the checks `hive_compliance.py`'s C1-C4 do not make: C1-C4
never leave STREAM_INPUT/STREAM_OUTPUT, so the whole AUDIO_CLUSTER /
AUDIO_MAP subtree - the part a role-pooled model changes most - was
unchecked by any controller-grade tool. Fold these in as C5-C9 or keep the
module beside it; the transport is imported from `hive_compliance` when that
module is importable so there is exactly one calibrated socket recipe.

THE CHECKS, each with the clause it rests on:

  C5 CLUSTER BLOCK IS ADDRESSABLE.  1722.1-2021 7.2.13 (Table 7-23): every
     STREAM_PORT_INPUT/OUTPUT carries number_of_clusters + base_cluster.
     Every AUDIO_CLUSTER in [base_cluster, base_cluster+number_of_clusters)
     must answer READ_DESCRIPTOR, and no two ports may claim the same
     cluster.  A port that advertises clusters it cannot serve is C3's
     defect one level down: the device contradicting itself between two
     commands.

  C6 MAP BLOCK IS ADDRESSABLE AND PORT-RELATIVE.  7.2.13 gives the port
     number_of_maps + base_map; 7.2.19 says an AUDIO_MAP maps stream
     channels to channels of the AUDIO_CLUSTERs "contained in the same"
     STREAM_PORT and that mapping_cluster_offset is "the offset from the
     base_cluster of the STREAM_PORT_INPUT or STREAM_PORT_OUTPUT".  So every
     declared map must answer, and every row's offset must be <
     number_of_clusters OF THAT PORT.  A model that wrote GLOBAL cluster
     indices satisfies every count check and is wrong on the wire; this is
     the check that catches it.

  C7 7.2.19 UNIQUENESS.  Input maps: at most one entry per cluster channel.
     Output maps: at most one entry per stream channel across the entire
     Configuration.  Read-only; violations are a real interop hazard because
     they describe two sources feeding one sink.

  C8 MILAN STATIC/DYNAMIC POSTURE.  Milan v1.2 5.4.2.27: "For each Stream
     Port Input and for each Stream Port Output that has no Audio Map, the
     PAAD-AE shall implement the ADD_AUDIO_MAPPINGS command"; 5.4.2.28 the
     same for REMOVE.  1722.1 7.2.13: dynamic-mapping entities "set the
     number_of_maps field to zero (0)".  So NOT_SUPPORTED on a port WITH
     Audio Maps is CONFORMANCE and is asserted, not flagged; and a port with
     number_of_maps == 0 must NOT answer NOT_SUPPORTED.
     ADD on a port WITH maps cannot mutate anything (it is refused by
     definition) and runs by default.  ADD on a DYNAMIC port would mutate a
     live device, so that half needs --allow-writes.

  C9 GET_AUDIO_MAP PAGING.  Milan 5.4.2.26 / 1722.1 7.4.44: the response
     carries a fixed number_of_maps partitioning of the port's cluster
     channels.  The bound is read OUT OF THE DEVICE (never assumed - the C1
     lesson) and map_index == that bound must answer BAD_ARGUMENTS.
     Read-only.  Skipped where the device serves no dynamic port.

  C10 ODD number_of_mappings.  1722.1-2021 7.4.45/7.4.46 bound the field
     only by what fits an AECPDU; Milan 5.4.2.27/28 enumerate every legal
     BAD_ARGUMENTS condition and NONE of them is a record count; 5.4.2.26
     fixes the granularity the other way ("at most one dynamic mapping per
     Stream Output's channel").  A single-mapping command is therefore
     ordinary traffic, and it is what a controller like Hive sends.
     Our entity refused an ODD count until 2026-08-03 - a pair-slot detail
     of OUR capture crossbar leaking into protocol acceptance - and every
     test we owned missed it because our own tools only ever sent L/R
     pairs.  The probe re-ADDs a mapping the DEVICE ITSELF just reported
     through GET_AUDIO_MAP: idempotent, so it is safe on a live device, and
     unarguable, because a mapping the entity is already serving cannot be
     an invalid mapping.  If it is refused, the refusal is about the COUNT.
     Needs --allow-writes (an idempotent write is still a write).

Exit code 0 = clean, 1 = at least one FAIL.
"""
import argparse
import os
import struct
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# One calibrated socket recipe: reuse hive_compliance's transport when it is
# importable (raw AVDECC tools MUST join 91:E0:F0:01:00:00 or the NIC drops
# every response - recorded bench trap), else fall back to a local copy.
try:
    from hive_compliance import open_sock, aecp_cmd, xchg, resp_parts
    _SHARED_TRANSPORT = True
except ImportError:                                    # pragma: no cover
    import socket
    _SHARED_TRANSPORT = False
    ETH_P_ALL, AVTP = 0x0003, 0x22F0
    MCAST = bytes.fromhex('91e0f0010000')
    SOL_PACKET, ADD_MEMBERSHIP, MR_MULTICAST = 263, 1, 0
    SUBTYPE_AECP = 0xFB

    def open_sock(iface):
        s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW,
                          socket.htons(ETH_P_ALL))
        s.bind((iface, 0))
        s.setsockopt(SOL_PACKET, ADD_MEMBERSHIP,
                     struct.pack("iHH8s", socket.if_nametoindex(iface),
                                 MR_MULTICAST, len(MCAST), MCAST))
        s.settimeout(1.0)
        return s

    def aecp_cmd(src, dst, target, ctrlr, seq, cmd, payload):
        # cdl counts octets FOLLOWING target_entity_id (1722.1-2021
        # 9.2.2.6), matching hive_compliance.aecp_cmd's 2026-08-02 fix.
        body = struct.pack('!8s8sHH', target, ctrlr, seq, cmd) + payload
        cdl = len(body) - 8
        avtp = bytes([SUBTYPE_AECP, 0x00, (cdl >> 8) & 0x07, cdl & 0xFF])
        return dst + src + struct.pack('!H', AVTP) + avtp + body, cdl

    def xchg(s, frame, src, seq, timeout=1.5):
        s.send(frame)
        end = time.time() + timeout
        while time.time() < end:
            try:
                f = s.recv(2048)
            except socket.timeout:
                return None
            if len(f) < 26 or f[12:14] != struct.pack('!H', AVTP):
                continue
            if f[14] != SUBTYPE_AECP or f[0:6] != src:
                continue
            if struct.unpack('!H', f[34:36])[0] != seq:
                continue
            return f
        return None

    def resp_parts(f):
        return (f[16] >> 3) & 0x1F, ((f[16] & 0x07) << 8) | f[17], f[38:]

CMD_READ_DESCRIPTOR = 0x0004
CMD_GET_AUDIO_MAP = 0x002B          # 43, 1722.1 7.4.44
CMD_ADD_AUDIO_MAPPINGS = 0x002C     # 44, 7.4.45  / Milan 5.4.2.27
CMD_REMOVE_AUDIO_MAPPINGS = 0x002D  # 45, 7.4.46  / Milan 5.4.2.28
DESC_STREAM_PORT_INPUT = 0x000E
DESC_STREAM_PORT_OUTPUT = 0x000F
DESC_AUDIO_CLUSTER = 0x0014
DESC_AUDIO_MAP = 0x0017
ST_SUCCESS, ST_NO_SUCH_DESCRIPTOR, ST_BAD_ARGUMENTS, ST_NOT_SUPPORTED = 0, 2, 7, 11

FAILS, SKIPS, CHECKS = [], [], [0]


def ck(ok, name, detail=""):
    CHECKS[0] += 1
    if not ok:
        FAILS.append(f"{name}: {detail}")
    print(f"  [{'ok  ' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))


def skip(name, why):
    SKIPS.append(name)
    print(f"  [skip] {name}  {why}")


class Probe:
    def __init__(self, sock, src, dst, tgt, ctl):
        self.s, self.src, self.dst, self.tgt, self.ctl = sock, src, dst, tgt, ctl
        self.seq = 0x7A00

    def _nx(self):
        self.seq = (self.seq + 1) & 0xFFFF
        return self.seq

    def cmd(self, code, payload):
        q = self._nx()
        fr, _ = aecp_cmd(self.src, self.dst, self.tgt, self.ctl, q, code, payload)
        r = xchg(self.s, fr, self.src, q)
        return resp_parts(r) if r else (None, None, None)

    def read_desc(self, dtype, index):
        """-> (status, descriptor_image). The image starts after the
        READ_DESCRIPTOR response's configuration_index(2)+reserved(2)."""
        st, _, pl = self.cmd(CMD_READ_DESCRIPTOR,
                             struct.pack('!HHHH', 0, 0, dtype, index))
        return st, (pl[4:] if pl is not None and len(pl) > 4 else b'')


def parse_port(img):
    """STREAM_PORT_INPUT/OUTPUT, 1722.1-2021 7.2.13 Table 7-23. Field order
    after descriptor_type(2)+descriptor_index(2): clock_domain_index(2),
    port_flags(2), number_of_controls(2), base_control(2),
    number_of_clusters(2), base_cluster(2), number_of_maps(2), base_map(2)."""
    if len(img) < 20:
        return None
    n_cl, b_cl, n_map, b_map = struct.unpack('!HHHH', img[12:20])
    return dict(clusters=n_cl, base_cluster=b_cl, maps=n_map, base_map=b_map)


def parse_map_rows(img):
    """AUDIO_MAP, 1722.1-2021 7.2.19: descriptor_type(2) descriptor_index(2)
    mappings_offset(2) number_of_mappings(2), then number_of_mappings x
    {mapping_stream_index, mapping_stream_channel, mapping_cluster_offset,
     mapping_cluster_channel} (2 bytes each)."""
    if len(img) < 8:
        return []
    off, n = struct.unpack('!HH', img[4:8])
    rows = []
    for k in range(n):
        o = off + 8 * k
        if o + 8 > len(img):
            break
        rows.append(struct.unpack('!HHHH', img[o:o + 8]))
    return rows


def parse_cluster_name(img):
    """AUDIO_CLUSTER, 7.2.16: object_name is the 64-byte field at descriptor
    offset 4."""
    if len(img) < 68:
        return ""
    return img[4:68].split(b'\0')[0].decode(errors='replace')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--iface', required=True)
    p.add_argument('--target-eid', required=True)
    p.add_argument('--target-mac', required=True)
    p.add_argument('--controller-eid', default='0011223344556677')
    p.add_argument('--max-ports', type=int, default=16,
                   help='highest STREAM_PORT index to probe (default 16)')
    p.add_argument('--allow-writes', action='store_true',
                   help='also exercise ADD_AUDIO_MAPPINGS on DYNAMIC ports '
                        '(number_of_maps == 0). This MUTATES the device; the '
                        'static half needs no such flag because a port with '
                        'Audio Maps refuses the command by definition.')
    a = p.parse_args()

    s = open_sock(a.iface)
    src = s.getsockname()[4][:6]
    pr = Probe(s, src, bytes.fromhex(a.target_mac.replace(':', '')),
               bytes.fromhex(a.target_eid), bytes.fromhex(a.controller_eid))

    print(f"=== hive_compliance_clusters {a.target_eid} on {a.iface} "
          f"(transport: {'shared' if _SHARED_TRANSPORT else 'local'}) ===")

    all_cluster_owners = {}          # global cluster index -> (dname, port)
    out_stream_keys = set()          # 7.2.19 output uniqueness, Configuration-wide
    any_port = False

    for dname, dcode in (('STREAM_PORT_INPUT', DESC_STREAM_PORT_INPUT),
                         ('STREAM_PORT_OUTPUT', DESC_STREAM_PORT_OUTPUT)):
        print(f"\n-- {dname} --")
        for i in range(a.max_ports):
            st, img = pr.read_desc(dcode, i)
            if st != ST_SUCCESS:
                break
            port = parse_port(img)
            if port is None:
                ck(False, f"C5 {dname}.{i} descriptor is 7.2.13-sized",
                   f"got {len(img)} bytes, need >= 20")
                continue
            any_port = True
            print(f"     {dname}.{i}: clusters={port['clusters']}@"
                  f"{port['base_cluster']} maps={port['maps']}@{port['base_map']}")

            # -- C5: every advertised cluster answers, and is owned once ----
            bad, dup = [], []
            for off in range(port['clusters']):
                idx = port['base_cluster'] + off
                cst, cimg = pr.read_desc(DESC_AUDIO_CLUSTER, idx)
                if cst != ST_SUCCESS:
                    bad.append((idx, cst))
                    continue
                if idx in all_cluster_owners:
                    dup.append((idx, all_cluster_owners[idx]))
                all_cluster_owners[idx] = (dname, i)
                if off < 3:
                    print(f"        cluster {idx} = "
                          f"'{parse_cluster_name(cimg)}'")
            ck(not bad, f"C5 {dname}.{i} every advertised AUDIO_CLUSTER "
                        f"answers READ_DESCRIPTOR (7.2.13)",
               f"unanswered={bad}" if bad else
               f"{port['clusters']} clusters from {port['base_cluster']}")
            ck(not dup, f"C5 {dname}.{i} cluster block does not overlap "
                        f"another port's (7.2.13)", f"shared={dup}")

            # -- C6: maps answer; rows are PORT-RELATIVE --------------------
            for k in range(port['maps']):
                midx = port['base_map'] + k
                mst, mimg = pr.read_desc(DESC_AUDIO_MAP, midx)
                ck(mst == ST_SUCCESS,
                   f"C6 {dname}.{i} declared AUDIO_MAP {midx} answers (7.2.13)",
                   f"status={mst}")
                if mst != ST_SUCCESS:
                    continue
                rows = parse_map_rows(mimg)
                oob = [r for r in rows if r[2] >= port['clusters']]
                ck(not oob,
                   f"C6 {dname}.{i} map {midx} offsets are PORT-RELATIVE "
                   f"(7.2.19)",
                   f"rows outside the {port['clusters']}-cluster block: {oob}"
                   if oob else f"{len(rows)} row(s), max offset "
                               f"{max([r[2] for r in rows], default=-1)}")
                # -- C7: 7.2.19 uniqueness --------------------------------
                if dcode == DESC_STREAM_PORT_INPUT:
                    keys = [(r[2], r[3]) for r in rows]
                    ck(len(keys) == len(set(keys)),
                       f"C7 {dname}.{i} map {midx}: <=1 entry per cluster "
                       f"channel (7.2.19)", f"keys={keys}")
                else:
                    clash = [(r[0], r[1]) for r in rows
                             if (r[0], r[1]) in out_stream_keys]
                    ck(not clash,
                       f"C7 {dname}.{i} map {midx}: <=1 entry per stream "
                       f"channel in the Configuration (7.2.19)",
                       f"already mapped: {clash}")
                    out_stream_keys.update((r[0], r[1]) for r in rows)

            # -- C8: Milan 5.4.2.27/28 posture ------------------------------
            # one well-formed record; on a port WITH maps this cannot mutate
            # anything because the command is refused by definition.
            addp = struct.pack('!HHHH', dcode, i, 1, 0) + \
                struct.pack('!HHHH', 0, 0, 0, 0)
            if port['maps'] > 0:
                ast, _, _ = pr.cmd(CMD_ADD_AUDIO_MAPPINGS, addp)
                ck(ast == ST_NOT_SUPPORTED,
                   f"C8 {dname}.{i} HAS Audio Maps -> ADD_AUDIO_MAPPINGS "
                   f"NOT_SUPPORTED (Milan 5.4.2.27/28 - conformance)",
                   f"status={ast}")
            elif a.allow_writes:
                ast, _, _ = pr.cmd(CMD_ADD_AUDIO_MAPPINGS, addp)
                ck(ast is not None and ast != ST_NOT_SUPPORTED,
                   f"C8 {dname}.{i} has NO Audio Map -> ADD_AUDIO_MAPPINGS "
                   f"is MANDATORY (Milan 5.4.2.27)", f"status={ast}")
                #: NOTE this probe deliberately does NOT assert SUCCESS -
                #: record {0,0,0,0} may be genuinely invalid on some ports.
                #: That tolerance is exactly why it could not see a device
                #: refusing every ODD count; C10 below is the check that can.
            else:
                skip(f"C8 {dname}.{i} dynamic-port ADD_AUDIO_MAPPINGS",
                     "number_of_maps == 0: the command MUTATES a live "
                     "device - re-run with --allow-writes")

            # -- C9: GET_AUDIO_MAP paging (read-only) -----------------------
            if port['maps'] == 0:
                gst, _, gpl = pr.cmd(CMD_GET_AUDIO_MAP,
                                     struct.pack('!HHHH', dcode, i, 0, 0))
                if gst != ST_SUCCESS or gpl is None or len(gpl) < 8:
                    skip(f"C9 {dname}.{i} GET_AUDIO_MAP paging",
                         f"map_index 0 answered status={gst}: nothing to "
                         "calibrate the page bound against")
                else:
                    # response: type(2) index(2) map_index(2) number_of_maps(2)
                    n_maps = struct.unpack('!H', gpl[6:8])[0]
                    bst, _, _ = pr.cmd(CMD_GET_AUDIO_MAP,
                                       struct.pack('!HHHH', dcode, i, n_maps, 0))
                    ck(bst == ST_BAD_ARGUMENTS,
                       f"C9 {dname}.{i} map_index == number_of_maps "
                       f"({n_maps}) -> BAD_ARGUMENTS (Milan 5.4.2.26, "
                       f"1722.1 7.4.44)", f"status={bst}")
            else:
                skip(f"C9 {dname}.{i} GET_AUDIO_MAP paging",
                     "static port (number_of_maps > 0): 5.4.2.26 paging "
                     "governs the DYNAMIC case")

            # -- C10: an ODD number_of_mappings is ordinary traffic ---------
            if port['maps'] > 0:
                skip(f"C10 {dname}.{i} single-mapping ADD",
                     "static port: 5.4.2.27 makes ADD NOT_SUPPORTED here")
            elif not a.allow_writes:
                skip(f"C10 {dname}.{i} single-mapping ADD",
                     "idempotent, but still a write - re-run with "
                     "--allow-writes")
            else:
                gst, _, gpl = pr.cmd(CMD_GET_AUDIO_MAP,
                                     struct.pack('!HHHH', dcode, i, 0, 0))
                live = []
                if gst == ST_SUCCESS and gpl is not None and len(gpl) >= 12:
                    n_rows = struct.unpack('!H', gpl[8:10])[0]
                    for r in range(n_rows):
                        o = 12 + 8 * r
                        if o + 8 <= len(gpl):
                            live.append(struct.unpack('!HHHH', gpl[o:o + 8]))
                if not live:
                    skip(f"C10 {dname}.{i} single-mapping ADD",
                         "the port reports no dynamic mapping to re-ADD "
                         "idempotently")
                else:
                    one = live[0]
                    one_pl = struct.pack('!HHHH', dcode, i, 1, 0) + \
                        struct.pack('!HHHH', *one)
                    ost, _, _ = pr.cmd(CMD_ADD_AUDIO_MAPPINGS, one_pl)
                    ck(ost == ST_SUCCESS,
                       f"C10 {dname}.{i} ADD of ONE mapping the device "
                       f"itself reports {one} is accepted "
                       f"(7.4.45: number_of_mappings is bounded by the "
                       f"PDU, not by parity)", f"status={ost}")
                    #: and the same for REMOVE's count rule, put straight
                    #: back so the device is left as it was found
                    rst, _, _ = pr.cmd(CMD_REMOVE_AUDIO_MAPPINGS, one_pl)
                    ck(rst == ST_SUCCESS,
                       f"C10 {dname}.{i} REMOVE of that ONE mapping is "
                       f"accepted (7.4.46)", f"status={rst}")
                    if rst == ST_SUCCESS:
                        bst2, _, _ = pr.cmd(CMD_ADD_AUDIO_MAPPINGS, one_pl)
                        ck(bst2 == ST_SUCCESS,
                           f"C10 {dname}.{i} single-mapping ADD restores it "
                           f"(device left as found)", f"status={bst2}")

        # boundary: one past the last port that answered
        pass

    if not any_port:
        print("\n  [skip] no STREAM_PORT descriptor answered - this entity "
              "exposes no audio ports, so C5-C9 have nothing to check")

    print("\n----------------------------------------")
    print(f"checks: {CHECKS[0]}   failures: {len(FAILS)}   skipped: {len(SKIPS)}")
    for f in FAILS:
        print(f"  FAIL {f}")
    print("RESULT:", "PASS" if not FAILS else "FAIL")
    return 1 if FAILS else 0


if __name__ == '__main__':
    sys.exit(main())
