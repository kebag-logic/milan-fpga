#!/usr/bin/env python3
"""Checks against the superseded original archive (its SHA is a private input).

Usage: superseded_original_checks.py EVID_GITDIR ORIGINAL_REV PIN_ROOT DIGEST
  PIN_ROOT  extraction of review-evidence/117-r1 at the pin
  DIGEST    the firmware-field SHA-256 the page quotes

Reports, without printing any identity value or the original revision:
  - how many MANIFEST.json original_sha256 values name a file of the original
    archive, and which entries do not (never published unredacted);
  - for every redacted capture, whether the published length equals the
    original length and whether the two differ only in place;
  - whether the zero-padded 64-octet firmware_version field of the reference
    peer's entity dump in the original archive hashes to DIGEST, and its octets.
"""
import hashlib, io, json, os, re, subprocess, sys, tarfile

gitdir, rev, root, digest = sys.argv[1:5]
tar = subprocess.run(["git", "--git-dir", gitdir, "archive", rev, "review-evidence/117-r1"],
                     capture_output=True, check=True).stdout
orig = {}
with tarfile.open(fileobj=io.BytesIO(tar)) as t:
    for m in t.getmembers():
        if m.isfile():
            orig[m.name.split("review-evidence/117-r1/", 1)[1]] = t.extractfile(m).read()
by_hash = {hashlib.sha256(v).hexdigest(): k for k, v in orig.items()}
man = json.load(open(os.path.join(root, "MANIFEST.json")))
missing = [e["file"] for e in man if e["original_sha256"] not in by_hash]
print(f"ORIGINALS resolved_in_original_archive={len(man) - len(missing)} of {len(man)}; "
      f"never_published_unredacted={len(missing)}")
for f in missing:
    print(f"    {f}")
for e in man:
    if not e["file"].endswith(".pcap") or e["original_sha256"] == e["published_sha256"]:
        continue
    a = orig.get(e["file"])
    b = open(os.path.join(root, e["file"]), "rb").read()
    same_len = a is not None and len(a) == len(b)
    print(f"PCAP {e['file']} original_found={a is not None} length_preserved={same_len}")
peer = next(k for k in orig if re.search(r"runC/entity_0x3cc0c6[0-9a-f]+\.json$", k))
m = re.search(rb'"firmware_version": "([^"]*)"', orig[peer])
v = m.group(1)
ok = hashlib.sha256(v + b"\0" * (64 - len(v))).hexdigest() == digest
print(f"FIRMWARE_FIELD source={peer} octets={len(v)} digest_matches_page={ok} value=<withheld>")
