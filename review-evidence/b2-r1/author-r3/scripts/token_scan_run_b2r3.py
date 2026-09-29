#!/usr/bin/env python3
"""[A447] Round 3 of PR #622: run both reviewers' token scanners over this packet.

The private deny-list is built in memory at run time and handed to each scanner
through a pipe (/dev/fd/N), so it is never written to disk and never printed.

Usage: token_scan_run_b2r3.py <clone> <round-1 author dir> <archive MANIFEST.json>
           <archive ref> <R404-2 scripts dir> <R405-2 scripts dir> <scan root>
Env:   EXTRA_PRIVATE  newline-separated literal names, supplied on the command
                      line at run time and never stored (tool and model names).
       SCAN_STAGE     an empty scratch directory outside the scan root; the
                      reviewers' scanners read a staged copy of the scan root.

Private classes:
  controller    every original token behind the archive's redaction placeholders
                in three redacted transcripts, in every spelling: the EUI-64 and
                the MAC it carries, plain and with ':' or '-' separators, and the
                dotted MAC form;
  host          this machine's host name, account name and home directory, the
                absolute paths of the clone, the author dir and the scan root and
                their first two components, and every network interface name and
                hardware address (in the same spellings, and as an EUI-64);
  extra         the EXTRA_PRIVATE literals.
The scan root's `receipts/token_scan_b2r3.txt` is excluded: it holds the
scanners' own hash prefixes. Prints labels and counts only.
"""
import getpass
import hashlib
import json
import os
import re
import shutil
import socket
import subprocess
import sys
from collections import Counter
from pathlib import Path

clone, author, manifest, ref, r404, r405, root = sys.argv[1:8]
A = Path(author)
RECEIPT = "receipts/token_scan_b2r3.txt"


def spellings(hexid):
    """Every spelling of an EUI-64 or MAC identity, and of its counterpart."""
    t = hexid.lower()
    out = set()
    if len(t) == 16:
        forms = [t] + ([t[:6] + t[10:]] if t[6:10] == "fffe" else [])
    else:
        forms = [t, t[:6] + "fffe" + t[6:]]
    for f in forms:
        pairs = [f[i:i + 2] for i in range(0, len(f), 2)]
        out |= {f, ":".join(pairs), "-".join(pairs)}
        if len(f) == 12:
            out.add(".".join(f[i:i + 4] for i in range(0, 12, 4)))
    return out


def literal(s):
    body = re.escape(s)
    if re.fullmatch(r"\w+", s):
        body = r"(?<![A-Za-z0-9])" + body + r"(?![A-Za-z0-9])"
    return body


private = []   # (label, regex)

# controller: align three redacted transcripts with their originals
entries = [e for e in json.loads(Path(manifest).read_text())
           if e["file"].startswith("author/") and e["file"].endswith(".jsonl")
           and e["original_sha256"] != e["published_sha256"]][:3]
PH = re.compile(r"<[A-Za-z0-9_-]+>")
found = Counter()
tokens = set()
for e in entries:
    pub = subprocess.run(["gh", "api", "-H", "Accept: application/vnd.github.raw",
                          f"repos/kebag-logic/milan-fpga/contents/review-evidence/b2-r1/{e['file']}?ref={ref}"],
                         capture_output=True, check=True).stdout
    orig = (A / e["file"][len("author/"):]).read_bytes()
    assert hashlib.sha256(pub).hexdigest() == e["published_sha256"], e["file"]
    assert hashlib.sha256(orig).hexdigest() == e["original_sha256"], e["file"]
    pl, ol = pub.decode().splitlines(), orig.decode().splitlines()
    assert len(pl) == len(ol), e["file"]
    for p, o in zip(pl, ol):
        names = PH.findall(p)
        if not names:
            continue
        rx = "(.+?)".join(re.escape(s) for s in PH.split(p))
        m = re.fullmatch(rx, o)
        assert m, e["file"]
        for name, tok in zip(names, m.groups()):
            found[name] += 1
            tokens.add(tok)
for tok in sorted(tokens):
    t = re.sub(r"[^0-9A-Fa-f]", "", tok)
    if len(t) in (12, 16) and re.fullmatch(r"(?:0x)?[0-9A-Fa-f:.-]+", tok):
        for s in sorted(spellings(t)):
            private.append(("controller", re.escape(s)))
    else:
        private.append(("controller", literal(tok)))
print(f"controller: {len(entries)} redacted transcripts aligned, placeholders {dict(found)}, "
      f"distinct original tokens {len(tokens)}, patterns {sum(1 for l, _ in private if l == 'controller')}")

# host
HOMEDIR = os.path.expanduser("~")
host = {socket.gethostname(), socket.gethostname().split(".")[0], getpass.getuser(), HOMEDIR}
fq = socket.getfqdn()
if fq and fq not in ("localhost", "localhost.localdomain"):
    host.add(fq)
for p in (clone, author, root):
    rp = Path(p).resolve()
    host.add(str(rp))
    host.add("/" + "/".join(rp.parts[1:3]))
for d in sorted(Path("/sys/class/net").iterdir()):
    if d.name == "lo":
        continue
    host.add(d.name)
    try:
        mac = (d / "address").read_text().strip()
    except OSError:
        continue
    if re.fullmatch(r"(?:[0-9a-f]{2}:){5}[0-9a-f]{2}", mac) and int(mac.replace(":", ""), 16) != 0:
        for s in sorted(spellings(mac.replace(":", ""))):
            private.append(("host", re.escape(s)))
for s in sorted(h for h in host if h):
    private.append(("host", literal(s)))

# extra
for s in (os.environ.get("EXTRA_PRIVATE") or "").splitlines():
    if s.strip():
        private.append(("extra", literal(s.strip())))
print("private patterns by class:", dict(Counter(l for l, _ in private)), "total", len(private))

# positive control: the controller class must hit the unredacted round-1 transcripts
ctl = Counter()
for f in sorted((A / "bind").rglob("*.jsonl")):
    txt = f.read_text(errors="replace")
    for label, rx in private:
        if label == "controller" and re.search(rx, txt, re.I):
            ctl[f.relative_to(A).as_posix()] += 1
            break
print(f"positive control, controller class over the unredacted round-1 bind/ transcripts: "
      f"{len(ctl)} files hit of {len(list((A / 'bind').rglob('*.jsonl')))}")
selftest = all(re.search(rx, s, re.I) for (label, rx), s in
               ((("host", literal(getpass.getuser())), getpass.getuser()),
                (("host", literal(HOMEDIR)), HOMEDIR)))
print(f"self-test, account and home patterns match their own source: {selftest}")

# scan set: every file under the scan root except the receipt this run produces
scan = Path(root).resolve()
files = [f for f in sorted(scan.rglob("*")) if f.is_file() and f.relative_to(scan).as_posix() != RECEIPT]
print(f"scan root files: {len(files)} (excluded: {RECEIPT})")

# own count, every class, before the reviewers' scanners
own = Counter()
for f in files:
    txt = f.read_text(errors="replace")
    for label, rx in private:
        if re.search(rx, txt, re.I):
            own[(label, f.relative_to(scan).as_posix())] += 1
print(f"own private-pattern count over the scan root: {sum(own.values())} hits",
      dict(Counter(l for l, _ in own)) or "")
stage = Path(os.environ.get("SCAN_STAGE", ""))
assert stage.is_dir() and not str(stage.resolve()).startswith(str(scan)), "SCAN_STAGE must be outside the scan root"
# the reviewers' scanners take directories: stage a copy without the receipt
for f in files:
    dst = stage / f.relative_to(scan)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(f, dst)


def pipe(data):
    r, w = os.pipe()
    os.write(w, data.encode())
    os.close(w)
    return r


pages = [str(Path(clone) / "docs/findings/606_FIRST_BIND_MEASUREMENT.md"),
         str(Path(clone) / "docs/findings/608_75_WITHDRAWAL_AND_RESTART.md")]
rc = 0
fd = pipe("\n".join(rx for _, rx in private) + "\n")
print(f"\n### R404-2 token_scan.py (sha256 {hashlib.sha256(Path(r404, 'token_scan.py').read_bytes()).hexdigest()}): "
      f"PRIVATE_TOKENS=<pipe, {len(private)} patterns> token_scan.py <clone> <scan root>", flush=True)
p = subprocess.run([sys.executable, "-B", str(Path(r404, "token_scan.py")), clone, str(stage)],
                   env={**os.environ, "PRIVATE_TOKENS": f"/dev/fd/{fd}"}, pass_fds=(fd,))
os.close(fd)
print(f"rc={p.returncode}", flush=True)
rc |= p.returncode
fd = pipe(json.dumps({f"private-{i}": "(?i)" + rx for i, (_, rx) in enumerate(private)}))
print(f"\n### R405-2 r405_scan_tokens.py (sha256 {hashlib.sha256(Path(r405, 'r405_scan_tokens.py').read_bytes()).hexdigest()}): "
      f"SCAN_PRIVATE_PATTERNS=<pipe, {len(private)} patterns> r405_scan_tokens.py <clone> 13eda870 -- <scan root> <two pages>",
      flush=True)
p = subprocess.run([sys.executable, "-B", str(Path(r405, "r405_scan_tokens.py")), clone,
                    "13eda870d1a6cf3f946fc228a98862366b08d102", "--", str(stage), *pages],
                   env={**os.environ, "SCAN_PRIVATE_PATTERNS": f"/dev/fd/{fd}"}, pass_fds=(fd,))
os.close(fd)
print(f"rc={p.returncode}", flush=True)
rc |= p.returncode
ok = not own and len(ctl) > 0 and selftest
print(f"\nRESULT {'CLEAN' if ok else 'NOT CLEAN'}")
sys.exit(rc or (0 if ok else 1))
