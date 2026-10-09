#!/usr/bin/env python3
"""R580-2 probe P8: extra mutants of the default-population code, judged by the gate self-test.

Usage: probe_population_mutants.py <repo> <scratch> <jobs>
Each mutant replaces one exact snippet (must occur once) in a copy of syn/ooc and runs
pp_resource_gate.py --selftest; DETECTED when it exits non-zero. Exits 0 when the probe ran.
"""
import concurrent.futures
import shutil
import subprocess
import sys
from pathlib import Path

GATE, PLACE = "pp_resource_gate.py", "pp_placement.py"
MUTANTS = [
    ("M0 control", None, None, None),
    ("M1 printed record judged", GATE,
     '        wrong = [] if printing else misplaced(directory, candidate["kind"], args.placement)\n',
     '        wrong = misplaced(directory, candidate["kind"], args.placement)\n'),
    ("M2 population judged before identity", GATE,
     '    if wrong:\n        return 2, [f"NOT COMPARABLE: {\'; \'.join(wrong)}; measure a split image with its --placement"]\n',
     '    pass\n'),
    ("M3 all-fabric mailbox tolerated", PLACE,
     '        count = 0 if role in ("mailbox", "processor-maap") else 1\n        return count, count\n',
     '        count = 0 if role in ("mailbox", "processor-maap") else 1\n        return count, 1\n'),
    ("M4 all-fabric roles may be absent", PLACE,
     '        count = 0 if role in ("mailbox", "processor-maap") else 1\n        return count, count\n',
     '        count = 0 if role in ("mailbox", "processor-maap") else 1\n        return 0, count\n'),
    ("M5 census names only the first problem", PLACE,
     '    return problems\n\n\ndef census_tcl', '    return problems[:1]\n\n\ndef census_tcl'),
    ("M6 record --write refusal after write", GATE,
     '            if wrong:\n                raise Refusal(f"{\'; \'.join(wrong)}; acceptance records only the all-fabric image")\n'
     '            emit([json.dumps(candidate, indent=1)])\n',
     '            emit([json.dumps(candidate, indent=1)])\n'),
    ("M7 own-row skip widened to every parenthesised module", PLACE,
     ' or fields[0].startswith("("):', ' or fields[0].startswith("(") or fields[1].startswith("KL_a"):'),
]


def run(repo: Path, scratch: Path, name: str, target, old, new) -> str:
    folder = scratch / name.split()[0]
    shutil.rmtree(folder, ignore_errors=True)
    shutil.copytree(repo / "syn/ooc", folder, ignore=shutil.ignore_patterns("__pycache__"))
    snippet = "ok"
    if target:
        text = (folder / target).read_text()
        if text.count(old) != 1:
            return f"{name}\t{target}\tsnippet-count={text.count(old)}\t-\tINVALID"
        (folder / target).write_text(text.replace(old, new))
    result = subprocess.run([sys.executable, "-B", str(folder / "pp_resource_gate.py"), "--selftest"],
                            capture_output=True, text=True, timeout=900)
    verdict = "CONTROL-PASS" if target is None and result.returncode == 0 else (
        "CONTROL-FAIL" if target is None else ("DETECTED" if result.returncode else "SURVIVED"))
    tail = (result.stdout + result.stderr).strip().splitlines()[-1:] or [""]
    return f"{name}\t{target}\t{snippet}\t{result.returncode}\t{verdict}\t{tail[0][:160]}"


repo, scratch, jobs = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3])
scratch.mkdir(parents=True, exist_ok=True)
print("mutant\tfile\tsnippet\tgate_rc\tverdict\tlast line")
with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
    for line in pool.map(lambda m: run(repo, scratch, *m), MUTANTS):
        print(line)
