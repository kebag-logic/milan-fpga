"""Plant one restated value per fresh tree copy and check the docs gate's verdict.

usage: python3 -I copy_probes.py <source-checkout> <work-dir>
Each probe copies the tracked files of <source-checkout>, edits one page,
runs scripts/check_docs.py and compares rc and the 'restates' diagnostic.
"""
import shutil, subprocess, sys
from pathlib import Path

source, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
HDL, INT, HIST = "docs/HDL_DEVELOPER.md", "docs/INTEGRATION.md", "docs/history/v1/RESOURCE_DELTAS_2026_10.md"

def append(page, text):
    return lambda root: (root / page).open("a", encoding="utf-8").write(f"\n{text}\n")

def after_heading(page, heading, text):
    def edit(root):
        path = root / page; s = path.read_text(encoding="utf-8")
        assert s.count(heading + "\n") == 1
        path.write_text(s.replace(heading + "\n", f"{heading}\n\n{text}\n", 1), encoding="utf-8")
    return edit

# (name, edit, expected rc, text the finding must contain or None)
PROBES = [
    ("control", lambda root: None, 0, None),
    ("integer_symbol", append(HDL, "A 375 ms watch."), 1, "'375 ms' restates SYNC_RTO_MS_C"),
    ("integer_no_space", append(HDL, "A 375ms watch."), 1, "restates SYNC_RTO_MS_C"),
    ("integer_hyphen", append(HDL, "A 375-ms watch."), 1, "restates SYNC_RTO_MS_C"),
    ("integer_grouped", append(HDL, "A 300,000 ms countdown."), 1, "restates CEASE_MS_C"),
    ("integer_ppm", append(HDL, "Inside 200 ppm."), 1, "restates RATE_PPM_C"),
    ("integer_ns", append(HDL, "An 800 ns bound."), 1, "restates NPD_HI_C"),
    ("whole_seconds", append(HDL, "A 300 s countdown."), 1, "restates CEASE_MS_C"),
    ("whole_us", append(HDL, "A 20 us threshold."), 1, "restates STEP_LINKUP_NS_C"),
    ("whole_micro_sign", append(HDL, "A 20 µs threshold."), 1, "restates STEP_LINKUP_NS_C"),
    ("whole_mu", append(HDL, "A 20 μs threshold."), 1, "restates STEP_LINKUP_NS_C"),
    ("minutes_digits", append(HDL, "A 5 min countdown."), 1, "restates CEASE_MS_C"),
    ("minutes_word", append(HDL, "A five minutes countdown."), 1, "restates CEASE_MS_C"),
    ("minutes_hyphen", append(HDL, "The five-minute countdown."), 1, "restates CEASE_MS_C"),
    ("same_page_other_section", append(INT, "A 375 ms watch."), 1, "restates SYNC_RTO_MS_C"),
    ("pass_decimal_seconds", append(HDL, "A 0.375 s watch."), 0, None),
    ("pass_decimal_ms", append(HDL, "A 0.1 ms threshold."), 0, None),
    ("pass_unit_word_ms", append(HDL, "A 375 milliseconds watch."), 0, None),
    ("pass_unit_word_us", append(HDL, "A 20 microseconds threshold."), 0, None),
    ("pass_fenced", append(HDL, "```\nsleep 375 ms\n```"), 0, None),
    ("pass_home_section", after_heading(INT, "## Protocol constants", "A 375 ms watch."), 0, None),
    ("pass_unitless", append(HDL, "The fifth lost response."), 0, None),
    ("pass_historical_page", append(HIST, "A 375 ms watch."), 0, None),
]

files = subprocess.run(["git", "-C", str(source), "ls-files", "-z"], check=True,
                       capture_output=True).stdout.split(b"\0")
failures = 0
for name, edit, want_rc, want_text in PROBES:
    root = work / name
    shutil.rmtree(root, ignore_errors=True)
    for entry in filter(None, files):
        target = root / entry.decode()
        target.parent.mkdir(parents=True, exist_ok=True)
        if (source / entry.decode()).is_file():
            shutil.copy2(source / entry.decode(), target)
    edit(root)
    run = subprocess.run([sys.executable, "-B", "scripts/check_docs.py"], cwd=root,
                         capture_output=True, text=True)
    out = run.stdout + run.stderr
    ok = run.returncode == want_rc and (want_text is None or want_text in out)
    failures += not ok
    detail = next((line.strip() for line in out.splitlines() if "restates" in line), out.strip().splitlines()[0])
    print(f"{'ok  ' if ok else 'FAIL'} {name:26s} rc={run.returncode} want={want_rc} | {detail}")
    shutil.rmtree(root)
print(f"probe failures {failures}")
sys.exit(1 if failures else 0)
