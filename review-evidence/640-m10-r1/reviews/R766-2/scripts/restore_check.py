"""Check every tracked blob of the review clone against the index: bytes and executable mode.
Usage: python3 -I restore_check.py <clone>"""
import hashlib, os, subprocess, sys
os.chdir(sys.argv[1]); bad = n = 0
for line in subprocess.run(["git", "ls-files", "-s", "-z"], capture_output=True).stdout.split(b"\0"):
    if not line: continue
    meta, path = line.split(b"\t", 1); mode, sha, _ = meta.split()
    if mode == b"160000": continue
    n += 1; p = path.decode()
    data = open(p, "rb").read() if mode != b"120000" else os.readlink(p).encode()
    h = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
    m = os.lstat(p).st_mode
    if h != sha.decode() or (mode != b"120000" and bool(m & 0o111) != (mode == b"100755")):
        bad += 1; print("MISMATCH", p)
print(f"tracked blobs checked {n}, byte or mode mismatches {bad}")
sys.exit(1 if bad else 0)
