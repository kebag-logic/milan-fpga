[R412] NEGATIVE - exact head 5b4a47e99f5a453832ccabccfbf4aae116d6fea0

Round R412-4. This is a cleared-context internal review of PR #623 (#70 lane 2).

- Exact head: `5b4a47e99f5a453832ccabccfbf4aae116d6fea0`, tree `4da3a4345786338298d728d06b82fe9d35bc2e2a`.
- Source base: `79c36963660c10e4c1c11a744fb5bff41a552b8b`.
- This round adds two commits to my round-3 head `0a80abcb`: `fa1d6e03` (the verdict's claims bounded, two limits named) and `5b4a47e9` (a planted break that reaches only an interior byte).
- Processor pin `b2db3a97` is unchanged. No firmware, RTL or bitstream changed.

One finding is open: **F1, MINOR** (Conformance, Robustness, Tests, Docs).

- The round-4 texts now bound what the pins prove, and that bounded claim is correct.
- But they then say the two named limits are the only way to reach the verdict without a relocation. They also say that outside those two, the word `milan_init()` stored is the word read back after `nvm_boot()`.
- That is still more than the census proves. Inside `nvm_boot()`, a called function can be handed a pointer whose value comes from a run-time source, such as a CSR read. That pointer is neither a literal address nor another object's relocated address. The whole gate function accepts such a firmware with the slot kept. In the same run it prints that "two writes" are outside the pins.

Round-3 F2 is **resolved**. Round-3 F1 is **resolved as ruled**: the ruled limit is stated, and both of its probes match its words. The overclaim that remains is a separate class, reported as F1 of this round.

## Sources reconstructed, in order

1. `AGENTS.md` (sections 3, 6 and 7) and `CONTRIBUTING.md`. `docs/README.md` was used as the documentation map.
2. Issue #70:
   - the round-4 assignment 5909983141, which rules round-3 F1 accepted as a second stated limit and requires round-3 F2 closed by a control;
   - the #495 residue record 5909985902;
   - the review-start comment 5910873723 on PR #623.
3. The interface authority, `docs/integration/BAREMETAL_FIRMWARE.md`:
   - "What the census does NOT observe" (`:808-830`);
   - the verdict-pin section (`:919-1033`);
   - the refusal row (`:1638`).
4. `git diff 0a80abcb..5b4a47e9` (`CHANGELOG.md`, `BAREMETAL_FIRMWARE.md`, `sw/builder/test_builder.py`), the history `79c36963..5b4a47e9` (28 commits), and the PR #623 body at the head.
5. Public evidence at `3f26cbbabb75900e83ce947c90a0e658d0cffee0`, `review-evidence/70L2-r1/author-r4`: the listing, `gates-5b4a47e9-builder.json` and `gates-5b4a47e9-rest.json`, all rc 0 at this head and tree, `clean_after` true. I also listed the hosted check runs at the head (`hosted_checks.txt`).
6. Only after my own pass over the diff was complete: my own round-3 report (R412-3, 5909975429), for its findings' required outcomes and published probe shapes. I read the other reviewer's round-3 report (R413-3, 5909532354) only after this verdict and the ledger were written, for the disposition table alone. I read no report of this round by anyone else.

## Method

The clone was never modified. `receipts/clone_integrity_mid.log` and `receipts/clone_integrity_end.log` record the check: HEAD and tree exact, an empty porcelain status including untracked files, the index equal to HEAD for all 976 entries (mode and object id), every tracked file's bytes and exec bit equal to its blob, and each initialized submodule clean at its gitlink. `external` is uninitialized, as it was at the start of the round.

All probes ran on disposable copies under the packet's `scratch/`, at most 8 jobs at once. The compiler is the pinned SDK, `$HOME/br-milan-rv32/host/bin/riscv32-linux-gcc` (Buildroot 2026.05, 14.3.0). Gate 1b adopts it with driver `()`, as every log shows. The scoped Verilator was not needed and was not used.

The scripts are in `scripts/`:

- `patch_probe_hook.py` (probe mode) inserts a hook into a copy of `test_builder.py`. The hook runs right after gate 1b has accepted the AEM-first base with the slot kept and refused it under forget-on-call. It grades each probe through the same `census_take()` and `assert_resolved_boot_flow(source=...)` call that the planted breaks use. It prints the outcome, the image layout of the objects involved, and every relocation that the `-no-pie` image places on `aem_loaded`'s bytes, with offset, function and kind.
- `make_probes.py` builds the 18 probes of this round. `make_probes_r3shapes.py` builds round 3's probe shapes exactly as the round-3 report published them.
- `census_mutants.py` holds nine census mutants of my own (K0 to K8), two mutants of the new break (B1, B2) and a null mutant (N0). It also adds a stop marker just after gate 1b prints its closing verdict line.
- `run_mutants.py` runs each mutant through `test_baremetal_profile_contract()` in a shared clone with its submodules, via `run_gate.sh` with `--require-rv32`.
- `whole_gate_plant.py` plants a probe into the shipping firmware file itself and runs the whole gate function uninstrumented. The shipping firmware is already AEM-first, so gate 1b's `aem_first()` is the identity on it.
- `clone_integrity.py` is the end-of-round check described above.

## Judgment of the round-4 items

### Item 1 (`fa1d6e03`; round-3 F1): the claims bounded and two limits named

**The bounded claim is correct.**

- The texts now say that, of the writes that reach the verdict through a relocation on its bytes, `milan_init()`'s one store is the only one: `test_builder.py:1647-1650`, `BAREMETAL_FIRMWARE.md:968-970` and the PR body's round-4 item 1.
- "Nothing writes the verdict but that one store" is gone from every text. A search of the tree finds no other instance.
- The escape bullet now reads "no relocation on those bytes forms their full address" (`BAREMETAL_FIRMWARE.md:934-941`, `test_builder.py:1638-1642`, and the docstring at `:6912-6915`).
- The refusal row (`:1638`) says "no relocation on its storage forming its full address".
- The `verdict_image_pins()` docstring (`:6922-6933`) is accurate as written. Its lead clause is general ("a write through an address with none on those bytes passes"), and the two bullets are examples.

**The second limit matches its probes.** All of these were rerun at this head (`probes/probe_run.log`, `probes/probe_run_r3shapes.log`):

| Probe inside `nvm_boot()` | Outcome | Layout, and the image's relocations on the verdict from `nvm_boot()` |
|---|---|---|
| round-3 `pre_overrun_sscanf` (`static char r412_line[4]` before the verdict, `sscanf("abcd\001", "%s", r412_line)`) | ACCEPTED, slot kept | `r412_line` `0x158c8`, verdict `0x158cc`; none |
| round-3 `nbr_runtime_sscanf` (`&r412_pad + k`, `volatile int k = -1`) | ACCEPTED, slot kept | verdict `0x158e0`, `r412_pad` `0x158e4`; none |
| this round's `pre_overrun_sscanf` and `nbr_runtime_sscanf` (the same shapes, with `k` read from a CSR) | ACCEPTED, slot kept | same adjacency; none |
| round-3 `nbr_byte_sscanf` (`(char *)&r412_pad - 3`) | REFUSED, escape | +1 (`HI20`, `LO12_I` on an addi) |
| `nbr_fold_byte0` to `nbr_fold_byte3` (`(char *)(&milan_nbr - 1) + j`), and `pre_fold_byte2` | REFUSED, escape | +0, +1, +2, +3 and +2 respectively |
| `own_store_fold` (`(&milan_nbr)[-1] = 1`) | REFUSED, store and escape | +0 |
| `own_store_localptr` (`int *p = &milan_nbr; p[-1] = 1`) and `own_store_pre_array_local` (`char *p = milan_pre; p[4] = 1`) | ACCEPTED, slot kept | none |
| `own_store_runtime` (`(&milan_nbr)[-(milan_read(MILAN_ID) & 1)] = 1`) and `own_store_bounded_loop` | REFUSED, rule 1b ("a STORE this gate cannot PLACE") | none |

Every row matches the second limit's words at `BAREMETAL_FIRMWARE.md:983-1000` and `test_builder.py:1662-1676`:

- a called function writing through a neighbour's pointer carried past its end or before its start is accepted;
- so is the unit's own store through a local pointer to the neighbour, indexed outside it;
- a folded offset lands on the verdict's bytes and is refused by address;
- a run-time offset in the unit's own store is refused by rule 1b.

The literal-address limit is stated as ruled in round 3: `literal_sscanf` is accepted, slot kept.

**What still claims more.** See F1 below. Four texts go beyond the bounded claim:

- "two addresses reach the verdict's bytes with no relocation on them";
- "Outside the two limits below, the word that store wrote is the word read back after `nvm_boot()`";
- the refusal row's "Two writes put no relocation on its storage and are outside these pins";
- the gate's own closing line, "two writes put no relocation on its storage and are outside these pins".

### Item 2 (`5b4a47e9`; round-3 F2): a break that reaches only an interior byte

The control (`test_builder.py:14646-14650`, entry `:14726-14728`):

- It declares `static int milan_verdict_next;` just after the verdict and hands `sscanf("%c")` `(char *)(&milan_verdict_next - 1) + 1`. It is graded with pins `(VERDICT_PIN_ESCAPE,)`.
- The premise check (`:14731-14756`) reads `_image["relocations"]` directly, not through `rv32_image_references()`. It requires the relocations from `nvm_boot()` that land inside the verdict to be non-empty, with none at +0.
- The closing line prints the bytes reached (`:17211-17214`).

Measured at the head:

| Run | Result | Receipt |
|---|---|---|
| N0: head, no mutation | passes gate 1b through its closing line: slot kept, 6 in-place references, "refused 15/15 ... one of them reaching it only at byte(s) +1" | `mutants/f1_5b4a47e99_N0.log` |
| K7 (first-byte-only range, `target != low`, the round-3 M9 class) at the head | KILLED: "the resolver accepted a neighbour's address folded onto an interior byte of aem_loaded" | `mutants/b1_5b4a47e99_K7.log` |
| K7 at round-3 head `0a80abcb` | SURVIVES: gate 1b passes, "refused 14/14" | `mutants/f1_0a80abcb3_K7.log` |
| K8 (the pins function's own range shrunk to one byte) | KILLED by the same break | `mutants/f2_batch.txt` |
| K0 (no pin ever breaks), K1 and K2 (the store pin's image and resolver halves), K3 (escape), K4 (one name), K5 (locality), K6 (AUIPC) | all KILLED, each by a control that names the pin or by an accepted control | `mutants/b1_batch.txt`, `mutants/f2_batch.txt` |
| B1 (the break moved onto the neighbour's own byte) and B2 (moved onto the verdict's first byte) | the premise check fails, on "byte(s) []" and "byte(s) [0]" respectively | `mutants/f2_batch.txt` |

The documentation matches the code:

- `BAREMETAL_FIRMWARE.md:1002` says "fifteen", and the table has 15 breaks (`:1006-1019`).
- `:1026-1032` describes the premise check as coded.
- The claim that "a census that read only the first byte passed the other fourteen" is what K7 at `0a80abcb` measures.
- The CHANGELOG line (`CHANGELOG.md:67`, "So does an overrun of another object onto the verdict.") makes no claim of exhaustiveness.

My mutant set is my own. It covers the pins that round 3 listed (M1 to M8), with different spellings. The round-3 scripts themselves were not rerun.

### No firmware, RTL or bitstream change

- `git diff 0a80abcb..5b4a47e9 -- sw/firmware hdl syn constraints tb` is empty. The gitlinks are unchanged: processor `b2db3a97`, gPTP `5dce647a`, verilog-axis `48ff7a7e`, external `efeb541a`.
- `milan_baremetal.c` has sha256 `a73ecc25...0eb3`, equal to `tb/verilator/nvm_capture_cpu/measurements.json`'s `product_firmware_sha256` (`receipts_static.txt`).

### Docs gates at the head

These ran in the clone: `docs_check.py` (0 findings, 177 md files), `check_doc_style.py` OK, `check_doc_paths.py` OK (861 paths), and `git diff --check 79c36963..HEAD` clean (`docs_gates/`).

## Findings

### F1 - MINOR - Conformance, Robustness, Tests, Docs - the texts still claim that only two addresses reach the verdict without a relocation; a run-time pointer handed to a callee is a third

**Where:**

- `docs/integration/BAREMETAL_FIRMWARE.md:970-971`: "Outside the two limits below, the word that store wrote is the word read back after `nvm_boot()`".
- `BAREMETAL_FIRMWARE.md:974-976`: "two addresses reach the verdict's bytes with no relocation on them".
- The refusal row at `:1638`: "Two writes put no relocation on its storage and are outside these pins: one through a literal address, and one through another object's address ...".
- `sw/builder/test_builder.py:1650-1652` ("outside the two limits below the word this function stored is still the word it reads back after the call") and `:1654-1656` ("two addresses reach the static's bytes with no relocation on them").
- The gate's closing line at `:17215-17220`, printed on every run: "two writes put no relocation on its storage and are outside these pins: ...".
- The PR body, round 4 item 1: "Two addresses reach those bytes with no relocation on them, and both are stated limits".

**Authority:**

- Round-4 assignment 5909983141, item 1: the texts "state only what the census proves" and "name both limits".
- Round-3 assignment 5905511808, item 1, is the same rule.
- `AGENTS.md` section 6, `Tests`: each test can fail for the defect it claims to detect.

**Evidence:**

- `csr_pointer_sscanf` plants `(void)sscanf("\001", "%c", (char *)(uintptr_t)milan_read(MILAN_ID));` as the first statement of `nvm_boot()`. The pointer is a run-time value read from a CSR. It is not a number written in the source, and it is not formed from any object's relocation.
  - The resolver accepts it, with the slot kept and the image's relocations on the verdict unchanged (`probes/probe_run.log`).
  - Planted into the shipping firmware file, the whole uninstrumented `test_baremetal_profile_contract()` returns (`whole/csr_pointer_sscanf.log`, "R412 GATE FUNCTION RETURNED").
  - In that same run the gate prints "kept the slot of aem_loaded ... two writes put no relocation on its storage and are outside these pins: one through a literal address, and one through another object's address carried outside that object".
- `stack_runtime_sscanf` hands `sscanf()` a frame local's address plus a CSR-read offset (`char loc[4]; ... loc + (int)milan_read(MILAN_ID)`). The whole gate function also accepts it (`whole/stack_runtime_sscanf.log`).
  - This one fits the second limit's heading ("another object's address, carried outside that object"). It does not fit the heading's own definition: "a pointer formed from a neighbouring object's relocation". A stack address carries none.
- A pointer read from NVM data, or returned by a callee this unit does not define, is of the same kind.
- The same pointer used in the unit's own store is refused by rule 1b (`own_store_runtime`). So the gap is exactly the standing callee limit, "What the census does NOT observe", first entry (`BAREMETAL_FIRMWARE.md:811-821`), applied to the verdict. The texts narrow that limit to a pointer's origin, and then count the origins as if the list were complete.
- The general sentences are accurate: "the pins prove this much and no more", and the docstring's "a write through an address with none on those bytes passes". The finding is the count and the "outside the two limits" consequence.

**Impact:**

- The shipping firmware is not affected. This is a claim defect, not a code defect.
- A reader, or the gate's own printed verdict, is told that outside two named shapes the verdict read after `nvm_boot()` is the one `milan_init()` stored. But a callee handed a CSR-derived or NVM-derived pointer inside `nvm_boot()` can change it, with gate 1b green and the slot kept.
- Neither limit's stated closure reaches this class: the SoC RAM map closes literal addresses, and memory safety closes overruns.

**Required outcome:** every one of the six places above states only what is proved. There are two ways to get there:

- Drop the count and the "outside the two limits" consequence.
- Or state the limit as the callee class it is: a called function writing through any pointer that carries no relocation on the verdict's bytes is not seen. Name the literal address, another object's address carried outside it, and a pointer of run-time origin (a CSR or NVM read, a callee's return, a frame address carried out of its frame) as examples.

The manager rules whether this is recorded on #495 beside the two limits, or closed.

**Verification:**

- Re-read the six places at the fix head.
- `scripts/make_probes.py` `csr_pointer_sscanf` and `stack_runtime_sscanf`, through `scripts/patch_probe_hook.py` and `scripts/whole_gate_plant.py`, are either refused naming a pin (if closed), or accepted and matched by the stated limit's words (if accepted).

## Considered and not raised

- **The docstring** (`test_builder.py:6922-6933`) is accurate. Its general lead clause covers F1's class.
- **The unit's own bounded-loop store** over a neighbour array (`own_store_bounded_loop`) is refused by rule 1b as unplaceable, not placed as a range. That is conservative, and consistent with "a store through an offset known only at run time is refused by rule 1b".
- **The stack class** (a store the census places on the stack is taken not to land on the verdict) is the standing model's stated assumption (`BAREMETAL_FIRMWARE.md:884-886`), repeated at `:966-968`. It is not a new claim.

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts (at the head) | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Assignment 5909983141 items 1 and 2 against `BAREMETAL_FIRMWARE.md:919-1033`, `:1638`, `test_builder.py:1631-1677`, `:6905-6933`, `:14646-14756`, `:17211-17220` and the PR body. Item 2 is met; item 1 is met except for F1 | R412-4 | 5b4a47e99f5a453832ccabccfbf4aae116d6fea0 |
| RTL | CLEAN | `git diff 0a80abcb..5b4a47e9 -- sw/firmware hdl syn constraints tb` is empty; the four gitlinks are unchanged; the firmware sha256 equals the capture receipt (`receipts_static.txt`). Nothing in RTL scope has changed since round-3 head `0a80abcb`, where RTL was accepted in round 3 | R412-4 (on an unchanged RTL scope since R412-3) | 5b4a47e99f5a453832ccabccfbf4aae116d6fea0 |
| Robustness | UNCLEAN (F1) | 18 gate-1b probes and 3 round-3 shapes: folded bytes +0 to +3 and before and after the neighbour, run-time offsets, the unit's own stores, a bounded loop, literal, CSR and stack-derived pointers; 2 whole-gate plants (`probes/`, `whole/`) | R412-4 | 5b4a47e99f5a453832ccabccfbf4aae116d6fea0 |
| Tests | UNCLEAN (F1: the gate's closing line and rule comment claim more than the gate measures) | The new control and its premise check (`test_builder.py:14646-14756`); N0 passing with 15/15 and +1; K0 to K8 all killed; K7 surviving at `0a80abcb`; B1 and B2 failing the premise (`mutants/`) | R412-4 | 5b4a47e99f5a453832ccabccfbf4aae116d6fea0 |
| Docs | UNCLEAN (F1) | `BAREMETAL_FIRMWARE.md:919-1033` and `:1638`, `CHANGELOG.md:66-67`, the PR body round 4; docs gates `docs_check.py`, `check_doc_style.py`, `check_doc_paths.py` and `git diff --check` (`docs_gates/`) | R412-4 | 5b4a47e99f5a453832ccabccfbf4aae116d6fea0 |

## Disposition of prior public review findings at this head

| Finding | At this head |
|---|---|
| R412-3 F1 (a callee writing through another object's pointer; "nothing writes the verdict but that one store") | **Resolved as ruled** (5909983141): the limit is stated in all required texts, the phrase is gone, and both probes are accepted and match the limit's words. The residual overclaim is a different class, raised as F1 above |
| R412-3 F2 (no control measures the four-byte range; M9 survives) | **Resolved.** The interior-byte break kills the first-byte-only mutant (my K7) at the head, and it survives at `0a80abcb`. The other pin mutants stay killed, and the head passes with the slot kept |
| R412-3's round-2 disposition (the alias and weakref class) | Unchanged at this head; still resolved as ruled |
| The other reviewer's round-3 report (R413-3, 5909532354, POSITIVE at `0a80abcb`; read after this verdict and ledger were written) | It has no open findings. Its resolved R413-2 F1 (the alias and weakref class) still holds: the alias and weakref breaks remain among the 15 refused, and K4 (no one-name pin) is killed on `alias_sscanf`. Its resolved F2 and S1 (the W6 control) are untouched: nothing under `tb/` changed since `0a80abcb` |

## Limits of this round

- I did not run the full builder bank, the parent, processor or gPTP banks, Yosys, hosted CI or the local CI replica, and I made no calibration or hardware claim.
- Gate 1b was run as the gate function alone:
  - N0 and the round-3 K7 comparison ran through a stop marker placed just after gate 1b's closing verdict line;
  - the two F1 plants ran the whole gate function uninstrumented;
  - a first N0 run of the whole function also returned, but its scratch tree was replaced while it ran, so it is excluded and not relied on. It is the first line of `mutants/b1_batch.txt`, and its log is not published. The K lines of that batch come from separate trees and stand.
- A first attempt from a `git archive` copy without git metadata failed at an unrelated RTL-mutant step, which needs `git ls-files` in the processor. It is excluded too.
- My census mutants are my own spellings of the round-3 M1 to M9 classes, not the round-3 scripts.
- The hosted contexts at the head are mixed. Completed with success: `rtl-fast`, `verilator-lint`, the `yosys-elaboration` and Yosys shards, Verilator shards 0 and 3, `bdd-conformance`, `wire-accountability`, `full-ci-gate` and `docs-check-no-git`. `docs-check`, `elaborate` and Verilator shards 1, 2 and 4 were in progress when I listed them, and "Physical gPTP" was skipped. A skipped context is not executed evidence.
- Paths in the published receipts are redacted to `$HOME`, `$PACKET` and `$CLONE`.

## Pending manager duties

- Rule on F1: accept the run-time-pointer callee class as a stated limit (text only, with #495), or require it closed.
- Hosted and local-replica acceptance at the exact head.
- The current-dev candidate build at the merge turn (live dev `ccdd07b5`), candidate-merge validation, and post-merge containment.
- Physical calibration was not run and remains open as stated.

R412-4 FINISHED
