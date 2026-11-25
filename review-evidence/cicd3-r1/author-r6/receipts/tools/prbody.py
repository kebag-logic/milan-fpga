"""prbody.py BASE OUT HOSTED.md: round 6's PR body for #1003, from round 5's (BASE): its sections kept where they still
hold, round 6's commit and hosted evidence added (HOSTED.md is the hosted section's text)."""
import sys

base, out, hosted_path = sys.argv[1:4]
text = open(base, encoding="utf-8").read()
hosted = open(hosted_path, encoding="utf-8").read().rstrip() + "\n"


def cut(text: str, start: str, end: str) -> tuple[str, str, str]:
    """text before `start`, from `start` up to `end`, and from `end` on."""
    a = text.index(start)
    b = text.index(end, a)
    return text[:a], text[a:b], text[b:]


STATUS = """## Status

`cicd-3`, nine commits stacked on PR #1001 (`cicd-verilator-perf`, head `fcbc31f3`); head
`9c62539365fea8316dae2b9fd7c68defeff5cb31`. Rebase onto `dev` once #1001 merges; the diff against `fcbc31f3` is
these nine commits only.

- Every local gate this PR touches passes at the head in a clean clone: 37 of 37 commands (list in How to
  validate).
- STATUS_HOSTED
- The full serial sweep was not run in this lane; the candidate bank runs it.

"""

ITEM9 = """9. **`9c625393` rtl-fast's `firmware-boundary` within the same budget** (the ruling on #998 acceptance 2:
   `firmware-boundary` is a hosted job too, and must project at most 1276 s).
   - **What exceeded it.** Over the fourteen hosted rtl-fast runs 45147231523 to 45481508222 the job took
     1302-1667 s. Its projection by the workers' method was 1765 s: its slowest step, 1613 s, plus its slowest
     setup, 152 s. Its builders run one after another under one capture and are 1033-1366 s of each step; the
     judgement after them takes 197-247 s.
   - **The split, with the existing mechanisms** (a literal matrix, artifacts within one run, the aggregate's
     result list):
     - `ctrl_boundary.py --leg K/2 --capture-out DIR` runs only leg K's builders, by their own commands in
       `ctrl_configs.BUILDERS`, under a capture of their own at DIR, and judges nothing. `ctrl_runs.LEGS`: leg 0
       is the control gate's build; leg 1 is every other builder the run judges.
     - `firmware-boundary-capture` runs `leg: [0, 1]` (`fail-fast: false`, 30 minutes, firmware-boundary's
       setup). Each leg uploads `firmware-boundary-capture-<leg>-<sha>`.
     - `firmware-boundary` needs both legs, downloads each capture to the path its leg made it at, and runs the
       unchanged judge: `--selftest --without verilator --capture <leg 0> --capture <leg 1>`. The image builders,
       the stack's own gate, the 112 boundary controls, 192 pin controls and 4 figure controls run there, as
       before.
     - The `rtl-fast` aggregate needs `firmware-boundary-capture` and lists its result. A failed leg skips the
       judge, and the aggregate counts a skipped job as a pass.
   - **Required contexts, cancellation and fork safety are unchanged.** `rtl-fast` is still the one verdict.
     The watcher's expected jobs gain the two legs (generated). Each new job records its job evidence as every
     job does. Nothing new needs a token.
   - **The contract** (`ci_events.py`): both jobs' whole step lists are pinned, and `strategy` is allowed on the
     capture job only. `check_boundary_legs` holds the matrix exactly and as many legs as `ctrl_runs.LEGS`
     holds, plus the judge's need of the legs and both 30-minute limits. The RV32 arms cover the capture job too.
     Six new arms are each caught: a leg dropped, fail-fast, the judge without the need, either timeout raised,
     a third leg in the gate.
   - **Same verdict.** A local replica of the three jobs ran each in a fresh clone at one checkout path. Each
     capture passed through an artifact-like copy (hidden files left out, exec bits dropped). With the paths and
     seconds normalised, the judge's log equals the whole step's, except the eight builder lines the legs print.
     That holds through the final count: `4033 compiled sources of 4326 recorded invocations … 0 finding(s),
     112 boundary, 192 pin and 4 figure controls, 0 misbehaved`, `PASS`. Given one leg's capture alone, the
     judge exits 2 and names each builder of the missing leg. Every `--leg` refusal was run.
   - **Projections** (a figure is the slowest hosted window of that job's part of the step in the fourteen runs;
     a projection adds the slowest setup, 152 s):

     | Job | Figure | Projection |
     |---|---:|---:|
     | `firmware-boundary-capture` leg 0, the control gate's build | 769 s | 921 s |
     | `firmware-boundary-capture` leg 1, the other five builders | 597 s | 749 s |
     | `firmware-boundary`, the step less its builds | 247 s | 399 s |

   - CI_WORKFLOWS.md (the job list, the aggregate's list, "The #998 budget"), the firmware README, the gate's
     docstrings.

"""

FINDINGS_ROW = ("| #998 acceptance 2, the manager's ruling on round 5's stop: rtl-fast's `firmware-boundary` is a "
                "hosted job too | Split into two capture legs and a judge; each projects within 1276 s | `9c625393` |\n")

LIMITS_OLD = """- **`firmware-boundary`** (rtl-fast) can exceed its 30-minute limit on a slow runner, and its timeout cancels
  every run of the head. It is outside this change.
"""
LIMITS_NEW = """- **Other hosted jobs exceed the bound too**, by the same measure: over the last sixty successful runs, rtl-fast's
  `publication-census` (2657 s at most, 1922 s on average, so over 30 minutes on ordinary runners),
  `firmware-control-mutants` (2357 / 1841), `firmware-unit` (1782 / 1472), `firmware-aecp-mutants` and
  `firmware-srp-mutants` (1587 / 1297, 1377 / 1288), `firmware-verilator` (1630 / 1021); docs `docs-gates-0`
  and `-2`; elaborate `elaborate-gates-1`, `-4` and `-0`. The four fail-fast watchers wait for their whole run.
  This change splits `firmware-boundary` only, as ruled. Each of the others needs its own split and a decision.
- **The capture artifacts** are about 46 MB zipped each, kept three days. The manifest collector downloads them
  too, as it downloads every artifact of the run, and reads none of their files.
- `ci/image/tool-inventory.json` and `exec-audit-receipt.json` still name `firmware-boundary`'s old step indices,
  as they did the old `rtl.yml`. No hosted workflow checks them; they are the image work's to regenerate.
"""

VALIDATE_ADD = """python3 scripts/ci_events.py --selftest            # includes the six boundary-leg arms and the capture job's RV32 arms
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --without verilator --leg 2/2 --capture-out /tmp/x   # refused, exit 2
# the hosted shape, at one checkout path (each command in a fresh clone there, as each hosted job is):
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --without verilator --leg 0/2 --capture-out "$T/firmware-boundary-capture-0"
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --without verilator --leg 1/2 --capture-out "$T/firmware-boundary-capture-1"
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator \\
  --capture "$T/firmware-boundary-capture-0" --capture "$T/firmware-boundary-capture-1"   # PASS, the whole run's lines
"""

head, status, rest = cut(text, "## Status", "## Linked Issue / roles")
text = head + STATUS + rest
text = text.replace("Eight commits. Each was measured, and each kept every verdict identical.",
                    "Nine commits. Each was measured, and each kept every verdict identical.")
head, old_hosted, rest = cut(text, "**Hosted run 45514146494 at `96df313f`.**", "## Review findings answered")
text = head + ITEM9 + hosted + "\n" + rest
row_anchor = "| #998 acceptance 2, the owner's ruling"
at = text.index(row_anchor)
eol = text.index("\n", at) + 1
text = text[:eol] + FINDINGS_ROW + text[eol:]
assert LIMITS_OLD in text
text = text.replace(LIMITS_OLD, LIMITS_NEW)
text = text.replace("- [CI_WORKFLOWS.md \"Exhaustive validation\"]",
                    "- [CI_WORKFLOWS.md \"Fast feedback\"](../docs/testing/CI_WORKFLOWS.md#fast-feedback): `firmware-boundary` and "
                    "`firmware-boundary-capture`, the aggregate's list.\n- [CI_WORKFLOWS.md \"Exhaustive validation\"]")
text = text.replace("python3 scripts/check_py_idiom.py && python3 scripts/ci_events.py --selftest\n",
                    "python3 scripts/check_py_idiom.py\n" + VALIDATE_ADD)
text = text.replace("Every command exits 0 at `96df313f`, except the `follow_ring__0` piece.",
                    "Every command exits 0 at `9c625393` (the `--leg 2/2` refusal exits 2 by design), except the "
                    "`follow_ring__0` piece.")
open(out, "w", encoding="utf-8").write(text)
print(f"wrote {out}: {len(text)} bytes")
