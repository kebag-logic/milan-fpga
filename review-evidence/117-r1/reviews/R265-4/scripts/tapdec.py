#!/usr/bin/env python3
"""Independent decoder for the issue 117 tap and host captures (reviewer-written).

Library only. Reads little-endian pcap (usec or nsec). A tapped record carries a
28-octet envelope: u32 tag 6, u32 length, u32 tap port (3 = DUT sent, 2 = far end
sent), u32 unused, u32 tap nanoseconds modulo 2^32, 8 octets of lengths, then the
Ethernet frame. Records without that envelope are the capture host's own traffic.
Host captures (no envelope) are decoded as plain Ethernet with port None.
"""
import struct

WRAP = 1 << 32


def pcap_records(path):
    raw = open(path, 'rb').read()
    magic = struct.unpack('<I', raw[:4])[0]
    if magic not in (0xA1B2C3D4, 0xA1B23C4D):
        raise SystemExit(f'{path}: not a little-endian pcap')
    nano = magic == 0xA1B23C4D
    off = 24
    while off + 16 <= len(raw):
        s, f, incl, _ = struct.unpack('<IIII', raw[off:off + 16])
        off += 16
        yield s * 10**9 + (f if nano else f * 1000), raw[off:off + incl]
        off += incl


def tap_records(path):
    """Returns (records, n_envelope_less). Each record: dict host_ns, tap_ns, port, frame."""
    recs, noenv, first = [], 0, None
    for host_ns, pkt in pcap_records(path):
        if len(pkt) >= 42:
            tag, _l, port = struct.unpack('<III', pkt[:12])
        else:
            tag = port = None
        if tag != 6 or port not in (2, 3):
            noenv += 1
            continue
        lo = struct.unpack('<I', pkt[16:20])[0]
        if first is None:
            first = (host_ns, lo)
        k = round(((host_ns - first[0]) - (lo - first[1])) / WRAP)
        recs.append(dict(host_ns=host_ns, tap_ns=lo - first[1] + k * WRAP, port=port, frame=pkt[28:]))
    return recs, noenv


def host_records(path):
    return [dict(host_ns=h, tap_ns=None, port=None, frame=p) for h, p in pcap_records(path)]


def fit_tap_to_host(recs, win_ns=5 * 10**9, drop_ms=1.0):
    """Least-squares line through per-window minima of (host - tap); iteratively
    drops minima more than drop_ms above the line. Returns (a, b, used, total, resid_max_ms)
    with host_ns ~= tap_ns + a + b * tap_ns."""
    if not recs:
        return None
    h0 = recs[0]['host_ns']
    wins = {}
    for r in recs:
        w = (r['host_ns'] - h0) // win_ns
        d = r['host_ns'] - r['tap_ns']
        if w not in wins or d < wins[w][1]:
            wins[w] = (r['tap_ns'], d)
    pts = sorted(wins.values())
    total = len(pts)
    while True:
        n = len(pts)
        mx = sum(p[0] for p in pts) / n
        my = sum(p[1] for p in pts) / n
        sxx = sum((p[0] - mx) ** 2 for p in pts) or 1
        b = sum((p[0] - mx) * (p[1] - my) for p in pts) / sxx
        a = my - b * mx
        res = [(p[1] - (a + b * p[0])) / 1e6 for p in pts]
        worst = max(range(n), key=lambda i: res[i])
        if res[worst] > drop_ms and n > 3:
            pts.pop(worst)
            continue
        return a, b, n, total, max(abs(x) for x in res)


def fit_consensus(recs, win_ns=5 * 10**9, tol_ms=2.5):
    """Line with the most per-window minima within tol_ms (pairwise search), then least squares
    over those inliers. Returns (a, b, used, total, resid_max_ms) like fit_tap_to_host."""
    if not recs:
        return None
    h0 = recs[0]['host_ns']
    wins = {}
    for r in recs:
        w = (r['host_ns'] - h0) // win_ns
        d = r['host_ns'] - r['tap_ns']
        if w not in wins or d < wins[w][1]:
            wins[w] = (r['tap_ns'], d)
    pts = sorted(wins.values())
    best = None
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            (x1, y1), (x2, y2) = pts[i], pts[j]
            if x2 == x1:
                continue
            b = (y2 - y1) / (x2 - x1)
            a = y1 - b * x1
            inl = [p for p in pts if abs(p[1] - (a + b * p[0])) <= tol_ms * 1e6]
            if best is None or len(inl) > len(best):
                best = inl
    q = best
    n = len(q)
    mx = sum(p[0] for p in q) / n
    my = sum(p[1] for p in q) / n
    sxx = sum((p[0] - mx) ** 2 for p in q) or 1
    b = sum((p[0] - mx) * (p[1] - my) for p in q) / sxx
    a = my - b * mx
    return a, b, n, len(pts), max(abs(p[1] - (a + b * p[0])) / 1e6 for p in q)


def tap_to_host(r, fit):
    a, b = fit[0], fit[1]
    return r['tap_ns'] + a + b * r['tap_ns']


def ts10(b):
    return int.from_bytes(b[0:6], 'big') * 10**9 + int.from_bytes(b[6:10], 'big')


PTP = {0x0: 'Sync', 0x2: 'Pdelay_Req', 0x3: 'Pdelay_Resp', 0x8: 'Follow_Up',
       0xA: 'Pdelay_Resp_Follow_Up', 0xB: 'Announce', 0xC: 'Signaling'}


def decode(fr):
    d = dict(dst=fr[0:6].hex(), src=fr[6:12].hex())
    et = struct.unpack('>H', fr[12:14])[0]
    p = fr[14:]
    d['vlan'] = None
    if et == 0x8100:
        tci = struct.unpack('>H', p[0:2])[0]
        d['vlan'] = (tci >> 13, tci & 0xFFF)
        et = struct.unpack('>H', p[2:4])[0]
        p = p[4:]
    d['et'] = et
    if et == 0x88F7 and len(p) >= 34:
        mt = p[0] & 0xF
        d['kind'] = 'gPTP ' + PTP.get(mt, hex(mt))
        d['mt'] = mt
        d['domain'] = p[4]
        d['corr_ns'] = struct.unpack('>q', p[8:16])[0] / 65536.0
        d['spi'] = p[20:28].hex() + ':' + '%04x' % struct.unpack('>H', p[28:30])[0]
        d['seq'] = struct.unpack('>H', p[30:32])[0]
        d['lmi'] = struct.unpack('b', p[33:34])[0]
        if mt == 0xB and len(p) >= 64:
            d['prio1'] = p[47]
            d['cclass'] = p[48]
            d['cacc'] = p[49]
            d['cvar'] = struct.unpack('>H', p[50:52])[0]
            d['prio2'] = p[52]
            d['gm'] = p[53:61].hex()
            d['steps'] = struct.unpack('>H', p[61:63])[0]
            d['tsrc'] = p[63]
            tl = []
            q = p[64:]
            while len(q) >= 4:
                t, ln = struct.unpack('>HH', q[:4])
                if t == 0x8:
                    tl = [q[4 + i:12 + i].hex() for i in range(0, ln, 8)]
                q = q[4 + ln:]
            d['path'] = tl
        if mt in (0x3, 0xA) and len(p) >= 54:
            d['t'] = ts10(p[34:44])
            d['req_spi'] = p[44:52].hex() + ':' + '%04x' % struct.unpack('>H', p[52:54])[0]
        if mt == 0x8 and len(p) >= 44:
            d['t'] = ts10(p[34:44])
    elif et == 0x22F0 and len(p) >= 12:
        st = p[0]
        d['subtype'] = st
        if st == 0x04:
            d['kind'] = 'CRF'
            d['tu'] = p[1] & 0x01
            d['seqnum'] = p[2]
            d['stream_id'] = p[4:12].hex()
        elif st == 0xFA:
            d['kind'] = 'ADP'
            d['adp_mt'] = p[1] & 0x0F
            d['eid'] = p[4:12].hex()
            if len(p) >= 48:
                d['avail'] = struct.unpack('>I', p[36:40])[0]
                d['adp_gm'] = p[40:48].hex()
        elif st == 0xFB:
            d['kind'] = 'AECP'
            d['aecp_mt'] = p[1] & 0x0F
            d['target'] = p[4:12].hex()
            if len(p) >= 24:
                d['ctrl'] = p[12:20].hex()
                d['cmd'] = struct.unpack('>H', p[22:24])[0] & 0x7FFF
        elif st == 0xFC:
            d['kind'] = 'ACMP'
            d['acmp_mt'] = p[1] & 0x0F
            d['status'] = p[2] >> 3
            if len(p) >= 44:
                d['talker'] = p[20:28].hex()
                d['listener'] = p[28:36].hex()
        elif st == 0xFE:
            d['kind'] = 'MAAP'
        else:
            d['kind'] = 'AVTP 0x%02x' % st
    elif et == 0x22EA:
        d['kind'] = 'MSRP'
    elif et == 0x22EB:
        d['kind'] = 'MVRP'
    elif et == 0x88CC:
        d['kind'] = 'LLDP'
    elif et == 0x0806 and len(p) >= 28:
        d['kind'] = 'ARP'
        d['arp_op'] = struct.unpack('>H', p[6:8])[0]
        d['arp_sha'] = p[8:14].hex()
        d['arp_spa'] = '.'.join(str(x) for x in p[14:18])
        d['arp_tpa'] = '.'.join(str(x) for x in p[24:28])
    elif et == 0x0800 and len(p) >= 20:
        ihl = (p[0] & 0xF) * 4
        proto = p[9]
        d['ip_src'] = '.'.join(str(x) for x in p[12:16])
        d['ip_dst'] = '.'.join(str(x) for x in p[16:20])
        d['proto'] = proto
        q = p[ihl:]
        if proto == 17 and len(q) >= 8:
            sp, dp = struct.unpack('>HH', q[:4])
            d['sport'], d['dport'] = sp, dp
            d['udp'] = q[8:]
            d['kind'] = 'mDNS' if 5353 in (sp, dp) else ('DHCP' if {sp, dp} & {67, 68} else 'UDP')
        elif proto == 6 and len(q) >= 20:
            d['sport'], d['dport'] = struct.unpack('>HH', q[:4])
            d['tcp_flags'] = q[13]
            d['kind'] = 'TCP'
        elif proto == 2:
            d['kind'] = 'IGMP'
            d['igmp_type'] = q[0] if q else None
        else:
            d['kind'] = 'IPv4 proto %d' % proto
    elif et == 0x86DD:
        d['kind'] = 'IPv6'
        if len(p) >= 40:
            d['nh'] = p[6]
            q = p[40:]
            if p[6] == 17 and len(q) >= 8:
                sp, dp = struct.unpack('>HH', q[:4])
                d['sport'], d['dport'] = sp, dp
                d['udp'] = q[8:]
                if 5353 in (sp, dp):
                    d['kind'] = 'mDNS6'
    else:
        d['kind'] = 'et 0x%04x' % et
    return d


def dns_name(msg, off, depth=0):
    labels = []
    while off < len(msg) and depth < 20:
        ln = msg[off]
        if ln == 0:
            return labels, off + 1
        if ln & 0xC0 == 0xC0:
            ptr = ((ln & 0x3F) << 8) | msg[off + 1]
            sub, _ = dns_name(msg, ptr, depth + 1)
            return labels + sub, off + 2
        labels.append(msg[off + 1:off + 1 + ln])
        off += 1 + ln
    return labels, off


def dns_records(msg):
    """Yields (section, name_labels, rtype, rdata_bytes, rdata_offset)."""
    if len(msg) < 12:
        return
    qd, an, ns, ar = struct.unpack('>HHHH', msg[4:12])
    off = 12
    for _ in range(qd):
        name, off = dns_name(msg, off)
        if off + 4 > len(msg):
            return
        yield 'q', name, struct.unpack('>H', msg[off:off + 2])[0], b'', off
        off += 4
    for sec, cnt in (('an', an), ('ns', ns), ('ar', ar)):
        for _ in range(cnt):
            name, off = dns_name(msg, off)
            if off + 10 > len(msg):
                return
            rt, _c, _ttl, rdl = struct.unpack('>HHIH', msg[off:off + 10])
            off += 10
            yield sec, name, rt, msg[off:off + rdl], off
            off += rdl
