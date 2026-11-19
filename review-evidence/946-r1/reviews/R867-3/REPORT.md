[R867] POSITIVE - exact head fe297847a3221997182fcb6a903b4e93a8997ef3

R867-3 is an internal, independent delta review of kebag-logic/milan-fpga PR #947 (issues #946 and #665).

- **Head:** `fe297847a3221997182fcb6a903b4e93a8997ef3`, tree `07e0ee858aa81687175510c1a83ef5f69ea35191`.
- **Delta:** `9f4f3de0..fe297847`, two commits: `cbbd1ac0` (tests and plants) and `fe297847` (a comment and the README).
- **Files changed:** `test_plat_sinks.cpp`, `sink_mutants.py`, one `#:` comment in `sw/litex/ctrl_memory.py`, and `sw/firmware/ctrl/plat/README.md`, plus the PR body.
- **Not changed:** no firmware, RTL or core source. `ctrl_plat.c`, `ctrl_plat_csr.c`, `ctrl_plat_csr.h` and `aecp.c` have the same blobs at `9f4f3de0` and at the head. `git diff --name-only 9f4f3de0..HEAD -- hdl tb syn sw/firmware/ctrl/plat/*.[ch]` is empty, and every submodule gitlink equals the base `cb96336d`.

All five lenses were applied.

**Result:** R867-2 F-1 (MINOR, Tests) and F-2 (MINOR, Docs) are resolved at their cause. R867-2 RESIDUE-1 to RESIDUE-3 and R868-2-R1/R2 are fixed. The suggestion answers are reasonable. There is no new BLOCKER, MAJOR or MINOR. There is no new RESIDUE. One correction to my own round-2 analysis and one SUGGESTION are recorded below.

## Evidence base

Receipts marked "mine" were produced at this exact head in this clone, or in disposable copies of it. The others are the author's published receipts (archive `57588db2`, `review-evidence/946-r1/author-r3`).

- **Author packet integrity:**
  - 11 fetched files match the sha256 prefixes in its `receipts/INDEX.md` (`receipts/author-packet-integrity.txt`). Three files were not fetched: the composition's docs steps, its fw_coverage and its ledger.
  - The archive commit is unsigned on GitHub (reason `unsigned`), so signer authentication is not claimed. Only byte agreement with the packet's own index is claimed.
- **Mine: Sinks at the head, 11/11 at 8x8/1if and 11/11 at 1x1/1if** (`receipts/sinks-head.log`, rc 0).
  - S11 runs and passes at both shapes.
  - At 1x1, which has no context, it returns through `SINKS_CONTEXT_OR_RETURN`, as S2-S10 do.
- **Mine: the sink table through the control campaign's own planter and kill check:** 28 of 28 caught (`receipts/sink-table.log`, rc 0; script `scripts/sinkcampaign3.py table`). This includes:
  - `[ok] mutant sink-output-taken-for-its-input (platsinks8): 2 check(s) failed`;
  - `[ok] mutant sink-any-kind-of-an-input (platsinks8): 1 check(s) failed`;
  - `set-format-bound-accepted`.

  This is consistent with the README's "28 defects" and the PR body's "the 27 `sink-*` and `set-format-bound-accepted`".
- **Mine: my own round-2 plants, run again** (`receipts/rv-plants.log` via `scripts/sinkcampaign3.py rv`; `receipts/plant-*.log` via `scripts/sinkprobe.py`):
  - **Round 2's two escaping plants (the basis of F-1).** Round 2 spelled them `bool one = kind == AECP_CHANGE_FORMAT && (type == STREAM_INPUT || type == 6u);` and `bool one = type == STREAM_INPUT;`. Both compiled and passed 10/10 at `9f4f3de0`. Both are now in `sink_mutants.py:95-102` verbatim, and both are caught by S11 on its own words (table run above).
  - **The kind test dropped, in my campaign:** `[ok] mutant rv-one-kind-dropped (platsinks8)`, first `[FAIL] Sinks.S11...: S11 SET_NAME of input 7 writes no context`.
  - **The type test dropped, in its bare spelling** `bool one = kind == AECP_CHANGE_FORMAT;`: the campaign's kill check reports it ESCAPED with 0 checks failed. The cause is that it does not compile: `ctrl_plat.c:165:54: error: unused parameter 'type' [-Werror=unused-parameter]` (`receipts/plant-type-dropped-sinkprobe.log`, rc 2, refused). That is a build refusal, not a test escape.
  - **The same plant made to compile** (`(void)type;` added): S11 fails by name, `S11 output 7's SET_STREAM_FORMAT is taken while input 7 is bound` (`receipts/plant-type-dropped-used-sinkprobe.log`, rc 1, only S11 failing).
  - **Both tests dropped** (`bool one = true; (void)type;`): S11 fails by name on both of its halves (`receipts/plant-any-kind-any-type-sinkprobe.log`, rc 1).
  - **Round 2's other seven wrap plants:** the same outcomes as in round 2.
    - Caught by name: the immediate write removed, the bound check on the settled stream, and refusing every wait.
    - Caught, but outside the test its row named: the redo flag set outside a wait fails 8 checks, first in S4. My row expected S2, as it did in round 2.
    - Escaped, equivalent as reported in round 2: the redo flag never cleared, and the bound check on `published_bound`.
    - Not a test escape: `one = true` without `(void)type` is a build refusal (see N-1).

    None of these is affected by the delta.
- **Mine: S1's new AAF loop can fail.** I planted `EXPECT_EQ` -> `EXPECT_NE` at `test_plat_sinks.cpp:592` in the checkout, ran it, then restored it and checked its sha256 (`receipts/s1-inversion-probe.log`).
  - At 8x8, S1 fails for every input 1-7, two formats each (14 failures). The image advertises `FORMATS = [0x0205022000806000, 0x0215022002006000]` (`avdecc/aem_descriptors.py:133`), so the loop is not vacuous.
  - At 1x1, which has no context, it passes, as it should.
  - First attempt: a copied-tree substitution of the test had no effect. The arms compile tests from the checkout (`ctrl_build.test_source`; `plat_arms.py:146`). That run was discarded and the probe was redone in place.
- **Mine: idiom gates at the head.**
  - `scripts/check_cpp_idiom.py`: rc 0 (`receipts/cpp-idiom-head.log`).
  - `scripts/check_py_idiom.py`: rc 0, over-long line 0 (`receipts/py-idiom-head.log`).
  - The repository has no C++ column rule, so `test_plat_sinks.cpp:918` at 121 columns is not a finding.
- **Author: firmware gate at fe297847:** 81 arms, 745 of 745 control-campaign defects caught, 729 AECP and SRP campaign defects caught, ESCAPED 0, rc 0 (`gates/lane-fe297847-firmware-gate.txt`).
- **Author: fw_coverage at fe297847:** `firmware coverage: PASS (39 files)`, rc 0. platsinks is 11/11 at both shapes inside the coverage run (`gates/lane-fe297847-fw-coverage.txt`).
- **Author: ledger at fe297847:** `plat_ledger: PASS (0 finding(s))`, with every control as required. The four points are 43.5, 44, 56.5 (`platform-8x8-one-interface`) and 61 (`platform-8x8-two-interfaces`) RAMB36 (`ledger/lane-fe297847-ledger.txt`).
- **Author: `test_ctrl_memory.py` at fe297847:** `0 failure(s)`, `RESULT: PASS` (`memory/lane-fe297847-test_ctrl_memory.txt`, hash-matched).
  - My own run could not start: no interpreter in this session imports `migen` (`receipts/test_ctrl_memory-head-no-migen.log`). This is an environment limit, not a result.
  - The delta changes only a `#:` comment in `ctrl_memory.py`.
- **Author: docs workflow steps at fe297847:** 93 steps rc 0 (`docs/lane-fe297847-docs-workflow-steps.txt`). Steps 73, 74 and 79-81 call `scripts/docs_inventory.py`, `scripts/gen_register_reference.py` and `docs/diagrams/memory_map.gen.py`. I confirmed that none of these exists at this head or at `cb96336d`, so those steps are inapplicable on this base rather than failing.
- **(5) No firmware behaviour changed:**
  - **Product images:** at the four ledger points, the lane's `ctrl_app.elf` sha256 is EQUAL at `548324b5` and `fe297847`, and the composition's is EQUAL at `d98dd322` and `f8694fdd` (`ledger/product-images-unchanged.txt`).
  - **CPU-budget images:** the lane's are EQUAL to `cb96336d`'s, and the composition's are EQUAL to the train `b1f1161b`'s (`budget/image-hashes-arm-a.txt`).
  - **My independent check is diff-based.** `548324b5..fe297847` touches only tests, the README, one `#:` comment in `ctrl_memory.py` and one module docstring in `ctrl_memory_ledger.py`. No image input moved, and no core, face or app source changed since `cb96336d`. That agrees with the receipts. I did not rebuild the images.

## Prior findings, resolved or retained at this head

| Prior finding | At fe297847 | Status |
|---|---|---|
| R867-2 F-1 MINOR, Tests: the refusal gate's kind and type tests were never exercised at an index with a context, and both plants escaped | `test_plat_sinks.cpp:881-921` S11 binds input n (n = 7 at 8x8) and settles its probe, so its stream is published. STREAM_OUTPUT n's first SET_STREAM_FORMAT waits IN_PROGRESS and, once acknowledged, answers SUCCESS (`:903`) and writes no context (window empty). SET_NAME of input n (IEEE 1722.1-2021 7.4.17.1 layout, 72 bytes) answers SUCCESS and writes no context (`:918`). The binding stays settled, the watcher saw checks, and the run is coherent. Both of round 2's plants are in `sink_mutants.py:95-102`, each caught by S11 by name, in my run and in the author's. The bare type-dropped spelling does not compile; made to compile, it is caught by S11 by name. | **Resolved** |
| R867-2 F-2 MINOR, Docs: "Why it is race-free" stated a mechanism (no mailbox access between the change and the write) the code does not have | The PR body's bullet (line 63) checked against the code: <ul><li>The port forwards to the face first, whose publication makes its own mailbox accesses. This is `ctrl_plat.c:209`, `sinks.changed`.</li><li>Unless it is doing a waiting change again, it then reads the face's applied state. This is `:210`, `redo \|\| sinks.applied(ctx)`, which short-circuits on `redo`.</li><li>Only then does it write (`:211`).</li><li>All of it happens before the answer and before the event loop: `aecp_note` calls `ports->changed` synchronously (`aecp_commands.c:88-97`). On the waiting path, `applied(a)`, `swap` and `aecp_note` run in one call (`aecp.c:906-917`), so no ACMP input is processed between the bound check and the write.</li></ul> The bullet now matches the code exactly. | **Resolved** |
| R867-2 RESIDUE-1 / R868-2-R1: a lane name in the `ctrl_memory.py:254` comment | The comment now reads "named debt owed to the hybrid XIP work, the cold-code and descriptor flash migration (#665 decision D3)". D3 is the owner's decision on #665 (6409738976) moving cold code and the descriptor image to QSPI flash (`docs/design/SPLIT_CONTROL_MEMORY.md:266`). The line is within 120 columns, and the Python idiom gate passes. The `Ledgered` owner string at `:273` is data, as before. | **Resolved** |
| R867-2 RESIDUE-2: #950 not named | Known limitations: "it is #950, which also carries the clause's status for a refused change". #950 is open, and its Fix states "refuses with the clause's status". | **Resolved** |
| R867-2 RESIDUE-3: line 61 | Covered by F-2's rewording. | **Resolved** |
| R868-2-R2: "no mailbox access" phrasing, including the author's resolution narrative | The PR body is rewritten as above. The author-r3 REVIEW READY says explicitly that it supersedes round 2's handoff text. No `no mailbox access` phrase remains in the live PR body or in the r3 packet's prose. | **Resolved** |
| R867-2 S-1, the status of a refused waiting change | Not taken. It is carried by #950, whose Fix requires the clause's status. This is reasonable: it is a core change that moves every CPU-budget image, and this round changes no behaviour. | Reasonable |
| R867-2 S-2, the context decided on the current format's subtype | Taken as a test. S1 (`test_plat_sinks.cpp:578-594`) asserts that every format an input with a context advertises is AAF, and its inversion fails 14 times at 8x8 (see above). This is reasonable: the shapes share `FORMATS`, so a non-AAF entry would fail at 8x8. A builder rule is left out as a builder change. | Reasonable |
| R867-2 S-3, stale boot figures in `ctrl_split_boot/README.md:137` | Left to #746. The line predates the PR, and the file takes the train's side at composition. | Reasonable |
| R868-2-S1, the core's unchecked redo, face copy and channel map | Answered in Known limitations as #950's scope. Widening #950 is the manager's call. | Reasonable |

## Findings

No BLOCKER, MAJOR, MINOR or RESIDUE is open at this head.

### N-1: correction to my own round-2 analysis (no severity, for the record)

R867-2 listed the extra plant `rv-held-any-kind` (`bool one = true;`) as "escaped for real". At both heads that spelling leaves `type` unused, so `ctrl_plat.c` does not build under `-Werror`. Its "escape" was therefore a build refusal, not a missed defect.

F-1 itself still stands as raised. Its basis was the two compiling plants (round 2's `plant-one-type-dropped.log` and `plant-one-kind-dropped.log`, rc 0 with 10/10 passing at `9f4f3de0`). Made to compile now (`(void)type;`), the any-kind plant is caught by S11. Nothing is required of the author.

### S-1 SUGGESTION: Tests: `sw/firmware/ctrl/test/sink_mutants.py:99`, `test_plat_sinks.cpp:889`, `:898`: name the output type

- **Evidence:** The new plant and S11 spell STREAM_OUTPUT as the literal `6u`. The suite names `kStreamInput = 5u` with its Table 7-1 citation (`test_plat_sinks.cpp:91`). The pre-existing S5 (`:720`, `:726`) uses `6u` the same way.
- **Impact:** None on detection. Readers must map `6u` to IEEE 1722.1-2021 Table 7-1 themselves.
- **Optional outcome:** A `kStreamOutput = 6u` beside `kStreamInput`, used by S5 and S11 (and a named constant in the plant).
- **Verification:** Sinks stay 11/11 at both shapes, and the table stays 28/28.

## Lens coverage at this head

| Lens | Verdict | Artifact | What was checked, against what |
|---|---|---|---|
| Conformance | PASS | `test_plat_sinks.cpp:881-921`, `:93`, `:578-594`; `ctrl_plat.c:165-213` (blob `1aad850bf9fd`, unchanged) | <ul><li>S11's expectations match IEEE 1722.1-2021: 7.4.9 refuses SET_STREAM_FORMAT only for the bound or running stream itself, so STREAM_OUTPUT n, with no talker connection, answers SUCCESS; 7.4.17 SET_NAME has no bound refusal.</li><li>The 7.4.17.1 payload layout (descriptor_type, descriptor_index, name_index, configuration_index, name; 72 bytes).</li><li>The STREAM_INPUT layout of 7.2.6: current_format at 74, formats_offset at 82, number_of_formats at 84, avb_interface_index at 126.</li><li>The AAF subtype 0x02 (IEEE 1722-2016 Table 6).</li><li>The firmware is unchanged, so round 2's conformance result carries over.</li></ul> |
| RTL | PASS | `git diff --name-only 9f4f3de0..HEAD -- hdl tb syn sw/firmware/ctrl/plat/*.[ch]` (empty); gitlinks equal to `cb96336d` (`receipts/clone-restore-check.txt`); `ledger/product-images-unchanged.txt`; `budget/image-hashes-arm-a.txt` | <ul><li>No HDL, firmware or core source in the delta.</li><li>The product ELF is EQUAL at all four ledger points, for the lane and for the composition.</li><li>The CPU-budget images are EQUAL to the base's.</li><li>Round 2's RTL verdict depends on nothing the delta touched.</li></ul> |
| Robustness | PASS | S11 (`test_plat_sinks.cpp:881-921`); `receipts/plant-*.log`; `receipts/rv-plants.log` | <ul><li>A change of the wrong type, or the wrong kind, at the exact index that has a context, with that input bound and its stream published, including the deferred (IN_PROGRESS) path.</li><li>The gate's type and kind discrimination, each in isolation and together, is caught when compilable.</li><li>Every other wrap plant gives the same result as round 2.</li></ul> |
| Tests | PASS | `test_plat_sinks.cpp` S1 (`:578-594`) and S11 (`:881-921`); `sink_mutants.py:16-20`, `:38`, `:55`, `:95-102`; `receipts/sinks-head.log` (11/11 at both shapes); `receipts/sink-table.log` (28/28); `receipts/s1-inversion-probe.log`; `receipts/cpp-idiom-head.log`, `py-idiom-head.log` | <ul><li>Each new test can fail for the defect it names: S11 fails on both plants by name, and S1's loop fails when inverted.</li><li>Positive behaviour (SUCCESS) and negative behaviour (no window write) are covered.</li><li>The 1x1 shape is exercised.</li><li>The author's full firmware gate (745/745, ESCAPED 0) and fw_coverage (PASS, 39 files) are at this head.</li></ul> |
| Docs | PASS | `plat/README.md:131`; `ctrl_memory.py:254`; `sink_mutants.py` docstring (`:16-20`); `test_plat_sinks.cpp:49-51`, `:578-580`, `:907-908` comments; the live PR #947 body (`receipts/pr-947-body-live.md`, lines 52, 59-66, 114-135) | <ul><li>The README states S11, the S1 AAF check and 28 defects, consistent with the table.</li><li>The PR body's race argument matches `ctrl_plat.c:205-213`, `aecp.c:906-917` and `aecp_commands.c:88-97`.</li><li>#950 is named.</li><li>The new source comments carry no lane label, review round, reviewer ID or comment ID, and they cite clause and issue IDs.</li><li>The `#665 decision D3` reference is checked against `SPLIT_CONTROL_MEMORY.md:266`.</li></ul> |

## Completion ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | S11 and the S1 loop against IEEE 1722.1-2021 7.2.6, 7.4.9, 7.4.17.1 and IEEE 1722-2016 Table 6; `ctrl_plat.c:165-213` unchanged | R867-3 | `fe297847a3221997182fcb6a903b4e93a8997ef3` |
| RTL | CLEAN | Empty HDL and firmware delta; gitlinks; product and budget image hash receipts | R867-3 | `fe297847a3221997182fcb6a903b4e93a8997ef3` |
| Robustness | CLEAN | S11's wrong-type and wrong-kind paths at a bound context index; my plants | R867-3 | `fe297847a3221997182fcb6a903b4e93a8997ef3` |
| Tests | CLEAN | Sinks 11/11 at both shapes; table 28/28; my plants caught by name; S1 inversion; idiom gates; the author's firmware gate and fw_coverage | R867-3 | `fe297847a3221997182fcb6a903b4e93a8997ef3` |
| Docs | CLEAN | README, ledger comment, mutant docstring, test comments, live PR body | R867-3 | `fe297847a3221997182fcb6a903b4e93a8997ef3` |

## Real limits

- **No manager source bank at this head:** none was run, and none is claimed or inferred. Source-head execution evidence is my focused runs above plus the author's published receipts.
- **Not re-run by me:** the full firmware gate, fw_coverage, `plat_ledger.py`, the docs workflow, the image builds and the CPU-budget harness. For these I relied on the author's hash-matched receipts and on the diff-based argument.
- **`test_ctrl_memory.py`:** I could not run it here, because no interpreter imports `migen`. I used the author's receipt.
- **Author packet:** the archive commit is unsigned, so only byte agreement with its own index is verified.
- **Hosted evidence:** I did not inspect hosted runs, and I make no hosted or act claim.
- **Hardware:** physical calibration was NOT RUN. Field skips are not hardware proof.
- **Probe cleanup:** all probes ran in copies under the packet's scratch directory, or as one in-place test edit that I restored. After the probes:
  - HEAD and tree are exact;
  - porcelain is empty;
  - index equals HEAD, and worktree equals index;
  - every tracked blob, mode and path matches the HEAD tree;
  - every submodule gitlink is unchanged (`receipts/clone-restore-check.txt`).

## Pending manager duties

- **Merge candidate:** validate the current-dev candidate (source base `cb96336d`, live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`; the PR's base ref is `dev-soft-core`) with the builder and native banks, and link the receipts on the PR.
- **Composition ROM entries:** the author's composition takes the train's side in seven conflicting files (`merge/composition.txt`). Preserve the composed ROM entries.
- **Hosted acceptance:** own the hosted and act acceptance on the exact head.
- **Residue checklist:** nothing new from this round. Close R867-2 RESIDUE-1 to RESIDUE-3 and R868-2-R1/R2 as fixed.
- **Issue #950:** consider widening it per R868-2-S1.
- **Hardware acceptance:** the frozen 8x8/1if stream, power-cycle and soak acceptance remain before #946 is done. The remaining requirements are still separate: two positive independent reviews, no review in flight, explicit merge authorization, containment and closure.

R867-3 FINISHED
