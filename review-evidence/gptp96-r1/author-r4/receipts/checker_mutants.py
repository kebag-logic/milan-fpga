"""Revert each round-4 checker fix in a scratch copy; --selftest must fail at its arm.

usage: python3 -I checker_mutants.py <repo> <scratch>
"""
import shutil
import subprocess
import sys
from pathlib import Path

MUTANTS = {
    "unit_needs_comma": (
        r'UNIT_CELL_RE = re.compile(r"(?:,\s*|\s+|\()(ms|ns|ppm)\)?\s*$")',
        r'UNIT_CELL_RE = re.compile(r",\s*(ms|ns|ppm)\s*$")',
        "Meaning ends 'syncReceiptTimeout ms' escaped"),
    "unit_no_paren": (
        r'(?:,\s*|\s+|\()(ms|ns|ppm)\)?\s*$',
        r'(?:,\s*|\s+)(ms|ns|ppm)\s*$',
        "Meaning ends 'syncReceiptTimeout (ms)' escaped"),
    "minute_digits_no_lookbehind": (
        r'rf"(?<![\d.,])\b{minutes}',
        r'rf"\b{minutes}',
        "decimal minutes failed"),
    "minute_digits_need_space": (
        r'{minutes}[\s-]?min',
        r'{minutes}[\s-]min',
        "unspaced minutes constant copy escaped"),
    "minute_digits_prefix_match": (
        r'{minutes}[\s-]?min(?:ute)?s?\b',
        r'{minutes}[\s-]?min',
        "word starting min failed"),
    "minute_word_no_lookbehind": (
        r'rf"(?<![\w-]){word}',
        r'rf"\b{word}',
        "larger number word failed"),
    "minute_word_needs_minute": (
        r'{word}[\s-]min(?:ute)?s?\b',
        r'{word}[\s-]minutes?\b',
        "number word and min constant copy escaped"),
    "fence_backticks_only": (
        'FENCE_MARKERS = ("```", "~~~")',
        'FENCE_MARKERS = ("```",)',
        "tilde fence failed"),
    "fence_any_marker_closes": (
        'if marker in FENCE_MARKERS and fence in ("", marker):',
        'if marker in FENCE_MARKERS:',
        "copy after a tilde fence constant copy escaped"),
}


def selftest(tree: Path) -> tuple[int, str]:
    result = subprocess.run([sys.executable, "-B", "scripts/check_docs.py", "--selftest"],
                            cwd=tree, capture_output=True, text=True)
    return result.returncode, (result.stdout + result.stderr).strip()


def main() -> int:
    repo, scratch = Path(sys.argv[1]), Path(sys.argv[2])
    source = (repo / "scripts/check_docs.py").read_text(encoding="utf-8")
    bad = 0
    for label, (old, new, expected) in [("control", ("", "", "PASS"))] + list(MUTANTS.items()):
        tree = scratch / label
        if tree.exists():
            shutil.rmtree(tree)
        tree.mkdir(parents=True)
        subprocess.run(f"git -C {repo} archive HEAD | tar -x -C {tree}", shell=True,
                       check=True, executable="/bin/bash")
        shutil.copy(repo / "scripts/check_docs.py", tree / "scripts/check_docs.py")
        if old:
            if source.count(old) != 1:
                print(f"{label}: anchor not unique ({source.count(old)})")
                bad += 1
                continue
            (tree / "scripts/check_docs.py").write_text(source.replace(old, new), encoding="utf-8")
        rc, out = selftest(tree)
        ok = (rc == 0) if label == "control" else (rc == 1 and expected in out)
        bad += not ok
        print(f"{label}: rc={rc} {'OK' if ok else 'UNEXPECTED'} :: {out.splitlines()[-1]}")
    print(f"mutants: {len(MUTANTS)} planted, {bad} unexpected")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
