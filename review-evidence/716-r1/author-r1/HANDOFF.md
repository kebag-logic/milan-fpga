[A601]

# Lane 716 handoff

Local implementation and touched gates are complete; ready for independent review.
Hosted acceptance item 2 remains for the manager's ten consecutive runs.
This handoff supplies evidence, not a review verdict or permission to merge.

Issue: #716; assignment comment 6107547907.
Executor: [A601]. Internal reviewer: [R620]. External reviewer: [R621].
Branch: `716-fw-unit-split`.
Head: `f41e4f2dd56eaccebb30d6c1ec255624b0ae7a48`.
Initial HEAD and resolved assigned base: `ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5`.
Origin was verified as `https://github.com/kebag-logic/milan-fpga.git`.
The initial tree was clean at the base, with the assigned submodules initialized.
Submodule roots were verified before nested Git operations.
The explicit assignment authorizes this lane; its project card still said Backlog.
No board update, push, PR mutation, hosted execution, merge, or hardware action occurred.

## Commits and changes

Both commits use the configured identity and one-line subjects, without bodies or trailers.

- `b27c5537b64925696bebe91fba49b65da685b609`: ci: partition firmware dispatch into four complete phases
- `f41e4f2dd56eaccebb30d6c1ec255624b0ae7a48`: ci: require four firmware jobs within unchanged timeout budgets

| File:line | Change |
|---|---|
| `.github/workflows/rtl-fast.yml:285` | Normal suites use shard 0; saved-state and coverage stay together. |
| `.github/workflows/rtl-fast.yml:296` | Three additional jobs run the complete control, AECP, and SRP campaigns. |
| `.github/workflows/rtl-fast.yml:403` | The required aggregate checks all four results, retaining failure and cancellation semantics. |
| `sw/firmware/ctrl/test/test_ctrl_firmware.py:123` | Four phase selectors and strict shard parsing. |
| `sw/firmware/ctrl/test/test_ctrl_firmware.py:141` | The original normal-suite dispatch remains complete and ordered. |
| `sw/firmware/ctrl/test/test_ctrl_firmware.py:162` | Both original SRP campaigns and pin controls stay together. |
| `sw/firmware/ctrl/test/test_ctrl_firmware.py:180` | Default and sharded dispatch share the same phases. |
| `sw/firmware/ctrl/test/test_ctrl_firmware.py:253` | Invalid or narrowing shard combinations refuse before builds. |
| `sw/firmware/ctrl/test/test_ctrl_firmware_shards.py:29` | Discover live normal-suite and mutant invocations. |
| `sw/firmware/ctrl/test/test_ctrl_firmware_shards.py:131` | Prove exact ownership with missing, duplicate, and future-suite controls. |
| `scripts/ci_events.py:2401` | Derive pinned split recipes from the original command list. |
| `scripts/ci_events.py:3561` | Generate command/condition census; pin all four 45-minute budgets. |
| `scripts/ci_events.py:7812` | Extend SDK cache and mandatory compiler controls to every worker. |
| `scripts/ci_events.py:7946` | Plant census, condition, timeout, and budget-row defects. |
| `scripts/ci_events.py:8644` | Expose `--firmware-census`. |
| `docs/testing/CI_WORKFLOWS.md:62` | Document ownership, preserved coverage, and timing budgets. |
| `docs/testing/CI_WORKFLOWS.md:2348` | Plain shell commands reproduce all four phases. |

Five changed files, 538 insertions and 46 deletions. No generated repository files changed.

## Hosted steps and suites

Seventeen recent completed jobs were read through `gh run list` and read-only APIs.
The slowest observed total is 2450/2700 seconds (90.74%).
This is historical baseline evidence, not the new layout's ten-run acceptance table.
The full per-step data, including timestamps and commit IDs, is [HOSTED-STEPS.csv](HOSTED-STEPS.csv).
Raw logs exceed 200 KB and stay in scratch; [HOSTED-LOG-MANIFEST.md](HOSTED-LOG-MANIFEST.md)
records every byte size and SHA-256 digest.

| Run ID | Job ID | Total s | Control s | Saved-state s | Coverage s |
|---|---|---:|---:|---:|---:|
| 38124499476 | 114426026755 | 2081 | 1716 | 96 | 225 |
| 38120473377 | 114414054241 | 2275 | 1888 | 103 | 253 |
| 38111694096 | 114388499315 | 1800 | 1491 | 82 | 203 |
| 38107600373 | 114376381204 | 2268 | 1868 | 109 | 261 |
| 38103716606 | 114364816994 | 2240 | 1853 | 103 | 253 |
| 38103511711 | 114364197967 | 2253 | 1874 | 103 | 250 |
| 38101301964 | 114357676596 | 1770 | 1464 | 80 | 198 |
| 38097652854 | 114351392059 | 1803 | 1485 | 81 | 204 |
| 38096691753 | 114345004883 | 2320 | 1927 | 105 | 262 |
| 38096542983 | 114344992704 | 1861 | 1469 | 78 | 191 |
| 38096183952 | 114342505501 | 2321 | 1915 | 105 | 262 |
| 38095263410 | 114339840343 | 2276 | 1882 | 103 | 255 |
| 38095215727 | 114339713622 | 2208 | 1833 | 101 | 247 |
| 38091166849 | 114327796960 | 2299 | 1901 | 107 | 257 |
| 38089662232 | 114323421935 | 2231 | 1853 | 101 | 250 |
| 38076540233 | 114284710904 | 1662 | 1393 | 73 | 170 |
| 38075658068 | 114282060753 | 2450 | 1933 | 108 | 263 |

For the assigned-base run 38095263410, job 114339840343, every observed step is below.
Job total includes gaps between API step boundaries.

| Job ID | Step | Seconds |
|---|---|---|
| 114339840343 | Set up job | 1 |
| 114339840343 | Run actions/checkout@v4 | 2 |
| 114339840343 | Fetch RTL dependencies | 2 |
| 114339840343 | Install GoogleTest and GoogleMock and print the versions | 18 |
| 114339840343 | Prove the tally reads a failing and a crashing test as failures | 5 |
| 114339840343 | Cache the pinned RV32 SDK | 2 |
| 114339840343 | Install and verify the pinned RV32 SDK | 2 |
| 114339840343 | Run the control-plane firmware suites and RV32 builds | 1882 |
| 114339840343 | Run the saved-state store suites and its RV32 build | 103 |
| 114339840343 | Hold the firmware coverage ratchet | 255 |
| 114339840343 | Post Cache the pinned RV32 SDK | 1 |
| 114339840343 | Post Run actions/checkout@v4 | 0 |
| 114339840343 | Complete job | 0 |

The control gate dominates. Its control mutation campaign is the largest reporting window,
followed by the combined SRP campaigns. AECP mutation and normal suites are smaller.
The complete coverage measurement costs 170-263 seconds; saved-state costs 73-109 seconds.
Normal dispatch includes the model/port/ADP/ACMP/MAAP families, SRP interfaces 1 and 2,
all shipped shape arms, and AECP core/mailbox/image arms.

The following log-derived table names the scheduling units inside the slow control step.
These are reporting windows, not precise individual binary execution durations.
Normal arms print after execution and coverage captures both drivers until completion.
Buffered transport can delay even a final summary (notably job 114426026755's RV32 line).
The SRP interface boundary includes the first one-interface result; zero pin-window values
mean coalesced output, not zero work. The original logs cannot supply honest per-binary
compile/run timings. No timestamp was invented to fill that gap.

| Job ID | RV32 | normal suite reports | control mutants | AECP window | SRP if2 window | SRP if1 window | pin controls |
|---|---:|---:|---:|---:|---:|---:|---:|
| 114426026755 | 262.936 | 20.398 | 733.268 | 185.374 | 351.402 | 163.385 | 0.000 |
| 114414054241 | 8.572 | 301.346 | 808.736 | 204.391 | 387.347 | 178.416 | 0.000 |
| 114388499315 | 6.179 | 236.614 | 637.526 | 159.553 | 306.972 | 144.855 | 0.000 |
| 114376381204 | 8.241 | 299.773 | 799.137 | 200.804 | 383.175 | 177.814 | 0.000 |
| 114364816994 | 7.250 | 296.439 | 793.711 | 200.058 | 378.927 | 177.277 | 0.000 |
| 114364197967 | 8.820 | 299.823 | 801.054 | 202.211 | 383.665 | 178.938 | 0.001 |
| 114357676596 | 8.730 | 232.000 | 623.501 | 158.035 | 301.340 | 140.640 | 0.000 |
| 114351392059 | 6.577 | 235.536 | 631.864 | 158.866 | 307.870 | 144.416 | 0.000 |
| 114345004883 | 8.240 | 308.283 | 823.960 | 207.973 | 394.759 | 183.865 | 0.000 |
| 114344992704 | 7.606 | 236.357 | 595.751 | 155.648 | 323.670 | 149.959 | 0.000 |
| 114342505501 | 8.307 | 302.805 | 813.952 | 208.520 | 395.634 | 186.335 | 0.000 |
| 114339840343 | 8.175 | 299.808 | 803.633 | 203.424 | 384.677 | 182.501 | 0.000 |
| 114339713622 | 7.924 | 289.903 | 786.370 | 199.338 | 374.867 | 175.346 | 0.000 |
| 114327796960 | 7.869 | 304.478 | 812.309 | 206.501 | 388.115 | 182.482 | 0.000 |
| 114323421935 | 7.867 | 296.711 | 791.267 | 200.430 | 377.514 | 179.420 | 0.000 |
| 114284710904 | 6.062 | 242.907 | 543.368 | 142.618 | 316.324 | 142.498 | 0.000 |
| 114282060753 | 8.259 | 303.899 | 836.018 | 208.083 | 388.737 | 188.729 | 0.000 |

The largest observed step-start-to-control-summary parent window is
1148.176 seconds; the remaining control
window is at most 790.490 seconds.
No observed indivisible suite crossed the 1890-second STOP threshold.

## Command census before and after

[COMMAND-CENSUS.json](COMMAND-CENSUS.json) is generated by the committed checker:

```sh
python3 scripts/ci_events.py --firmware-census
```

The before inventory exactly equals the independently captured original workflow.
Before: 19 normalized script lines in one job.
After: 55 lines in four jobs, including repeated setup.
The command/condition sets are identical after stripping only the exact new shard suffixes.
All job conditions remain `${{ needs.changes.outputs.rtl == 'true' }}`.
All script-step conditions remain implicit `success()`.
Checkout and the digest-keyed SDK cache are also pinned by the complete step-list contract.
Only the authenticated SDK is cached; no check reuses a persisted build output.

Each original line and its destination are listed below. Destination names omit `firmware-`.
The four control-driver destinations add `--shard 0/4`, `1/4`, `2/4`, and `3/4`, respectively.
The linked JSON retains every before/after step name and condition without abbreviation.

| Original line | Command | After: jobs |
|---|---|---|
| 1 | `git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP` | unit, control-mutants, aecp-mutants, srp-mutants |
| 2 | `set -euo pipefail` | unit, control-mutants, aecp-mutants, srp-mutants |
| 3 | `sudo apt-get update -qq` | unit, control-mutants, aecp-mutants, srp-mutants |
| 4 | `sudo apt-get install -y --no-install-recommends libgtest-dev libgmock-dev` | unit, control-mutants, aecp-mutants, srp-mutants |
| 5 | `python3 -m pip install --quiet pyyaml` | unit, control-mutants, aecp-mutants, srp-mutants |
| 6 | `dpkg-query -W libgtest-dev libgmock-dev` | unit, control-mutants, aecp-mutants, srp-mutants |
| 7 | `g++ --version \| head -n 1` | unit, control-mutants, aecp-mutants, srp-mutants |
| 8 | `gcov --version \| head -n 1` | unit, control-mutants, aecp-mutants, srp-mutants |
| 9 | `python3 sw/firmware/gtest/tally_selftest.py` | unit |
| 10 | `set -euo pipefail` | unit, control-mutants, aecp-mutants, srp-mutants |
| 11 | `python3 scripts/ci_rv32_sdk_selftest.py` | unit, control-mutants, aecp-mutants, srp-mutants |
| 12 | `python3 scripts/ci_rv32_sdk.py --destination "$HOME/br-milan-rv32/host"` | unit, control-mutants, aecp-mutants, srp-mutants |
| 13 | `set -euo pipefail` | unit, control-mutants, aecp-mutants, srp-mutants |
| 14 | `python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32` | unit |
| 15 | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4` | unit, control-mutants, aecp-mutants, srp-mutants |
| 16 | `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs "$(nproc)"` | unit |
| 17 | `set -euo pipefail` | unit, control-mutants, aecp-mutants, srp-mutants |
| 18 | `python3 sw/firmware/gtest/fw_coverage.py --selftest` | unit |
| 19 | `python3 sw/firmware/gtest/fw_coverage.py --check --jobs "$(nproc)"` | unit |

## Shard coverage and planted mutants

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware_shards.py --census "$SCRATCH/shard-invocations.json"
```

All 844 discovered invocations occur exactly once: 59 normal, 472 control,
75 AECP, and 238 SRP/pin invocations. These are invocation counts, not test-case counts.
Composite shape and AECP builders enumerate their live entries; mutation identities come
from the current tables, including the unchanged one-interface SRP subset.
Concatenating the four inventories exactly equals the independently recorded baseline,
including order. [BASELINE-INVOCATIONS.json](BASELINE-INVOCATIONS.json) and
[SHARD-INVOCATIONS.json](SHARD-INVOCATIONS.json) preserve those generated records.

The self-test removes the entire normal phase from the selector, then duplicates it in
the control shard. Both planted mutants produce missing/duplicate inventory findings.
A future normal-suite injection is discovered and owned without updating any ownership list.
Nine invalid/narrowing argument combinations refuse with exit 2 before builds.
A failed normal run still prevents mutation dispatch.
Every actual sharded invocation runs these controls before its real workload.
The CI event self-test separately catches missing commands, changed conditions, raised
timeouts, missing budget rows, worker-step drift, SDK drift, and aggregate-result drift.

## Coverage merge comparison

Coverage stays one complete measurement, so no per-shard merge is applicable.
The coverage driver, suite population, exclusion table, ratchet, and thresholds are unchanged.
Both baseline and candidate complete checks passed. An additional comparison recollected
their retained gcov data through the unchanged collector and found equality for all 30 files:
raw and post-exclusion line/branch fractions, plus every covered line and branch location.
Both measurements independently satisfy the existing ratchet with no exclusion findings.
[COVERAGE-COMPARISON.csv](COVERAGE-COMPARISON.csv) provides both sides explicitly.

| File | Raw lines | Raw branches | After exclusions: lines | After exclusions: branches | Baseline = candidate |
|---|---|---|---|---|---|
| sw/firmware/ctrl/acmp/acmp.c | 742/742 | 348/348 | 742/742 | 348/348 | yes |
| sw/firmware/ctrl/acmp/acmp_mbx.c | 73/73 | 26/26 | 73/73 | 26/26 | yes |
| sw/firmware/ctrl/acmp/acmp_nvm.c | 38/38 | 10/10 | 38/38 | 10/10 | yes |
| sw/firmware/ctrl/adp/adp.c | 204/206 | 95/102 | 204/204 | 95/95 | yes |
| sw/firmware/ctrl/adp/adp_mbx.c | 83/83 | 38/40 | 83/83 | 38/38 | yes |
| sw/firmware/ctrl/aecp/aecp.c | 357/357 | 308/308 | 357/357 | 308/308 | yes |
| sw/firmware/ctrl/aecp/aecp_commands.c | 424/424 | 362/362 | 424/424 | 362/362 | yes |
| sw/firmware/ctrl/aecp/aecp_image.c | 77/77 | 80/80 | 77/77 | 80/80 | yes |
| sw/firmware/ctrl/aecp/aecp_maps.c | 222/222 | 290/290 | 222/222 | 290/290 | yes |
| sw/firmware/ctrl/aecp/aecp_mbx.c | 101/101 | 40/40 | 101/101 | 40/40 | yes |
| sw/firmware/ctrl/aecp/aecp_nvm.c | 102/102 | 86/86 | 102/102 | 86/86 | yes |
| sw/firmware/ctrl/aecp/aecp_state.c | 63/63 | 69/69 | 63/63 | 69/69 | yes |
| sw/firmware/ctrl/app/ctrl_app.c | 42/43 | 40/44 | 42/42 | 40/40 | yes |
| sw/firmware/ctrl/app/ctrl_app_aecp.c | 107/107 | 64/64 | 107/107 | 64/64 | yes |
| sw/firmware/ctrl/app/ctrl_app_srp.c | 82/82 | 62/62 | 82/82 | 62/62 | yes |
| sw/firmware/ctrl/loop/ctrl_loop.c | 101/101 | 62/62 | 101/101 | 62/62 | yes |
| sw/firmware/ctrl/maap/maap.c | 209/209 | 140/140 | 209/209 | 140/140 | yes |
| sw/firmware/ctrl/maap/maap_csr.c | 39/39 | 18/18 | 39/39 | 18/18 | yes |
| sw/firmware/ctrl/maap/maap_mbx.c | 98/98 | 60/60 | 98/98 | 60/60 | yes |
| sw/firmware/ctrl/mbx/mbx.c | 189/189 | 74/74 | 189/189 | 74/74 | yes |
| sw/firmware/ctrl/mbx/mbx_wire.h | 15/15 | 12/12 | 15/15 | 12/12 | yes |
| sw/firmware/ctrl/plat/mbx_plat_mmio.c | 10/10 | 0/0 | 10/10 | 0/0 | yes |
| sw/firmware/ctrl/port/ctrl_debug.c | 19/19 | 6/6 | 19/19 | 6/6 | yes |
| sw/firmware/ctrl/port/ctrl_pool.c | 99/99 | 60/60 | 99/99 | 60/60 | yes |
| sw/firmware/ctrl/port/shlan_port.c | 22/22 | 6/6 | 22/22 | 6/6 | yes |
| sw/firmware/ctrl/srp/srp_mbx.c | 515/515 | 478/478 | 515/515 | 478/478 | yes |
| sw/firmware/ctrl/wire/wire.h | 10/10 | 2/2 | 10/10 | 2/2 | yes |
| sw/firmware/ctrl_nvm/nvm_klj2.c | 198/199 | 106/110 | 198/198 | 106/106 | yes |
| sw/firmware/ctrl_nvm/nvm_store.c | 434/434 | 259/266 | 434/434 | 259/259 | yes |
| sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c | 100/100 | 63/64 | 100/100 | 63/63 | yes |

After retaining the baseline and candidate `fw_coverage.py --check --keep` outputs,
the comparison can be reproduced without rebuilding:

```sh
python3 - "$SCRATCH" <<'PY'
from pathlib import Path
import sys
sys.path.insert(0, str(Path.cwd() / "sw/firmware/gtest"))
import fw_coverage as c
scratch = Path(sys.argv[1])
rows = []
locations = []
for label in ("baseline", "candidate"):
    merged = c.collect([scratch / (label + "-coverage") / part
                        for part in ("ctrl", "ctrl_nvm")])
    raw = c.tally(merged)
    locations.append({rel: {n: (ln.count > 0, tuple(a > 0 for a in ln.arcs))
                             for n, ln in source.lines.items()}
                      for rel, source in merged.items()})
    kept, findings = c.apply_exclusions(merged, c.exclusions(c.README.read_text()))
    measured = c.tally(kept)
    assert not findings
    assert not c.compare(measured, c.read_ratchet(c.RATCHET.read_text()))
    rows.append((raw, measured))
assert rows[0] == rows[1] and locations[0] == locations[1]
assert len(rows[0][0]) == 30
print("PASS: all 30 files match before and after exclusions")
PY
```

## Four-CPU timing and prediction

Baseline and candidate commands used CPython 3.12.3, affinity CPUs 112-115, and at most
four build workers. No other test/build workload from this lane ran concurrently.
Only brief status reads and evidence preparation accompanied the measurements.
Long series used a foreground child command at each step, timestamped logs, and a final
exit-code receipt. Every timed command exited zero. Builds started fresh; only the pinned
SDK persisted. The baseline ran before implementation; the candidate ran at the head above.

Host tools: GCC/G++/gcov 16.2.1 (20260810), GoogleTest/GoogleMock 1.18.0.
Hosted logs report GCC 13.3.0 and GoogleTest/GoogleMock 1.14.0.
The matching Python version and measured ratio address the comparison without claiming
identical compiler speed. RV32 GCC is 14.3.0, installed and authenticated by the unchanged
`scripts/ci_rv32_sdk.py`; archive digest:
`d42680e926542595c4c87629d33f5f90aac1e9a964c8955089e0514caa01b78f`.
No SDK, package environment, tree export, or oversized log is in this output directory.

The original job's matching hosted compute steps total 2247 s
on base job 114339840343. The local baseline totals
2606.655866 s. Their ratio is
`2247 / 2606.655866 = 0.862024032`.
Matching steps include tally, SDK verification/self-test, RV32/control, saved-state, and coverage.
Checkout, package installation, cache restore/save, and completion are added separately.

As a conservative second estimate, the slowest matching compute total among all 17 jobs is
2312 s at job 114282060753, giving ratio
0.886960197. The largest observed remaining overhead is
37 s at job 114426026755.
The unrelated TSN-boundary step present on other branches is excluded from that overhead.
Each prediction adds 60 s, the larger of observed overhead and 60 s.
Formula: `ceil(local job seconds * ratio + setup allowance)`.
These estimates use the observed SDK-cache regime; the manager's runs establish hosted acceptance.

| Job | Local 4-CPU s | Base-ratio prediction s | Conservative prediction s | Timeout used |
|---|---|---|---|---|
| firmware-unit | 642.830 | 615 | 631 | 23.37% |
| firmware-control-mutants | 922.927 | 856 | 879 | 32.56% |
| firmware-aecp-mutants | 219.862 | 250 | 256 | 9.48% |
| firmware-srp-mutants | 617.701 | 593 | 608 | 22.52% |

The slowest conservative prediction is 879 s (32.56% of 45 min),
below the required 1620 s / 60% ceiling. All four timeouts remain 45 minutes.
[TIMING-PREDICTIONS.json](TIMING-PREDICTIONS.json), [BASELINE-RESULTS.json](BASELINE-RESULTS.json),
and [CANDIDATE-RESULTS.json](CANDIDATE-RESULTS.json) contain the measurements and arithmetic.

## Gate table

Commands below are plain shell; no gate output was piped into a truncating command.
Set `SCRATCH` to disk storage outside the checkout, `TMPDIR="$SCRATCH"`, and
`MILAN_RV32_CC="$SCRATCH/rv32-sdk/bin/riscv32-linux-gcc"` after installing the SDK.
`--keep` retains complete coverage output for comparison; it does not select fewer suites.
Repeated SDK checks passed in every worker; the table lists repeated identical commands once.

| Command | Exit | Evidence |
|---|---|---|
| `python3 scripts/ci_events.py --check` | 0 | ci-events-check |
| `python3 scripts/ci_scope.py --selftest` | 0 | ci-scope-selftest |
| `python3 scripts/docs_check.py` | 0 | docs-check |
| `python3 scripts/check_doc_style.py` | 0 | doc-style |
| `python3 scripts/check_doc_style.py --selftest` | 0 | doc-style-selftest |
| `python3 scripts/gen_toc.py --check` | 0 | toc-check |
| `python3 scripts/gen_toc.py --selftest` | 0 | toc-selftest |
| `python3 scripts/check_em_dash.py --selftest` | 0 | em-dash-selftest |
| `python3 scripts/check_py_idiom.py` | 0 | python-idiom |
| `python3 scripts/check_py_idiom.py --selftest` | 0 | python-idiom-selftest |
| `python3 sw/firmware/ctrl/test/test_ctrl_firmware_shards.py` | 0 | shards-selftest |
| `python3 scripts/ci_events.py --selftest` | 0 | 2672 arms; ci-events-selftest.log |
| `python3 scripts/ci_events.py --firmware-census` | 0 | preserved=true; COMMAND-CENSUS.json |
| `python3 scripts/check_em_dash.py --base ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5` | 0 | 54 added lines; 339/339 controls |
| `git diff --check ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5 HEAD` | 0 | No whitespace errors in committed change |
| `python3 sw/firmware/gtest/tally_selftest.py` | 0 | Baseline 4.457 s; baseline-tally.log |
| `python3 scripts/ci_rv32_sdk_selftest.py` | 0 | Baseline 1.621 s; baseline-sdk-selftest.log |
| `python3 scripts/ci_rv32_sdk.py --destination "$SCRATCH/rv32-sdk"` | 0 | Baseline 1.008 s; baseline-sdk-verify.log |
| `python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32` | 0 | Baseline 7.276 s; baseline-rv32.log |
| `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4` | 0 | Baseline 2237.606 s; baseline-ctrl.log |
| `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4` | 0 | Baseline 99.549 s; baseline-nvm.log |
| `python3 sw/firmware/gtest/fw_coverage.py --selftest` | 0 | Baseline 0.403 s; baseline-coverage-selftest.log |
| `python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4 --keep "$SCRATCH/baseline-coverage"` | 0 | Baseline 254.736 s; baseline-coverage.log |
| `python3 sw/firmware/gtest/tally_selftest.py` | 0 | Candidate 3.077 s; candidate-firmware-unit-00-tally_selftest.log |
| `python3 scripts/ci_rv32_sdk_selftest.py` | 0 | Candidate 1.237 s; candidate-firmware-unit-01-ci_rv32_sdk_selftest.log |
| `python3 scripts/ci_rv32_sdk.py --destination "$SCRATCH/rv32-sdk"` | 0 | Candidate 1.779 s; candidate-firmware-unit-02-ci_rv32_sdk.log |
| `python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32` | 0 | Candidate 6.290 s; candidate-firmware-unit-03-fw_rv32_selftest.log |
| `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 0/4` | 0 | Candidate 289.319 s; candidate-firmware-unit-04-test_ctrl_firmware.log |
| `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4` | 0 | Candidate 93.962 s; candidate-firmware-unit-05-test_ctrl_nvm.log |
| `python3 sw/firmware/gtest/fw_coverage.py --selftest` | 0 | Candidate 0.400 s; candidate-firmware-unit-06-fw_coverage.log |
| `python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4 --keep "$SCRATCH/candidate-coverage"` | 0 | Candidate 246.763 s; candidate-firmware-unit-07-fw_coverage.log |
| `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 1/4` | 0 | Candidate 920.806 s; candidate-firmware-control-mutants-02-test_ctrl_firmware.log |
| `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 2/4` | 0 | Candidate 216.736 s; candidate-firmware-aecp-mutants-02-test_ctrl_firmware.log |
| `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 3/4` | 0 | Candidate 615.094 s; candidate-firmware-srp-mutants-02-test_ctrl_firmware.log |

The CI contract passed 1944 items and all 2672 self-test arms.
Documentation checks reported zero findings, including 23 scrub controls and four routing controls.
All contents, wording, Markdown punctuation, and Python checks passed; no budgets were loosened.
Baseline and candidate caught all 471 control mutants; AECP and both SRP campaigns and pin
refusals passed. Saved-state ran five shapes and 435 tests; coverage self-test passed 28 cases.
[GATE-RESULTS.json](GATE-RESULTS.json) and [LOCAL-LOG-MANIFEST.md](LOCAL-LOG-MANIFEST.md)
record command results and the sizes/digests of raw logs retained outside this directory.
The file-by-file coverage comparison above and independently captured baseline inventory
comparisons also exited zero.

The full PR lifecycle's local RTL sweeps, protected hosted contexts, candidate-merge checks,
independent reviews, and post-merge containment remain manager/reviewer work. No PR exists
from this author session, and no PR has been marked validated. Those gates are not claimed here.

## Acceptance and STOP audit

| Item | State |
|---|---|
| Historical step analysis | 17 recent jobs; all step timestamps retained. |
| Historical suite analysis | Observable campaign/reporting windows retained; exact individual binary times unavailable from buffered logs. |
| Local split and timing prediction | Four required jobs; each conservative prediction below 60%. |
| Ten consecutive hosted runs below 70% | Pending manager; no hosted runs dispatched. |
| Command and condition preservation | Generated census matches independently captured base. |
| Disjoint, exhaustive live ownership | 844 invocations; missing/duplicate mutants fail; future suite discovered. |
| Coverage population and thresholds | Unchanged; 30-file baseline/candidate equality. |
| CI contract and policy | Updated and validated. |
| Check/arm/ratchet weakening STOP | Not triggered; none removed or weakened. |
| Indivisible hosted suite over 1890 s STOP | Not observed. |
| More than four new jobs STOP | Not triggered; exactly three new jobs. |
| Files outside assignment STOP | Not triggered; all five files are inside the permitted areas. |

The manager owns publication and acceptance item 2's ten-run table.
The prepared PR body therefore says `Relates to #716`.
Internal and external reviewers must independently reconstruct and judge the change.
TAKEN was posted as issue comment 6107555801.
Final public status: [A601] REVIEW READY at `f41e4f2dd56eaccebb30d6c1ec255624b0ae7a48`.
Publication: https://github.com/kebag-logic/milan-fpga/issues/716#issuecomment-6108397728
The branch is left committed and clean; the two local commits have not been pushed.
