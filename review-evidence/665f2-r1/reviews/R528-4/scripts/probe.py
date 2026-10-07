#!/usr/bin/env python3
"""Plant one reviewer defect in a disposable clone and run one gate command.

Usage: probe.py <repo> <rev> <workdir> <receipts-dir> <name> <expect: fail|pass> <file> <old> <new> -- <cmd...>

<old> must occur exactly once in <file> (escape sequences \\n and \\t are
decoded). The clone shares objects with <repo> (git clone --shared) and links
the repo's submodule checkouts after checking each gitlink equals the
checkout's HEAD. The receipt records the planted diff, the command, its exit
code, the tail of its output and whether the outcome matched the expectation.
"""
import json, shutil, subprocess, sys, time
from pathlib import Path

repo, rev, work, receipts, name, expect, rel, old, new = sys.argv[1:10]
cmd = sys.argv[sys.argv.index("--") + 1:]
old, new = (s.encode().decode("unicode_escape") for s in (old, new))
work, receipts = Path(work).resolve(), Path(receipts).resolve()
receipts.mkdir(parents=True, exist_ok=True)
clone = work / name
if clone.exists():
    shutil.rmtree(clone)
subprocess.run(["git", "clone", "-q", "--shared", "--no-checkout", repo, str(clone)], check=True)
subprocess.run(["git", "-C", str(clone), "checkout", "-q", "--detach", rev], check=True)
for sub in ("protocol-processor", "gptp-processor", "third_party/verilog-axis"):
    pin = subprocess.run(["git", "-C", repo, "ls-tree", rev, sub], check=True, capture_output=True, text=True).stdout.split()[2]
    head = subprocess.run(["git", "-C", str(Path(repo) / sub), "rev-parse", "HEAD"], check=True, capture_output=True,
                          text=True).stdout.strip()
    assert pin == head, f"{sub}: {head} is not the pin {pin}"
    (clone / sub).rmdir()
    (clone / sub).symlink_to(Path(repo).resolve() / sub)
target = clone / rel
text = target.read_text(encoding="utf-8")
if text.count(old) != 1:
    sys.exit(f"{name}: fixture occurs {text.count(old)} times in {rel}")
target.write_text(text.replace(old, new), encoding="utf-8")
diff = subprocess.run(["git", "-C", str(clone), "diff", "--", rel], capture_output=True, text=True).stdout
start = time.time()
res = subprocess.run(cmd, cwd=clone, capture_output=True, text=True)
log = res.stdout + res.stderr
(receipts / f"{name}.log").write_text(log)
matched = (res.returncode != 0) if expect == "fail" else (res.returncode == 0)
receipt = {"name": name, "rev": rev, "file": rel, "planted_diff": diff, "cmd": cmd, "rc": res.returncode,
           "expect": expect, "matched_expectation": matched, "wall_s": round(time.time() - start),
           "fail_lines": [ln for ln in log.splitlines() if "[FAIL]" in ln or "REFUSED" in ln or "ESCAPED" in ln][:20],
           "tail": log.splitlines()[-8:]}
(receipts / f"{name}.json").write_text(json.dumps(receipt, indent=1) + "\n")
print(f"{name}: rc {res.returncode} expect {expect} -> {'MATCHED' if matched else 'UNEXPECTED'}")
shutil.rmtree(clone)
