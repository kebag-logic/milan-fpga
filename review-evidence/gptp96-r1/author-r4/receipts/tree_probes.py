"""Plant each case the round-3 reviews named into an archive of a commit; run the docs check.

usage: python3 -I tree_probes.py <repo> <commit> <scratch>
Each probe edits a fresh archive copy; the repository itself is never touched.
"""
import concurrent.futures
import shutil
import subprocess
import sys
from pathlib import Path

GUIDE = "docs/HDL_DEVELOPER.md"
CELL = "| syncReceiptTimeout, ms |"
# name: (appended guide text, (old, new) edit of docs/INTEGRATION.md or None, expect_reject)
PROBES = {
    "control": ("", None, False),
    "decimal_min_2_5": ("A 2.5 min hold.\n", None, False),
    "decimal_minutes_7_5": ("A 7.5 minutes hold.\n", None, False),
    "decimal_minutes_0_5": ("Wait 0.5 minutes.\n", None, False),
    "decimal_min_1_5": ("A 1.5 min hold.\n", None, False),
    "tilde_fence": ("~~~sh\nsleep 375 ms\n~~~\n", None, False),
    "twenty_five_minutes": ("A twenty-five minutes soak.\n", None, False),
    "five_minimum": ("At least 5 minimum samples.\n", None, False),
    "unspaced_5min": ("A 5min countdown.\n", None, True),
    "five_min_word": ("A five min countdown.\n", None, True),
    "cell_in_ms": ("The watch is 375 ms.\n", (CELL, "| syncReceiptTimeout in ms |"), True),
    "cell_no_comma": ("A 375 ms watch.\n", (CELL, "| syncReceiptTimeout ms |"), True),
    "cell_paren": ("A 375 ms watch.\n", (CELL, "| syncReceiptTimeout (ms) |"), True),
    "cell_comma_control": ("A 375 ms watch.\n", None, True),
    "copy_after_tilde_fence": ("~~~\n```\n~~~\nA 375 ms watch.\n", None, True),
    "digits_5_min": ("A 5 min countdown.\n", None, True),
    "word_five_minutes": ("A five minutes countdown.\n", None, True),
    "word_five_minute": ("The five-minute countdown.\n", None, True),
    "five_mins": ("A 5 mins countdown.\n", None, True),
    "seconds_300_s": ("A 300 s countdown.\n", None, True),
    "micro_20_us": ("A 20 us threshold.\n", None, True),
    "grouped_300000_ms": ("A 300,000 ms countdown.\n", None, True),
    "decimal_seconds": ("A 0.375 s watch.\n", None, False),
    "unit_word_ms": ("A 375 milliseconds watch.\n", None, False),
    "backtick_fence": ("```sh\nsleep 375 ms\n```\n", None, False),
}


def run(repo: Path, commit: str, scratch: Path, name: str) -> str:
    text, edit, reject = PROBES[name]
    tree = scratch / name
    if tree.exists():
        shutil.rmtree(tree)
    tree.mkdir(parents=True)
    subprocess.run(f"git -C {repo} archive {commit} | tar -x -C {tree}", shell=True,
                   check=True, executable="/bin/bash")
    if text:
        with open(tree / GUIDE, "a", encoding="utf-8") as handle:
            handle.write("\n" + text)
    if edit:
        page = tree / "docs/INTEGRATION.md"
        body = page.read_text(encoding="utf-8")
        assert body.count(edit[0]) == 1, name
        page.write_text(body.replace(*edit), encoding="utf-8")
    result = subprocess.run([sys.executable, "-B", "scripts/check_docs.py"], cwd=tree,
                            capture_output=True, text=True)
    copies = [line.strip() for line in result.stdout.splitlines() if "restates" in line]
    other = [line.strip() for line in result.stdout.splitlines()[1:] if "restates" not in line]
    ok = (bool(copies) == reject) and not other and (result.returncode != 0) == reject
    shutil.rmtree(tree)
    return (f"{name}: expect {'reject' if reject else 'pass'}; rc={result.returncode}; "
            f"{'OK' if ok else 'DIFFERS'} :: {copies or other or result.stdout.strip()}")


def main() -> int:
    repo, commit, scratch = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
    print(f"commit {subprocess.check_output(['git', '-C', str(repo), 'rev-parse', commit], text=True).strip()}")
    with concurrent.futures.ThreadPoolExecutor(8) as pool:
        lines = list(pool.map(lambda name: run(repo, commit, scratch, name), PROBES))
    print("\n".join(lines))
    differs = sum("DIFFERS" in line for line in lines)
    print(f"probes: {len(PROBES)}, differing from expectation: {differs}")
    return 1 if differs else 0


if __name__ == "__main__":
    sys.exit(main())
