## Rule 12: prefer idiomatic Python

> New first-party Python MUST avoid the constructs that make a defect
> invisible — a bare `except`, a mutable default, a shell string, a shadowed
> built-in, a wildcard import, an unguarded `eval`. New and touched public
> functions SHOULD carry a complete PEP 484 signature and a docstring, and
> SHOULD be short enough to read. Existing debt is ratcheted, not rewritten.

There is more Python in this tree than SystemVerilog — 129 files, 99 526
lines — and before this rule there was no `pyproject.toml`, no `.flake8`, no
`ruff.toml`, no `mypy` configuration and no gate anywhere in it. Twenty-six
hand-written gates policed the RTL and the documentation. Nothing policed the
gates.

### Six refusals, and why the population was already almost clean

| Refusal | Population found |
|---|---:|
| Bare `except:` | 0 |
| Mutable default argument | 0 |
| `shell=True` or `os.system()` | 0 |
| Shadowed built-in | 0 |
| Wildcard import outside the recorded exception | 0 |
| Unguarded `eval`/`exec` | 2 |

Five of the six were already at zero across 3 192 function definitions, which
is worth saying plainly: the house habits are good, and the rule's job is to
keep the seventh occurrence from being the first. The exception list holds one
entry — `from migen import *`, which is that framework's documented usage.

The two real findings were in `sw/trace/test_trace_roundtrip.py`, which read
two `#define` values out of `milan_trace.h` — correctly, because the header is
the ABI and restating the numbers in the test is how the two drift — and then
handed the text to `eval`. `_c_define_int` now parses the expression and walks
every node against an integer-arithmetic whitelist before compiling it. The
other two sites are guarded by explicit character-class matches and are
recorded in the gate's `DYNAMIC_EXEC_INVENTORY` with the guard that makes each
safe; an unguarded `eval` on file text is refused however good the reason.

### A precision bug the first version of the gate had, on the record

The first shadowed-built-in check counted four findings: a dataclass field
`type: int` in `tb/tools/avtp_wire_truth.py`, another in
`scripts/gen_hdl_reference.py`, and a method `def set(...)` in
`sw/builder/test_builder.py`. **All four were wrong.** A class body is not a
scope any unqualified call resolves in, so none of them costs any scope the
ability to call `type()` or `set()` — and `avtp_wire_truth.py` names its field `type`
because IEEE 1722 names it `type`. Acting on those findings would have
demanded a rename that made the structure disagree with the document it
encodes. The gate now descends into a class body only for its functions, and
carries three fixture arms holding that distinction.

### Nine ratchets, and the shape of the debt

The measured populations are in `scripts/py_idiom.budget`. The census that
opened this rule, and what the tree holds now:

| Ratchet | Census | Now |
|---|---:|---:|
| Function over 100 lines | 133 | **9** |
| Module over 1 000 lines | 27 | **10** |
| Public function with no complete signature | 2 312 | **0** |
| Public function with no docstring | 1 687 | **0** |
| `os.path` use | 911 | **1** |
| `open()` outside a `with` statement | 249 | **0** |
| Function taking more than six parameters | 84 | **7** |
| `global` statement | 55 | **0** |
| Line over 120 columns | 106 | **0** |

**This page said of the first and third rows: "Neither is repairable in a
behaviour-preserving change, and attempting either in one pass is precisely
the churn the governing rule forbids." That assessment was wrong, and the tree
now disproves it.** Annotations went 2 312 to 0, docstrings 1 687 to 0, and
long functions 133 to 9, with every gate green,
`sw/builder/test_builder.py`'s printed output byte-identical, and the whole
[RTL sweep](#the-sweep-is-the-oracle-and-it-is-unchanged) unchanged. An
annotation and a docstring add no statement and change no branch, which is why
the sweep and the gate outputs are the oracle they need; the mistake was
reading "large" as "not behaviour-preserving".

What remains is 9 long functions and 10 long modules, and leaving them is a
judgement rather than an oversight. **Four of the 9 are in
`sw/builder/test_builder.py`**. The largest is
`test_baremetal_profile_contract` at line 1903, **7 059 lines** holding 102
nested `def`s and 228 assertions; the other three are `assert_boot_contract`
(969), `test_qspi_owner_transition_completed_write_prefixes` (433) and
`assert_resolved_boot_flow` (411). They are the boot-contract and flash-deploy
gates. The only evidence any of them prints is a summary line, so a stdout
diff cannot prove that an arm inside one was not silently dropped by the
split. Splitting a function whose
output cannot show that it still runs every arm is not a behaviour-preserving
change; it is a change whose oracle does not exist yet, and building that
oracle is its own reviewable work. The other five are in
`sw/litex/milan_soc.py`; the ten that were in `scripts/act_ci.py` and the
three in `scripts/ci_events.py` went with #345's pass over the CI runners.

### Formatting is deliberately not checked

No formatter runs. Rule 9 records why a flag-day rollout is refused here, and
that reasoning applies unchanged to `black` or `ruff format`. Line length is
the one lay-out property this rule gates, at 120 columns rather than the 100
Rule 9 measured and rejected — 100 fights two documented house rules and 120
fights neither.

### Review checklist

- Does this public function say what it takes and what it returns?
- Can a reader see all of this function at once?
- Does this module have one subject a filename could name?
- Is every path a `Path`, or is it a string in one place and a `Path` in the
  next?
- Does every file this opens close deterministically?
- If a hazard is deliberate, is its guard written down where the gate can see
  it?
