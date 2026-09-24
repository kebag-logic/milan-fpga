#!/usr/bin/env python3
"""Run one --selftest case of a (possibly mutated) act_slot_proof.sh and keep its SUMMARY.

usage: proof_one_case.py SCRIPT WORKDIR 'NAME|FAULTS|PR_B|STATUS|LINE' [SUBSTITUTION_OLD SUBSTITUTION_NEW]...
Writes WORKDIR/scripts/act_slot_proof.sh: SCRIPT with the given substitutions
(each exactly once), its case table reduced to the one given case, and its
scratch kept, then prints the case result, the SUMMARY and isolation.log.
Run it inside sandbox.sh.
"""
import pathlib, re, subprocess, sys
script, work, case, *subs = sys.argv[1:]
text = pathlib.Path(script).read_text()
for old, new in zip(subs[::2], subs[1::2]):
    assert text.count(old) == 1, old
    text = text.replace(old, new, 1)
start = text.index("  done <<'EOF'\n") + len("  done <<'EOF'\n")
end = text.index("EOF\n", start)
text = text[:start] + case + "\n" + text[end:]
text = text.replace('  rm -rf "$scratch"\n', '  echo "scratch kept: $scratch"\n', 1)
out = pathlib.Path(work) / "scripts" / "act_slot_proof.sh"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(text); out.chmod(0o755)
proc = subprocess.run(["bash", str(out), "--selftest"], capture_output=True, text=True)
print(proc.stdout + proc.stderr)
kept = re.search(r"scratch kept: (\S+)", proc.stdout).group(1)
name = case.split("|")[0]
for f in ("logs/SUMMARY", "logs/isolation.log"):
    p = pathlib.Path(kept) / name / f
    print(f"--- {f}"); print(p.read_text() if p.exists() else "(absent)")
for p in sorted((pathlib.Path(kept) / name / "logs").glob("parallel-*.log")):
    print(f"--- {p.name}"); print(p.read_text())
