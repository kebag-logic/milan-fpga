#!/usr/bin/env python3
"""R580-2 probe P4: the default (all-fabric) selection's population check, without any census file.

Usage: probe_default_population.py <repo> <scratch> [<real route hierarchy report>]
Builds the gate self-test's synthetic route fixture (head code). Variant "synthetic" uses its
hierarchy; variant "real" transplants a published post-route hierarchy report into the same
fixture. For each planted population (no marker, no baseline_placement.tsv) it runs
`check` and `record --write` under the default selection against a fresh baseline recorded
from the unplanted directory, and requires: exit 2, every expected role named in the
first reason, baseline bytes unchanged. Controls require exit 0. Prints one TSV row per
case and a summary; exits 1 if any case is unexpected.
"""

import json
from pathlib import Path
import re
import shutil
import sys

repo, scratch = Path(sys.argv[1]), Path(sys.argv[2])
real = Path(sys.argv[3]) if len(sys.argv) > 3 else None
sys.path.insert(0, str(repo / "syn/ooc"))
import pp_placement  # noqa: E402
import pp_resource_gate as gate  # noqa: E402
from pp_resource_gate_selftest import POLICY, cli, fixture  # noqa: E402

MOD = pp_placement.MODULES
failures = 0


def rows_of(text: str) -> list[str]:
    return text.splitlines(keepends=True)


def module_of(line: str) -> str:
    fields = [field.strip() for field in line.split("|")[1:-1]]
    return fields[1] if len(fields) == 10 else ""


def instance_of(line: str) -> str:
    fields = line.split("|")[1:-1]
    return fields[0].strip() if len(fields) == 10 else ""


def drop(text: str, modules: set[str], subtree: bool = True) -> str:
    """Remove every instance row (and own row, and with subtree its descendants) of the given modules."""
    out, skip_indent = [], None
    for line in rows_of(text):
        fields = line.split("|")[1:-1]
        if len(fields) == 10 and fields[2].strip() != "Total LUTs":
            indent = len(fields[0]) - len(fields[0].lstrip())
            if skip_indent is not None and indent > skip_indent:
                continue
            skip_indent = None
            if re.sub(r"__parameterized[0-9]+$", "", fields[1].strip()) in modules:
                if subtree:
                    skip_indent = indent
                continue
        out.append(line)
    return "".join(out)


def add(text: str, after_module: str, instance: str, module: str) -> str:
    """Insert one uniquely named child row of the given module right after the first row of after_module."""
    out, done = [], False
    for line in rows_of(text):
        out.append(line)
        if not done and module_of(line) == after_module and not instance_of(line).startswith("("):
            fields = line.split("|")[1:-1]
            indent = len(fields[0]) - len(fields[0].lstrip()) + 2
            width0, width1 = len(fields[0]), len(fields[1])
            name = (" " * indent + instance).ljust(width0)
            out.append("|" + name + "|" + module.rjust(width1 - 1) + " |" + "|".join(
                "0".rjust(len(f) - 1) + " " for f in fields[2:]) + "|\n")
            done = True
    if not done:
        raise SystemExit(f"probe could not place {instance} under {after_module}")
    return "".join(out)


def run(variant: str, folder: Path, label: str, text: str, wanted: int, roles: tuple[str, ...]) -> None:
    global failures
    report = folder / "baseline_hierarchy.rpt"
    pristine_report = report.read_text()
    report.write_text(text)
    try:
        for command in (("check",), ("record", "--write")):
            baseline = scratch / f"{variant}-baseline.json"
            baseline.write_text(PRISTINE[variant])
            status, lines = cli(*command[:1], folder, "--endpoint", "route-1x1", "--baseline", baseline, *command[1:])
            changed = baseline.read_text() != PRISTINE[variant]
            reason = next((line for line in lines if "NOT COMPARABLE" in line or "RESULT" in line), "")
            missing = [role for role in roles if f"{role} ({MOD[role]})" not in reason]
            extra = [role for role in MOD if role not in roles and f"{role} ({MOD[role]})" in reason]
            ok = status == wanted and not missing and not extra and (changed == (wanted == 0 and command[0] == "record"))
            failures += not ok
            print(f"{variant}\t{label}\t{command[0]}{' --write' if len(command) > 1 else ''}\twanted {wanted}\tgot {status}"
                  f"\tbaseline_changed={changed}\tnamed_missing={missing}\tnamed_extra={extra}"
                  f"\t{'as-expected' if ok else 'UNEXPECTED'}\t{reason[:300]}")
    finally:
        report.write_text(pristine_report)


shutil.rmtree(scratch, ignore_errors=True)
scratch.mkdir(parents=True)
PRISTINE = {}
variants = [("synthetic", None)] + ([("real", real)] if real else [])
print("variant\tcase\tcommand\twanted\tobserved\tbaseline\tmissing\textra\tverdict\treason")
for variant, source in variants:
    folder = fixture(scratch / variant, "route")
    if source is not None:
        (folder / "baseline_hierarchy.rpt").write_text(source.read_text())
    assert not (folder / pp_placement.REPORT).exists()
    assert pp_placement.MARKER not in (folder / "baseline_integrated.tcl").read_text()
    PRISTINE[variant] = json.dumps({"endpoints": {"route-1x1": {"record": gate.record(folder, "route"), **POLICY}}})
    text = (folder / "baseline_hierarchy.rpt").read_text()
    moved = ("adp", "acmp-listener", "acmp-talker", "srp", "maap")
    cases = [("control", text, 0, ())]
    cases.append(("f0-f4 wrapper retained, no marker", drop(text, {MOD[r] for r in moved}), 2, moved))
    cases.append(("f0-f4 wrapper retained + mailbox, no marker",
                  add(drop(text, {MOD[r] for r in moved}), "milan_datapath" if source else MOD["gptp"],
                      "u_mbx", MOD["mailbox"]), 2, moved + ("mailbox",)))
    cases.append(("all-fabric with SRP removed", drop(text, {MOD["srp"]}), 2, ("srp",)))
    for role in MOD:
        if pp_placement.limits("all-fabric", role) == (1, 1) and role != "wrapper":
            cases.append((f"{role} removed", drop(text, {MOD[role]}), 2, (role,)))
            cases.append((f"{role} duplicated", add(text, MOD["wrapper"], f"dup_{role}", MOD[role]), 2, (role,)))
        elif role != "wrapper":
            cases.append((f"{role} present", add(text, MOD["wrapper"], f"extra_{role}", MOD[role]), 2, (role,)))
    cases.append(("wrapper duplicated (second wrapper elsewhere)",
                  add(text, MOD["gptp"], "dup_wrapper", MOD["wrapper"]), 2, ("wrapper",)))
    # Wrapper and its whole subtree gone: legacy root refusal, now naming each role.
    cases.append(("wrapper subtree removed (full split shape, no marker)", drop(text, {MOD["wrapper"]}), 2,
                  ("wrapper", "adp", "acmp-listener", "acmp-talker", "srp", "aecp", "notify")))
    for label, changed, wanted, roles in cases:
        run(variant, folder, label, changed, wanted, roles)
print(f"probe_default_population: {failures} unexpected")
sys.exit(1 if failures else 0)
