#!/usr/bin/env python3
"""Partial, independent re-run of the author's round-2 extraction scripts.

The retained raw captures are private; only a few inputs survive publicly
byte-identical to the raw index (the redacted packet's dryrun/final consoles
and gm events, and three controller transcripts of the purged round-1
archive). This harness:
  1. builds a raw root from every public file whose (bytes, SHA-256) equals
     a raw-index entry, and reports which of the 50 extraction inputs that
     covers;
  2. runs the author's extract_console_rounds and extract_saved_state code
     unchanged, restricted by patching their ACTIONS / OTHER_TRANSCRIPTS
     lists to the covered actions, and compares each per-action line with the
     author's archived output;
  3. runs negative controls on disposable copies: a one-byte tamper must be
     refused by the author's input hash check (exit 2); with the hash check
     bypassed, a flipped link_status word must be reported as a disagreement;
     an injected CONNECT_RX record and an injected SET_NAME must be counted as
     state-changing; an injected ADD_AUDIO_MAPPINGS is reported for the record.

usage: rerun_extractions.py <repo-at-head> <author-r2-dir> <old-r1-author-dir-or-> <scratch-dir>
"""
import contextlib
import hashlib
import importlib
import io
import json
import re
import shutil
import sys
from pathlib import Path

repo, pk, old, scratch = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], Path(sys.argv[4])
sys.path.insert(0, str(pk / "extract"))
sys.dont_write_bytecode = True
idx = {f["path"]: f for f in json.loads((pk / "r1" / "RAW-ARTIFACTS.json").read_text())["files"]}


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def build_root(root):
    if root.exists():
        shutil.rmtree(root)
    pools = [pk / "r1"] + ([Path(old)] if old != "-" else [])
    byhash = {}
    for base in pools:
        for p in base.rglob("*"):
            if p.is_file():
                byhash.setdefault((p.stat().st_size, sha(p)), p)
    got = []
    for rel, f in idx.items():
        src = byhash.get((f["bytes"], f["sha256"]))
        if src:
            dst = root / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
            got.append(rel)
    return sorted(got)


def run(modname, patch, argv):
    mod = importlib.import_module(modname)
    mod = importlib.reload(mod)
    for k, v in patch.items():
        setattr(mod, k, v)
    buf, rc = io.StringIO(), None
    old_argv = sys.argv
    sys.argv = [modname] + [str(a) for a in argv]
    try:
        with contextlib.redirect_stdout(buf):
            try:
                mod.main()
                rc = 0
            except SystemExit as e:
                rc = e.code
            except Exception as e:  # noqa: BLE001 - partial inputs end some summaries early
                print(f"[harness] stopped after the per-action part: {type(e).__name__}: {e}")
                rc = "partial"
    finally:
        sys.argv = old_argv
    return rc, buf.getvalue()


def lines_for(text, action):
    return [x for x in text.splitlines() if x.startswith(action + " ") or x.startswith(f"{action:15s}")]


root = scratch / "rawroot"
got = build_root(root)
needed = set()
for f in (pk / "extract").glob("*.txt"):
    needed |= set(re.findall(r"^INPUT (\S+)", f.read_text(), re.M))
cov = sorted(needed & set(got))
print(f"raw-index files with a public byte-identical copy: {len(got)}; extraction inputs: {len(needed)}; covered: {len(cov)}")
for c in cov:
    print("  covered", c)

print("\n== console rounds, author code, ACTIONS patched to the covered actions")
acts = [a for a in ("dryrun", "final") if f"{a}/console.jsonl" in cov]
rc, out = run("extract_console_rounds", {"ACTIONS": acts}, [root, repo])
author = (pk / "extract" / "extract_console_rounds.txt").read_text()
for a in acts:
    mine = [x for x in out.splitlines() if x.split()[:1] == [a] and "rounds" in x]
    theirs = [x for x in author.splitlines() if x.split()[:1] == [a] and "rounds" in x]
    print(f"  {a}: rerun {mine} author {theirs} -> {'MATCH' if mine == theirs else 'DIFFER'}")
print("  INPUT lines:", [x for x in out.splitlines() if x.startswith("INPUT")])

print("\n== saved state, author code, ACTIONS and OTHER_TRANSCRIPTS patched")
sacts = [a for a in ("dryrun", "baseline-bound", "final") if f"{a}/console.jsonl" in cov and f"{a}/controller.jsonl" in cov]
rc, out = run("extract_saved_state", {"ACTIONS": sacts, "OTHER_TRANSCRIPTS": []}, [root, repo])
author = (pk / "extract" / "extract_saved_state.txt").read_text()
for a in sacts:
    mine = [x for x in out.splitlines() if x.startswith(f"{a:15s}")]
    theirs = [x for x in author.splitlines() if x.startswith(f"{a:15s}")]
    print(f"  {a}: {'MATCH' if mine == theirs else 'DIFFER'} ({len(mine)} line(s) each)")
    for m in mine:
        print("    " + m[:230])
rb = [x for x in out.splitlines() if x.startswith(("READBACK", "  milan_nvm", "  NVM:"))]
rb_author = [x for x in author.splitlines() if x.startswith(("READBACK", "  milan_nvm", "  NVM:"))]
print(f"  identity/final readbacks: {'MATCH' if rb == rb_author else 'DIFFER'} ({len(rb)} lines)")
for x in rb:
    print("    " + x[:230])
tail = [x for x in out.splitlines() if x.startswith(("nvm_pend:", "nvm_dirty", "image seq", "[harness]"))]
for x in tail:
    print("  " + x[:230])

# baseline-bound has a public controller transcript but no public console: check its polled binding directly
bb = root / "baseline-bound" / "controller.jsonl"
if bb.exists():
    ss = importlib.import_module("extract_saved_state")
    recs = [json.loads(x) for x in bb.read_text().splitlines() if x.strip()]
    b = sorted({tuple(str(r["response"].get(k)) for k in ss.BINDING_KEYS) for r in recs
                if r.get("role") == "dut" and r.get("what") == "state-5-1" and r["response"].get("status") == 0})
    muts = [ss.mutating(r) for r in recs if "what" in r and ss.mutating(r)]
    theirs = [x for x in author.splitlines() if x.startswith("baseline-bound  [")]
    mine = f"baseline-bound  {b}"
    print(f"  baseline-bound polled DUT binding: {mine} -> {'MATCH' if theirs == [mine] else 'DIFFER'}; state-changing {len(muts)}")

print("\n== negative controls on disposable copies")
neg = scratch / "negroot"
if neg.exists():
    shutil.rmtree(neg)
shutil.copytree(root, neg)
con = neg / "dryrun" / "console.jsonl"
data = bytearray(con.read_bytes())
data[-3] ^= 0x01
con.write_bytes(bytes(data))
rc, out = run("extract_console_rounds", {"ACTIONS": ["dryrun"]}, [neg, repo])
print(f"  N1 one-byte tamper of dryrun console: exit {rc} ({'REFUSED' if rc == 2 else 'NOT REFUSED'}): {out.strip().splitlines()[-1][:160]}")
shutil.copyfile(root / "dryrun" / "console.jsonl", con)
rows = [json.loads(x) for x in con.read_text().splitlines() if x.strip()]
for r in rows:
    if r["cmd"] == "mem_read 0xf000181c 4":
        r["raw"] = re.sub(r"^(0xf000181c\s+)0d", r"\g<1>00", r["raw"], flags=re.M)
        break
con.write_text("".join(json.dumps(r) + "\n" for r in rows))
common = importlib.import_module("b1r2_common")
orig_path = common.Inputs.path
common.Inputs.path = lambda self, rel: self.raw / rel  # bypass the hash gate for the logic probes only
try:
    rc, out = run("extract_console_rounds", {"ACTIONS": ["dryrun"]}, [neg, repo])
    dis = [x for x in out.splitlines() if x.startswith("DISAGREE") or x.startswith("dryrun")]
    print(f"  N2 flipped link_status in one round: exit {rc}; {dis[:2]}")
    ss = importlib.import_module("extract_saved_state")
    probes = {
        "CONNECT_RX": {"role": "dut", "what": "acmp-6", "response": {"status": 0, "listener_uid": 1, "talker_uid": 2, "conn_count": 1}},
        "SET_NAME": {"role": "dut", "what": "set-name", "response": {"cmd": "SET_NAME", "status": "SUCCESS", "payload": "00"}},
        "ADD_AUDIO_MAPPINGS": {"role": "dut", "what": "map", "response": {"cmd": "ADD_AUDIO_MAPPINGS", "status": "SUCCESS", "payload": "00"}},
    }
    for name, rec in probes.items():
        print(f"  N3 injected {name}: mutating() -> {ss.mutating(rec)!r}")
finally:
    common.Inputs.path = orig_path
