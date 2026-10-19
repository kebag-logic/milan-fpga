"""usage: r3_plant.py <comparison-script> <out-dir>
Write the planted mutants of the comparison script into <out-dir>, one file each; every
edit must match exactly once."""
import sys
from pathlib import Path

PLANTS = {
    # R668-2-F1 itself: every record counted as a mutant.
    "baselines-counted": [('baseline = name.startswith("golden-")', "baseline = False"),
                          ('baseline = name == "golden"', "baseline = False"),
                          ('baseline = name.startswith("control ")\n', "baseline = False\n"),
                          ('if baseline == ("patch" in r):', "if False:"),
                          ('if baseline != (r["named_checks"] == []):', "if False:")],
    # The changed test ignores failure IDs: a mutant gaining a failure counts unchanged.
    "changed-ignores-ids": [("if base[n] != head[n]", "if base[n][0] != head[n][0]")],
    # The dispatch log is no longer held to results.json's failure count.
    "dispatch-count-unchecked": [('if "patch" in record and len(lines) != record["failures"]:',
                                  "if False:")],
    # A golden that plants checks is no longer refused.
    "plant-disagreement-ignored": [('if baseline != (r["named_checks"] == []):', "if False:")],
}


def main() -> int:
    source = Path(sys.argv[1]).read_text()
    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    for name, edits in PLANTS.items():
        text = source
        for old, new in edits:
            if text.count(old) != 1:
                raise SystemExit(f"{name}: {old!r} occurs {text.count(old)} times")
            text = text.replace(old, new)
        (out / f"{name}.py").write_text(text)
        print(f"planted {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
