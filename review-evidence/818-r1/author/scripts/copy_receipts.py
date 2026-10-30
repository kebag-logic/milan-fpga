"""(#818) copy_receipts.py <out-dir>: copy this lane's cited logs into <out-dir>/receipts with host paths replaced
by placeholders, files over 200 KB recorded by sha256 and size instead, and write a sha256/size manifest of every
route report the gate reads in each recorded route set.
"""
import hashlib
from pathlib import Path
import sys

OUT = Path(sys.argv[1]) / "receipts"
SCRATCH = Path("$VALIDATION_STORAGE/scratch/818-a710")
LIMIT = 200 * 1024
#: Longest first, so a nested root is replaced before its parent.
PLACEHOLDERS = (("$VALIDATION_STORAGE/scratch/814-a703/viv-dev/w1", "<dev-routes>"),
                ("$VALIDATION_STORAGE/scratch/814-a703b/w-h1", "<head-routes>"),
                ("$VALIDATION_STORAGE/scratch/814-a703b/w-c1", "<control-routes>"),
                ("$VALIDATION_STORAGE/scratch/818-a710", "<scratch>"),
                ("$LANES/818-wns-gate", "<lane>"),
                ("$MANAGEMENT/2026-09-23", "<management>"),
                ("$VALIDATION_STORAGE/scratch", "<scratch-root>"),
                ("$VALIDATION_TOOLS", "<tools>"),
                ("$WORKSPACE_HOME", "<home>"))
SETS = {"dev-1e80128f": "$VALIDATION_STORAGE/scratch/814-a703/viv-dev/w1",
        "head-8b28ebaf": "$VALIDATION_STORAGE/scratch/814-a703b/w-h1",
        "control-c1": "$VALIDATION_STORAGE/scratch/814-a703b/w-c1"}
READ = ("baseline_integrated.tcl", "baseline_implementation.tcl", "baseline_utilization.rpt", "baseline_timing.rpt",
        "baseline_hierarchy.rpt", "baseline_cells.tsv", "baseline_images.json", "alinx_ax7101_route_status.rpt",
        *(f"alinx_ax7101_signoff_{model}_{temp}C_timing.rpt" for model in ("Slow", "Fast") for temp in (0, 85)))


def clean(text: str) -> str:
    """Replace every host root with its placeholder."""
    for root, placeholder in PLACEHOLDERS:
        text = text.replace(root, placeholder)
    return text


def copy(source: Path, target: Path, large: list[str]) -> None:
    """Copy one text file cleaned, or record a large one by digest."""
    data = source.read_bytes()
    if len(data) > LIMIT:
        large.append(f"{hashlib.sha256(data).hexdigest()}  {len(data)}  {target.relative_to(OUT)}")
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(clean(data.decode(errors="replace")))


large: list[str] = []
plan = {
    "before": [*sorted((SCRATCH / "out-before").glob("*.log")), SCRATCH / "out-before/rc.txt",
               SCRATCH / "selftest-dev.log"],
    "after": [*sorted((SCRATCH / "out-after").glob("*.log")), SCRATCH / "out-after/rc.txt",
              SCRATCH / "out-after/mutant-words.tsv"],
    "gates": [SCRATCH / "selftest-1.log", SCRATCH / "mutants-1.log", SCRATCH / "check-baseline-2.txt",
              SCRATCH / "py_idiom-2.txt"],
}
for folder, files in plan.items():
    for source in files:
        if source.is_file():
            copy(source, OUT / folder / source.name, large)
for run in ("rtlfast-32f0d9b5",):
    base = SCRATCH / "r" / run
    for source in sorted(base.rglob("*")):
        if source.is_file() and "runner-temp" not in source.parts:
            copy(source, OUT / run / source.relative_to(base), large)
for run in ("docs-32f0d9b5",):
    base = SCRATCH / "docs" / run
    for source in sorted(base.rglob("*")):
        if source.is_file() and "runner-temp" not in source.parts:
            copy(source, OUT / run / source.relative_to(base), large)
manifest = ["route set\tdirective directory\treport\tbytes\tsha256"]
for name, root in SETS.items():
    for directory in ("ax7101/gateware", "ax7101-AltSpreadLogic_high", "ax7101-ExtraTimingOpt"):
        for report in READ:
            path = Path(root) / directory / report
            if path.is_file():
                data = path.read_bytes()
                manifest.append(f"{name}\t{directory}\t{report}\t{len(data)}\t{hashlib.sha256(data).hexdigest()}")
(OUT / "route-reports.tsv").write_text("\n".join(manifest) + "\n")
(OUT / "large.sha256").write_text("\n".join(large) + ("\n" if large else ""))
print(f"receipts written; {len(large)} large files recorded by digest")
