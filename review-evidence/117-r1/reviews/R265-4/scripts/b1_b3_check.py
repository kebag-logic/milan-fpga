#!/usr/bin/env python3
"""Check the page's B1/B3 and observation 5 statements about the bench switch against captures.

usage: b1_b3_check.py <archive-root: .../review-evidence/117-r1> [<original-archive-root>]
For every A202 capture (tap and controller-host port, attempt 1, cycles 1-6, final) and the
A200 captures: classifies the switch's IPv4/ARP/IGMP/mDNS/DHCP traffic by source MAC. The
switch's MACs are the sources of gPTP Announce with the switch's grandmaster identity and any
MAC sharing its OUI and upper octets. With a second (pre-redaction) archive root, it also
reports, per capture, whether a DNS-SD TXT record from the switch carries a firmware key and
whether that capture's published copy still carries it. Prints structure and counts only,
never TXT values, host names or firmware strings.
"""
import collections
import glob
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tapdec  # noqa: E402

root = sys.argv[1]
orig = sys.argv[2] if len(sys.argv) > 2 else None
SW_GM = '3cc0c6fffefe0210'


def frames(path):
    recs, noenv = tapdec.tap_records(path)
    if recs:
        return [(r['host_ns'], r['port'], r['frame']) for r in recs]
    return [(h, None, p) for h, p in tapdec.pcap_records(path)]


def classify(path):
    fr = frames(path)
    sw_macs = set()
    for h, port, f in fr:
        d = tapdec.decode(f)
        if d.get('kind') == 'gPTP Announce' and d.get('gm') == SW_GM:
            sw_macs.add(d['src'])
    out = collections.OrderedDict()
    out['switch_gptp_macs'] = sorted(sw_macs)
    ip = collections.Counter()
    arp = []
    igmp_src = collections.Counter()
    dhcp = []
    mdns = []
    tcp = collections.Counter()
    for h, port, f in fr:
        d = tapdec.decode(f)
        src = d['src']
        # a switch-owned MAC: same first four octets as its gPTP MAC
        own = any(src[:8] == m[:8] for m in sw_macs) if sw_macs else src.startswith('3cc0c6')
        k = d.get('kind')
        if k == 'ARP' and own:
            arp.append((h / 1e9, d['arp_op'], d['arp_spa'], d['arp_tpa']))
        elif k == 'IGMP' and own:
            igmp_src[d['ip_src']] += 1
        elif k == 'DHCP' and own:
            dhcp.append(h / 1e9)
        elif k == 'mDNS' and own:
            msg = d['udp']
            flags = struct.unpack('>H', msg[2:4])[0] if len(msg) >= 4 else 0
            recs = list(tapdec.dns_records(msg))
            kinds = collections.Counter()
            srv_tcp = False
            txt_n = 0
            for sec, name, rt, rdata, off in recs:
                kinds[(sec, rt)] += 1
                labels = [x.decode('latin-1') for x in name]
                if rt == 33 and any(l == '_tcp' for l in labels):
                    srv_tcp = True
                if rt == 16:
                    txt_n += 1
            mdns.append((h / 1e9, d['ip_src'], bool(flags & 0x8000), srv_tcp, txt_n, dict(kinds)))
        elif k == 'TCP':
            tcp[(d['ip_src'], d['ip_dst'], d['dport'])] += 1
        if 'ip_src' in d and own:
            ip[d['ip_src']] += 1
    def cls(a):
        return a if a in ('0.0.0.0',) else ('169.254.x.x (link-local)' if a.startswith('169.254.') else 'second IPv4 address (value withheld)')
    ipc = collections.Counter()
    for a, c in ip.items():
        ipc[cls(a)] += c
    out['ipv4_sources_from_switch_macs'] = dict(ipc)
    out['arp_from_switch'] = [(round(a[0] - fr[0][0] / 1e9, 2), 'probe' if a[2] == '0.0.0.0' else ('announce' if a[2] == a[3] else 'op%d' % a[1]), a[2] if a[2] == '0.0.0.0' else a[2].split('.')[0] + '.' + a[2].split('.')[1] + '.x.x') for a in arp]
    ig = collections.Counter()
    for a, c in igmp_src.items():
        ig[cls(a)] += c
    out['igmp_sources_from_switch'] = dict(ig)
    ds = sorted(dhcp)
    out['dhcp_from_switch'] = len(ds)
    out['dhcp_intervals_s'] = [round(b - a, 2) for a, b in zip(ds, ds[1:])]
    out['mdns_from_switch'] = [(round(m[0] - fr[0][0] / 1e9, 2), 'response' if m[2] else 'query', 'SRV _tcp' if m[3] else '-', 'TXT x%d' % m[4]) for m in mdns]
    out['tcp_flows_any'] = len(tcp)
    out['tcp_to_or_from_link_local'] = sum(c for (s, dst, p), c in tcp.items() if s.startswith('169.254.') or dst.startswith('169.254.'))
    return out


def txt_keys(path):
    """Structure-only view of DNS-SD TXT keys from the switch: count of TXT strings whose key
    contains 'firmware' (key name only, compared case-insensitively)."""
    n = 0
    for h, port, f in frames(path):
        d = tapdec.decode(f)
        if d.get('kind') != 'mDNS':
            continue
        for sec, name, rt, rdata, off in tapdec.dns_records(d['udp']):
            if rt != 16:
                continue
            i = 0
            while i < len(rdata):
                ln = rdata[i]
                s = rdata[i + 1:i + 1 + ln]
                if s.split(b'=')[0].lower().find(b'firmware') >= 0:
                    n += 1
                i += 1 + ln
    return n


def main():
    paths = sorted(glob.glob(os.path.join(root, 'bench-a202', 'bench', '*', '*.pcap')) +
                   glob.glob(os.path.join(root, 'bench-a200', 'bench', '*.pcap')) +
                   glob.glob(os.path.join(root, 'bench-a200', 'bench', '*', '*.pcap')))
    for p in paths:
        rel = os.path.relpath(p, root)
        r = classify(p)
        print('==', rel)
        for k, v in r.items():
            if k == 'arp_from_switch':
                c = collections.Counter((x[1], x[2]) for x in v)
                print('  ', k, dict(c))
            elif k == 'mdns_from_switch':
                c = collections.Counter(x[1:] for x in v)
                print('  ', k, dict(c))
            elif k == 'dhcp_intervals_s':
                print('  ', k, (min(v), max(v), round(sum(v) / len(v), 2)) if v else [])
            else:
                print('  ', k, v)
        if orig:
            op = os.path.join(orig, rel)
            if os.path.exists(op):
                print('   firmware-key TXT strings: original', txt_keys(op), 'published', txt_keys(p))


if __name__ == '__main__':
    main()
