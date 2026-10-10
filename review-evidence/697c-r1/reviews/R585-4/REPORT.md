[R585] NEGATIVE - exact head e07b305458ed3520e4adfc55e9746144ce5cdc79

# R585-4: external review of PR #705 (issue #697, lane 697c), round 4

Exact head `e07b305458ed3520e4adfc55e9746144ce5cdc79`, tree `ec8f8fb21ee972f83bf14a535e07f3633bc9a35e`.
This is a delta review of `d1b22e80..e07b3054`: four commits (`6d43e1978`, `d25ae924a`, `9453fcc10`, `e07b30545`).
The delta changes only the boundary gate (`ctrl_boundary.py`, `ctrl_configs.py`), its new controls module (`ctrl_plants.py`), `sw/firmware/ctrl/README.md` and `docs/testing/CI_WORKFLOWS.md`.

## Summary

- **R585-3-F1 (MAJOR) is resolved.**
  - Hosted `firmware-unit` at this exact head is green (job 114206016568, 2489 s of its 2700 s limit).
  - The boundary step took 93 s, inside its 300 s budget. Steps 10 (store suites, 102 s) and 11 (coverage ratchet, 258 s, `firmware coverage: PASS (30 files)`) ran.
  - The gate judges exactly the configurations it judged at `d1b22e80`. I recorded every exploration at both heads: 148 explorations and 942 configurations each. The sets of (unit, flags, label) are equal, and so is what each configuration read and tested.
  - All 45 controls of `d1b22e80` are kept with identical plant fields and needles. 14 are new, plus the shared unplanted base: 60 in all.
  - The reuse is sound on every control. I judged all 60 in full, with reuse on and with reuse off: 0 of 60 differ (173 findings each), and every verdict is right in both modes.
- **R584-3-F1 (MINOR) and R585-3-S2 are resolved.** My own plant of R584-3's shape (a C++-only `maap/maap_r584.h` reached only through `test_maap_differential.cpp`) is CAUGHT at this head and ESCAPED at `d1b22e80`. An unresolved and a computed C++ name in a real builder each fail the gate by name.
- **R585-3-S1 is resolved for the forms it named, but its class is not closed: R585-4-F1 (MINOR).**
  - `"-D" + NAME`, `"-DNAME={}".format(x)` and `"".join(["-D", name])` in a real builder are refused by name.
  - But four ordinary spellings of a builder's `-D` are neither derived nor refused. A firmware unit that reaches a stack example header under that mode passes the gate:
    - Makefile `$(patsubst %,-D%,$(MODES))`, a sibling of the listed `$(addprefix -D,...)`;
    - Makefile `CFLAGS+=-DNAME` with no space;
    - an f-string whose `-D` is not its first text;
    - a `-D` inside a multi-word literal, which R584-3-S1 already noted.
  - The same plant written as `CFLAGS += -DNAME` or `["-DNAME"]` is CAUGHT.
  - No current builder writes a firmware flag in these forms, so today's verdict holds.
- One RESIDUE: the PR body still says round 4 has no hosted run (R585-4-RS1). There are also two SUGGESTIONs.

## 1. Findings

### R585-4-F1 - MINOR - Conformance, Robustness, Tests, Docs - a builder's `-D` that is not at the start of a literal or a Makefile word is neither a mode nor refused

`[R585] MINOR Conformance/Robustness/Tests/Docs - sw/firmware/ctrl/test/ctrl_configs.py:203-253 - -D flags in patsubst, VAR+=-D, mid-f-string and multi-word literal forms escape derivation and refusal`

**Where**
- `ctrl_configs.py:229` (Python): a string constant is considered only when `node.value[:2]` is `-D`/`-U`.
- `ctrl_configs.py:213` (Python): an f-string is considered only when its literal start is `-D`/`-U`.
- `ctrl_configs.py:247` (Makefile): a word is considered only when `word[:2]` is `-D`/`-U`.
- Any other `-D` token a builder holds is skipped silently.

**Authority**
- Round-4 assignment item 3 ([issuecomment-6096148471](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6096148471)): "a flag that is neither a literal nor an f-string" is "refused by name".
- The head's own contract:
  - `sw/firmware/ctrl/README.md:98`: "The builders' own `-D` and `-U` flags ... are the build modes".
  - `README.md:100`: "A flag a builder computes at run time, an f-string, is a value".
  - `README.md:101-102`: "Any other `-D` or `-U` a builder writes that is neither a literal nor an f-string refuses the gate by name", with `$(addprefix -D,...)` as an example.
  - The same claims are at `ctrl_boundary.py:54-64` and `ctrl_configs.py:12-24`.

**Evidence** (`receipts/probes-head-e07b3054.txt`; each probe's patch, log and rc are in `receipts/probes-head-e07b3054/`)
- Every probe appends `#ifdef <M>` / `#include "adp_port.h"` / `#endif` to `sw/firmware/ctrl/adp/adp_mbx.c`. Only how a real builder writes `-D<M>` changes.
- `mk-spaced-control`, `CFLAGS += -DCTRL_R585_MAKE` in `tb/verilator/mbx/Makefile`: CAUGHT, `firmware [-DCTRL_R585_MAKE]: adp/adp_mbx.c includes tsn-c-stack/examples/adp_port.h`.
- `py-list-literal-control`, `["-DCTRL_R585_MODE"]` in `ctrl_arms.py`: CAUGHT the same way.
- `mk-patsubst`, `CFLAGS += $(patsubst %,-D%,$(R585_MODES))`: **0 findings**. The mode list printed in the log lacks `CTRL_R585_MAKE`.
- `mk-append-nospace`, `CFLAGS+=-DCTRL_R585_MAKE`: **0 findings**. This also escapes at `d1b22e80` (`receipts/probes-base-d1b22e80.txt`).
- `py-fstring-mid`, `f"{R585_CC} -DCTRL_R585_MODE -c x.c"`: **0 findings**.
- `py-midstring`, `"-O2 -DCTRL_R585_MODE".split()`: **0 findings**. This is R584-3-S1's form.
- `receipts/scan_unread_flags_head.txt` lists every `-D`/`-U` token of the 32 builders that the readers do not take. There are two, both in the tsn-gen CMake command at `scripts/ci_events.py:547`. They are CMake cache variables, not a firmware build. So no current firmware mode is missed.

**Impact**
- `CFLAGS+=-DX` and `$(patsubst %,-D%,...)` are ordinary Make idioms. A shell command string with `-D` is an ordinary Python form.
- A builder written that way compiles the firmware or the stack under a mode the gate never explores. A boundary include under that mode then passes the required gate silently. These are honest spellings, not deliberately hidden text.
- Round-4 item 3 is met for the forms that were probed, not for the class the item and the README state. `$(patsubst ...)` is the same kind of Make-computed flag as the listed `$(addprefix ...)`.
- Severity is MINOR, not MAJOR, because no builder at this head uses these forms (scan above).

**Required outcome**
- Every `-D`/`-U` token a builder holds is either derived (a mode or a value) or refuses the gate by name. "Every token" means anywhere in a Python string constant or f-string part, or a Makefile word, not only at its start.
- A token that is not a firmware compile flag may sit on an exclusion list that the gate checks and prints, as `NOT_SOURCES` is: today that is the tsn-gen CMake line.
- Planted controls refuse each of the four forms above by name.
- The README and docstring statements then hold as written. Narrowing the docs alone would leave round-4 item 3 unmet for `$(patsubst ...)`. That would need a manager decision.

**Verification**
- `scripts/run_probes.sh <copy> <out> mk-patsubst mk-append-nospace py-fstring-mid py-midstring`: each gives a finding or `REFUSED` by name.
- `mk-spaced-control` and `py-list-literal-control` stay CAUGHT.
- `scripts/scan_unread_flags.py <tree>` reports no unread token outside the checked exclusions.
- `ctrl_boundary.py --require-rv32 --selftest` passes with 0 misbehaved.

### R585-4-RS1 - RESIDUE - Docs (PR body only) - the Status and Known-limitations lines still say round 4 has no hosted run

This is wording only. The body changes no measurement, test or code, and the hosted run has since happened.

Exact fix:
- In Status, replace "Round 4 is not pushed, so no hosted run covers it yet." with: "Hosted checks at `e07b3054`: `rtl-fast` success; `firmware-unit` passed in 41 min 29 s of its 45 (job 114206016568), its boundary step in 93 s, with the store suites and the coverage ratchet run."
- In Known limitations, replace "it is not yet measured on a hosted runner." with: "on a hosted runner at `e07b3054` the step took 93 s (job 114206016568)."

### R585-4-S1 - SUGGESTION - Robustness - the hosted `firmware-unit` job has 211 s of headroom, mostly because step 8 varies

- At this head the job took 2489 s of 2700 s. Step 8 alone took 1999 s. The delta does not touch step 8.
- On 34 recent hosted runs, step 8 ranged from 1099 s to 2082 s (`receipts/hosted_firmware_unit_history.tsv`). One branch without the boundary step already reached a 2468 s job.
- At step 8's observed peak, this head's job would take about 2572 s. That is still under the limit. A step that used its full 300 s budget on such a runner would exceed 45 minutes.
- The boundary step itself meets its budget with a 69 % margin (93 of 300 s).
- Consider tracking the job's headroom: raise `timeout-minutes` or split step 8. That belongs to a separate Issue, outside this lane's scope.

### R585-4-S2 - SUGGESTION - Docs - CI_WORKFLOWS states a local stand-in figure that a hosted run now replaces

- `docs/testing/CI_WORKFLOWS.md:71-74` gives the pinned-host runs (74 to 82 s, 218 s margin). It says that figure "stands in until a hosted run". That is accurate as written.
- The hosted figure is now known: 93 s, job 114206016568.
- Consider stating it the next time the file is touched.

## 2. Round-4 items, re-run independently at this head

| Item | Result | Receipt |
|---|---|---|
| 1. Same configurations, modes and shapes, nothing dropped or sampled | 148 explorations and 942 configurations at both `d1b22e80` and `e07b3054`. The (side argv, unit, flags, label) sets are equal, and each configuration's deps, tested macros and errors are equal. 0 findings at both. The derived universe is 18 modes, 5 shapes and 2 contracts. | `receipts/configs_base_d1b22e80.json`, `configs_head_e07b3054.json`, `compare_configs.txt` |
| 1. Every control kept | All 45 `d1b22e80` controls are unchanged in every plant field and needle (the field `mode` is renamed `words`). 14 controls are new, plus the base: 60 in all. Pin controls (`ctrl_pin.py`) are untouched by the delta. | `receipts/compare_plants.txt` |
| 1. Reuse and early stop do not change a verdict | All 60 controls judged in full (no early stop), with reuse on (8842 run, 40944 reused) and off (49786 run): identical findings on 60 of 60, every verdict right in both. The real checkout's judgement reuses nothing from the controls: its keys hold the checkout's own paths, and it ran 943 preprocessings for 942 configurations. | `receipts/memo_on.json`, `memo_off.json`, `memo_compare.txt` |
| 1. Hosted `firmware-unit` at the exact head | success, 2489 s. Step 9 took 93 s and printed `942 configurations, 943 preprocessed ... 0 finding(s), 60 boundary and 20 pin controls, 0 misbehaved` and `ctrl_boundary: PASS`; all 60 `[ok] boundary control` lines are present. Step 10 took 102 s (PASS). Step 11 took 258 s (`firmware coverage: PASS (30 files)`). At `d1b22e80`, job 114173809799 was cancelled at 2716 s with step 9 at 750 s. | `receipts/hosted_firmware_unit_timings.txt`, `hosted_firmware_unit_e07b3054_steps9-11.log`, `hosted_firmware_unit_job_*.json` |
| 1. The gate stays in the required job | `rtl-fast.yml:294-295` runs `ctrl_boundary.py --require-rv32 --selftest` inside `firmware-unit`. The delta changes no workflow. | `git diff --stat d1b22e80..e07b3054` |
| 1. Local self-test | rc 0, the same summary line, 60 boundary and 20 pin controls, 0 misbehaved, peak RSS 293 MB. Wall time was 6 min 17 s on four pinned CPUs of a host at load 30 to 38. That is not representative; the hosted 93 s is the budget evidence. | `receipts/head_selftest_4cpu.log`, `.time`, `.rc` |
| 2. Builder C++ names resolve or fail by name | `test_maap_differential.cpp` is followed: my R584-3-shape plant is CAUGHT, `firmware c++: maap/maap_r584.h includes tsn-c-stack/tests/acmp_fake.hpp, not one of the stack's public headers`. At `d1b22e80` the same plant gives 0 findings. `ctrl_arms.py` naming `test/test_r585_missing.cpp` fails by name ("resolves to no file"), and so does an f-string name ("computes the name of a C++ source"); both escape at `d1b22e80`. | `receipts/probes-head-e07b3054/`, `probes-base-d1b22e80/` |
| 3. A flag neither literal nor f-string refused by name | `"-D" + ...`, `.format`, and `"".join(["-D", name])` in `ctrl_arms.py` give exit 2 with the builder and flag named. The six Python and Makefile forms of the self-test pass. Four other forms escape: R585-4-F1. | as above |
| No behaviour, image, coverage or kill change | Only the gate's three modules import one another (importer scan). No firmware source, header, test, builder, mutation table, coverage row, Makefile or workflow is in the delta. Hosted steps 8, 10 and 11 are green at the exact head. Earlier rounds' image and coverage evidence stands. | `git diff --stat`, hosted log |
| Python idiom ratchet | `check_py_idiom.py` rc 0; `ctrl_boundary.py` is 906 lines. | `receipts/check_py_idiom.log` |

## 3. Prior public findings at this head

| Finding | Status at `e07b3054` | Evidence |
|---|---|---|
| R585-3-F1 (MAJOR): hosted `firmware-unit` timeout | **Resolved.** See section 2, item 1. | hosted job 114206016568; `compare_configs.txt`; `compare_plants.txt`; `memo_compare.txt` |
| R584-3-F1 (MINOR): `test_maap_differential.cpp` not followed | **Resolved.** CAUGHT at the head, ESCAPED at the prior head. The self-test control is present. | `probes-head-e07b3054/r584-maap-differential.*` |
| R585-3-S1: a flag neither literal nor f-string | **Resolved for its forms.** The class remains open as R585-4-F1 (MINOR). | section 1 |
| R585-3-S2: one C++ source not followed | **Resolved** (same as R584-3-F1). Unresolved names now fail by name. | as above |
| R584-3-S1: multi-word literal, `FORCED` constant, pin recipe ignoring errors | **Retained as SUGGESTION** for the `FORCED` and pin-recipe parts, which are not addressed and optional. The multi-word literal part is folded into R585-4-F1, because round-4 item 3 and the README's new refusal claim now cover it. | `probes-head-e07b3054/py-midstring.*` |
| R585-2-S2: `aecp_arms.py:83` takes the submodule's `tests/` under an explicit `--stack` | **Retained as SUGGESTION** (optional, untouched by the delta). | code read |
| R585-3-RS1: PR body hosted wording | **Applied** for `d1b22e80`. Superseded by R585-4-RS1. | PR body lines 20 and 214 |
| Earlier rounds (R584-1/2, R585-1/2 findings) | **Still holding.** Every `d1b22e80` control is unchanged and passes at the head, locally and hosted. | `compare_plants.txt`, hosted step 9 |

## 4. Lens lines

```text
[R585] MINOR Conformance — R585-4-F1 (ctrl_configs.py:213,229,247; README.md:98-102) — round-4 item 3 is unmet for $(patsubst %,-D%,...) and three other spellings. Otherwise checked: item 1 (hosted job 114206016568; receipts/compare_configs.txt, compare_plants.txt, memo_compare.txt), item 2 (receipts/probes-head-e07b3054/r584-maap-differential.*, cxx-name-*.*), acceptance 2 at the head (local and hosted self-test, 0 findings), acceptance 4 coverage (hosted step 11, 30 files PASS).
[R585] PASS RTL — git diff --stat d1b22e80..e07b3054 (no hdl/, Makefile, firmware source or workflow); ctrl_boundary.py:479-498,732-771 (sides -> explorers -> compiler pool, no wait cycle; judge returns only after every side finishes; a side's exception sets stop and re-raises) — the gate's architecture is checked against the module contract. Images are unaffected by construction: only the gate's three modules import one another. Peak RSS is 293 MB; the module is under its 1000-line limit.
[R585] MINOR Robustness — R585-4-F1 — four -D spellings are neither derived nor refused. Otherwise checked: Memo key, digest and listing rule (ctrl_boundary.py:249-347) against 60 controls with reuse on and off; stop and exception paths (ctrl_boundary.py:396-401,446-447,758-770); NOT_SOURCES checks (ctrl_configs.py:111-116,597-613).
[R585] MINOR Tests — R585-4-F1 — no control covers the four escaping forms, and each escapes. Otherwise checked: 14 new controls, each matching a probe that escapes at d1b22e80 and is caught at the head (receipts/probes-*); all 60 controls reach their verdict when judged in full (receipts/memo_*.json); hosted 60/60 [ok].
[R585] MINOR Docs — R585-4-F1 — sw/firmware/ctrl/README.md:98-102, ctrl_boundary.py:54-64 and ctrl_configs.py:12-24 claim more than the readers do. Otherwise checked: README.md:94-97,114-118 and CI_WORKFLOWS.md:67-74 against the code and the runs (56 refused plus 3 passing plus the base = 60; 218 s = 300 - 82; job 114173809799 at 2716 s with step 9 at 750 s); 0 U+2014 in the delta; residue RS1 recorded with its exact fix.
```

## 5. Completion ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R585-4-F1) | Round-4 items 1 to 3; acceptance 2 and 4 through the delta; hosted `firmware-unit` and `rtl-fast` at the head | R585-4 | `e07b3054` |
| RTL | CLEAN | Delta file list (no HDL, firmware, Makefile or workflow); `ctrl_boundary.py` concurrency and stop structure; the importer scan | R585-4 | `e07b3054` |
| Robustness | UNCLEAN (R585-4-F1) | `ctrl_configs.py` flag and name readers; the Memo; stop and exception paths; 13 head probes and 5 base probes | R585-4 | `e07b3054` |
| Tests | UNCLEAN (R585-4-F1) | 60 controls (45 kept, 14 new, the base), full judgement with reuse on and off, hosted 60/60 | R585-4 | `e07b3054` |
| Docs | UNCLEAN (R585-4-F1); RS1 carried | `README.md:90-118`, `CI_WORKFLOWS.md:55-78`, module docstrings, PR body | R585-4 | `e07b3054` |

## 6. Real limits

- I ran no source bank and no merge candidate. Images and coverage were not rebuilt locally. The delta touches no input of theirs, and the hosted steps 8, 10 and 11 at the exact head are the execution evidence. Earlier rounds' image identity stands.
- The local timing (6 min 17 s on four pinned CPUs) was taken at host load 30 to 38. It says nothing about the hosted budget.
- `check_em_dash.py` could not run: its pinned renderer is not installed, and no shared install was allowed. A raw count over the delta finds 0 U+2014. Hosted `docs-check` and `docs-check-no-git` are green at the head.
- Probes call the gate's own `derive` and `judge` on a scratch copy. They skip the stack's gate and the Makefile pin check, which the full local self-test ran (PASS).
- Local tools differ from hosted: Python 3.14, gcc 16 and clang 23 here; the RV32 SDK is the pinned one.
- I initialised `third_party/lwSRP` and `third_party/tsn-c-stack` in the review clone at their gitlinks. Tracked bytes, modes and index equal the head tree (`receipts/clone_integrity.txt`).
- At my last check, hosted Verilator shards 1/5 and 2/5 were still in progress (`receipts/hosted_check_runs_e07b3054.tsv`). `Physical gPTP` is skipped. That is a skipped context, not hardware proof. Physical calibration was NOT RUN.

## 7. Pending manager duties

- Hosted acceptance at the exact head: the two Verilator shards still running, and act per policy.
- Merge-candidate validation on current dev `e8454e27` (builder and native banks), with receipts linked on the PR.
- Carry R585-4-RS1 to the residue checklist and the PR body.
- Decide on R585-4-S1: track the job headroom in a separate Issue.

## 8. Reproduce

- `scripts/record_configs.py <tree> <out.json> [jobs]` and `scripts/compare_configs.py a.json b.json`
- `scripts/compare_plants.py <base-tree> <head-tree>`
- `scripts/memo_probe.py <tree> on|off <out.json> [jobs]`
- `scripts/run_probes.sh <tree-copy> <out-dir> <probe...>` (uses `scripts/probe_gate.py`)
- `scripts/scan_unread_flags.py <tree>`

R585-4 FINISHED
