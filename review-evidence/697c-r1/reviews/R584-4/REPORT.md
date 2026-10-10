[R584] NEGATIVE - exact head e07b305458ed3520e4adfc55e9746144ce5cdc79

# R584-4: internal independent review of PR #705 (issue #697, lane 697c), round 4

**Head.** `e07b305458ed3520e4adfc55e9746144ce5cdc79`, tree `ec8f8fb21ee972f83bf14a535e07f3633bc9a35e`. The PR head is the same commit. In the review clone the index equals the head tree, and `git write-tree` gives that tree. The `tsn-c-stack` (`1a9f651c`) and `lwSRP` (`9197193e`) gitlinks match their checkouts, and every submodule is clean (`receipts/clone_restore_check.txt`, `receipts/submodule_clean.txt`).

**Delta reviewed.** `d1b22e804..e07b30545` has four commits (`6d43e1978`, `d25ae924a`, `9453fcc10`, `e07b30545`) and five files (`receipts/delta_d1b22e80_e07b3054.diff`):
- `sw/firmware/ctrl/test/ctrl_boundary.py` and `ctrl_configs.py`;
- `ctrl_plants.py`, which is new;
- `sw/firmware/ctrl/README.md`;
- `docs/testing/CI_WORKFLOWS.md`.

The delta touches none of these:
- a firmware or stack source, header or test;
- a gitlink, a workflow, a Makefile or a build flag;
- a coverage row, a mutation table, or any `hdl/` file.

**Authorities read, in this order:**
- AGENTS.md and CONTRIBUTING.md;
- docs/README.md;
- issue #697 acceptance 1 to 5, the owner decisions, and the lane assignment 6091228902;
- the round-4 assignment 6096148471: item 1 is R585-3-F1; item 2 is R584-3-F1 together with R585-3-S2; item 3 is R585-3-S1;
- the author's REVIEW READY (round 4), 6097154937;
- the diff and its four commits;
- the exact-head hosted runs.

The published evidence `review-evidence/697c-r1` at `ec6854f6` holds only round 1's pin proof and author notes, so it does not bear on this delta. I read the prior public findings (R584-3 and R585-3) only after my own pass over the diff and my probes.

**Verdict.** NEGATIVE. Two MINOR findings are open, R584-4-F1 and R584-4-F2.
- Round-4 item 1 (R585-3-F1) is met.
- Item 2's own plant (R584-3-F1) is caught.
- Item 3's listed forms are refused.
- Some forms that items 2 and 3 cover, and that the new README sentences name as refused, still pass the gate silently.

## 1. Findings

### R584-4-F1 - MINOR - Conformance, Robustness, Tests, Docs - a C++ source that a builder computes, or writes from computed or copied text, passes the gate silently

`[R584] MINOR Conformance/Robustness/Tests/Docs - sw/firmware/ctrl/test/ctrl_configs.py:542-548,586-616; ctrl_boundary.py:672-689; sw/firmware/ctrl/README.md:95-96 - computed C++ names and written-source includes are skipped silently`

**Authority**
- Round-4 item 2: "Any C++ name that resolves to no file fails the gate by name. It must not be skipped silently."
- The head states the rule at `sw/firmware/ctrl/README.md:96`: "A C++ name that resolves to no file, or that the builder computes, fails the gate by name."
- `README.md:95` adds: "A C++ source the builder writes itself is followed through the builder's own literals."
- The same rule is in the `ctrl_configs.py` module docstring (THE C++ SOURCES) and at `ctrl_boundary.py:49-53`.

**Evidence** (`scripts/boundary_probes4.py`, run in a disposable copy of the head; `receipts/probes4/verdicts.txt` and one log per probe)

Every probe plants the same new firmware header, `adp/adp_r584.h`. It holds `#ifdef __cplusplus` / `#include "adp_port.h"`, which is the stack's `examples/` header. A C++ source reaches the header in a different way in each probe.

| Probe | How the builder gives the C++ source | Gate result |
|---|---|---|
| B0 (control) | a Makefile names `probe_r584/bench.cpp` literally | CAUGHT: `firmware c++: adp/adp_r584.h includes tsn-c-stack/examples/adp_port.h` |
| C0 (control) | a Python builder writes `planted_r584.cpp` from a literal `#include "adp_r584.h"` | CAUGHT, same finding |
| B1 | a Makefile builder: `SRCS := $(wildcard probe_r584/*.cpp)` | ESCAPED: rc 0, `ctrl_boundary: PASS` |
| C1 | the written source's include comes from an f-string, `f"#include \"{HDR}\"\n"` | ESCAPED |
| C2 | the written source comes from `TEMPLATE.format(...)`, with `TEMPLATE = '#include "{}"\n'` | ESCAPED |
| C3 | the written source is `shutil.copy(<template file>, "planted_r584.cpp")` | ESCAPED |
| B2 | a Python builder: `glob("probe_r584/*.cpp")` | CAUGHT: refused by name as an unresolved name |
| B3 | a Python builder: `[p for p in dir.iterdir() if p.suffix == ".cpp"]` | ESCAPED. No name is written, so this does not contradict the documented rule, which covers sources a builder *names*. It is listed for completeness only. |

The causes in the code:
- `makefile_names` (`ctrl_configs.py:542-548`) counts a Makefile word as a computed C++ name only when the word itself ends in `.cpp`, `.cc` or `.cxx`. The `$(wildcard ...)` word ends in `)`, so the name is neither followed nor refused.
- For a written source, `named_sources` (`:609`) hands the builder's literals to `cxx_units` (`ctrl_boundary.py:672`). An include operand that the builder computes gives `#include "` or `#include "{}"`. Its name resolves to nothing, and `cxx_units` (`:685-689`) drops it without a finding.
  - This happens even though the same gate refuses a macro-computed operand by name (`:681-684`).
- For a copy, the text compiled is the copied file. `write_target` (`ctrl_configs.py:489-490`) still treats the copy as a write and follows only the builder's literals.

At `d1b22e80`, B1 and C1 also escape, and so do the controls A1 and C0 (`receipts/probes4_at_d1b22e80.log`). So the delta fixes the named and literal cases, but the computed and copied cases it now documents as refused are not.

**Impact**
- A firmware header that only such a C++ source reaches is judged as C only. A C++-only include in it of the stack's `src/`, `tests/` or `examples/` passes the boundary.
- `$(wildcard *.cpp)` is the ordinary Makefile idiom.
- No current builder uses these forms:
  - the configuration set is unchanged (section 2);
  - the only written source today is `aecp_wire.py`'s `reference.cpp`, whose real includes come from `sim_main.cpp`, which is resolved.
- So no current include escapes. But the README's stated rule is false for these forms, and item 2's "never skipped silently" does not hold for them.

**Required outcome**
- Each of B1, C1, C2 and C3 is refused by name, or followed to the text actually compiled. That covers:
  - a Makefile word that computes a C++ name inside a make function or variable;
  - an `#include` in a builder-written source whose operand the gate cannot resolve from the literals;
  - a written source whose text the builder copies or reads from elsewhere.
- Planted controls of these shapes are in `--selftest`.
- `README.md:95-96` and the docstrings state exactly what is followed and what is refused. The design is the author's choice.

**Verification**
- `python3 -I scripts/boundary_probes4.py <disposable copy> <out> B1-makefile-wildcard-cpp C1-written-fstring-include C2-written-format-include C3-written-copied-template` reports CAUGHT, or a by-name refusal, for each.
- B0 and C0 stay CAUGHT, and the checkout's configuration set is unchanged (`scripts/compare_configs.py`).

### R584-4-F2 - MINOR - Conformance, Robustness, Tests, Docs - a `-D` flag that make computes inside a function word is neither derived nor refused

`[R584] MINOR Conformance/Robustness/Tests/Docs - sw/firmware/ctrl/test/ctrl_configs.py:239-253; sw/firmware/ctrl/README.md:101-102 - $(patsubst %,-D%,...) and $(foreach m,...,-D$(m)) pass silently`

**Authority**
- Round-4 item 3: "R585-3-S1 (a flag that is neither a literal nor an f-string) is required now: it is refused by name."
- `README.md:101-102` at the head: "Any other `-D` or `-U` a builder writes that is neither a literal nor an f-string refuses the gate by name." Its examples include `$(addprefix -D,...)`.
- The PR body's round-4 table says the same ("R585-3-S1 ... Refused by name").

**Evidence** (`receipts/probes4/verdicts.txt`)

Each probe plants a firmware-side defect: `adp/adp_mbx.c` gains `#ifdef CTRL_R584_PAT` / `#include "adp_port.h"`. A new Makefile or Python builder of `sw/firmware/ctrl` then writes the mode in a different form.

| Probe | Form | Gate result |
|---|---|---|
| D0 (control) | Makefile `cc -DCTRL_R584_PAT` | CAUGHT: `firmware [-DCTRL_R584_PAT]: adp/adp_mbx.c includes tsn-c-stack/examples/adp_port.h` |
| D1 | Makefile `$(patsubst %,-D%,CTRL_R584_PAT)` | ESCAPED: rc 0, PASS |
| D2 | Makefile `$(foreach m,CTRL_R584_PAT,-D$(m))` | ESCAPED |
| D4 | Python `["-D", NAME if X else ...]` | REFUSED by name |
| D5 | Python `"-D{}".format(...)` | REFUSED by name |
| D6 | Makefile `-D $(M)` | REFUSED by name |

`makefile_flags` (`ctrl_configs.py:245-253`) only looks at a word that *starts* with `-D` or `-U`. Inside `$(patsubst ...)` and `$(foreach ...)`, the `-D` sits mid-word (`%,-D%,...` and `...,-D$(m))`), so it is skipped. These are the same class as `$(addprefix -D,...)`, which the delta does refuse. Both forms also escape at `d1b22e80` (D1 in `receipts/probes4_at_d1b22e80.log`).

**Impact**
- A mode written this way is never explored, so an include that only that mode reaches passes the boundary.
- The configuration set is unchanged at the head, because no builder uses these forms today. But item 3's requirement and the README's general sentence are false for them.

**Required outcome**
- A `-D` or `-U` that make computes anywhere in a word is refused by name. Alternatively, the Makefile's flags are read from make's own expansion, as `ctrl_pin.py` already reads recipes.
- D1 and D2 become controls.
- `README.md:101-102` and the PR body's round-4 row match what the gate does.

**Verification**
- `boundary_probes4.py ... D1-makefile-patsubst D2-makefile-foreach` reports CAUGHT, or a by-name refusal.
- D0 stays CAUGHT, and the 18 derived modes are unchanged.

### R584-4-RS1 - RESIDUE - Docs (PR body only) - round-4 status lines are stale and two counts are off

These are PR-body sentences only. Fixing them changes no code, test, generated artifact or measurement. My receipts confirm the corrected figures.
- **Line 20.** Replace "Round 4 is not pushed, so no hosted run covers it yet." with "At `e07b3054`, hosted `firmware-unit` passed (job 114206016568): the boundary step took 1 min 33 s, and the store suites and coverage ratchet ran."
- **Line 214.** Replace "it is not yet measured on a hosted runner." with "on a hosted runner at `e07b3054` it took 93 s (job 114206016568)."
- **Line 136.** "twelve controls are new in this round" becomes "fourteen controls are new in this round (59 plants against 45 at `d1b22e80`, beside the shared base)".
  - Evidence: `receipts/controls_kept.txt` lists the 14 new names. All 45 earlier controls are kept with an unchanged plant, needle and builder.
- **Line 130.** "0 of 58 differ" becomes "0 of 60 differ", to match line 214 and `receipts/memo_compare.txt`.

### R584-4-S1 - SUGGESTION - Docs - add the exact-head hosted figure to the budget paragraph

`docs/testing/CI_WORKFLOWS.md:67-74` gives local figures: "74 to 82 s", and "The worst leaves 218 s of the 300 s budget, a 73% margin". It says they stand in until a hosted run. The hosted step at this head took 93 s (job 114206016568, `receipts/hosted_firmware_unit_steps.tsv`). That leaves 207 s, a 69% margin, which is slower than the local runs. The text is true as worded, so this is optional. Consider stating the hosted figure.

### R584-4-S2 - SUGGESTION - Robustness - the `firmware-unit` job's own margin is thin, and nothing enforces the 5-minute step budget

- At this head the job took 41:29 of its 45 minutes, a 7.8% margin.
- Step 8 (the firmware suites, whose code is unchanged) took 33:19. The same step took 19:04 to 32:12 at earlier heads and 24:17 to 26:45 on dev (`receipts/hosted_firmware_unit_history.txt`).
- This delta's step 9 is 1:33 of that total, so the thin margin is runner variance in step 8 and predates this delta.
- The 5-minute step budget is documented but not enforced: no step-level `timeout-minutes` is set.
- Consider a separate Issue for the job budget. A step-level limit would turn a cost regression into a named failure.

## 2. Round-4 items, checked independently at this head

| Item | Result | Receipt |
|---|---|---|
| Item 1: the same configurations are judged; no configuration dropped or sampled | **Met.** I recorded every configuration the checkout judgement explores at `d1b22e80` and at `e07b3054`: 942 configurations at each, over 148 unit-and-side pairs. The argument vectors, units and flags are identical, and so are each configuration's label, files read, deciding macros and `#error` state (0 only-old, 0 only-new, 0 differing). The derived modes (18), shapes (5), image stream counts, contracts (2) and computed values print identically | `scripts/record_configs.py`, `scripts/compare_configs.py`, `receipts/compare_configs.txt`, `receipts/configs_*.json`, `receipts/record_*.log` |
| Item 1: every control kept | **Met.** All 45 controls of `d1b22e80` are present, with the same plant, needle and builder. 14 are new. 59 plants plus the shared base make 60 | `receipts/controls_kept.txt` |
| Item 1: the speed comes only from reuse, a shared base, early stop and parallelism | **Met.** The checkout judgement reuses nothing: 943 preprocessings = 942 configurations + 1 GoogleTest probe. Control keys are distinct from the checkout's (different paths), so the checkout verdict never depends on reuse. For the controls, I judged all 60 in full with early stop disabled, with reuse (7,700 run, 36,412 reused) and without it (44,112 run). The complete finding lists are identical for 60 of 60 (164 findings) | `scripts/memo_soundness.py`, `receipts/memo_compare.txt`, `receipts/memo_on.json`, `receipts/memo_off.json` |
| Item 1: hosted `firmware-unit` green at this head, steps 10 and 11 run, the boundary well inside the limit | **Met (executed, not skipped).** In run 38049616643 (`pull_request`), job 114206016568 succeeded: step 9 took 12:21:17 to 12:22:50 (1:33), step 10 took 1:42 and step 11 took 4:18. Step 9's log ends `942 configurations, 943 preprocessed ... 0 finding(s), 60 boundary and 20 pin controls, 0 misbehaved` and `ctrl_boundary: PASS`. The `rtl-fast` aggregate succeeded. Job margin: see S2 | `receipts/hosted_firmware_unit_steps.tsv`, `receipts/hosted_firmware_unit_step9.log`, `receipts/hosted_runs_e07b3054.tsv` |
| Item 1: the CI command run locally | **PASS, rc 0, in 3:38** with `taskset -c 0-3` on a shared host at load 25 to 39. Same summary line; `boundary controls: 3460 preprocessings run, 35693 reused`. The run and reuse counts vary between runs because the early-stop timing varies. Verdicts do not | `receipts/selftest_head.log`, `.rc`, `.uptime` |
| Item 2: R584-3's `maap_r584.h` plant through `test_maap_differential.cpp` | **CAUGHT at the head, ESCAPED at `d1b22e80`.** The finding reads `firmware c++: maap/maap_r584.h includes tsn-c-stack/tests/acmp_fake.hpp, not one of the stack's public headers`. Also CAUGHT: the angle-bracket form (A2) and a header two levels deep (A3) | `receipts/probes4/A1..A3*.log`, `receipts/probes4_at_d1b22e80.log` |
| Item 2: an unresolved or computed name fails by name | **Partly.** A literal that resolves nowhere (`glob("probe_r584/*.cpp")`) and a `+`-computed name are refused. A Makefile `$(wildcard ...)` name and computed or copied written-source text are not: **R584-4-F1** | `receipts/probes4/verdicts.txt` |
| Item 3: a flag that is neither a literal nor an f-string is refused by name | **Partly.** The PR's listed forms are refused. So are my D4 (bare `-D` then a conditional expression), D5 (`"-D{}".format`) and D6 (`-D $(M)`). `$(patsubst ...)` and `$(foreach ...)` are not: **R584-4-F2** | `receipts/probes4/verdicts.txt` |
| Images, coverage and kills | Unchanged by construction. The delta holds no firmware, stack, build-flag, coverage, mutation or Makefile file. Nothing outside the gate's own modules imports `ctrl_configs`, `ctrl_boundary` or `ctrl_plants` (a repository search found only the gate). The gitlinks are unchanged | delta diff, `receipts/clone_restore_check.txt` |
| Python idiom ratchet and the 1000-line module limit | `check_py_idiom.py` rc 0, with no ratchet raised. `ctrl_boundary.py` is 906 lines, `ctrl_configs.py` 616 and `ctrl_plants.py` 268 | `receipts/idiom_docstyle.log` |
| Docs gates | `check_doc_style.py`: OK. Em or en dashes in the delta's added lines: 0. The hosted `docs` run 38049616656 succeeded at this head (docs-check, docs-check-no-git, wire-accountability) | `receipts/idiom_docstyle.log`, `receipts/hosted_runs_e07b3054.tsv` |

## 3. Prior public findings at this head

| Finding | Status at `e07b3054` | Evidence |
|---|---|---|
| R585-3-F1 (MAJOR, hosted `firmware-unit` timed out inside the boundary step) | **Resolved.** The exact-head job is green, step 9 took 1:33 (inside its 5-minute budget), and steps 10 and 11 executed. The same configurations and every control are kept (section 2). The job-level margin is S2, which is not caused by this delta | section 2 rows 1-4 |
| R584-3-F1 (MINOR, `test_maap_differential.cpp` not followed) | **Resolved.** The named plant and two variants are CAUGHT. The broader computed-name class it led to is the new R584-4-F1 | `receipts/probes4/A*.log` |
| R585-3-S2 (same source not followed) | **Resolved** with R584-3-F1 | as above |
| R585-3-S1 (flag forms), required in round 4 | **Resolved for the listed forms. Retained** for the make-function forms as R584-4-F2 | `receipts/probes4/D*.log` |
| R585-3-RS1 (PR body statuses) | **Applied for `d1b22e80`. Stale again at this head**: R584-4-RS1 | PR body |
| R584-3-S1 (multi-word literal flags; `FORCED` constant; ignored-error pin recipe) | **Retained as SUGGESTION**, not addressed. My D3 (`"cc -DCTRL_R584_PAT -c x.c"`) and D7 (`shlex.split("-O2 -DCTRL_R584_PAT")`) still ESCAPE. The checkout holds that shape at `aecp_wire.py:116` (`-CFLAGS "-DPP_TOP_IF2"`). It is derived only because `:136` also writes `"-DPP_TOP_IF2"` as a literal | `receipts/probes4/D3*.log`, `D7*.log` |
| R585-2-S2 (`--stack` pins the clone while the AECP tests take the submodule's `tests/`) | **Retained as SUGGESTION**, not addressed (`aecp_arms.py` is untouched by the delta) | delta diff |
| Earlier rounds (R584-1/2, R585-1/2 findings) | Stand. The delta does not touch their artifacts, and every one of their controls is kept and passes (section 2) | `receipts/controls_kept.txt`, `receipts/selftest_head.log` |

## 4. Lens results

```text
[R584] MINOR Conformance - R584-4-F1, R584-4-F2 (above)
[R584] PASS RTL - delta_d1b22e80_e07b3054.diff (no hdl/, CDC, FSM or interface file); ctrl_boundary.py:433-498,732-771 - checked the gate's concurrency (explorers wait on the compiler pool, whose tasks never wait, so it cannot deadlock; Stopped and Refusal paths join every started task), judge()'s positional signature kept, cxx_sources' callers (only the gate's own modules)
[R584] MINOR Robustness - R584-4-F1, R584-4-F2 (above)
[R584] MINOR Tests - R584-4-F1, R584-4-F2 (above); the self-test has no control for the forms the README names as refused
[R584] MINOR Docs - R584-4-F1, R584-4-F2 (README.md:95-96,101-102 state refusals that do not happen); R584-4-RS1 is RESIDUE and S1 is a SUGGESTION, neither of which affects coverage
```

The Conformance, Robustness, Tests and Docs lenses were each applied in full at this head. Their clean parts are in section 2:
- the configuration set and control set are identical to `d1b22e80`;
- reuse is sound;
- the hosted step is green;
- the R584-3 plant is caught;
- the documented counts (56 plants, 3 passing controls, 60 in all) are correct.

## 5. Completion ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | round-4 items 1-3 against `ctrl_configs.py`, `ctrl_boundary.py`, `ctrl_plants.py`; configuration-set comparison; hosted job 114206016568; probes A1-D7 | R584-4 | e07b305458ed3520e4adfc55e9746144ce5cdc79 |
| RTL | CLEAN | delta (no HDL); `ctrl_boundary.py:433-498,732-771` concurrency and interfaces | R584-4 | e07b305458ed3520e4adfc55e9746144ce5cdc79 |
| Robustness | UNCLEAN (F1, F2) | probes B0-D7; reuse soundness (60/60 controls with and without reuse); early-stop paths | R584-4 | e07b305458ed3520e4adfc55e9746144ce5cdc79 |
| Tests | UNCLEAN (F1, F2) | `--selftest` locally and hosted (60 + 20 controls, 0 misbehaved); `controls_kept.txt`; missing controls for the F1/F2 forms | R584-4 | e07b305458ed3520e4adfc55e9746144ce5cdc79 |
| Docs | UNCLEAN (F1, F2) | `sw/firmware/ctrl/README.md:91-118`; `docs/testing/CI_WORKFLOWS.md:60-74`; module docstrings; PR body (RS1) | R584-4 | e07b305458ed3520e4adfc55e9746144ce5cdc79 |

## 6. Real limits

- No source bank was run by me or the manager at this head. Source-head execution evidence is the author's published gate receipts plus my focused runs: the boundary gate with and without its self-test, the probes, the reuse comparison, the idiom and doc-style checks.
- I did not rebuild the RV32 images or re-run coverage or mutation campaigns. They are unchanged by construction (section 2).
- My local timing (3:38) was taken on a host at load 25 to 39 and is not a budget figure. The hosted 1:33 is the budget figure.
- At review time `rtl-full` run 38049616634 was still in progress: Verilator shards 1/5 and 2/5 were running, and the other shards had succeeded. `Physical gPTP` was **skipped** (nightly and manual only). A skip is not hardware proof, and physical calibration was NOT RUN.
- No act or Docker replica was run, as instructed.
- The probes exercise the gate's text and AST reading. They do not prove the absence of other unread forms beyond those named.

## 7. Pending manager duties

- Hosted and act acceptance at the exact head, including the final `rtl-full` verdict (two Verilator shards were still running at review time).
- Decide R584-4-F1 and R584-4-F2: fix, or a public scope ruling.
- Carry R584-4-RS1 to the residue checklist.
- Validate the current-dev merge candidate (source base `8b61b709`, live dev `e8454e27`), with builder and native banks, at the merge turn, and link those receipts.
- Image byte-identity, coverage and kills for the merge candidate are the manager's merge-turn validation.

R584-4 FINISHED
