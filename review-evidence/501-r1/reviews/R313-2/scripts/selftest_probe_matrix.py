#!/usr/bin/env python3
"""Reviewer probe (R313-2): does --self-test refuse every way a control can
stop proving its assertion?

Usage: python3 selftest_probe_matrix.py <head-tree-copy>

SAVED_STATE_FASTCONNECT.md section 4.4 (this head): "Each must exit 1 with its
registered, named FINDING: line. Missing or unrelated findings fail the
self-test. A traceback fails even alongside the expected finding."

Each arm replaces the body of the existing `collide` control on the COPY with
one exact-text edit, runs --self-test, and requires rc 1 with the self-test's
own "SELF-TEST FAILED: negative control --mutate=collide" line. A last arm
keeps the source unchanged and requires rc 0. Original bytes are restored and
re-verified by SHA-256 after every arm.
"""
import hashlib
import subprocess
import sys
from pathlib import Path

T = Path(sys.argv[1]).resolve()
p = T / "scripts/check_nvm_record_space.py"
orig = p.read_bytes()
BODY = '    ALLOC["FMT_OUT"] = (ALLOC["FMT_IN"][0], ALLOC["FMT_IN"][1])\n'
assert orig.decode().count(BODY) == 1
ARMS = [
    ("crash_before_finding", '    raise RuntimeError("R313 probe: this control crashed")\n'),
    ("crash_after_finding",
     BODY + '    import atexit\n'
     '    atexit.register(lambda: (_ for _ in ()).throw(RuntimeError("late")))\n'),
    ("unrelated_finding", '    _mut_block()\n'),
    ("silent_exit_1", '    raise SystemExit(1)\n'),
    ("no_op", '    pass\n'),
    ("required_text_not_a_finding",
     '    print("is claimed by both FMT_IN[0] and FMT_OUT[0]")\n    _mut_block()\n'),
]
rc = 0
for name, new in ARMS + [("unmodified", None)]:
    if new is not None:
        p.write_text(orig.decode().replace(BODY, new))
    try:
        single = subprocess.run([sys.executable, str(p), "--mutate=collide", "--quiet"],
                                cwd=T, capture_output=True, text=True)
        r = subprocess.run([sys.executable, str(p), "--self-test", "--quiet"],
                           cwd=T, capture_output=True, text=True)
        failed_line = next((ln for ln in r.stdout.splitlines()
                            if ln.startswith("SELF-TEST FAILED")), "")
        tb = "Traceback" in single.stdout + single.stderr
        fl = [ln for ln in single.stdout.splitlines() if ln.startswith("FINDING:")]
        if new is None:
            ok = r.returncode == 0 and not failed_line
        else:
            ok = r.returncode == 1 and "--mutate=collide" in failed_line
        print(f"{name}: control alone rc={single.returncode} traceback={tb} "
              f"findings={len(fl)}; --self-test rc={r.returncode} -> "
              f"{'AS REQUIRED' if ok else 'NOT AS REQUIRED'}")
        if failed_line:
            print(f"    {failed_line[:260]}")
        rc |= 0 if ok else 1
    finally:
        p.write_bytes(orig)
        assert hashlib.sha256(p.read_bytes()).digest() == hashlib.sha256(orig).digest()
print("restored original bytes after every arm")
sys.exit(rc)
