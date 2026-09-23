#!/usr/bin/env python3
"""Reviewer observation: a job-control stop (SIGTSTP) of the sweep entry.

Usage: probe_tstp.py CLONE WORKDIR RECEIPT.json
Holds suite a1, stops the entry with SIGTSTP, releases a1, and records
whether later suites run while the launched process is stopped.
"""
import json, os, signal, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_sweep as ps  # parses the same three arguments

root, probe, env = ps.build("o-command-TSTP")
p, out = ps.launch(root, probe, env)
hs = ps.handshake(probe, "a1", p)
ps.send(p, signal.SIGTSTP, False)
time.sleep(0.5)
rec = dict(entry_state_after_tstp=ps.stat_of(p.pid)["state"])
(probe / "release").write_text("go\n")
ps.wait_for(lambda: (probe / "ran-a3").exists(), 20)
rec["sentinels_while_entry_stopped"] = sorted(x.name for x in probe.glob("ran-*"))
rec["entry_state_then"] = ps.stat_of(p.pid)["state"]
os.kill(p.pid, signal.SIGCONT)
rec["exit_after_cont"] = p.wait(timeout=60)
out.close()
rec["summary_printed"] = "suites:" in (probe / "entry.out").read_text()
Path(sys.argv[3]).write_text(json.dumps(rec, indent=1) + "\n")
print(json.dumps(rec))
