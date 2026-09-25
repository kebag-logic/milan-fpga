from pathlib import Path
import datetime
import json
import shlex
import subprocess
import time

OUT = Path(__file__).resolve().parent
ROOT = Path("$LANES/443-render-csr")
GATES = [
    ("csr", ["make", "-C", "tb/verilator/csr"]),
    ("milan-dp", ["make", "-C", "tb/verilator/milan_dp"]),
    ("render-csr-controls", ["make", "-C", "tb/verilator/milan_dp", "render-csr-controls"]),
    ("milan-dp-render", ["make", "-C", "tb/verilator/milan_dp_render"]),
    ("docs-check", ["python3", "scripts/docs_check.py"]),
    ("docs-check-no-git", ["env", "GIT_DIR=/dev/null", "python3", "scripts/docs_check.py"]),
    ("em-dash", ["python3", "scripts/check_em_dash.py", "--base", "864b36f5e9450ef64f75ca3f0d68c44330e447d7"]),
    ("doc-style", ["python3", "scripts/check_doc_style.py"]),
    ("toc", ["python3", "scripts/gen_toc.py", "--check"]),
    ("anchors", ["python3", "scripts/gen_toc.py", "--verify-anchors"]),
    ("doc-paths", ["python3", "scripts/check_doc_paths.py"]),
    ("xvlog", ["python3", "scripts/xvlog_gate.py", "--check"]),
    ("sv-idiom", ["python3", "scripts/check_sv_idiom.py"]),
    ("cpp-idiom", ["python3", "scripts/check_cpp_idiom.py"]),
    ("py-idiom", ["python3", "scripts/check_py_idiom.py"]),
    ("test-evidence", ["python3", "scripts/measure_test_evidence.py", "--check"]),
    ("diff-check", ["git", "diff", "--check"]),
]
records = []
for name, cmd in GATES:
    command = shlex.join(cmd)
    print(f"START {name}: {command}", flush=True)
    start = time.monotonic()
    record = {"gate": name, "command": command, "started_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    with (OUT / f"{name}.log").open("w") as log:
        log.write(f"Command: {command}\nHead: b3458db0db5a7c8b15582d80b492620f05f62e70\n\n")
        log.flush()
        result = subprocess.run(["rtk", "proxy", "timeout", "7200", *cmd], cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
    record.update(rc=result.returncode, seconds=round(time.monotonic()-start, 3), log=f"{name}.log")
    records.append(record)
    (OUT / "gate-results.json").write_text(json.dumps(records, indent=2)+"\n")
    handoff = OUT / "HANDOFF.md"
    s = handoff.read_text()
    prefix, rest = s.split("## Gates\n", 1)
    _, suffix = rest.split("## Review handoff\n", 1)
    table = "\nAll commands run in the foreground, without pipelines, with a 7200-second per-command guard. Exact unfiltered output is saved in the listed logs.\n\n| Gate command | Exit | Seconds | Evidence |\n|---|---|---|---|\n"
    for row in records:
        table += f"| `{row['command']}` | {row['rc']} | {row['seconds']} | [{row['log']}]({row['log']}) |\n"
    for pending, cmd_pending in GATES[len(records):]:
        table += f"| `{shlex.join(cmd_pending)}` | Pending | -- | -- |\n"
    handoff.write_text(prefix + "## Gates\n" + table + "\n## Review handoff\n" + suffix)
    print(f"DONE {name}: rc={result.returncode}, {record['seconds']} seconds", flush=True)
print("ALL REQUESTED GATES FINISHED", flush=True)
raise SystemExit(int(any(row["rc"] for row in records)))
