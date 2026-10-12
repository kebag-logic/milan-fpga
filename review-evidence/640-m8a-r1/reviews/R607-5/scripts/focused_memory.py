#!/usr/bin/env python3
"""Exercise the unchanged memory contract at the newly linked bank shapes."""
import functools, json, pathlib, sys, tempfile
root = pathlib.Path.cwd()
packet = pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "sw/litex"))
import test_ctrl_memory as t
problems = []
with tempfile.TemporaryDirectory(dir=packet / "scratch", prefix="focused-memory-") as tmp:
    tmp = pathlib.Path(tmp)
    green = set()
    for key, arm in (
        ("banks", t.bank_arms),
        ("checks", functools.partial(t.check_arms, tmp=tmp)),
        ("sim", t.sim_arms),
        ("link", functools.partial(t.link_arms, tmp=tmp)),
        ("registry", functools.partial(t.registry_arms, tmp=tmp)),
    ):
        before = len(problems)
        result = t.run_arm(problems, key, arm)
        if key == "link":
            assert result is True, "RV32 link arm must execute"
        if len(problems) == before:
            green.add(key)
    needs = set()
    for shape in ("1x1_tdm8", "8x8"):
        for interfaces in (1, 2):
            data = json.loads((packet / f"fit-{shape}-if{interfaces}.json").read_text())
            needs.update(data["split"][r]["bytes"] for r in ("rom", "sram"))
    for need in sorted(needs):
        print("NEW LINKED NEED", need)
        t.sim_arms(problems, need=need)
    # The full SoC export arm belongs to the published source validation.
    # This focused run exercises every non-SoC mutation after green baselines.
    t.MUTANTS = tuple(m for m in t.MUTANTS if m.arm != "soc")
    print("FOCUSED MUTANTS", len(t.MUTANTS))
    t.mutant_arms(problems, tmp, green)
assert not problems, problems
print("PASS focused bank, refusal, actual-shape simulation, link, registry and non-SoC mutation checks")
