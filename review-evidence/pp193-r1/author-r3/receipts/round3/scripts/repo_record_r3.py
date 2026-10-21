#!/usr/bin/env python3
"""Round-3 repository record and scope check, base 7b424cdf vs the head.

usage: repo_record_r3.py <lane> <out dir>
Writes repo-record.txt (base, head, commits with their bodies, clean tree,
diff stat, sha256 of every changed file at the head, remote refs) and
scope-ports.txt (the module header, `module ... );`, of the listener, the SRP
top and the processor top at base and head; files changed under hdl/; the
register-map and interface documents, architecture 02 and 07).
"""
import datetime
import hashlib
import re
import subprocess
import sys
from pathlib import Path

lane, out = Path(sys.argv[1]), Path(sys.argv[2])
BASE = "7b424cdfe111a426f00517ff471246b4b9650726"


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(lane), *args], check=True,
                          capture_output=True, text=True).stdout


head = git("rev-parse", "HEAD").strip()
lines = [f"repository: {git('remote', 'get-url', 'origin').strip()}",
         f"branch: {git('rev-parse', '--abbrev-ref', 'HEAD').strip()}",
         f"base (PR head before this round): {BASE}",
         f"head: {head}",
         f"head tree: {git('rev-parse', 'HEAD^{tree}').strip()}", "",
         "commits (oldest first):"]
for sha in git("rev-list", "--reverse", f"{BASE}..HEAD").split():
    subj = git("log", "-1", "--format=%s", sha).strip()
    body = git("log", "-1", "--format=%b", sha).strip()
    trailers = git("log", "-1", "--format=%(trailers)", sha).strip()
    lines += [f"{sha} <author> <email>", f"  {subj}",
              f"  body lines: {body}", f"  trailers: {trailers}"]
lines += ["", "status (clean if empty):", git("status", "--short").rstrip(), "",
          f"diff stat {BASE[:8]}..head:", git("diff", "--stat", f"{BASE}..HEAD").rstrip(), "",
          "sha256 of every changed file at the head:"]
for f in git("diff", "--name-only", f"{BASE}..HEAD").split():
    data = subprocess.run(["git", "-C", str(lane), "show", f"HEAD:{f}"], check=True,
                          capture_output=True).stdout
    lines.append(f"{hashlib.sha256(data).hexdigest()}  {f}")
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
lines += ["", f"remote refs at {now}:",
          git("ls-remote", "origin", "refs/heads/193-shared-listener-leave",
              "refs/heads/main", "refs/pull/198/head").rstrip()]
(out / "repo-record.txt").write_text("\n".join(lines) + "\n")


def header(rev: str, path: str, name: str) -> str:
    text = git("show", f"{rev}:{path}")
    m = re.search(rf"module\s+{name}\b.*?\)\s*;", text, re.S)
    return hashlib.sha256(m.group(0).encode()).hexdigest()[:16]


scope = [f"Module header (module ... );) of each file, base {BASE[:8]} vs head {head[:8]}:"]
for path, name in [("hdl/top/protocol_processor_top.sv", "protocol_processor_top"),
                   ("hdl/srp/KL_srp_listener_fsm.sv", "KL_srp_listener_fsm"),
                   ("hdl/srp/KL_srp_top.sv", "KL_srp_top")]:
    b, h = header(BASE, path, name), header("HEAD", path, name)
    scope.append(f"{path}: base {b} head {h} {'identical' if b == h else 'DIFFERENT'}")
scope += ["", f"files under hdl/ changed {BASE[:8]}..head:",
          git("diff", "--name-only", f"{BASE}..HEAD", "--", "hdl").rstrip(), "",
          "register-map and interface documents changed (docs/architecture/02, 07):",
          git("diff", "--name-only", f"{BASE}..HEAD", "--", "docs/architecture/02*",
              "docs/architecture/07*").rstrip(), "(none if empty)"]
(out / "scope-ports.txt").write_text("\n".join(scope) + "\n")
print("written")
