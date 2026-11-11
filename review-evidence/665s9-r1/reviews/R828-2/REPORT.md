[R828] POSITIVE - exact head a69fc0f597355a0a200ec5be6bb134b897e97ff5

# R828-2: external delta review of PR #889 (issue #870, Mark II split S9)

- **Exact head:** `a69fc0f597355a0a200ec5be6bb134b897e97ff5`, tree `bc5cc0e0f7d41e4a8a1aff1a704afc1cc58f5adc`.
- **Source base:** `1d6bf555`.
- **Delta:** `a91fb27d..a69fc0f5`. These are three commits by the executor under the round 4 ruling (#870 issuecomment-6796161767).

**Verdict: POSITIVE.**

- The four prior MINOR findings are resolved at their cause at this head: R827-1 F1 and F2, and R828-1 F1 and F2.
- No BLOCKER, MAJOR or MINOR is open.
- Two RESIDUE items and four SUGGESTIONs are recorded below.

One reviewer covers this delta, under the owner's speed-up rule. Code the delta does not touch keeps its round 1 lens verdict (R828-1 at `a91fb27d`). The delta changes nothing that this code depends on.

## Order of reconstruction

1. AGENTS.md and CONTRIBUTING.md: the five lenses, the severity rules, the completion ledger and the comment rule.
2. The body of issue #870: its scope, decision D2, the identity gate, and acceptance 1-6. Acceptance 6 is the item this delta touches.
3. The round 4 ruling, items 1-5, and the review-start comment (PR #889 issuecomment-6799479526).
4. The diff, read first: `git diff --stat` and `git diff a91fb27d a69fc0f5`. Then the history of `a91fb27d..a69fc0f5`, and the touched code at head:
   - `sw/litex/check_image_identity.py:79-88, 165-225`
   - `sw/litex/milan_soc.py:3003-3022, 4950-4966`
   - `sw/builder/test_builder.py:23604-23780`
   - `tb/verilator/mbx/suite.hpp:136-156, 958-963`
   - `mutants.py:138, 596-604`
   - `README.md:97-102, 155-164, 265, 393`
   - `docs/design/MAILBOX_SPLIT.md:128-141, 1622-1648`
   - `docs/design/MARK_II_AREA_PLAN.md:964-1016`
5. The executor's round 4 packet, `review-evidence/665s9-r1/author-r4` at archive `460db965`: HANDOFF, PR-BODY, `receipts/r4/*` and round 3's route hashes. Then the REVIEW READY comment (#870 issuecomment-6799404933) and the PR body.
6. The two round 1 reviews, read only after my own pass over the diff and only for the findings named here: R827-1 (issuecomment-6796150573) and R828-1 (issuecomment-6796136305). I read no other reviewer's report.

## Scope verification (ruling: tests and docs only)

The evidence for this section is in `receipts/delta_scope.txt`.

- `git diff --stat a91fb27d a69fc0f5` changes six files, all mode `100644`:
  - `docs/design/MAILBOX_SPLIT.md`
  - `docs/design/MARK_II_AREA_PLAN.md`
  - `sw/builder/test_builder.py`
  - `tb/verilator/mbx/README.md`, `mutants.py` and `suite.hpp`
- `git diff --name-only` limited to `hdl sw/mailbox sw/litex configs VERSION scripts .github *.tcl *.xdc *.yaml *.sh` is empty. So no RTL, mailbox generator, SoC, recipe, routed or workflow file changed, and no gitlink changed.
- `git diff --check` is clean over `1d6bf555..a69fc0f5` and over `a91fb27d..a69fc0f5`.
- Each of the three commits has a one-line subject, with no body and no trailers.

## Prior findings at this head

| Prior finding | Status at `a69fc0f5` | Evidence |
|---|---|---|
| R827-1 F1 (MINOR, Tests): the bound-bitstream branch had no positive control | **Resolved** | (1) |
| R828-1 F1 (MINOR, Tests, Conformance): the manifest-ident rule `check_image_identity.py:175-176` had no plant | **Resolved** | (1) |
| R827-1 F2 and R828-1 F2 (MINOR, Tests, Docs): the new check reused `H0` | **Resolved at its cause.** Read literally across both suite files, "no shared prefix" still finds pairs that predate this PR | (2), S-A |
| R827-1 R1 and R828-1 R1 (RESIDUE, Docs): the routed-net counts | **Resolved** | (3) |
| R827-1 S1 (SUGGESTION, Docs): publish the bus-clock path headers | **Taken**, and the doc's sentence corrected | (4) |
| R827-1 S2 (SUGGESTION, RTL, Robustness): a default transition for the FSM | Declined by the ruling, for #495. Not a finding here | Ruling item 4 |
| R828-1 S1 (SUGGESTION, Tests): A5 versus `axil-rdata-follows-port` | Not addressed, and not asked for by the ruling. Carried as S-C | `mutants.py:169-170` unchanged |
| R828-1 F1, optional part: no plant for the manifest-fields rule `:167-171` | Not addressed. It was optional, and it is a schema rule, not an identity mismatch under acceptance 6. Carried as S-B | `test_builder.py:23669-23711` |

### (1) Gate 23p: the positive control and the manifest-ident plant

**The control** is at `sw/builder/test_builder.py:23714-23723` and is graded at `:23757-23764`.

- It copies the good split image and writes a fixture bitstream at `gateware/alinx_ax7101.bit`.
- It sets the manifest's `bitstream` to `qspi_transition.bitstream_binding(bit)`. That is what a split `--build` writes:
  - `milan_soc.py:4964-4966` passes the sram bitstream to `write_image_manifest`.
  - `check_image_identity.manifest()` stores `bitstream_binding(bitstream)` (`:88`).
- The gate must exit 0 with no `FINDING`.
- The good split image is exported without `--build`, so the copy holds exactly one `.bit`. The control therefore reaches the comparison at `:224`, not the branch "binds a bitstream, the image has N".

**The plant** is at `:23706-23710`.

- It sets the manifest's `ident` to the split ident without its last word. That is the all-fabric ident (`milan_soc.py:3003`).
- The image's ident is left alone.
- The gate must fail with `FINDING manifest:`.

**The executor's receipts.**

- `receipts/r4/gate23p-mutants-dev.txt`, at tree `bc5cc0e0`, from the driver `tools/gate_mutants.sh`, with the file restored after each arm:
  - `if True:` fails 23p on the control.
  - `have == bound` fails it on the control and on "another bitstream".
  - Removing lines 175-176 fails it on "the manifest's ident changed ... (exit 0)".
- `gate23p-mutants-base.txt`, at `a91fb27d`: `if True:` and the removed rule both give `ALL GATES PASS`. So the new tests are the ones that bite.
- `gates/test-builder.log:279-294` lists the control as "passes", lists 13 plants each with its `FINDING`, and prints the summary line. The run ends `ALL GATES PASS EXCEPT 2 NOT RUN` with rc 0. The two rows not run are the same as round 3's.

**My own probe** is `scripts/probe_identity_rules.py`, with its output in `receipts/probe_identity_rules.log`.

- Gate 23p itself cannot run here, because no interpreter on this host imports migen or LiteX.
- The probe instead drives `_manifest_rules` and `_bitstream_rules` directly. It runs them on the head's module and on three planted copies held in memory, with facts shaped like the control and the plant.
- The binding goes through a JSON round trip, as it does in the manifest.

| Module | Control (bound bitstream held) | Plant (manifest ident changed) |
|---|---|---|
| Head | passes | `FINDING manifest` |
| `if True:` | refused (`bitstream`) | `FINDING manifest` |
| `have == bound` | refused (`bitstream`) | `FINDING manifest` |
| Lines 175-176 removed | passes | NOT FOUND |

So neither new test is vacuous: each one fails for the defect it is meant to catch.

**The documentation follows the code.**

- `MAILBOX_SPLIT.md:1634-1647` names the control and the new plant.
- "Thirteen" is the 6 `IDENTITY_SOC_PLANTS` plus the 7 file plants, listed one for one.
- The header comment at `test_builder.py:23606-23614` matches the gate.

Acceptance 6 now has a planted negative control for the manifest-versus-image ident mismatch, which was the gap.

### (2) The check IDs

`scripts/check_id_families.sh` lists every ID prefix used in `suite.hpp` and `suite_face.hpp` at the head, at `a91fb27d` and at `1d6bf555`. Its output is `receipts/check_id_families.txt`.

- `U0` is used only at `suite.hpp:153-154`. Its needle at `mutants.py:603` is the same text as the `ck_.dec` label at `:153`.
- `H0` is again only the RX_TAIL guard (`suite.hpp:958-963`, needle `mutants.py:138`).
- No `H0` reference to the head check is left anywhere in the repository. The only other `H0` is `README.md:265`, `rx-tail-unguarded` → H0, which is correct.
- The citations at `README.md:102,164,393`, `MAILBOX_SPLIT.md:137` and `suite.hpp:141` all read U0.
- `F0`-`F2` and `T0`-`T1` are each shared between the two files at all three revisions:
  - F0-F2: the adp channel checks and the face block.
  - T0-T1: the token bucket and the face timing.
- Those pairs are already on `dev-soft-core` `1d6bf555`, and the delta does not touch them. The executor published them as an open question (PR body, "Known limitations"). See S-A.

The executor's receipts, run on a clean clone of the head:

- `gates/mbx-make.log`: WB 546, AXI-Lite 591, cosim 32, WB 2if 553, AXI-Lite 2if 598, model 490, 0 failures, rc 0. Its quick arms include `rx-head-published-one-cycle-early`, failing `U0 ... got=169 exp=0`.
- `gates/mbx-mutants.log`: `mbx mutants: 231 of 231 caught`. That arm and its `-axil` twin fail U0 (`:232-233`).

I did not re-run the bench. The change renames label strings and one needle string, and the label-to-needle grep shows the strings are identical. The round 1 RTL and bench verdicts stand on unchanged code.

### (3) The routed-net wording

`MARK_II_AREA_PLAN.md:971-972` and PR body line 36 carry the ruling's sentence word for word:

> "Every routable net is routed in every directive of every round, none with an error. At the recipe's directive: 66,578 of 66,578, then 66,913 of 66,913, then 67,358 of 67,358 (67,354 and 67,333 at the other two directives in round 3)."

The figures are round 3's published route-status figures, which R827-1 checked. No figure changed.

### (4) S1: the published path headers

`receipts/r4/bus-clock-paths.txt` covers the three directives.

- **Route report** (`report_timing_summary -datasheet -max_paths 10`): 10 setup paths within `milansoc_crg_clkout0`, and 10 into it from `eth_clocks0_rx`.
- **Each slow signoff corner** (`-max_paths 5`): 5 of each. My own tally from the receipt gives exactly those counts for all three directives.
- No line names `KL_mbx/u_rx`.
- The first route-report path of `ExtraPostPlacementOpt` is `rd_off_r` → `reg_rdata_r`, +0.516 ns over 15 levels. This equals the bullet "the worst paths left" at `:1014`.

The doc's new sentence at `MARK_II_AREA_PLAN.md:1011-1012` states exactly what the reports list. It replaces "the 15 worst", a list the reports never gave. A repository grep for "15 worst" is now empty.

Round 3 published hashes for only three of the nine reports (`receipts/author_packet_check.txt`):

- The three Slow_85C signoff reports' hashes equal round 3's published `receipts/r3/route/split-*/alinx_ax7101_signoff_Slow_85C_timing.rpt.sha256`.
- The three route reports and the three Slow_0C reports have no round 3 hash anywhere in the archive. See RES-2.

## Findings

**RES-2: RESIDUE (Docs).** The provenance claim covers 3 of the 9 reports.

- **Where:** the REVIEW READY comment (#870 issuecomment-6799404933), "the report sha256s equal round 3's"; the executor's HANDOFF.md:75 and :82.
- **Evidence:** of the nine reports that `bus-clock-paths.txt` reads, only the three `signoff_Slow_85C` reports have a round 3 published sha256, and those match. The three `alinx_ax7101_timing.rpt` reports and the three `signoff_Slow_0C` reports had none (`receipts/author_packet_check.txt`). Their hashes are published for the first time in round 4.
- **Impact:** wording only. The receipt's own header states each input's hash correctly. No figure, count or verdict changes.
- **Exact fix:** "the three Slow_85C signoff reports' sha256 equal round 3's published hashes; the route and Slow_0C reports' sha256 are published here for the first time".

**RES-1: RESIDUE (Docs).** The PR body names the wrong final line for the builder run.

- **Where:** the PR #889 body, first bullet of "Expected result / pass criteria": "`test_builder.py` prints `ALL GATES PASS`".
- **Evidence:** the run at this head prints `ALL GATES PASS EXCEPT 2 NOT RUN` and exits rc 0 (the tail of `receipts/r4/gates/test-builder.log`).
- **Impact:** wording only. A cold reader may expect the bare line.
- **Exact fix:** "`test_builder.py` exits 0 and prints `ALL GATES PASS EXCEPT 2 NOT RUN` (gate 1b's MAKEFLAGS arm and gate 11's absent mf48 build tree, as in round 3)".

**S-A: SUGGESTION (Tests, Docs).** Some check-ID prefixes are shared, and were shared before this PR.

- **Where:** `tb/verilator/mbx/suite.hpp` (adp F0-F2, token bucket T0-T1) against `tb/verilator/mbx/suite_face.hpp` (face F0-F10, face timing T0-T2), and the README rows "F0 to F10" and "T0 to T2".
- **Evidence:** `receipts/check_id_families.txt` shows the same pairs at `1d6bf555`, `a91fb27d` and `a69fc0f5`.
- **Why this does not hold the PR:**
  - The round 1 F2 findings were about the new `H0`, and that is fixed.
  - Read literally across both files, the ruling's verification sentence would also require renaming these IDs from the base tree.
  - That is outside #870's scope, and AGENTS section 4 makes it new work.
- **Impact:** a `[FAIL] F1 ...` or `T0 ...` line, or a doc that cites one, is ambiguous between two families. This is equally true on `dev-soft-core` today.
- **Outcome:** the manager records the decision the executor asked for, and opens an Issue that gives each family its own prefix.
- **Verification:** `scripts/check_id_families.sh` prints no `SHARED` line.

**S-B: SUGGESTION (Tests).** The manifest-fields rule still has no plant.

- **Where:** `sw/builder/test_builder.py:23669-23711` against `sw/litex/check_image_identity.py:167-171`.
- This was optional in R828-1 F1.
- A plant that drops or adds one manifest key would make the schema rule bite.

**S-C: SUGGESTION (Tests).** Carried from R828-1 S1.

- **Where:** `tb/verilator/mbx/mutants.py:169-170`.
- `axil-rdata-follows-port` is still caught by the needle "F1 record LEN" rather than by A5's own claim.
- Stalling RREADY across a ring read inside A5 would restore that check's own detecting power.

**S-D: SUGGESTION (Docs).** Three byte counts in the executor's packet index are stale.

- **Where:** the executor's packet `receipts/r4/INDEX.md`.

| File | Index bytes | File bytes |
|---|---:|---:|
| `gates/test-builder.log` | 128,783 | 128,763 |
| `sdk-verify.log` | 1,461 | 1,397 |
| `tools/env.sh` | 407 | 399 |

- The other 166 rows match.
- Each of these three files carries path placeholders, which fits redaction after indexing (`receipts/author_packet_check.txt`).
- No claim in this review rests on those counts. The gate 23p results are also in `gate23p-mutants-dev.txt`, whose row matches, and in my own probe.
- **Outcome:** in later packets, regenerate the index after redaction.

**Comment rule, in the reviewed delta: no RESIDUE.**

- The new source comments state behaviour and reason:
  - `test_builder.py:23606-23614`
  - the plant comment at `:23706`
  - the `_identity_file_controls` docstring
  - `suite.hpp:141`
- None shows a bench lane label, a lane name, a review round, a reviewer ID or an issue-comment ID.
- Doc prose that names rounds and rulings (`MARK_II_AREA_PLAN.md`) is allowed.

## Lens results (artifact-specific)

| Lens | Result | Artifacts examined at this head | What was checked |
|---|---|---|---|
| Conformance | PASS | `sw/builder/test_builder.py:23706-23723, 23757-23764`, against #870 acceptance 6 and `sw/litex/check_image_identity.py:165-225`; `receipts/delta_scope.txt` | Every identity mismatch the gate refuses now has a planted negative control; the manifest-ident plant closes the round 1 gap. The bound-bitstream control matches what `milan_soc.py:4964-4966` and `check_image_identity.py:79-88` write. Acceptance 1-5 depend on no file the delta touches, so R828-1's evidence for them stands. |
| RTL | PASS | `receipts/delta_scope.txt` (`git diff a91fb27d a69fc0f5` limited to hdl/, sw/mailbox, sw/litex, configs and recipes is empty); `receipts/r4/bus-clock-paths.txt` | No RTL, generator, contract or routed file changed, so R828-1's RTL lens at `a91fb27d` covers the RTL. The delta's one RTL-adjacent claim, the path listing, holds: no `KL_mbx/u_rx` line, and counts of 10/10 and 5/5 per directive. |
| Robustness | PASS | `check_image_identity.py:175-176` and `:208-225`, exercised by the new plant and control; `receipts/probe_identity_rules.log` | A malformed manifest (an ident copied from another image), the one-bitstream case and the JSON round trip of the binding. The three mutants (comparison always refusing, comparison inverted, ident rule removed) are each detected. Paths the delta does not touch keep R828-1's result. |
| Tests | PASS | `test_builder.py:23704-23771`; `receipts/r4/gate23p-mutants-{dev,base}.txt`; `receipts/probe_identity_rules.log`; `suite.hpp:153-154` and `mutants.py:603`; `receipts/check_id_families.txt`; the executor's `gates/mbx-make.log` and `gates/mbx-mutants.log` | Each new test fails for the defect it claims, and passes at `a91fb27d` where it should not. The needle equals its label. The rename keeps every arm caught (231 of 231, the U0 arm included). No test was weakened. |
| Docs | PASS | `MAILBOX_SPLIT.md:137, 1634-1647`; `MARK_II_AREA_PLAN.md:971-972, 1011-1012`; `tb/verilator/mbx/README.md:102, 164, 265, 393`; the PR body; `receipts/doc_gates.log` | The text matches the code and the receipts, and "15 worst" is removed. The doc style gate passes on 23 documents and the doc path gate on 1086 paths. RES-1 and RES-2 are wording only. |

## Executed in this round

All commands ran in the foreground, in this clone or in the packet's scratch directory.

| What | Result | Receipt |
|---|---|---|
| Delta scope, modes, whitespace, commit shape | Six test and doc files, no protected path, `--check` clean, one-line subjects | `receipts/delta_scope.txt` |
| Identity-rule probe: the head and three mutants held in memory | The control and the plant bite as claimed | `scripts/probe_identity_rules.py`, `receipts/probe_identity_rules.log` |
| Check-ID families at the head, `a91fb27d` and `1d6bf555` | U0 is unique; H0 is only the RX_TAIL guard; F0-F2 and T0-T1 shared since the base | `scripts/check_id_families.sh`, `receipts/check_id_families.txt` |
| `scripts/check_doc_style.py` and `scripts/check_doc_paths.py` | Both OK, rc 0 | `receipts/doc_gates.log` |
| The executor's packet: archive digest, receipt digests, index sizes, hash provenance of S1's inputs | 166 of 169 index rows match (S-D); 3 of 9 report hashes trace to round 3 (RES-2) | `receipts/author_packet_check.txt` |
| Hosted checks at the exact head, read only | See below. None of the failures I opened comes from the delta | `receipts/hosted_checks_a69fc0f5.tsv`, `receipts/hosted_failed_steps.txt` |
| Restore check | HEAD and tree exact; index and worktree identical; no untracked file; gitlinks as at head | `receipts/restore_check.txt` |

Hosted checks at capture time: 15 success, 11 failure, 40 cancelled, 1 skipped and 1 in progress.

- The failures I opened are aggregate gates over cancelled shards.
- `docs-gates-1` failed at "Install diagram gate dependencies" on a DNS error: `Temporary failure resolving 'azure.archive.ubuntu.com'`.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #870 acceptance 6 against `check_image_identity.py:79-88, 165-225`, `milan_soc.py:3003-3022, 4950-4966`, `test_builder.py:23604-23780`; acceptance 1-5 inputs unchanged (`receipts/delta_scope.txt`) | R828-2 | a69fc0f597355a0a200ec5be6bb134b897e97ff5 |
| RTL | CLEAN | The delta has no file in RTL scope (`receipts/delta_scope.txt`). R828-1 covered RTL clean at `a91fb27d`, an ancestor whose RTL nothing has changed since. Path listing `receipts/r4/bus-clock-paths.txt` | R828-1 (RTL); R828-2 (scope confirmation) | a91fb27dd39483e4694e193504da1dbe06208807 (RTL unchanged to a69fc0f597355a0a200ec5be6bb134b897e97ff5) |
| Robustness | CLEAN | The new plant and control on the gate's manifest and bitstream rules; `receipts/probe_identity_rules.log`; the rest unchanged since R828-1 | R828-2 (delta); R828-1 (unchanged scope) | a69fc0f597355a0a200ec5be6bb134b897e97ff5 |
| Tests | CLEAN | Gate 23p in `test_builder.py`; `gate23p-mutants-{dev,base}.txt`; `suite.hpp:141-156`; `mutants.py:138, 603`; `check_id_families.txt`; `gates/mbx-make.log`, `gates/mbx-mutants.log`, `gates/test-builder.log` | R828-2 | a69fc0f597355a0a200ec5be6bb134b897e97ff5 |
| Docs | CLEAN | `MAILBOX_SPLIT.md`, `MARK_II_AREA_PLAN.md`, `tb/verilator/mbx/README.md`, the PR body, the doc style and path gates | R828-2 | a69fc0f597355a0a200ec5be6bb134b897e97ff5 |

## Real limits

- **Gate 23p did not run here.** No interpreter on this host imports migen or LiteX, so its results are the executor's receipts. A direct probe confirmed independently that the two new tests bite, on the rules they target, but it is not the gate itself.
- **The mailbox bench and the mutant campaign were not re-run.** The delta renames only label and needle strings. The counts are the executor's receipts.
- **The packet is unsigned.** The archive commit `460db965` is unsigned according to the commits API, and the packet has no signature file. Its integrity rests on the archive digest recorded in `receipts/author_packet_check.txt`, and on the receipts agreeing with the code.
- **Six of the nine timing reports behind S1 have no round 3 hash** (RES-2). Their agreement with round 3 rests on the matching Slow_85C hashes and the matching worst-path figure.
- **No manager source bank ran at this head**, and none is claimed or inferred. The execution evidence at the source head is the executor's published gate receipts.
- **Not run in this round:**
  - the route, per the ruling;
  - Vivado;
  - the builder bank and the native bank;
  - Docker and act.
- **Physical calibration: NOT RUN.** Field skips are not hardware proof.

## Pending manager duties

- Build and validate the current-dev merge candidate (source base `1d6bf555`, live dev `fa6c094b8e196666a8a8865788d5e83b5bbaea09`). Run the builder and native banks, and link their receipts on the PR.
- Accept the hosted and act checks at the exact head. At capture, these contexts had failed:
  - `verilator-suites`, `yosys-portability`, `elaborate`, `docs-check` and `docs-gates-1`;
  - the six `Union` contexts.
- At the same capture, 40 jobs had been cancelled, and `docs-gates-1` had failed on DNS in its apt step. These contexts need a re-run before they can be accepted.
- Decide the executor's open question on the F0-F2 and T0-T1 ID pairs that predate this PR, and open the Issue for it (S-A).
- Carry RES-1 and RES-2 to the residue checklist.
- Merge still requires two independent positive reviews and the full completion bar of AGENTS section 7.

R828-2 FINISHED
