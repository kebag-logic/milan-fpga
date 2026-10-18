[R644] POSITIVE - exact head 26ddcba423a204e75238d737ef41e6cb6e30ebc3

Round R644-2 of the internal independent review, issue #176 / PR #183. Reviewed tree
`c3f5e8f17caa9dcb64093b01b6ac988c11fe9400`. The PR's source base is processor main `77cf6fb4`. The previously
reviewed head is `29f58ad3` (R644-1). The round-2 delta covers three commits:

- `e59804d8`: merge of main `f0b1b9d8`;
- `bee33ff2`: the author's round-2 commit;
- `26ddcba4`: the manager's merge of main `77cf6fb4`.

## Verdict

POSITIVE. No BLOCKER, MAJOR or MINOR finding is open at this head, and all five lenses are CLEAN.

Prior findings:

- R645-1-F1 (MAJOR) is CLOSED.
- R644-1-F1 (MINOR) is CLOSED.
- R644-1-R1 (RESIDUE) is applied.
- R645-1-F2 (RESIDUE) is applied.

Two new RESIDUE items and two SUGGESTIONS follow. None of them affects the verdict.

What was verified at the exact head:

- SET_STREAM_INFO accepts only cdl 60 and cdl 96.
- Every other length gets the same refusal, from cdl 12 up to cdl 500, including 59, 61, 95, 97, 98, 107, 108 and 109:
  - status BAD_ARGUMENTS;
  - a cdl-96 response that is 2021-form: {type, index} over a zero body;
  - no offset write.
- The 2021 ip block (@70..@107) is echoed byte-exact.
- The two new planted mutants fail their named checks.
- The manager merge is the automatic merge except for the one re-recorded digest.
- The GET_AVB_INFO and SET_CONFIGURATION arms are unchanged, and their mutant arms are still killed.

## Reconstruction order followed

1. The processor tree has no AGENTS.md or CONTRIBUTING.md and no gitlinks. I read `README.md` and `docs/README.md`
   (conventions, the citation rule, the single-source rules and the `make check` scope).
2. Issue #176:
   - the body and its frozen "Done when";
   - the owner decision of 2026-10-17;
   - the assignment (6236134563);
   - the ruling on R645-1-F1 (6243713960), which set the round-2 contract: only cdl 60 and 96 are accepted, and every
     other length is refused like a short body (same status, a cdl-96 response, no offset write);
   - the REVIEW READY posts.

   PR #183:
   - the round-2 assignment (6244127636);
   - the R644-2 review start (6248863682);
   - the PR body.
3. Authorities in the tree:
   - `docs/00_MILAN_COMPLIANCE_REVIEW.md:433` (REQ-AEM-009, Milan v1.2 5.4.2.9);
   - `docs/architecture/06_aecp_engine.md` F06.14, §6.3 and §8.1;
   - `docs/architecture/09_verification.md` §8.1 (:184) and §8.11 (:604-616).

   The clause baseline is IEEE 1722.1-2021 7.4.15.1 / Figure 7-40, IEEE 1722.1-2013 Figure 7.46 and Milan v1.2
   5.4.2.9, each at the field offsets these documents give.
4. Diffs: `git diff 77cf6fb4..26ddcba4` (12 files, +288/-76), the round-2 delta `e59804d8..bee33ff2` (10 files), and
   the history.
5. Public evidence: `kebag-logic/milan-fpga@3f760c40:review-evidence/pp176-r1/`.
   - All 204 entries of `MANIFEST.json` match their `published_sha256`, and no file is unlisted.
   - The packet commit carries no Git signature (`verified: false, unsigned`). Its integrity rests on the manifest
     digests alone.
   - I read the `author-r2/` HANDOFF round-2 sections, the probe outputs and script, `mutants/round2/RESULTS.txt` and
     its patches, and `parent-adoption-milan_dp-67.patch`.
6. Prior public findings: I read the R645-1 comment (6243715823) and the R644-1 comment (6244122972) only after my own
   pass over the diff and my probes were done. No other reviewer's round-2 report was read.

## Delta judged

### RTL (`hdl/aecp/KL_aecp_engine.sv`)

- `SI21_CDL_C = 96` (`:812`) and a new discriminator, `si21_w` (`:1569-1572`): SET_STREAM_INFO with exactly cdl 96
  and 84 walked bytes. This mirrors `si13_w` (`:1566-1567`).
- The dispatch route to E_SIBAD (`:3628`) is now `!si13_w && !si21_w`. It replaces
  `!si13_w && (cdl < 96 || pld < 84)`, which let any longer body through to E_SINFO.
- With `echo_r = 0`, E_SIBAD's response length comes from the microprogram's 84-byte stub at A_RUN (`:3767-3772`), so
  every refused length answers at cdl 96.
- The echo-length line (`:3775`) and `si13_pad_w` (`:2584-2586`) are unchanged in logic and still keyed on `si13_w`.
- Only comment lines change elsewhere: `gen_ucode.py` and the comment anchors.
- The generated ROM is byte-identical:
  - base `77cf6fb4` and head both give sha256 `a3b62cab…bcb3` (`results/ucode-rom-sha256.txt`);
  - no non-comment `gen_ucode.py` line changes (`results/merge-check.txt`).
- No register-map, top-level port or parameter change: `SI21_CDL_C` is a module-internal localparam.

### Tests (`tb/pp_top/sim_main.cpp`)

- W24a3 (`:8231-8243`): a 2021 body whose ip block is non-zero, graded byte-exact.
- `w24n_bodies_longer_than_the_2021_body()` (`:8374-8402`), at cdl 97 and cdl 140. Each case:
  - starts from a valid MSRP_ACC_LAT_VALID template with latency 640000 and a non-zero tail;
  - is graded byte-exact against `{type, index}` over 84 zero bytes with BAD_ARGUMENTS (W24n, W24o);
  - checks the offset row (W24n1, W24o1).
- `tb/aecp_cmds/sim_main.cpp:311-313` sweeps the valid templates at cdl 60, 96, 97 and 100, and `decode.json` is
  re-recorded:
  - SINFO, SIRUN, BADARG and NSUPPE appear only at "60, 96", each answering cdl 96;
  - SIBAD appears at "12-59, 61-95, 97-100".

### Docs

- 06 F06.14 (generated), §6.3 and §8.1.
- 09 §8.1 (:184) and §8.11.
- `tb/aecp_cmds/README.md`.
- `tb/pp_top/README.md` M45 and M46, plus the provenance paragraph for the M38-M44 replant.

### Manager merge `26ddcba4`

- `git merge-tree --write-tree bee33ff2 77cf6fb4` gives tree `77d0874e`. That tree differs from `26ddcba4`'s tree only
  by the conflicted engine digest line in `tb/aecp_cmds/decode.json`, which now reads `93f6800f…4778`
  (`results/merge-check.txt`).
- The exact-head `tb/aecp_cmds` run accepts that record: 617,908 trials, 176/176 PASS, rc 0, with the comment-stripped
  input digests matching. So the observed decode is unchanged.
- The PR's engine hunks against `77cf6fb4` sit only in the SET_STREAM_INFO regions. None touches the GET_AVB_INFO or
  SET_CONFIGURATION arms.

## Prior findings, resolved at this head

### R645-1-F1 (MAJOR; Conformance, RTL, Robustness, Tests, Docs): CLOSED

- **Cause.** The old guard routed only lengths below cdl 96 to E_SIBAD, and the echo kept the command's own length.
  Both are gone: `si21_w` requires exactly cdl 96 with 84 walked bytes, and E_SIBAD takes every SET_STREAM_INFO that
  is neither form.
- **Probe at the exact head** (`results/length-probe-head.txt`, my own `scripts/probe_insert_r644.py`). Each command is
  a valid MSRP_ACC_LAT_VALID body on Stream Output 0 with latency 600000 + cdl and a non-zero tail. All 33 rows match
  the ruling:

  | cdl | status | response cdl | body after {type, index} | offset row |
  |---|---|---|---|---|
  | 12, 16, 24, 40, 59 | BAD_ARGUMENTS | 96 | zero | unset |
  | 60 | SUCCESS | 96 | 2013 echo, then zeros | 600060 |
  | 61, 72, 84, 95 | BAD_ARGUMENTS | 96 | zero | 600060 (kept) |
  | 96 | SUCCESS | 96 | byte-exact echo | 600096 |
  | 97, 98, 100, 107, 108, 109, 140, 200, 300, 500 | BAD_ARGUMENTS | 96 | zero | 600096 (kept) |

  At cdl 97 and 140, BAD_ARGUMENTS with the zero stub also wins over three other refusal causes: a Stream Input
  target, an extra flag, and a bit-31 latency. A short body behaves the same way. At cdl 60 and 96 those three causes
  still answer NOT_SUPPORTED, NOT_SUPPORTED and BAD_ARGUMENTS, in the 2021 form.

  The author's probe at `bee33ff2` (`author-r2/probe/head-bee33ff2.txt`) agrees row for row on the eight lengths it
  covers.
- **Upper-bound checks and their mutant.**
  - Exact head: the full `tb/pp_top` run passes 10,519 of 10,519 checks over 7 builds (default 10,017), rc 0
    (`results/pp_top-run-head.txt`). That is the author's 10,506 plus the 13 GET_AVB_INFO checks from `77cf6fb4`.
  - M45 replanted at the exact head (`si21_w` compares `>=`): the default build gives 7 FAIL of 10,017. The failures
    are W24n, W24n1, W24o and W24o1 by name, plus the collateral W24h2, W25b2 and W25b3 (`results/m45-pp_top.txt`).
  - Under M45, `tb/aecp_cmds` fails on AEM 0x000E's recorded BADARG, NSUPPE, SIBAD and SINFO lengths, not only on the
    input digest (`results/m45-aecp_cmds.txt`).
- **Docs.** 06 F06.14, §6.3 and §8.1, 09 §8.1 and §8.11, `aecp_commands.json` and `tb/aecp_cmds/README.md` all state
  the two-length contract. `make check` is rc 0 at the exact head, with 231 of 231 planted command-model defects
  caught (`results/gate-make_check-head.txt`).

### R644-1-F1 (MINOR; Tests): CLOSED

- W24a3 sends a cdl-96 body with `0xC1 + 7*i` across @70..@107 and grades its echo byte-exact. It passes at the exact
  head.
- M46 (`si13_pad_w` keyed on `ssinfo_r`), replanted at the exact head: the default build gives 1 FAIL of 10,017,
  W24a3 by name (`results/m46-pp_top.txt`).
- The row sits beside M38-M44 in `tb/pp_top/README.md:1052`.
- The required verification from R644-1 is met: the default build passes at the new head, and the widened-pad mutant
  fails the new check by name.

### R644-1-R1 (RESIDUE; Docs): APPLIED

`docs/architecture/09_verification.md:184` reads "W24c-W24f, W24h-W24m, W25b, W25b3". No "W24h, W24j" remains in the
tree.

### R645-1-F2 (RESIDUE; Docs): APPLIED

- The engine's new behavioural anchors (`:803`, `:1562`, `:1569`, `:2582`, `:3606-3608`, `:3773-3774`) cite
  `issue #176, REQ-AEM-009`.
- In `tb/pp_top/sim_main.cpp`:
  - the section anchor reads "(issue #176, REQ-AEM-009)" (`:8178`) and "(W24m)" is gone;
  - the banner is the exact required sentence (`:8297-8298`);
  - the W24g/W24g2/W24i-W24l/W24m/W25b3 comment prefixes are removed;
  - the comment says "back to the initial offset".
- Function names, assertion strings and the findings tables are unchanged.

## New findings at this head

### R644-2-R1: RESIDUE (Docs), `tb/pp_top/README.md:1051`

- **Evidence.** The M45 row describes the arm as "(`si21_w` compares `>=`, the dispatch before this row)". "The
  dispatch before this row" has no clear referent: it means the pre-fix dispatch, which accepted any body of at least
  cdl 96.
- **Impact.** Wording only. No measurement, check or verdict changes.
- **Exact fix.** Replace "the dispatch before this row" with "which restores the earlier dispatch that took any body of
  at least cdl 96".
- **Verification.** Read the edited row.

### R644-2-R2: RESIDUE (Docs), PR #183 body, first paragraph ("Branch `176-ssi-2013-body`, three commits on main `f0b1b9d8`")

- **Evidence.** The published head `26ddcba4` also carries the manager's merge of main `77cf6fb4` (PR #182, #177). The
  PR body does not list it. The body's gate tables are correctly dated to `bee33ff2`, so no measurement claim changes.
- **Exact fix.**
  - Replace "three commits on main `f0b1b9d8`:" with "four commits on main `77cf6fb4`:".
  - Append the bullet: "`26ddcba4`: merge of processor main `77cf6fb4` (PR #182, #177 GET_AVB_INFO NOT_IMPLEMENTED).
    Its only conflict was the recorded engine input digest in `tb/aecp_cmds/decode.json`, which was re-recorded; the
    observed decode is unchanged."
- **Verification.** Read the PR body. The PR text is manager-owned.

### R644-2-S1: SUGGESTION (Docs), `tb/pp_top/README.md:1044`

The M38 row names "the short-command route". Since round 2 that route is the wrong-length route (the engine comment at
`:3624` calls it "the wrong-length stub"). Optional rewording: "the `!si13_w` term of the wrong-length route".

### R644-2-S2: SUGGESTION (Tests), `tb/aecp_cmds/sim_main.cpp:313`

- The recorded sweep holds the valid-template refusal only to cdl 100. `tb/pp_top` grades cdl 140, and my probe covers
  cdl 500.
- If the sweep ever gains a longer bucket, the valid template could add one length near the slot limit, so the record
  pins far-oversize refusal too.
- No action is needed for this issue.

## Lens results

### Conformance: CLEAN

- The only accepted lengths are cdl 60 and 96. Both take the same routes in the same order:
  1. Stream Input: NOT_SUPPORTED;
  2. streaming output: STREAM_IS_RUNNING;
  3. flags not exactly MSRP_ACC_LAT_VALID: NOT_SUPPORTED;
  4. bit-31 latency: BAD_ARGUMENTS;
  5. then lock and locate.

  This matches Milan v1.2 5.4.2.9 and REQ-AEM-009.
- Every response is cdl 96 in the 2021 Figure 7-40 form.
- Every other length gets the short-body refusal, as the ruling requires.

Evidence: the probe table above; W24a-W24o and W25b3 passing; decode.json 0x000E.

### RTL: CLEAN

- The delta is two comparator conjunctions and one route condition, all on registered walk fields. No new state, clock
  domain or port.
- `si21_w` and `si13_w` are mutually exclusive by their cdl terms.
- The E_SIBAD response length is microprogram-sized, so it does not depend on the command's length.
- The echo-length and pad logic is unchanged and still confined to `si13_w`.
- The ROM is byte-identical, `lint_hdl.sh` is rc 0 at the exact head, and the merge touches neither the GET_AVB_INFO
  nor the SET_CONFIGURATION arm.

### Robustness: CLEAN

- 33 probe rows from cdl 12 to cdl 500 at the exact head. They include the boundaries 59/61, 95/97, 107/108/109 and
  far-oversize bodies with non-zero tails.
- Combined refusal causes on oversize bodies all take the length refusal.
- No probe row moved the offset, and none produced a response other than cdl 96.

### Tests: CLEAN

- W24a3, W24n, W24n1, W24o and W24o1 are byte-exact or state-exact.
- M45 and M46, replanted at the exact head, fail them by name.
- The `tb/aecp_cmds` record pins the refusal at 61-95 and 97-100 and fails under M45.
- The full `tb/pp_top` run passes 10,519 of 10,519 and `tb/aecp_cmds` passes 176 of 176 at the exact head.
- The dispatch campaign subset at the exact head: control PASS and 15 of 15 arms killed
  (`results/dispatch-mutants-subset-head.txt`). The subset covers:
  - m9-guard-set-stream-info and m9-guard-get-avb-info;
  - the eight gavb-* arms;
  - the five scfg-* arms.

### Docs: CLEAN

- 06, 09, both suite READMEs, the command JSON and the field registry agree with the behaviour.
- `make check` and `gen_matrix.py --check` (94 rows, 0 untested) are rc 0 at the exact head.
- The comment rule is clean in the delta. The added comment lines carry no bench lane label, lane name, review round,
  reviewer ID or issue-comment ID. M-row IDs and W-labels appear only in the README findings tables and in assertion
  strings, and the delta adds no U+2014.
- R644-2-R1 and R644-2-R2 are RESIDUE and do not leave the lens unclean.

## Executed evidence (reviewer-owned, exact head unless stated)

| Execution | Result | Receipt |
|---|---|---|
| Simulator identity | pinned 5.050 wrapper; `--version` prints "Verilator 5.050 2026-07-01 rev v5.050" | this report |
| Length probe, 33 rows | rc 0; every row matches the ruling | `results/length-probe-head.txt` |
| `make -C tb/pp_top run` (7 builds) | 10,519 PASS, 0 FAIL, rc 0 | `results/pp_top-run-head.txt` |
| `make -C tb/aecp_cmds run` | 617,908 trials, 176/176 PASS, rc 0 | `results/aecp_cmds-run-head.txt` |
| M45 planted, pp_top default | 7 FAIL of 10,017 (W24n/n1/o/o1 + W24h2, W25b2, W25b3), rc 1 | `results/m45-pp_top.txt` |
| M45 planted, aecp_cmds | 175/176; decode 0x000E BADARG, NSUPPE, SIBAD and SINFO moved; rc 2 | `results/m45-aecp_cmds.txt` |
| M46 planted, pp_top default | 1 FAIL of 10,017 (W24a3), rc 1 | `results/m46-pp_top.txt` |
| `aecp_dispatch_mutants.py --jobs 4`, 15 arms | control PASS, 15/15 KILLED, rc 0 | `results/dispatch-mutants-subset-head.txt` |
| `make check` | rc 0; 231/231 planted command-model defects caught | `results/gate-make_check-head.txt` |
| `gen_matrix.py --check` / `lint_hdl.sh` | rc 0 / rc 0 | `results/gate-gen_matrix-head.txt`, `results/gate-lint_hdl-head.txt` |
| ROM base `77cf6fb4` vs head | identical sha256 | `results/ucode-rom-sha256.txt` |
| Merge reconstruction | automatic merge plus the one digest line | `results/merge-check.txt` |
| Clone integrity | HEAD and tree exact; 632 blobs and modes match; index equals HEAD; status empty; 0 gitlinks | `results/final-integrity.txt` |

Execution notes:

- Runs used disposable `git archive` extracts under `scratch/`. The verilator `--build -j` was lowered to 4 in the
  copies' Makefiles only, so at most 16 compile jobs ran at once.
- `make check` needs Git metadata, so it ran in a local scratch clone at the exact head.
- Two of my own first attempts are not results:
  - The first probe build segfaulted on my probe's own out-of-range write for 12- and 16-byte payloads. I fixed the
    bounds and reran.
  - The first `make check` ran in an extract without `.git`.

  Both are kept unpublished in `receipts/` as `*-attempt1-*`.
- The review clone was never edited.

## Hosted evidence (inspected, not owned)

Two `hdl` workflow runs exist at `26ddcba4` (`results/hosted-runs.txt`):

- `docs-gates` and `portability` completed with successful execution steps.
- `suites` was still in progress when inspected. Its "Build Verilator v5.050" step is skipped because of the
  cached-compiler path, and a skip is not a test result.

Hosted and act acceptance belongs to the manager.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Engine SET_STREAM_INFO arm, `si13_w`/`si21_w`, E_SIBAD route and A_RUN length. The ruling 6243713960 and REQ-AEM-009 / Milan 5.4.2.9. The 33-row length probe; decode.json 0x000E | R644-2 | 26ddcba423a204e75238d737ef41e6cb6e30ebc3 |
| RTL | CLEAN | `KL_aecp_engine.sv` full PR hunks (`:803-817`, `:1562-1572`, `:2582-2593`, `:3603-3631`, `:3724-3730`, `:3773-3775`). `gen_ucode.py` comment-only; ROM identical; lint rc 0. Merge tree vs automatic merge; GET_AVB_INFO and SET_CONFIGURATION arms untouched | R644-2 | 26ddcba423a204e75238d737ef41e6cb6e30ebc3 |
| Robustness | CLEAN | cdl 12-500 probe including the 59/61, 95/97 and 107-109 boundaries. Oversize bodies with Stream Input, extra-flag and bit-31 causes. Offset row on every refusal | R644-2 | 26ddcba423a204e75238d737ef41e6cb6e30ebc3 |
| Tests | CLEAN | W24a3, W24n/n1/o/o1 and the existing W24/W25 rows. M45 and M46 replanted; the aecp_cmds record under M45. Full pp_top run (10,519) and aecp_cmds (176). Dispatch mutant subset, 15/15 | R644-2 | 26ddcba423a204e75238d737ef41e6cb6e30ebc3 |
| Docs | CLEAN (R644-2-R1, R644-2-R2 RESIDUE carried) | 06 F06.14, §6.3 and §8.1. 09 §8.1 and §8.11. `tb/aecp_cmds/README.md`, `tb/pp_top/README.md` M38-M46. `aecp_commands.json`, `aecp_fields.json`, `check_aecp_commands.py`. Delta comment rule; PR body; `make check` and `gen_matrix --check` | R644-2 | 26ddcba423a204e75238d737ef41e6cb6e30ebc3 |

## Real limits

- I did not obtain the specification PDFs. Clause claims rest on the offsets and wording recorded in the tree's
  authorities and in the ruling.
- I did not run the full processor bank (`run_suites.sh`), Yosys, any parent bank or milan_dp.
- For the following, I rely on the author's published receipts at `bee33ff2`, not at this head, as published hashes
  and summaries:
  - the processor gates other than those listed above;
  - the other mutant campaigns (acmp, notify, d3, gsi, elab_guards, adp/maap/name_state);
  - the parent consumer gates.
- No source bank was run by the manager at this exact head, and I claim or infer none.
- I did not check the parent `#67` patch against the parent tree in this round. The patch is byte-identical to the
  round-1 patch, and round 2 changes neither of the 2013 or 2021 answers that its two rows send.
- I did not run stall or reset permutations of the length gate, or a separate lock-holder test of the oversize refusal.
  The route is a dispatch-time constant, and it sits before lock and locate.
- Physical calibration is NOT RUN, and field skips are not hardware proof.

## Pending manager duties

- Build and validate the current-dev merge candidate at the merge turn (source base `77cf6fb4`, live dev
  `e9cbb676…`), and publish its builder and native bank receipts on the PR.
- The pin adoption needs three parent items, each tracked separately:
  - the parent `milan_dp` section #67 two-row patch, the only parent change this PR needs;
  - the evidence classification of the three earlier processor-main readers, from PR #180;
  - the pin documentation for `check_submodule_docs`.
- At the new pin, rerun the parent consumer gates, including whatever `77cf6fb4` (#177) itself needs at the parent.
- Carry R644-2-R1 and R644-2-R2 to the residue checklist. R645-1's note about two stale parent comments
  (`tests/steps/aecp_engine_steps.py:186`, `tb/verilator/milan_dp/sim_nxn.cpp:6862`) also belongs to the adoption.
- Accept the hosted and act runs at the exact head after the `suites` job completes.

## Reproduction

```sh
scripts/extract.sh <processor-clone> 26ddcba423a204e75238d737ef41e6cb6e30ebc3 <dir>
python3 -I scripts/probe_insert_r644.py <dir>/tb/pp_top/sim_main.cpp
make -C <dir>/tb/pp_top gsi-build VERILATOR=<pinned 5.050> && (cd <dir>/tb/pp_top && ./obj_dir/Vpp_top_sim)
(cd <m45-dir> && patch -p1 < scripts/sinfo-upper-bound-reopened.patch)   # then gsi-build + run, and tb/aecp_cmds run
(cd <m46-dir> && patch -p1 < scripts/sinfo13-pad-every-sinfo.patch)     # then gsi-build + run
scripts/audit_checkout.sh <processor-clone> 26ddcba4... c3f5e8f1...
```

`scripts/run_bg.sh` wraps each run with its own log and rc file. `MANIFEST.sha256` lists every published file other
than this report.

R644-2 FINISHED
