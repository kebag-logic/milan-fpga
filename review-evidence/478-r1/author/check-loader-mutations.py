import ast
import inspect
from pathlib import Path
import sys
sys.path.insert(0, str(Path.cwd() / "sw/builder"))
import test_builder as tb
original = tb.eb._load_clocking
original_max = tb.eb.MAX_AUDIO_UNIT_RATES

def require_failure(label, expected):
    try:
        tb.test_audio_unit_rates_loader_contract()
    except AssertionError as exc:
        assert expected in str(exc), f"{label}: unexpected failure {exc}"
        print(f"PASS: {label} caught: {exc}")
    else:
        raise AssertionError(f"{label} escaped gate 36a")

try:
    tb.eb.MAX_AUDIO_UNIT_RATES = 9
    require_failure("maximum raised to nine", "distinct ninth entry accepted")
    tb.eb.MAX_AUDIO_UNIT_RATES = 7
    try:
        tb.test_audio_unit_rates_loader_contract()
    except tb.eb.ConfigError as exc:
        assert "walk bound is 7" in str(exc)
        print(f"PASS: maximum lowered to seven caught by legal-eight boundary: {exc}")
    else:
        raise AssertionError("seven-entry bound escaped boundary test")
    tb.eb.MAX_AUDIO_UNIT_RATES = original_max
    tree = ast.parse(inspect.getsource(original))
    fn = tree.body[0]
    before = len(fn.body)
    fn.body = [node for node in fn.body if not (
        isinstance(node, ast.If) and ast.unparse(node.test) == "len(set(rates)) != len(rates)")]
    assert len(fn.body) == before - 1
    namespace = vars(tb.eb).copy()
    exec(compile(tree, "<duplicate-refusal-removed>", "exec"), namespace)
    tb.eb._load_clocking = namespace["_load_clocking"]
    require_failure("duplicate refusal removed", "duplicate accepted")
finally:
    tb.eb.MAX_AUDIO_UNIT_RATES = original_max
    tb.eb._load_clocking = original
print("PASS: all three loader mutations refused; checkout source unchanged")
