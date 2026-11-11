[R827] POSITIVE - exact head a69fc0f597355a0a200ec5be6bb134b897e97ff5

# R827-2: internal delta review of PR #889 (issue #870, S9 of #665), round 4

- **Head under review.** `a69fc0f597355a0a200ec5be6bb134b897e97ff5`, tree `bc5cc0e0f7d41e4a8a1aff1a704afc1cc58f5adc`. That is 17 commits on `dev-soft-core` `1d6bf555`.
- **Delta.** `a91fb27d..a69fc0f5`: three commits by the executor under the round 4 ruling (#870 issuecomment-6796161767), which allows tests and docs only.
- **Previously reviewed head.** `a91fb27d`, by R827-1 (issuecomment-6796150573) and R828-1 (issuecomment-6796136305). Both were NEGATIVE, on MINOR findings only.
- **Lenses applied.** All five: Conformance, RTL, Robustness, Tests and Docs. Each one has its evidence below.
- **Verdict: POSITIVE.**
  - No BLOCKER, MAJOR or MINOR finding is open.
  - Every named prior finding is resolved at its cause.
  - Two RESIDUE items and four SUGGESTIONs are recorded for the author and the manager. One SUGGESTION, N1, needs a manager decision on how the ruling's check-ID verification line is worded; the details are under N1.

## Order of reconstruction

1. `AGENTS.md`, then `CONTRIBUTING.md` by reference: the lens, ledger and RESIDUE rules.
2. The round 4 ruling, issuecomment-6796161767. Its items 1 to 5 are the frozen scope of this round.
3. The delta: `git diff --stat a91fb27d a69fc0f5`, `git diff a91fb27d a69fc0f5` and `git log a91fb27d..a69fc0f5`. Then the code the delta depends on: `sw/litex/check_image_identity.py:165-225`, `sw/litex/milan_soc.py:2998-3003` (`soc_ident`) and the `tb/verilator/mbx` check labels.
4. The author packet `review-evidence/665s9-r1/author-r4` at archive commit `460db965`, fetched read-only into a separate bare repository. I read the REVIEW READY text, HANDOFF, `receipts/r4/*` and the round 3 `route_status.rpt` and sha256 files, each by section.
5. My own probes. I ran them only in copies of the clone under the packet's `scratch/`.
6. Only after that independent pass did I read the two round 1 reviews' findings. They are resolved below.
7. Hosted check runs at the exact head, read-only.

## Scope check (ruling: no RTL, generator, contract, SoC, recipe or routed file)

- `git diff --stat a91fb27d a69fc0f5` touches six files: `docs/design/MAILBOX_SPLIT.md`, `docs/design/MARK_II_AREA_PLAN.md`, `sw/builder/test_builder.py`, `tb/verilator/mbx/README.md`, `tb/verilator/mbx/mutants.py` and `tb/verilator/mbx/suite.hpp`.
- Nothing under `hdl/`, `sw/mailbox/`, `sw/litex/` (the SoC and the gate itself), `sw/firmware/`, `sw/builder/endstation_builder.py` or `sw/builder/configs/` changed. No submodule changed either. The author's `r4/delta-inputs.txt` agrees, with a count of 0, and I confirmed it from the clone.
- The route's inputs are therefore those of `a2690e68`, and the route is not re-run, as the ruling directs.

## Focus items

### (1) Gate 23p: the positive control and the manifest-ident plant (ruling item 1; R827-1 F1, R828-1 F1)

**The code**

- **The control** is `sw/builder/test_builder.py:23714-23723`, `_identity_file_controls`.
  - It copies the good split image and writes a fixture bitstream to `gateware/alinx_ax7101.bit`, using `qspi_transition._fake_bit`.
  - It sets the manifest's `bitstream` to `bitstream_binding(bit)`, which is the shape a split `--build` writes.
  - `:23757-23764` runs each control through the CLI and requires exit 0 with no `FINDING`.
  - The good images carry `"bitstream": null`, so before this delta `_bitstream_rules` (`check_image_identity.py:208-225`) never reached `have != bound` on a passing image.
- **The plant** is `:23706-23710`.
  - It sets the manifest's `ident` to `record["ident"].rsplit(" ", 1)[0]` and leaves the image untouched.
  - That value is the all-fabric ident, because `soc_ident` (`milan_soc.py:2998-3003`) appends only `SPLIT_WORD` for a split build. The plant comment "its ident is the all-fabric one" is therefore accurate.
  - The plant must fail with `FINDING manifest:`.
  - No other rule catches it. Schema, VERSION, mailbox, firmware, ident word, bitstream (null), placement and DDR3 all agree, so only `check_image_identity.py:175-176` fires.

**Probes**

I ran gate 23p alone, with `test_builder.py --gates test_image_identity_gate` under a LiteX-capable interpreter, in four fresh copies of the exact head (`tools/probe23p.sh`):

| Arm (planted in `check_image_identity.py`) | Result | Receipt |
|---|---|---|
| none (head) | rc 0. "a bound bitstream the image holds: passes". "the manifest's ident changed: FINDING manifest: the manifest's ident '... baremetal' is not the image's '... baremetal split'". "[gate 23p] the good split and all-fabric images and 1 bound-bitstream control pass ...; 13 planted images each fail it by their kind" | `receipts/gate23p-head.log` |
| `if have != bound:` changed to `if True:` | rc 1, failing on the control: "the gate refused an image that agrees with its identity (exit 1): FINDING bitstream: ..." | `receipts/gate23p-if-true.log` |
| `if have != bound:` changed to `if have == bound:` | rc 1, failing on the control and on "a bitstream other than the one the manifest binds" | `receipts/gate23p-have-eq-bound.log` |
| lines 175-176 removed | rc 1, failing on the plant: "the manifest's ident changed: the gate did not find it by its manifest rule (exit 0)" | `receipts/gate23p-no-manifest-ident.log` |

**What the probes show**

- The control can fail for the defect it targets, and so can the plant.
- The author's base receipt (`r4/gate23p-mutants-base.txt`) shows that `if True:` and the removed rule both passed gate 23p at `a91fb27d`. So both tests are new detection power, not restatements of existing coverage.
- `MAILBOX_SPLIT.md:1635-1647` says "Thirteen planted images" and adds the control. Counted against the code: 6 SoC plants (`IDENTITY_SOC_PLANTS`, `:23621-23634`) plus 7 file plants (`:23682-23710`) make 13. The doc's list names all 13.

### (2) The check ID: U0 (ruling item 2; R827-1 F2, R828-1 F2)

**At the head**

- `suite.hpp:153-154` labels the head-publication checks `U0`.
- `H0` is used only by the RX_TAIL guard, at `suite.hpp:958-963`.
- Every other `U0` reference follows: `mutants.py:603` (the needle), `README.md:102`, `:164` and `:393`, `MAILBOX_SPLIT.md:137` and the comment at `suite.hpp:141`.
- `README.md:265` still says `H0` for `rx-tail-unguarded`, which is correct.
- No other `U0` exists in `tb/verilator/mbx`. The `U0` labels in `tb/verilator/mmcm_servo` and `tb/verilator/reboot_ctrl` belong to other benches.
- Receipt: `receipts/check-ids.txt` (`tools/check_ids.sh`).

**The IDs this PR introduced**

- G1, S0, U0, V0, V1 and W0 each name one check family, and none appears in `suite_face.hpp`.

**The literal verification line**

- The line reads "no two checks in suite.hpp and suite_face.hpp share an ID prefix". It is **not** met.
- F0, F1, F2, T0 and T1 are shared between the adp-channel and token-bucket checks in `suite.hpp` and the face block in `suite_face.hpp`.
- The shared set is identical at `1d6bf555`, at `a91fb27d` and at the head.
- The PR changes 0 lines that carry an F or T label in either file. The README documents both families on dev already, at `:136`, `:152`, `:166` and `:167`.
- The executor published this as an open question rather than renaming the face block's IDs inside this lane. That is the handling `AGENTS.md` section 4 asks for.
- Disposition: see N1.

**`make -C tb/verilator/mbx`**

- I ran it with the pinned Verilator 5.050 (`--version` "Verilator 5.050 2026-07-01 rev v5.050"), in a copy of the exact head: rc 0.
- Tallies: Wishbone 546, AXI4-Lite 591, cosim 32, at 2 interfaces 553 and 598, and the model 490, all with 0 failures.
- Quick mutants: 12 of 12 caught. Among them, `rx-head-published-one-cycle-early` fails "U0 no receive ring word is written under the head the core sees got=169 exp=0".
- The tree was clean afterwards.
- These tallies equal the author's `r4/gates/mbx-make.log`.
- Receipt: `receipts/mbx-make.log`.

**`make mutants`**

- I did not re-run the full campaign; see the limits.
- The author's `r4/gates/mbx-mutants.log` reports 231 of 231 caught, with both the head-publication arm and its `-axil` twin failing on U0.
- The only needle the delta changes is `mutants.py:603`, and my quick run exercised it.

### (3) The routed-nets wording (ruling item 3; R1 of both reviews)

- `MARK_II_AREA_PLAN.md:971-972` and the live PR body both carry the ruling's sentence verbatim. I checked the PR body by an exact substring match; the live body equals the packet's `PR-BODY.md`.
- I checked the figures against the nine published reports, `receipts/{route,r2/route,r3/route}/split-*/alinx_ax7101_route_status.rpt` (`receipts/routed-nets.txt`).
  - At the recipe's directive, `ExtraPostPlacementOpt` (named as the recipe's at `MARK_II_AREA_PLAN.md:977`): 66,578, then 66,913, then 67,358.
  - Round 3's other two directives: `ExtraTimingOpt` 67,354 and `AltSpreadLogic_high` 67,333.
  - In all nine reports, every routable net is fully routed with 0 errors.

### (4) S1: the published path headers (ruling item 4)

- **What was published.** `r4/bus-clock-paths.txt` carries, per round 3 directive:
  - from `alinx_ax7101_timing.rpt` (`-max_paths 10`), the 20 setup paths of group `milansoc_crg_clkout0`: 10 within the bus clock and 10 from `eth_clocks0_rx`;
  - from each slow signoff corner's report (`-max_paths 5`), 10 more paths.
- **`u_rx`.** The file's own count of lines naming `KL_mbx/u_rx` is 0. My grep finds `u_rx` only in that count line.
- **The doc.** The reports do not enumerate "15 worst". `MARK_II_AREA_PLAN.md:1011-1012` now states what they do list, and that text agrees with the file's group headings.
- **The input hashes.**
  - The three `Slow_85C` report sha256s in the file equal round 3's published `.sha256` files: `0a8afabe...`, `eb04c486...` and `7b681e72...`.
  - Round 3 published no sha256 for `alinx_ax7101_timing.rpt` or the `Slow_0C` reports, so those six inputs are named only by this round's receipt. See the limits.
- **S2** was declined by the ruling and moved to #495. It is not graded here.

## Prior findings, resolved or retained at this head

| Prior finding | Lens(es) | Status at `a69fc0f5` | Evidence |
|---|---|---|---|
| R827-1 F1: no positive control for the bound-bitstream branch | Tests | **Resolved** | Focus (1). The control passes, and `if True:` and `have == bound` fail it (my probes) |
| R828-1 F1: no plant for the manifest-ident rule `:175-176` | Tests, Conformance | **Resolved** | Focus (1). The plant fails `FINDING manifest:`, and with `:175-176` removed gate 23p fails (my probe). R828-1's optional fields-rule plant (`:168-170`) is not added; it is retained as SUGGESTION S-a |
| R827-1 F2 / R828-1 F2: the new check reused `H0` | Tests, Docs | **Resolved at its cause** | Focus (2). The new check is U0 everywhere and H0 is the RX_TAIL guard only. The literal "no shared prefix" line still finds the pre-existing F0-F2 and T0-T1, which this PR does not touch: N1 |
| R1 (both reviews): routed-nets wording | Docs | **Resolved** | Focus (3). The sentence is verbatim and the figures match the nine reports |
| R827-1 S1: publish the bus-clock path headers | Docs | **Taken** | Focus (4) |
| R827-1 S2: the FSM's unused codes in `KL_mbx_rx.sv` | RTL, Robustness | **Retained as SUGGESTION** on #495, per the ruling | Not in this round's scope |
| R828-1 S1: A5 no longer detects AXI4-Lite RDATA following the port | Tests | **Retained as SUGGESTION**. The delta does not touch it, and the defect is still caught by F1's record LEN | `mutants.py:167-170` unchanged |

## Findings of this round

### N1 - SUGGESTION - Tests, Docs - `tb/verilator/mbx/suite.hpp` (the F0-F2 and T0-T1 labels) against `tb/verilator/mbx/suite_face.hpp` (F0-F10, T0-T2); `tb/verilator/mbx/README.md:136,152,166,167`

**Authority and evidence**

- The ruling's item 2 has two parts:
  - its action is "Move the new check to an unused ID", and the delta does that;
  - its verification is "no two checks in `suite.hpp` and `suite_face.hpp` share an ID prefix". R827-1 F2 (this reviewer identity's own wording) and R828-1 F2 used the same line.
- `receipts/check-ids.txt` shows the shared set, F0 F1 F2 T0 T1, identical at `1d6bf555`, `a91fb27d` and `a69fc0f5`. The PR's diff changes 0 lines that carry an F or T label.
- So the collision is dev's, from before this lane. It is not introduced, extended or moved by the PR.
- **This reviewer narrows R827-1 F2's verification line to the defect its title and required outcome name.** That defect is the round 2 check reusing H0. It is fixed.

**Why the remainder is a SUGGESTION**

- `AGENTS.md` section 4 says newly discovered work in code the task does not touch becomes another Issue.
- Section 7's "a finding moved to another Issue is not resolved" applies to a defect that is in the lane's work, and this one is not.

**Impact and required outcome**

- Impact: a failure or a document that cites "F1" or "T0" for the mailbox bench is ambiguous between two check families. Grading is unaffected, because the needles use full labels.
- Required outcome: a separate Issue that renames one family, for example the adp-channel or token-bucket IDs, and their README rows. Alternatively, the manager records a ruling that the two families keep their IDs.

**Verification and manager decision**

- Verification: `tools/check_ids.sh` prints `shared:` empty at that Issue's head.
- Manager duty: record whether the ruling's item 2 verification is read as narrowed this way. If the manager reads it literally instead, item 2 is unmet only by IDs this PR does not touch, and that is the manager's call to make publicly.

### N2 - RESIDUE - Docs - `sw/builder/test_builder.py:23727` (gate 23p's docstring)

- **Wording only.** "the identity gate passes the two real images and fails every planted one by its kind" omits the new bound-bitstream control. The header comment at `:23610-23614` and the summary line at `:23774` already name it. The docstring changes no test.
- **Exact fix.** "gate 23p - the identity gate passes the two real images and a copy of the split one that binds its bitstream, and fails every planted one by its kind."

### N3 - RESIDUE - Docs - the PR body, "How to validate", "Expected result" ("`test_builder.py` prints `ALL GATES PASS`")

- **Wording only.** At this head, `--require-rv32` prints `ALL GATES PASS EXCEPT 2 NOT RUN`. The two rows are gate 1b's MAKEFLAGS mutation and gate 11's absent Arty build tree (`r4/gates/test-builder.log`), and the REVIEW READY comment states them correctly. The PR body's Status section says rc 0, which is true, but it does not name the two NOT RUN rows.
- **Exact fix.** "`test_builder.py` prints `ALL GATES PASS`, or `ALL GATES PASS EXCEPT N NOT RUN` with each row named. At `a69fc0f5` that is 2: gate 1b's MAKEFLAGS mutation and gate 11's Arty build tree." Add the same two rows to the Status bullet for `test_builder.py --require-rv32`.

### N4 - SUGGESTION - Docs (evidence) - `review-evidence/665s9-r1/author-r4/receipts/r4/INDEX.md`

- 169 files are indexed and all are present. Three byte counts differ from the published files, by 20, 64 and 8 bytes:
  - `gates/test-builder.log`: 128,783 indexed, 128,763 published;
  - `sdk-verify.log`: 1,461 and 1,397;
  - `tools/env.sh`: 407 and 399.
- They are consistent with path redaction after indexing. The published `test-builder.log` header names a "full log 129546 bytes, sha256 3bc93767..." that is not itself published.
- Optional: regenerate the index after redaction. Also, publish a sha256 per receipt, or say which receipts are redacted excerpts. The packet commit `460db965` is not cryptographically signed. Its integrity rests on the commit id and this index.

### S-a - SUGGESTION - Tests - `sw/litex/check_image_identity.py:168-170` (the schema-fields rule)

- This is R828-1 F1's optional part, retained. No plant adds or removes a manifest field.
- Optional: a plant with one extra field, which must fail with `FINDING manifest:`.

### Comment rule

- Source comments in the delta: `test_builder.py:23610-23614`, `:23706` and `:23715`, and `suite.hpp:141`.
- They state behaviour and reason. None shows a bench lane label, a lane name, a review round, a reviewer ID or an issue-comment ID. **No new RESIDUE.**
- The design docs name rounds and rulings, which the rule allows in docs.

## Lens results (clean lenses, with evidence)

```text
[R827] PASS Conformance - issuecomment-6796161767 items 1-5 against git diff a91fb27d a69fc0f5; test_builder.py:23706-23724,23757-23764; MARK_II_AREA_PLAN.md:971-972,1011-1012; PR #889 body - every ruling item is met: the control and the plant exist and bite (receipts/gate23p-*.log); the new check is U0 (receipts/check-ids.txt); the routed-nets sentence is verbatim in doc and PR text; the S1 headers are published; S2 is deferred to #495 by the ruling; #870 acceptance 6 now has 13 plants and a positive control. Item 2's literal shared-prefix line is unmet only by the pre-existing F0-F2 and T0-T1, which the PR does not touch (N1, a manager decision)
[R827] PASS RTL - git diff --stat a91fb27d a69fc0f5 (6 files, none under hdl/, sw/mailbox/, sw/litex/ or the recipe); author r4/delta-inputs.txt (count 0) - the delta changes no RTL or anything the RTL verdict depends on. R827-1's clean RTL coverage at a91fb27d, whose RTL equals a2690e68, carries to a69fc0f5 unchanged. S2 is retained on #495
[R827] PASS Robustness - check_image_identity.py:208-225 (the bound-bitstream branch) and :175-176, exercised by test_builder.py:23714-23723 and :23706-23710 - the shipping split --build path (a bound and matching bitstream) is now graded positively, and a manifest copied from another image is graded negatively. The probes show an always-refusing or inverted comparison and a missing ident rule are each caught. The RTL's robustness is unchanged (no RTL in the delta)
[R827] PASS Tests - receipts/gate23p-{head,if-true,have-eq-bound,no-manifest-ident}.log; receipts/mbx-make.log (pinned Verilator 5.050); author r4/gates/mbx-mutants.log (231/231); r4/gate23p-mutants-base.txt - each new test fails for the defect it targets, and 2 of the 3 arms were undetected at a91fb27d; U0's quick arm fails on U0; all suite tallies equal the author's; no test is weakened (the diff only adds to gate 23p and renames labels)
[R827] PASS Docs - MAILBOX_SPLIT.md:137,1635-1647; MARK_II_AREA_PLAN.md:971-972,1011-1012; tb/verilator/mbx/README.md:102,164,265,393; mutants.py:603; PR #889 body (equal to the packet's PR-BODY.md) - every changed claim matches the code and receipts: the 13 plants by count, U0 by grep, the net counts against 9 route_status.rpt, and the path lists against r4/bus-clock-paths.txt group headings. Wording residue N2 and N3 only
```

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | ruling issuecomment-6796161767; the delta diff; `test_builder.py:23706-23764`; `MARK_II_AREA_PLAN.md:971-972,1011-1012`; PR body; `receipts/gate23p-*.log`, `check-ids.txt`, `routed-nets.txt` | R827-2 | `a69fc0f597355a0a200ec5be6bb134b897e97ff5` |
| RTL | CLEAN | `git diff --stat a91fb27d a69fc0f5`; author `r4/delta-inputs.txt`; R827-1's RTL coverage at `a91fb27d` (RTL equal to `a2690e68`), which carries because nothing in RTL scope changed | R827-2 (carrying R827-1's RTL result) | `a69fc0f597355a0a200ec5be6bb134b897e97ff5` |
| Robustness | CLEAN | `check_image_identity.py:165-225`; gate 23p control and plant; my four probes | R827-2 | `a69fc0f597355a0a200ec5be6bb134b897e97ff5` |
| Tests | CLEAN | `receipts/gate23p-*.log`; `receipts/mbx-make.log`; author `r4/gates/{mbx-mutants,test-builder}.log`, `r4/gate23p-mutants-{base,dev}.txt` | R827-2 | `a69fc0f597355a0a200ec5be6bb134b897e97ff5` |
| Docs | CLEAN (RESIDUE N2, N3 carried) | `MAILBOX_SPLIT.md:137,1635-1647`; `MARK_II_AREA_PLAN.md:971-972,1011-1012`; `tb/verilator/mbx/README.md:102,164,265,393`; PR body; `r4/bus-clock-paths.txt`; 9 `route_status.rpt` | R827-2 | `a69fc0f597355a0a200ec5be6bb134b897e97ff5` |

## Real limits

**What I did not run**

- I ran gate 23p alone (`--gates test_image_identity_gate`), not the full `test_builder.py --require-rv32`. The author's `r4/gates/test-builder.log` is the full-run evidence: `ALL GATES PASS EXCEPT 2 NOT RUN`, rc 0.
- I did not re-run the full `make mutants` campaign (231 arms). I ran the default `make`, which includes the 12 quick arms and U0's arm, and relied on the author's receipt for the rest.
- I did not run the docs.yml gates. The author's `r4/docsyml/*` receipts report 64 ran, 31 not run with a reason and 0 bad. That includes a first `gate_13` attempt that failed on a missing `wavedrom` and a clean re-run.

**What I could only check in part**

- I could not check the bus-clock path headers against the report bytes.
  - The reports are not published; they are over 200 KB.
  - Only the three `Slow_85C` sha256s are anchored to round 3's own published sha files.
  - The `alinx_ax7101_timing.rpt` and `Slow_0C` inputs are named only by this round's receipt.
- The author packet is an unsigned git commit (`460db965`). I verified it by its commit id, the round-4 index (N4) and spot checks, not by a signature.

**What is not evidence here**

- No manager source bank runs at this exact head, and I claim none. Source-head execution evidence is the author's receipts plus my own probes above.
- No hosted job at this head shows an executed pass.
  - The four workflow runs at `a69fc0f5` all ended `cancelled`.
  - `docs-gates-1` failed at "Install diagram gate dependencies", which is a dependency install, not a gate of the delta.
  - The other failures are aggregator steps after cancellation, for example "Require every gate exactly once".
  - 17 jobs succeeded, among them `verilator-lint`, `split-cdc`, `bdd-conformance`, `docs-check-no-git` and `wire-accountability`.
  - Hosted and act acceptance is the manager's.
- Physical calibration was NOT RUN, and field skips are not hardware proof.

**The clone**

- The clone at `$REVIEWS/r827-2-665s9` was never modified; all probes ran in copies.
- `receipts/clone-integrity.txt`: HEAD and index tree are `bc5cc0e0`, the status is empty, and there is no index or worktree diff.
- The five required submodule gitlinks match. `external` was uninitialised before and after, as at the session's start.

## Pending manager duties

1. **N1.** Record whether ruling item 2's verification is read as narrowed to the IDs this PR introduces or changes. Then open, or rule out, an Issue for the pre-existing F0-F2 and T0-T1 collision.
2. Carry RESIDUE **N2** (the gate 23p docstring) and **N3** (the PR body's expected builder verdict) to the residue checklist.
3. R827-1 S2 goes to #495, per the ruling. R828-1 S1, S-a and N4 are optional.
4. Hosted and act acceptance at the exact head. The current hosted runs are cancelled, with no executed pass.
5. The current-dev merge candidate (source base `1d6bf555`, live dev `fa6c094b8e196666a8a8865788d5e83b5bbaea09`): builder and native banks at the merge turn, with receipts linked on the PR.
6. Physical calibration is NOT RUN. It stays a limit, not proof.

## Publishable files

Every published receipt is listed in `MANIFEST.sha256`: `tools/probe23p.sh`, `tools/mbx_make.sh`, `tools/check_ids.sh`, and `receipts/gate23p-{head,if-true,have-eq-bound,no-manifest-ident}.log`, `mbx-make.log`, `check-ids.txt`, `routed-nets.txt` and `clone-integrity.txt`. Local paths are redacted to `<home>`, `<scratch>` and `<clone>`.

R827-2 FINISHED
