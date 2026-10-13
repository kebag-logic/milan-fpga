"""Scratch (round 18): each choice of the merge's workflow resolution, undone alone in a disposable clone, must be
refused by `ci_events.py --check` (rc 1) and the head must pass (rc 0). The clone is restored after each plant.
usage: python3 -I -B ciplants18.py <disposable clone>"""
import subprocess, sys
from pathlib import Path
clone = Path(sys.argv[1]).resolve()
YML, DOC = clone / ".github/workflows/rtl-fast.yml", clone / "docs/testing/CI_WORKFLOWS.md"
FETCH = "run: git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP"

def job_block(text, job):
    start = text.index(f"\n  {job}:\n") + 1
    end = text.index("\n  # ", start) if "\n  # " in text[start:] else len(text)
    nxt = [i for i in (text.find("\n  firmware-", start + 3), text.find("\n  # ", start + 3)) if i > 0]
    return start, min(nxt)

def unfetch(job):
    def plant(files):
        t = files[YML]; s, e = job_block(t, job); b = t[s:e]
        assert b.count(FETCH + " third_party/tsn-c-stack\n") == 1
        files[YML] = t[:s] + b.replace(FETCH + " third_party/tsn-c-stack\n", FETCH + "\n") + t[e:]
    return plant

def replace(path, old, new):
    def plant(files):
        assert files[path].count(old) == 1, old
        files[path] = files[path].replace(old, new)
    return plant

def drop_job(job):
    def plant(files):
        t = files[YML]; s, e = job_block(t, job); files[YML] = t[:s] + t[e + 1:]
    return plant

PLANTS = [
    ("firmware-unit fetches no tsn-c-stack", unfetch("firmware-unit")),
    ("firmware-control-mutants fetches no tsn-c-stack", unfetch("firmware-control-mutants")),
    ("firmware-aecp-mutants fetches no tsn-c-stack", unfetch("firmware-aecp-mutants")),
    ("firmware-srp-mutants fetches no tsn-c-stack", unfetch("firmware-srp-mutants")),
    ("the aggregate does not need firmware-boundary",
     replace(YML, "firmware-srp-mutants, firmware-boundary, firmware-verilator]", "firmware-srp-mutants, firmware-verilator]")),
    ("the aggregate does not need firmware-verilator",
     replace(YML, "firmware-srp-mutants, firmware-boundary, firmware-verilator]", "firmware-srp-mutants, firmware-boundary]")),
    ("the aggregate does not need firmware-control-mutants",
     replace(YML, "firmware-unit, firmware-control-mutants, firmware-aecp", "firmware-unit, firmware-aecp")),
    ("the aggregate's loop drops firmware-boundary's result",
     replace(YML, '            "firmware-boundary:$FIRMWARE_BOUNDARY_RESULT" \\\n', "")),
    ("the aggregate's loop drops firmware-srp-mutants' result",
     replace(YML, '            "firmware-srp-mutants:$FIRMWARE_SRP_MUTANTS_RESULT" \\\n', "")),
    ("firmware-unit runs every phase (no --shard 0/4)",
     replace(YML, "--self-test --jobs 4 --shard 0/4\n", "--self-test --jobs 4\n")),
    ("firmware-boundary job removed", drop_job("firmware-boundary")),
    ("firmware-verilator job removed", drop_job("firmware-verilator")),
    ("firmware-aecp-mutants job removed", drop_job("firmware-aecp-mutants")),
    ("firmware-boundary step without --require-rv32",
     replace(YML, "ctrl_boundary.py --require-rv32 --selftest --without verilator", "ctrl_boundary.py --selftest --without verilator")),
    ("the policy page drops firmware-srp-mutants' budget row",
     replace(DOC, "| `firmware-srp-mutants` | 45 min | 1890 s | 1620 s |\n", "")),
]

def check(label):
    r = subprocess.run([sys.executable, "-I", "-B", str(clone / "scripts/ci_events.py"), "--check", "--root", str(clone)],
                       capture_output=True, text=True)
    lines = [ln.strip() for ln in (r.stdout + r.stderr).splitlines() if ln.strip()]
    fails = [ln for ln in lines if ln.startswith("FAIL ")]
    finding = f"{len(fails)} finding(s), first: {fails[0]}" if fails else (lines[-1] if lines else "")
    return r.returncode, finding, lines[-1] if lines else ""

original = {p: p.read_text() for p in (YML, DOC)}
rc, _, last = check("head")
print(f"head: rc={rc} {last}")
bad = rc != 0
for label, plant in PLANTS:
    files = dict(original)
    plant(files)
    for p, t in files.items():
        p.write_text(t)
    try:
        rc, finding, last = check(label)
    finally:
        for p, t in original.items():
            p.write_text(t)
    ok = rc == 1
    bad |= not ok
    print(f"[{'CAUGHT' if ok else 'ESCAPED'}] {label}: rc={rc}: {finding[:220]}")
print(f"{len(PLANTS)} plants, {'all caught' if not bad else 'NOT ALL CAUGHT'}")
sys.exit(1 if bad else 0)
