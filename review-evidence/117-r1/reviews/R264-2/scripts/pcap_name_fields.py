#!/usr/bin/env python3
"""Inventory name-bearing fields in every capture under ROOT: DHCP options
12/15/60/77/81 (any source), mDNS/LLMNR/NBNS UDP payloads, and LLDP TLVs 5/6
(system name/description). For each (file, field, source MAC OUI) report the
number of occurrences, whether the value is all '#' (redacted) and a masked
shape (letters->a/A, digits->9). Values are never printed.

usage: pcap_name_fields.py ROOT
Source MACs are reported by role, never by OUI: 'switch-family' is the OUI of
the grandmaster clock identity, 'controller-host' the OUI of the controller
EUI in the watcher logs, anything else 'other-host'.
"""
import sys, os, struct, re, collections, json, glob
root = sys.argv[1]
GM_OUI = '3cc0c6'  # first three octets of the grandmaster clock identity quoted on the page
ctl = set()
for w in glob.glob(os.path.join(root, '**', '*watch*.jsonl'), recursive=True):
    for ln in open(w):
        o = json.loads(ln)
        if o.get('controller_eid'):
            ctl.add(o['controller_eid'][:6])


def role(oui):
    return 'switch-family' if oui == GM_OUI else ('controller-host' if oui in ctl else 'other-host')


def shape(v):
    s = re.sub(rb'[a-z]', b'a', re.sub(rb'[A-Z]', b'A', re.sub(rb'[0-9]', b'9', v)))
    return s.decode('latin-1')[:40]


out = collections.Counter()
for dp, dn, fn in os.walk(root):
    for f in sorted(fn):
        if not f.endswith('.pcap'):
            continue
        p = os.path.join(dp, f)
        rel = os.path.relpath(p, root)
        raw = open(p, 'rb').read()
        off = 24
        while off + 16 <= len(raw):
            _s, _f, incl, _o = struct.unpack('<IIII', raw[off:off + 16])
            rec = raw[off + 16:off + 16 + incl]
            off += 16 + incl
            fr = rec[28:] if rec[:4] == b'\x06\x00\x00\x00' else rec
            if len(fr) < 14:
                continue
            src_oui = role(fr[6:9].hex())
            et = fr[12:14]
            pl = fr[14:]
            if et == b'\x81\x00':
                et, pl = fr[16:18], fr[18:]
            if et == b'\x08\x00' and len(pl) > 28:
                ihl = (pl[0] & 15) * 4
                if pl[9] != 17:
                    continue
                sp, dpp = struct.unpack('>HH', pl[ihl:ihl + 4])
                u = pl[ihl + 8:]
                if (sp, dpp) in ((68, 67), (67, 68)) and len(u) > 240:
                    o = 240
                    while o < len(u) and u[o] != 255:
                        if u[o] == 0:
                            o += 1
                            continue
                        c, l = u[o], u[o + 1]
                        v = u[o + 2:o + 2 + l]
                        if c in (12, 15, 60, 77, 81):
                            red = 'redacted' if v and set(v) <= {35} else ('partly-#' if b'#' in v else 'clear')
                            out[(rel, 'dhcp-opt%d' % c, src_oui, red, shape(v))] += 1
                        o += 2 + l
                elif 5353 in (sp, dpp) or 5355 in (sp, dpp) or 137 in (sp, dpp):
                    red = 'partly-#' if b'#' in u else 'clear'
                    names = re.findall(rb'[A-Za-z][A-Za-z0-9-]{3,}', u)
                    out[(rel, 'mdns/llmnr/nbns udp%d' % dpp, src_oui, red, ' '.join(shape(n) for n in names[:3]))] += 1
            elif et == b'\x86\xdd' and len(pl) > 48 and pl[6] == 17:
                sp, dpp = struct.unpack('>HH', pl[40:44])
                u = pl[48:]
                if 5353 in (sp, dpp) or 547 in (sp, dpp):
                    red = 'partly-#' if b'#' in u else 'clear'
                    names = re.findall(rb'[A-Za-z][A-Za-z0-9-]{3,}', u)
                    out[(rel, 'v6 udp%d' % dpp, src_oui, red, ' '.join(shape(n) for n in names[:3]))] += 1
            elif et == b'\x88\xcc':
                o = 0
                while o + 2 <= len(pl):
                    h = struct.unpack('>H', pl[o:o + 2])[0]
                    t, l = h >> 9, h & 0x1FF
                    v = pl[o + 2:o + 2 + l]
                    if t == 0:
                        break
                    if t in (5, 6, 4):
                        red = 'redacted' if v and set(v) <= {35} else ('partly-#' if b'#' in v else 'clear')
                        out[(rel, 'lldp-tlv%d' % t, src_oui, red, shape(v))] += 1
                    o += 2 + l
for k, v in sorted(out.items()):
    print(v, *k)
