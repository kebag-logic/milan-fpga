#!/usr/bin/env python3
"""Private-token scrub of a published evidence tree, with tokens harvested at run time.

Tokens are harvested from PRIVATE sources given on the command line (the
retained raw captures, the unredacted round-1 packet) and from the local
environment, then every file of each TARGET is scanned byte-wise and
case-insensitively. A token that already appears in the public repository at
the reviewed head is allowlisted (the DUT, peer and switch identities, the
multicast addresses). Nothing private is printed, not even a hash of a token
(a MAC hash prefix is brute-forceable): each token is shown only as its kind and
a label drawn from a keyed digest whose random key is discarded at exit.

Kinds: host MAC (colon, hyphen, plain, dotted and EUI-64 forms, and the
modified EUI-64 with the U/L bit flipped), clock identity (EUI-64 and the
dotted gPTP form), interface name, account name, host name, home path.

usage: scrub_packet.py --repo <repo-at-head> --private <dir> [--private <dir> ...] --target <name>=<dir> [...]
exit 1 when any target has a hit.
"""
import argparse
import getpass
import hashlib
import hmac
import os
import re
import socket
import struct
import subprocess
from collections import defaultdict
from pathlib import Path

MAC_RE = re.compile(rb"(?<![0-9a-f:])((?:[0-9a-f]{2}[:-]){5}[0-9a-f]{2})(?![0-9a-f:])", re.I)
EUI_RE = re.compile(rb"(?<![0-9a-f])([0-9a-f]{6}fffe[0-9a-f]{6})(?![0-9a-f])", re.I)
DOT_RE = re.compile(rb"(?<![0-9a-f])([0-9a-f]{6})\.fffe\.([0-9a-f]{6})(?![0-9a-f])", re.I)
IF_RE = re.compile(rb"\b(en[opsx][0-9a-z]{1,16}|eth[0-9]{1,3}|wl[a-z][0-9a-z]{1,14}|enx[0-9a-f]{12})\b")
HOME_RE = re.compile(rb"/home/([A-Za-z_][\w.-]{0,31})")
OWNER_RE = re.compile(rb"^[-dlcbps][rwxsStT-]{9}[.+@]?\s+\d+\s+([A-Za-z_][\w.-]*)\s+([A-Za-z_][\w.-]*)\s", re.M)
PROMPT_RE = re.compile(rb"\b([a-z_][\w.-]{0,31})@([A-Za-z][\w-]{1,62})\b")
START_IF_RE = re.compile(rb'"argv": \["\w+", "([^"]+)"')
GENERIC = {b"root", b"nobody", b"daemon", b"users", b"wheel", b"git", b"github", b"noreply", b"example", b"localhost"}


_KEY = os.urandom(32)


def h8(tok):
    return "t" + hmac.new(_KEY, tok, hashlib.sha256).hexdigest()[:6]


def mac_forms(hex12):
    h = hex12.lower()
    b = [h[i:i + 2] for i in range(0, 12, 2)]
    flip = "%02x" % (int(b[0], 16) ^ 2)
    forms = {":".join(b), "-".join(b), h, f"{h[:4]}.{h[4:8]}.{h[8:]}",
             f"{h[:6]}fffe{h[6:]}", f"{h[:6]}.fffe.{h[6:]}", f"{flip}{h[2:6]}fffe{h[6:]}",
             f"{flip}{b[1]}:{b[2]}ff:fe{b[3]}:{b[4]}{b[5]}"}
    return {f.encode() for f in forms}


def pcap_macs(p):
    out = set()
    data = p.read_bytes()
    if len(data) < 24:
        return out
    magic = data[:4]
    if magic in (b"\xd4\xc3\xb2\xa1", b"\x4d\x3c\xb2\xa1"):
        e = "<"
    elif magic in (b"\xa1\xb2\xc3\xd4", b"\xa1\xb2\x3c\x4d"):
        e = ">"
    else:
        return out
    off = 24
    while off + 16 <= len(data):
        _, _, incl, _ = struct.unpack(e + "IIII", data[off:off + 16])
        pkt = data[off + 16:off + 16 + incl]
        if len(pkt) >= 12:
            out.add(pkt[0:6].hex())
            out.add(pkt[6:12].hex())
        off += 16 + incl
    return out


def harvest(private_dirs):
    macs, euis, ifs, accts, hosts = set(), set(), set(), set(), set()
    for d in private_dirs:
        for p in Path(d).rglob("*"):
            if not p.is_file():
                continue
            if p.suffix == ".pcap":
                macs |= pcap_macs(p)
                continue
            b = p.read_bytes()
            macs |= {m.replace(b":", b"").replace(b"-", b"").lower().decode() for m in MAC_RE.findall(b)}
            euis |= {m.lower().decode() for m in EUI_RE.findall(b)}
            euis |= {(a + b"fffe" + c).lower().decode() for a, c in DOT_RE.findall(b)}
            ifs |= set(IF_RE.findall(b)) | set(START_IF_RE.findall(b))
            accts |= set(HOME_RE.findall(b))
            for o, g in OWNER_RE.findall(b):
                accts |= {o, g}
            for u, hname in PROMPT_RE.findall(b):
                accts.add(u)
                hosts.add(hname)
    accts.add(getpass.getuser().encode())
    hosts.add(socket.gethostname().split(".")[0].encode())
    accts -= GENERIC
    hosts -= GENERIC
    tokens = {}
    for m in macs:
        if m[:4] == "0000" or m == "ffffffffffff" or int(m[:2], 16) & 1:
            continue  # 00:00:xx OUI (payload fragments), broadcast, multicast: not a host NIC
        for f in mac_forms(m):
            tokens[f] = ("host MAC", m.encode())
    for e in euis:
        tokens[e.encode()] = ("clock identity", e.encode())
        tokens[f"{e[:6]}.fffe.{e[10:]}".encode()] = ("clock identity", e.encode())
    for i in ifs:
        tokens[i] = ("interface name", i)
    for a in accts:
        if len(a) >= 3:
            tokens[b"/home/" + a] = ("home path", a)
            tokens[a] = ("account name", a)
    for hname in hosts:
        if len(hname) >= 3:
            tokens[hname] = ("host name", hname)
    return tokens


def public(repo, tokens):
    """Tokens already in the tracked tree at the reviewed head are public by definition."""
    pub = set()
    for tok, (kind, base) in tokens.items():
        if kind in ("account name", "host name"):
            continue  # a common word may appear in the tree by accident; never allowlist these
        r = subprocess.run(["git", "-C", repo, "grep", "-I", "-q", "-i", "-F", tok.decode(errors="ignore"), "HEAD", "--", "docs"],
                           capture_output=True)
        if r.returncode == 0:
            pub.add(base)
    return pub


def scan(root, tokens, pub):
    hits = defaultdict(list)
    n = 0
    for p in sorted(Path(root).rglob("*")):
        if not p.is_file() or ".git" in p.parts:
            continue
        n += 1
        low = p.read_bytes().lower()
        for tok, (kind, base) in tokens.items():
            if base in pub:
                continue
            t = tok.lower()
            if kind in ("account name", "host name"):
                ms = [m.start() for m in re.finditer(rb"(?<![\w.-])" + re.escape(t) + rb"(?![\w])", low)]
            else:
                # a bare hex form counts standalone and embedded in a longer hex run alike
                ms = [m.start() for m in re.finditer(re.escape(t), low)]
            for s in ms:
                line = low.count(b"\n", 0, s) + 1
                hits[(kind, h8(base))].append(f"{p.relative_to(root).as_posix()}:{line}")
    return n, hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--private", action="append", default=[])
    ap.add_argument("--target", action="append", default=[])
    a = ap.parse_args()
    tokens = harvest(a.private)
    pub = public(a.repo, tokens)
    kinds = defaultdict(set)
    for tok, (kind, base) in tokens.items():
        kinds[kind].add(base)
    print("harvested private-token bases by kind (allowlisted public ones in brackets):")
    for k in sorted(kinds):
        print(f"  {k}: {len(kinds[k])} [{len(kinds[k] & pub)} public]")
    bad = 0
    for spec in a.target:
        name, root = spec.split("=", 1)
        n, hits = scan(root, tokens, pub)
        total = sum(len(v) for v in hits.values())
        bad += total
        print(f"\nTARGET {name}: {n} files scanned, {total} private-token hits")
        for (kind, hh), locs in sorted(hits.items()):
            print(f"  {kind} #{hh}: {len(locs)} at {', '.join(locs[:6])}{' ...' if len(locs) > 6 else ''}")
    print(f"\nTOTAL hits {bad}")
    raise SystemExit(1 if bad else 0)


if __name__ == "__main__":
    main()
