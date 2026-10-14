#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Planted omissions and changed observations must fail executed-union proofs."""

from collections.abc import Callable
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile

import ci_case_receipts as receipts

ROOT = Path(__file__).resolve().parents[1]
DRIVER = ROOT / "tb/verilator/milan_dp_mclk/mclk_mutants.py"


def refuse(action: Callable[[], object], label: str) -> None:
    """A negative control is useful only if the real verifier refuses it."""
    try:
        action()
    except (ValueError, KeyError, TypeError, OSError):
        print(f"receipt control: {label} refused")
        return
    raise AssertionError(f"receipt control accepted: {label}")


def source_controls() -> None:
    """Real Git controls include index-hidden edits and changes during a run."""
    with tempfile.TemporaryDirectory(prefix="receipt-source-") as directory:
        root = Path(directory)

        def git(*args: str) -> bytes:
            """Run fixture Git with the existing configured identity."""
            return subprocess.check_output(["git", *args], cwd=root, stderr=subprocess.STDOUT)

        git("init", "-q")
        path = root / "source.c"
        path.write_text("original\n")
        git("add", "source.c")
        git("commit", "-qm", "Create receipt source control")
        identity = receipts.source_identity(root)
        receipt = receipts.Receipt(root, "control", ["case"], None, root.parent / (root.name + ".json"))
        for flag in (None, "--assume-unchanged", "--skip-worktree"):
            if flag:
                git("update-index", flag, "source.c")
            path.write_text("changed\n")
            refuse(lambda: receipts.source_identity(root), f"dirty source {flag}")
            refuse(receipt.finish, "source changed during execution")
            path.write_text("original\n")
            if flag:
                git("update-index", flag.replace("--", "--no-", 1), "source.c")
        path.write_text("staged\n")
        git("add", "source.c")
        path.write_text("original\n")
        refuse(lambda: receipts.source_identity(root), "staged source under clean working bytes")
        git("reset", "-q", "HEAD", "source.c")
        extra = root / "extra.c"
        extra.write_text("untracked\n")
        refuse(lambda: receipts.source_identity(root), "untracked source")
        extra.unlink()
        path.chmod(0o755)
        refuse(lambda: receipts.source_identity(root), "source executable mode")
        path.chmod(0o644)
        path.unlink()
        refuse(lambda: receipts.source_identity(root), "missing source")
        path.symlink_to("missing")
        refuse(lambda: receipts.source_identity(root), "source replaced by symlink")
        path.unlink()
        path.write_text("original\n")
        assert receipts.source_identity(root) == identity


def main() -> int:
    """Exercise source identity, inventory union, and output comparisons."""
    source_controls()
    spec = importlib.util.spec_from_file_location("mclk_inventory", DRIVER)
    driver = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = driver
    spec.loader.exec_module(driver)
    names = [driver.case_id(case) for case in driver.run_inventory()]
    listed = subprocess.check_output([sys.executable, str(DRIVER), "--list"], text=True)
    assert json.loads(listed) == names
    # Every selector and every mode of the actual mutation table participates.
    assert {run[2] for run in driver.run_inventory() if run[0] == "mutant"} == {
        mutant.mid for mutant in driver.MUTANTS}
    assert {run[1] for run in driver.run_inventory() if run[0] == "control"} == {
        mutant.mode for mutant in driver.MUTANTS}
    head, tree = "1" * 40, "2" * 40
    suite = "milan_dp_mclk"

    def result(name: str) -> dict:
        """A passing or caught observation for one synthetic case."""
        mutant = name.startswith("mutant/")
        return {"case": name, "outcome": "caught" if mutant else "pass",
                "returncode": 1 if mutant else 0,
                "output_sha256": hashlib.sha256(name.encode()).hexdigest()}

    def record(shard: str | None) -> dict:
        """Construct a receipt from the driver inventory."""
        return {"schema": receipts.SCHEMA, "suite": suite, "head": head, "tree": tree,
                "inventory": names, "shard": shard,
                "results": [result(name) for name in receipts.partition(names, shard)]}

    def verify(records: list[dict]) -> dict:
        """Apply the real verifier to synthetic receipts."""
        return receipts.verify(names, records, suite, head, tree)

    unsharded = verify([record(None)])
    for count in (1, 2, 4, len(names)):
        assert verify([record(f"{n}/{count}") for n in range(count)]) == unsharded
    base = [record(f"{n}/4") for n in range(4)]
    # Drop a case from EVERY leg and their claimed inventories. The authority
    # is the driver's independent inventory, never the union's own declaration.
    dropped = copy.deepcopy(base)
    for part in dropped:
        part["inventory"] = names[1:]
        part["results"] = [item for item in part["results"] if item["case"] != names[0]]
    refuse(lambda: verify(dropped), "one case removed from all legs and inventories")
    refuse(lambda: verify(base[1:]), "dropped entire leg")
    refuse(lambda: verify(base + [base[0]]), "duplicate leg")
    for key, value in (("schema", 0), ("suite", "wrong"), ("head", "3" * 40),
                       ("tree", "4" * 40), ("shard", "0/3"), ("inventory", [])):
        changed = copy.deepcopy(base)
        changed[0][key] = value
        refuse(lambda: verify(changed), f"changed {key}")
    for key, value in (("case", "foreign"), ("outcome", "failure"), ("returncode", -9),
                       ("returncode", True), ("output_sha256", "missing")):
        changed = copy.deepcopy(base)
        changed[0]["results"][0][key] = value
        refuse(lambda: verify(changed), f"changed result {key}")
    for bad in ("-1/4", "4/4", "0/0", "0/32"):
        refuse(lambda: receipts.partition(names, bad), f"shard {bad}")
    with tempfile.TemporaryDirectory(prefix="case-receipts-") as directory:
        work = Path(directory)
        inventory = work / "inventory.json"
        inventory.write_text(json.dumps(names))

        def save(path: Path, value: dict) -> None:
            """Retain a receipt with its matching diagnostic files."""
            path.write_text(json.dumps(value))
            logs = path.with_suffix(".logs")
            logs.mkdir(exist_ok=True)
            for item in value["results"]:
                logs.joinpath(hashlib.sha256(item["case"].encode()).hexdigest() + ".log").write_text(item["case"])

        reference = work / "reference.json"
        save(reference, record(None))
        paths = [work / f"shard-{n}.json" for n in range(4)]
        for path, value in zip(paths, base):
            save(path, value)
        command = [sys.executable, str(ROOT / "scripts/ci_case_receipts.py"),
                   "--inventory", str(inventory), "--suite", suite, "--head", head,
                   "--tree", tree, "--reference", str(reference), *map(str, paths)]
        subprocess.run(command, check=True)
        changed = copy.deepcopy(base[0])
        changed["results"][0]["output_sha256"] = hashlib.sha256(b"different checked value").hexdigest()
        paths[0].write_text(json.dumps(changed))
        refuse(lambda: receipts.read_receipts(paths), "changed receipt output digest")
        log = paths[0].with_suffix(".logs") / (hashlib.sha256(names[0].encode()).hexdigest() + ".log")
        log.write_text("different checked value")
        altered = subprocess.run(command, capture_output=True, text=True)
        assert altered.returncode == 1 and names[0] in altered.stdout
        print("receipt control: changed checked value and its digest refused by comparison")
    print(f"case receipt self-test: {len(names)} driver cases, union and comparison controls pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
