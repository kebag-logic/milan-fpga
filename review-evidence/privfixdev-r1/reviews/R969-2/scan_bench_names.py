"""Scan tracked content at a revision for the bench-name classes issue #1028 removes.

The product, host and switch tokens are assembled from code points so this file
does not itself carry them. Prints matching lines (or only a count with --count).
usage: python3 -I scan_bench_names.py <repo> <rev> [--count]
"""
import subprocess, sys
c = lambda *cp: "".join(map(chr, cp))
product = c(112, 114, 111, 102, 105) + " ?" + c(115, 104, 97, 114, 107)
hosts = r"\b" + c(112, 119) + r"[01]\b"
switch = r"\b" + c(68, 78) + r"-?1\b"
private = (r"\b10\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\b|\b192\.168\.[0-9]"
           r"|\b172\.(1[6-9]|2[0-9]|3[01])\.[0-9]")
names_only = "--names-only" in sys.argv
pattern = "|".join([product, hosts, switch] + ([] if names_only else [private]))
repo, rev = sys.argv[1], sys.argv[2]
out = subprocess.run(["git", "-C", repo, "grep", "-n", "-I", "-i", "-E", pattern, rev, "--",
                      ".", ":!*.pcap", ":!*.hex", ":!*.svg"] + ([] if names_only else [":!*.json"]),
                     capture_output=True, text=True).stdout.splitlines()
if "--count" in sys.argv:
    files = {line.split(":", 2)[1] for line in out}
    print(f"{rev}: {len(out)} line(s) in {len(files)} file(s)")
else:
    print("\n".join(out))
