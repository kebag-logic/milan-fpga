# [A460] #70 lane 2 round 4 handoff (PR #623)

Status: **item 1 done (`fa1d6e03`), item 2 done (`5b4a47e9`)**. Every gate is rc 0 at
`5b4a47e9` (clean tree, physical path, never piped), both builder banks included. REVIEW READY
is posted.

- Branch `70-lane2-pin-d352`, local only. Start head `0a80abcb3a09f8f6236379d7b2ed91fc4cc478d4`.
- End head `5b4a47e99f5a453832ccabccfbf4aae116d6fea0`, tree `4da3a4345786338298d728d06b82fe9d35bc2e2a`:
  28 commits on dev `79c36963`, two this round, `fa1d6e03` (item 1) and `5b4a47e9` (item 2).
  Processor pin `b2db3a97`, unchanged. No push, no PR edit.
- Assignment: round 4 on #70, comment 5909983141. Also read: ruling 5894183475, the round-3
  assignment 5905511808 and its ruling 5906400668, the reviews R412-3 (5909975429, NEGATIVE on
  F1 and F2, both MINOR) and R413-3 (5909532354, POSITIVE), and R412-3's packet (scripts and
  receipts).
- On #70: TAKEN 5909997393, REVIEW READY 5910819312 (text in `REVIEW-READY.md`). Nothing else
  was posted, and no comment was edited or deleted.

## Item 1: R412-3 F1, the bounded claim and both limits (`fa1d6e03`)

The ruling accepts F1 as a second stated limit. The texts now say only what the census proves,
replace "nothing writes the verdict but that one store" with the bounded claim, and name both
limits.

- `sw/builder/test_builder.py:1632-1676`, the rule comment in `rv32_step()`'s call rule. The
  escape sentence now reads "no relocation on those bytes forms their full address" (was "no
  relocated reference forms its full address"). The conclusion now reads (`:1647-1652`): "That
  is all the pins prove: of the writes that reach the static through a relocation on its bytes,
  milan_init()'s one store is the only one, so outside the two limits below the word this
  function stored is still the word it reads back after the call". `LIMITS, stated rather than
  closed` (`:1654-1676`) names:
  - a literal address (unchanged in substance, #495);
  - another object's address carried outside that object: a pointer formed from another
    object's relocation and carried past that object's end or before its start. A called
    function writing through it is not seen, since a call's arguments are recorded and not
    judged (`sscanf()` overrunning a neighbouring static buffer, or handed `&neighbour + k` with
    k known only at run time). Neither is a store this unit makes through it at an offset the
    resolver places on the other static. A folded offset is refused by address, and a run-time
    offset stored in the unit by rule 1b. "This is the memory-safety class the standing model
    leaves open, and this gate does not prove memory safety."
- `sw/builder/test_builder.py:6899-6933`, the `verdict_image_pins()` docstring: the escape
  bullet bounded the same way, and a `LIMITS` paragraph naming both (the rulings on the round-3
  STOP and review). The paragraph was tightened to keep the function at 98 lines: the idiom
  ratchet's 100-line bound failed at 102 on the first draft.
- `sw/builder/test_builder.py:17216-17220`, the gate's closing line: "two writes put no
  relocation on its storage and are outside these pins: one through a literal address, and one
  through another object's address carried outside that object, such as a called function's
  overrun of a neighbouring static" (was the literal address alone).
- `docs/integration/BAREMETAL_FIRMWARE.md`:
  - `:935-941`: the escape bullet bounded to relocations on those bytes, plus "An address formed
    from another object's relocation is not a reference to those bytes (the second limit
    below)";
  - `:966-972`: the standing-model paragraph, with the bounded claim in place of "So, within that
    model and that limit, nothing writes the verdict but that one store";
  - `:974-998`: **Two limits, stated rather than closed**, the literal address (`:978`) and
    another object's address carried outside that object (`:983`), which cites the standing
    callee entry of "What the census does NOT observe" (`:811-821`) and ends "gate 1b is not a
    memory-safety prover";
  - `:1638`, the refusal row: "with no relocation on its storage forming its full address" (was
    "with its full address never formed"), and both limits in place of the literal one.
- `CHANGELOG.md:67`: "So does an overrun of another object onto the verdict." after the literal
  line.

The gate's closing line and the CHANGELOG were not listed by the assignment. They were the other
two places stating the literal limit alone, so a reader of either would have taken it for the
only one.

### Why the limit names this unit's own store as well as a callee's

This round's own probes (`probes/plants_a460.py`, early mode, `receipts/gate1b_early_a460_*.log`):
at `0a80abcb` and at the head, a store this unit makes through a local pointer to a neighbour
static, carried outside it by a constant offset applied in a register, is **accepted with the
slot kept**:

| Probe | Shape (inside `nvm_boot()`) | At `0a80abcb` | At `5b4a47e9` |
|---|---|---|---|
| `unit_under_store` | `static int r460_pad;` after the verdict; `int *r460_p = &r460_pad; r460_p[-1] = 1;` | ACCEPTED, kept | ACCEPTED, kept |
| `unit_over_store` | `static char r460_line[4];` before the verdict; `char *r460_q = r460_line; r460_q[4] = 1;` | ACCEPTED, kept | ACCEPTED, kept |
| `interior_const` | the item-2 control's shape, spelled `(char *)&r460_next - 3` | REFUSED, escape | REFUSED, escape |

The resolver places each store on the other static (`Rv32Sym` plus the offset, `:1580-1584`) and
forgets only that static's slots. The image shows the relocation on the neighbour, not the
verdict. This is the standing-model clause "one it places at ... another static is taken not to
land on it", which the texts already stated. The ruling's rationale ("the general memory-safety
class") covers it, so the second limit states it rather than claiming a store in the unit is
always refused.

## Item 2: R412-3 F2, a break on an interior byte (`5b4a47e9`)

- `sw/builder/test_builder.py:14646-14650`, `verdict_interior_break`: the AEM-first base with
  `static int milan_verdict_next;` declared just after the verdict, and
  `(void)sscanf("\001", "%c", (char *)(&milan_verdict_next - 1) + 1);` opening `nvm_boot()`. The
  offset is written as one `int` back plus one byte, not as `- 3`. The SDK compiler at the
  census flags plus `-no-pie` folds it to one relocation pair, `R_RISCV_HI20` and
  `R_RISCV_LO12_I` on `milan_verdict_next - 3`, with the neighbour at `aem_loaded + 4`.
- `:14726-14728`, the fifteenth entry of `verdict_pin_breaks`, "a neighbour's address folded onto
  an interior byte of aem_loaded and handed to sscanf() inside nvm_boot()", pins
  `(VERDICT_PIN_ESCAPE,)`.
- `:14731-14756`, the premise check before the breaks are graded. It takes
  `verdict_image_take()` of the break and reads the relocation targets directly, not through
  `rv32_image_references()`, whose range is under test. It requires `nvm_boot()` to place at
  least one on the verdict's bytes and none on the first byte, else "the interior-byte break's
  references from nvm_boot() land on byte(s) [...] of aem_loaded's storage, not past its first
  byte alone, so it does not measure the census's range: milan_verdict_next must follow the
  verdict, and the compiler must fold the offset into the relocation".
- `:17211-17215`, the closing line: "refused 15/15 planted pin breaks on the verdict, each naming
  its pins, one of them reaching it only at byte(s) +1 of its storage, which measures the
  census's four-byte range".
- `:14613-14621`, the comment over the controls.
- `docs/integration/BAREMETAL_FIRMWARE.md:1002` "fifteen breaks", `:1019` the new table row
  (escape), and `:1026-1032` a paragraph on what the break measures.

### The planted control and its refusal text (head, `receipts/gate1b_full_base.log`)

At the head, the whole gate 1b refuses the break naming the escape pin, as `interior_const` and
R412-3's `nbr_byte_sscanf` show on the early path: "the linked image forms the full address of
aem_loaded's storage (the full address formed in a register (%lo on an addi) at 0x0001319c in
nvm_boot() (R_RISCV_LO12_I))". No other image pin is named, and no early diagnostic fires. The
whole gate prints "refused 15/15 ... one of them reaching it only at byte(s) +1".

### The premise check can fail (`probes/premise_mutants.py`, `receipts/premise_mutant_*.log`)

Each mutant rewrites only the break's C statement in a byte copy of the clone at `5b4a47e9`, and
the whole gate 1b is run with R412-3's `run_gate1b.py`:

| Mutant | Statement | Result |
|---|---|---|
| P1 on the neighbour | `(char *)&milan_verdict_next + 1` | REFUSED: "the interior-byte break's references from nvm_boot() land on byte(s) [] of aem_loaded's storage, not past its first byte alone, so it does not measure the census's range: ..." |
| P2 on the first byte | `(char *)(&milan_verdict_next - 1)` | REFUSED: "... land on byte(s) [0] of aem_loaded's storage, ..." |

So a layout or folding change that moved the break off an interior byte reddens the gate with that
reason. Without the check, P1 would show up as the break being accepted, and P2 would pass the
gate while measuring nothing new.

## Census mutants (R412-3's `census_mutants.py` and `census_mutants_run.sh`, unchanged)

Each is run through the whole gate 1b on a byte copy of the clone at `5b4a47e9`
(`receipts/census_mutant_*.log`).

| Mutant | At `0a80abcb` (R412-3) | At `5b4a47e9` | Killed by |
|---|---|---|---|
| M1 no escape pin | KILLED | KILLED | `&aem_loaded` break refused without naming escape |
| M2 no name pin | KILLED | KILLED | `alias_sscanf` refused without naming one name |
| M3 no locality pin | KILLED | KILLED | external linkage refused without naming local |
| M4 no AUIPC pin | KILLED | KILLED | the AUIPC break accepted |
| M5 no image half of the store pin | KILLED | KILLED | the `#ifndef __PIE__` write accepted |
| M6 no resolver half of the store pin | KILLED | KILLED | `&aem_loaded` break refused without naming the store |
| M7 `%lo` on OP-IMM read as a load | KILLED | KILLED | `&aem_loaded` break refused without naming escape |
| M8 no image | KILLED | KILLED | a second assignment accepted |
| **M9 only the first byte counts** | **SURVIVED** (`GATE1B PASS`, 14/14) | **KILLED** | "the resolver accepted a neighbour's address folded onto an interior byte of aem_loaded and handed to sscanf() inside nvm_boot()" |

## The reviewers' probes, rerun (R412-3's `plants3.py`, `probe_all.sh`, `early_stop3.py`, `run_gate1b.py`, unchanged)

The scripts were copied from R412-3's packet, byte-identical to its `MANIFEST.sha256`, and run from a
scratch packet on disposable copies (`git archive` of the head plus each submodule at its
gitlink for the early mode, a byte copy of the clone for the whole gate). Early mode at
`5b4a47e9` (`receipts/gate1b_early_*.log`), identical in outcome to R412-3's table at `0a80abcb`:

| Probe | Result | Pins named, or the rule that refused first |
|---|---|---|
| base | ACCEPTED, `kept=['aem_loaded']` | 6 references, all in place; refused under forget-on-call |
| `nbr_runtime_sscanf` | **ACCEPTED, kept** | the second stated limit (a called function, `&r412_pad + k`, k = -1 at run time) |
| `pre_overrun_sscanf` | **ACCEPTED, kept** | the second stated limit (a called function, `"%s"` overrunning a four-byte static before the verdict) |
| `nbr_after_sscanf`, `arr_overrun_sscanf` | accepted | layout controls: their writes land on `nvm_started`, above the verdict |
| `nbr_before_sscanf`, `nbr_byte_sscanf` | REFUSED | escape only (folded offset, on the verdict's first and second byte) |
| `alias_sscanf`, `weakref_sscanf`, `static_alias_sscanf` | REFUSED | escape, one name |
| `alias_decl_only` | REFUSED | one name |
| `alias_write`, `static_alias_write` | REFUSED | store, one name |
| `splice_write`, `paste_write`, `m_macro_set` | REFUSED | store |
| `m_macro_addr` | REFUSED | store, address (early) |
| `m_macro_addr_sscanf` | REFUSED | escape, address (early) |
| `plain_write`, `bcp_write`, `pie_write`, `optimize_write` | REFUSED | source rule "aem_loaded must contain only the image verifier's verdict" (the last two per arm selection) |
| `block_extern_sscanf` | REFUSED | source rule "the address of aem_loaded must not be taken" |
| `nbr_runtime_store` | REFUSED | rule 1b, "a STORE this gate cannot PLACE" |
| `nbr_memset` | REFUSED | identity-sample register diagnostic, not on the verdict |

Through the whole gate 1b (`R412_MODE=full`, `receipts/gate1b_full_*.log`): the unplanted head,
`nbr_runtime_sscanf` and `pre_overrun_sscanf` each end `GATE1B PASS`, rc 0, with the slot kept
and "refused 15/15 ... one of them reaching it only at byte(s) +1". The two F1 probes are
accepted, and each matches the second limit's words: a pointer formed from a neighbouring
static's relocation, carried before its start (`nbr_runtime_sscanf`, a run-time offset) or past
its end (`pre_overrun_sscanf`, the callee's advance), written by a called function.

`check_review_runs.py` asserts all of the above from the receipts, each naming this head (gate
`review-runs`).

A first whole-gate run of the unplanted head was cut short: R412-3's `probe_all.sh` names each
scratch tree by probe, so the early-mode `base` probe, started while it ran, replaced its tree.
It was stopped and set aside (`receipts/invalid/`), and the whole-gate `base` was rerun alone.

## Gates at `5b4a47e9`

Two receipts, from one gate runner (`run_gates.py`): `gates-5b4a47e9-builder.json` (the two builder
banks, one after the other) and `gates-5b4a47e9-rest.json` (the other fourteen, run beside the
second bank). Each records the command, rc, seconds, log size and sha256, and the head, tree and
cleanliness after the run: `5b4a47e9`, tree `4da3a434`, clean in both. The logs were written under
the scratch area on `/data` and are copied byte for byte to `receipts/gates-5b4a47e9/`, each under
200 KB. Every gate ran at the clean committed tree, from the physical path, never piped.

| Gate | rc | s | Result (last lines of the log) |
|---|---|---|---|
| builder bank, RV32 compiler required (`--require-elaboration --require-rv32`) | 0 | 1043 | gate 1b "... and refused 15/15 planted pin breaks on the verdict, each naming its pins, one of them reaching it only at byte(s) +1 of its storage, which measures the census's four-byte range; two writes put no relocation on its storage and are outside these pins: one through a literal address, and one through another object's address carried outside that object, such as a called function's overrun of a neighbouring static". Ends "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 11's calibration build tree, as in rounds 1 to 3). Log sha256 `051f447b...` |
| builder bank, every cross-compiler candidate hidden (`full-builder-absent.py`) | 0 | 668 | "ALL GATES PASS EXCEPT 2 NOT RUN" (gate 1b's compiled census, by design of that arm, and gate 11), then "FULL BUILDER ABSENT PASS: all three cross-compiler candidates hidden". Log sha256 `732fad5c...` |
| `review-runs` (`check_review_runs.py` over the probe and mutant receipts) | 0 | 0.0 | "REVIEW RUNS AS EXPECTED at 5b4a47e9...: 25 review probes and 3 of this round's early, 3 through the whole gate 1b, and census mutants M1-M9 all killed" |
| firmware digest (`check_firmware_digest.py`) | 0 | 0.0 | unchanged since `597dba85`, `943a3dac`, `0a80abcb`; sha256 = capture receipt |
| `scripts/check_nvm_capture.py` | 0 | 0.7 | "PASS: capture census, clocks, both timing arms and receipt agree" |
| `fw_service_budget/run.py --self-test` | 0 | 0.6 | oracle 52 checks, 0 failures |
| grader mutants (`check_grader_mutants.py`, R412-3's `grader_mutants.py` and `grader_mutants2.py` unchanged) | 0 | 2.6 | "W0 passes; W1-W6 killed (W3, W4 and W6 by name); X1, X2, X4, X5 killed and X3 passes as a stricter rule" |
| `scripts/check_py_idiom.py` | 0 | 3.4 | every ratchet at or under its bound (long functions 9 <= 9: `rv32_step` 97 lines, `verdict_image_pins` 98) |
| `scripts/measure_test_evidence.py --check` | 0 | 5.7 | "TEST-EVIDENCE RATCHET: PASS" |
| `git diff --check 79c36963 HEAD` | 0 | 0.0 | empty |
| `scripts/docs_check.py` (pinned Markdown environment, as are the next five) | 0 | 4.4 | "0 finding(s) across 177 md files" |
| `scripts/check_doc_paths.py` | 0 | 0.1 | "OK (861 cited paths all resolve)" |
| `scripts/check_doc_style.py` | 0 | 0.1 | "OK (22 current documents)" |
| `scripts/check_archive.py` | 0 | 0.3 | "OK (21 historical page(s))" |
| `scripts/gen_toc.py --check` | 0 | 3.0 | "OK (119 page(s))" |
| `scripts/check_em_dash.py --base 79c36963` | 0 | 3.0 | "0 finding(s) over 555 added line(s) in 24 changed Markdown page(s)" |

The assignment's gates are the two builder banks, R412-3's `census_mutants_run.sh` and
`probe_all.sh` (through `review-runs`), the docs gates and the firmware digest. The capture check,
the grader self-test and mutants, the idiom and evidence ratchets and `git diff --check` are
supporting.

## Firmware digest

`sw/firmware` has no difference from `597dba85`, `943a3dac` or `0a80abcb`. `milan_baremetal.c`
sha256 is `a73ecc25c77bfb7c4e1c2c711d72f0b560dd7e8d18cde92f40e67efcc84f0eb3`, equal to the
capture receipt's `product_firmware_sha256`. No firmware, RTL, bitstream, CI or processor byte
changed: the round's diff `0a80abcb..5b4a47e9` touches `CHANGELOG.md`,
`docs/integration/BAREMETAL_FIRMWARE.md` and `sw/builder/test_builder.py` only.

## Packet

- `TAKEN.md` (posted, 5909997393), `REVIEW-READY.md` (posted, 5910819312), `PR-BODY.md` (the Round 4 section,
  a pointer from round 3's limit sentence, the planted-break count in Items; not pushed).
- `run_gates.py`, `full-builder-absent.py` (the previous round's, byte-identical),
  `check_firmware_digest.py`, `check_grader_mutants.py`, `check_review_runs.py`,
  `run_detached.sh`, `wait_for.py`, `gates-5b4a47e9-builder.json`, `gates-5b4a47e9-rest.json`.
- `probes/plants_a460.py` and `probes/probe_a460.sh` (this round's three early probes),
  `probes/premise_mutants.py` and `probes/premise_mutants_run.sh` (P1, P2).
- `receipts/gates-5b4a47e9/` (every gate log), `receipts/review-runs-5b4a47e9/` (R412-3's 25
  early probes, 3 whole-gate probes and 9 census mutants, this round's 3 probes and 2 premise
  mutants, all at the head), `receipts/review-runs-0a80abcb/` (the same scripts at the start
  head, before any edit: base, R412-3's three F1/F2 probes and this round's three),
  `receipts/invalid/` (the cut-short whole-gate `base` run).
- R412-3's scripts were run from a scratch copy on `/data`, byte-identical to that review's
  `MANIFEST.sha256`. Scratch trees were exports or byte copies of the committed clone and are
  deleted.
- `MANIFEST.sha256`: the sha256 of every file in the packet but itself.

## Open

- Both stated limits, the literal address and another object's address carried outside it, are
  recorded on #495 by the manager (per the round-4 assignment and the round-3 ruling).
- The second limit covers this unit's own store through a pointer carried off another static at
  an offset the resolver places on that static (measured above). That store was already inside
  the standing model's "another static" clause, and the ruling's rationale is the whole
  memory-safety class. It is stated here so the text claims nothing the census does not prove.
