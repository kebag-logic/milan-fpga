"""Prove local-binding regressions fail and valid external definitions still pass."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from unittest.mock import patch
sys.path.insert(0, str(Path("sw/firmware/gtest").resolve()))
import fw_rv32_selftest as checks
cc = os.environ["MILAN_RV32_CC"]
for arm in ("ctrl", "nvm"):
    with tempfile.TemporaryDirectory(prefix="binding-mutant-") as tmp:
        if arm == "ctrl":
            original = checks.ctrl_arms.run
            def mutated(command, **kwargs):
                return original([arg for arg in command if arg != "--extern-only"], **kwargs)
            context = patch.object(checks.ctrl_arms, "run", mutated)
        else:
            original = checks.nvm_rv32._tool
            def mutated(compiler, tool, *args):
                return original(compiler, tool, *(arg for arg in args if arg != "--extern-only"))
            context = patch.object(checks.nvm_rv32, "_tool", mutated)
        with context:
            try:
                checks.runtime_cases(cc, Path(tmp))
            except AssertionError as exc:
                message = str(exc)
                assert ("RESULT: PASS" in message if arm == "ctrl" else message == "[]"), message
                print(f"PASS: {arm} same-name static control catches restored local-name resolution")
            else:
                raise AssertionError(f"{arm}: local-name resolution mutation survived")

work = Path(__file__).resolve().parent / "scratch/runtime-binding"
symbol = "__review_runtime_service"
for arm, source in (("ctrl", "port/ctrl_debug.c"), ("nvm", "nvm_store.c")):
    tree = work / arm
    private = tree / source
    local_source = private.read_text()
    nm = cc.removesuffix("gcc") + "nm"
    objects = work / (arm + "-masked")
    if arm == "ctrl":
        objects /= "rv32"
    listing = subprocess.check_output([nm, *map(str, sorted(objects.glob("*.o")))], text=True)
    assert f"t {symbol}" in listing and f"U {symbol}" in listing, listing
    print(f"PASS: {arm} private-definition probe emitted both t and U for {symbol}")
    for binding, declaration in (("global", ""), ("weak", "__attribute__((weak)) ")):
        private.write_text(local_source.replace("__attribute__((used)) static ", declaration))
        output = work / (arm + "-" + binding)
        if arm == "ctrl":
            result = checks.ctrl_arms.arm_rv32(checks.Tree(tree, output, work / "reuse"), True)
            assert result.rc == 0, result.log
            output /= "rv32"
        else:
            findings, _ = checks.nvm_rv32.build(tree, output, work / "gen", cc)
            assert not findings, findings
        merged = work / (arm + "-" + binding + "-partial.o")
        subprocess.run([cc.removesuffix("gcc") + "ld", "-m", "elf32lriscv", "-r", "-o", str(merged),
                        *map(str, sorted(output.glob("*.o")))], check=True)
        unresolved = subprocess.check_output([nm, "-u", str(merged)], text=True)
        assert symbol not in unresolved, unresolved
        print(f"PASS: {arm} accepts {binding} definition; partial link resolves the reference")
    private.write_text(local_source)
print("Binding controls: all passed")
