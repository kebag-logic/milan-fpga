#!/usr/bin/env python3
"""Label-only private-name scan for the B5 round 4 output.

usage: b5_scan.py <local_lane_packet> <published_lane_packet> <manifest.json>
                  <repo> <range>[,<range>...] <path>... < labelled_patterns.json

The private literals are built in memory and never written:
  - every value the archive mask replaced, recovered by matching each masked
    line of a path_redacted lane-packet file against the local original;
  - the local host names (this host, /etc/hosts, ssh client config).
stdin carries {"patterns": [[label, regex], ...], "controls": [text, ...]}
(vendors, link types, clock-topology words, tool and model names, and one
sample line per pattern) so those spellings stay out of every file. MAC
addresses, home directories and interface-name forms are built in.

Positive control, in memory before the scan: every private literal is
planted in a line and must hit its own pattern, and every labelled pattern
must hit at least one control line. The scan refuses to run otherwise.

Searched, case-insensitively: every file under each <path>, the lines each
range adds, and each range's commit messages. A hit prints the label, the
place and the line number, never the matched text.
"""
import glob
import json
import os
import re
import socket
import subprocess
import sys

LAB = re.compile(r"<[a-z0-9-]+>")


def masked_values(local, pub, manifest):
    vals = {}
    for e in json.load(open(manifest)):
        if not (e["file"].startswith("author/") and e.get("path_redacted")):
            continue
        rel = e["file"][len("author/"):]
        orig = open(os.path.join(local, rel), errors="replace").read().splitlines()
        for pl in open(os.path.join(pub, rel), errors="replace").read().splitlines():
            labs = LAB.findall(pl)
            if not labs:
                continue
            parts = re.split(r"(<[a-z0-9-]+>)", pl)
            rx = "^" + "".join(re.escape(x) if i % 2 == 0 else "(.+?)"
                               for i, x in enumerate(parts)) + "$"
            for ol in orig:
                m = re.match(rx, ol)
                if m:
                    for lab, v in zip(labs, m.groups()):
                        if v != lab and len(v) >= 3 and not re.fullmatch(r"[\d ,\[\]]+", v):
                            vals.setdefault(v, lab.strip("<>"))
                    break
    return vals


def host_names():
    hs = {socket.gethostname().split(".")[0]}
    for line in open("/etc/hosts"):
        for n in line.split("#")[0].split()[1:]:
            if not (n.startswith("localhost") or n.startswith("ip6-")):
                hs.add(n.split(".")[0])
    for f in glob.glob(os.path.join(os.path.expanduser("~"), ".ssh", "config")):
        for line in open(f, errors="replace"):
            t = line.split()
            if len(t) >= 2 and t[0].lower() in ("host", "hostname"):
                hs.update(n.split(".")[0] for n in t[1:]
                          if "*" not in n and not re.fullmatch(r"[\d.]+", n))
    return {h for h in hs if len(h) >= 3}


def main():
    local, pub, manifest, repo, ranges = sys.argv[1:6]
    paths = sys.argv[6:]
    lits = masked_values(local, pub, manifest)
    hosts = sorted(host_names())
    pats = [(lab, re.compile(re.escape(v), re.I)) for v, lab in lits.items()]
    pats += [("host name", re.compile(r"(?<![\w-])" + re.escape(h) + r"(?![\w-])", re.I))
             for h in hosts]
    n_private = len(pats)
    # positive control for the private literals, in memory
    planted = [f"x {v} y" for v in lits] + [f"x {h} y" for h in hosts]
    assert len(planted) == n_private
    ok_private = sum(bool(rx.search(line)) for (_, rx), line in zip(pats, planted))
    spec = json.load(sys.stdin)
    pats += [(lab, re.compile(rx, re.I)) for lab, rx in spec["patterns"]]
    pats += [
        ("generic MAC address", re.compile(r"\b(?:[0-9a-f]{2}[:-]){5}[0-9a-f]{2}\b", re.I)),
        ("home directory", re.compile(r"/hom[e]/|/User[s]/|~[/]")),
        ("interface name", re.compile(r"\b(?:eth\d+|enp\d+s\d+\w*|eno\d+\w*|ens\d+\w*"
                                      r"|enx[0-9a-f]{12}|wlp\d+s\d+\w*|wlan\d+)\b", re.I)),
    ]
    ok_labelled = sum(any(rx.search(c) for c in spec["controls"]) for _, rx in pats[n_private:])
    labels = sorted({lab for lab, _ in pats})
    print(f"patterns: {n_private} private literals built in memory, "
          f"{len(pats) - n_private} labelled patterns; labels: {labels}")
    print(f"positive control in memory: {ok_private} of {n_private} private literals and "
          f"{ok_labelled} of {len(pats) - n_private} labelled patterns hit their planted line")
    if ok_private != n_private or ok_labelled != len(pats) - n_private:
        print("positive control FAILED; scan not run")
        return 2
    texts = []
    for rng in ranges.split(","):
        diff = subprocess.run(["git", "-C", repo, "diff", "-U0", rng], check=True,
                              capture_output=True, text=True).stdout
        cur, n = None, 0
        for line in diff.splitlines():
            if line.startswith("+++ "):
                cur = line[6:]
            elif line.startswith("@@"):
                n = int(re.search(r"\+(\d+)", line).group(1))
            elif line.startswith("+"):
                texts.append((f"{rng} added {cur}", n, line[1:]))
                n += 1
        log = subprocess.run(["git", "-C", repo, "log", "--format=%B", rng], check=True,
                             capture_output=True, text=True).stdout
        for i, line in enumerate(log.splitlines(), 1):
            texts.append((f"{rng} commit messages", i, line))
    nfiles = 0
    for p in paths:
        for f in sorted(glob.glob(os.path.join(p, "**"), recursive=True)) if os.path.isdir(p) else [p]:
            if os.path.isfile(f):
                nfiles += 1
                for i, line in enumerate(open(f, errors="replace").read().splitlines(), 1):
                    texts.append((os.path.relpath(f, p) if os.path.isdir(p) else os.path.basename(f), i, line))
    hits = 0
    for place, i, line in texts:
        for lab, rx in pats:
            if rx.search(line):
                hits += 1
                print(f"HIT {lab}: {place}:{i}")
    print(f"scanned: {nfiles} files, {len(texts)} lines in all")
    print(f"hits: {hits}")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
