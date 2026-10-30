#!/usr/bin/env python3
"""Run bounded, read-only source checks and disposable documentation probes."""
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile

SOURCE = Path(sys.argv[1]).resolve()
PACKET = Path(__file__).resolve().parent
SCRATCH = PACKET / "scratch"
LOGS = PACKET / "receipts"
HEAD = "db9ab2215ba18aec4c1828090b3611b001dbf2b8"
PIN = Path(os.environ.get("REVIEW_LINT_DIR", "$VALIDATION_TOOLS/pinned-verilator-5.050"))
LOGS.mkdir(exist_ok=True)
(SCRATCH / "tmp").mkdir(parents=True, exist_ok=True)
ENV = dict(os.environ, PATH=str(PIN) + os.pathsep + os.environ["PATH"],
           TMPDIR=str(SCRATCH / "tmp"), PYTHONDONTWRITEBYTECODE="1")

def run(name, command, cwd=SOURCE):
    result = subprocess.run(command, cwd=cwd, env=ENV, capture_output=True, timeout=180)
    (LOGS / (name + ".log")).write_bytes(result.stdout + result.stderr)
    (LOGS / (name + ".rc")).write_text(str(result.returncode) + "\n")
    return {"name": name, "command": command, "rc": result.returncode}

def audit(name):
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=SOURCE).decode().strip()
    tree = subprocess.check_output(["git", "rev-parse", "HEAD^{tree}"], cwd=SOURCE).decode().strip()
    entries = subprocess.check_output(["git", "ls-files", "-s", "-z"], cwd=SOURCE).split(b"\0")
    bad = []
    links = []
    records = []
    for entry in filter(None, entries):
        meta, raw = entry.split(b"\t", 1)
        mode, blob, stage = meta.decode().split()
        relative = raw.decode()
        if mode == "160000":
            links.append([relative, blob])
            continue
        path = SOURCE / relative
        data = os.readlink(path).encode() if path.is_symlink() else path.read_bytes()
        actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        actual_mode = "120000" if path.is_symlink() else ("100755" if path.stat().st_mode & 0o111 else "100644")
        records.append([relative, mode, blob, actual_mode, actual])
        if (actual, actual_mode, stage) != (blob, mode, "0"):
            bad.append(relative)
    status = subprocess.check_output(["git", "status", "--porcelain=v1", "--untracked-files=all"], cwd=SOURCE).decode()
    index_diff = subprocess.check_output(["git", "diff", "--cached", "--raw", HEAD], cwd=SOURCE).decode()
    result = dict(head=head, tree=tree, tracked=len(records), mismatches=bad,
                  required_gitlinks=links, status=status, index_diff=index_diff, blobs=records)
    (LOGS / (name + ".json")).write_text(json.dumps(result, indent=2) + "\n")
    assert head == HEAD and not bad and not status and not index_diff, result
    return {k: v for k, v in result.items() if k != "blobs"}

print(json.dumps(audit("checkout-before")))
identity = run("lint-identity", [str(PIN / "verilator"), "--version"])
assert identity["rc"] == 0
assert "Verilator 5.050" in (LOGS / "lint-identity.log").read_text()
commands = [
    ("docs", ["make", "-j16", "docs"]),
    ("contract", ["make", "-j16", "contract"]),
    ("lint", ["make", "-j16", "lint"]),
    ("diff-check-base", ["git", "diff", "--check", "135afd04", HEAD]),
    ("diff-check-previous", ["git", "diff", "--check", "411b35fc", HEAD]),
]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(lambda entry: run(*entry), commands))
for result in results:
    print(json.dumps(result), flush=True)

archive = SCRATCH / "source.tar"
with archive.open("wb") as output:
    subprocess.run(["git", "archive", HEAD], cwd=SOURCE, stdout=output, check=True)
probe = SCRATCH / "probe"
probe.mkdir(exist_ok=True)
with tarfile.open(archive) as source:
    source.extractall(probe, filter="data")
integration = probe / "docs/INTEGRATION.md"
guide = probe / "docs/HDL_DEVELOPER.md"
original_integration = integration.read_bytes()
original_guide = guide.read_bytes()
cases = [
    ("stale-table-value", None, "stale"),
    ("stale-duplicate-row", None, "duplicate"),
    ("restated-unit-value", "The Sync watch is 375 ms.\n", None),
    ("decimal-minutes", "A 2.5 min hold.\n", None),
    ("decimal-minute-word", "Wait 0.5 minutes.\n", None),
    ("larger-number-word", "A twenty-five minutes soak.\n", None),
    ("rejected-set-example", "A 5min countdown.\n", None),
    ("number-word-min", "A five min countdown.\n", None),
    ("unit-without-comma", "The Sync watch is 375 ms.\n", "unit"),
    ("tilde-fence-control", "~~~\nsleep 375 ms\n~~~\n", None),
    ("tilde-other-marker-control", "~~~\n```\n~~~\n\nThe Sync watch is 375 ms.\n", None),
    ("tilde-shorter-inner-marker", "~~~~text\n~~~\n~~~~\n\nThe Sync watch is 375 ms.\n", None),
]
try:
    for name, appended, change in cases:
        integration.write_bytes(original_integration)
        guide.write_bytes(original_guide)
        text = original_integration.decode()
        if change == "stale":
            text = text.replace("| `SYNC_RTO_MS_C` | 375 |", "| `SYNC_RTO_MS_C` | 374 |")
        elif change == "duplicate":
            row = "| `SYNC_RTO_MS_C` | 374 | syncReceiptTimeout, ms | Milan Table 4.2 |\n\n"
            text = text.replace("## Integration checklist", row + "## Integration checklist")
        elif change == "unit":
            text = text.replace("syncReceiptTimeout, ms", "syncReceiptTimeout ms")
        integration.write_text(text)
        if appended:
            guide.write_text(original_guide.decode() + "\n" + appended)
        result = run("probe-" + name, ["make", "-j16", "docs"], probe)
        result.update(append=appended, change=change)
        results.append(result)
        print(json.dumps(result), flush=True)
finally:
    integration.write_bytes(original_integration)
    guide.write_bytes(original_guide)
results.append(run("probe-restored", ["make", "-j16", "docs"], probe))
(LOGS / "checks.json").write_text(json.dumps(results, indent=2) + "\n")
print(json.dumps(audit("checkout-after")))
