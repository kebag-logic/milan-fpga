[R602] POSITIVE - exact head c7d0ad63510cf1aaee41ef440675d110ad2730d7

# R602-6: internal cleared-context review of PR #715 (#671), round 6

- Head under review: `c7d0ad63510cf1aaee41ef440675d110ad2730d7`, tree `06f494ec738a0c0eb0147a22b7b57c3545f5d6f9`. This is a delta review of two commits on `0c276b62` (`793641131` host suite, `c7d0ad635` docs), read alongside the full diff from source base `e8454e2751d05b02ee8e5a571857589ab358ab86`.
- Assignment: the [round-6 ruling](https://github.com/kebag-logic/milan-fpga/issues/671#issuecomment-6112358549), which answers [R602-5](https://github.com/kebag-logic/milan-fpga/pull/715#issuecomment-6112353068) and [R603-5](https://github.com/kebag-logic/milan-fpga/pull/715#issuecomment-6112253974). It requires one fault class and one removal control for each comparison term, both derived from one term list.
- Order of reading:
  1. AGENTS.md and CONTRIBUTING.md (sections 3 and 6).
  2. docs/README.md.
  3. The #671 body, the lane assignment and the round-5 and round-6 manager rulings, then the author's round-6 REVIEW READY.
  4. FASTCONNECT section 7, the BAREMETAL_FIRMWARE saved-state and host-suite text, and the host-suite README.
  5. The delta and full diffs and their history.
- Independence:
  - I wrote my verdict and ledger to `receipts/independent_pass_ledger.txt` (2026-10-11T20:44:09Z) before reading any prior review finding or probe on this PR.
  - Only then did I read R602-5 and R603-5 and fetch their published probes.
  - I read no private author material and nothing from the management workspace.

## Verdict

**POSITIVE.** No BLOCKER, MAJOR or MINOR is open. One RESIDUE is filed (README wording only), and two earlier SUGGESTIONs are retained as optional.

At this head, every item of the round-6 ruling holds, checked by execution:

1. **Terms listed once.** `read_fault_cases.py:24-27` defines `COMPARISON` as (verdict, byte count, prefix CRC, trailer). Each entry gives the firmware's spelling and the manner of fault. The following are all generated from it:
   - the term classes (`term_class`, `:299`);
   - the four `r_omit_` controls (`:145`, via `control_of` and `alone_in`, `:32-38`);
   - the findings' wording (`judged`);
   - the comparison check (`comparison_findings`, `:323`).

   The check requires the firmware's `nvm_reads_agree` (`milan_baremetal.c:776-779`) to compare by exactly the listed terms (`probe_check.log`).
2. **One class per term, differing in that term alone.** A probe build of the shipped firmware prints each read's four terms (`probe_terms.py`). Across all 384 class cases (3 shapes × 4 terms × 32), the faulted slot's judgement is two refusals that differ in their own term only, then a VD_OK read. That is 0 deviations. Example on arty 4x4 (`probe_terms.json`):
   - verdict: VD_ENT then VD_SHAPE, with equal bytes, prefix CRC and trailer;
   - byte count: 0x12cc then 0x12d0, with equal prefix CRC and trailer;
   - prefix CRC: two digests, with an equal trailer;
   - trailer: 0xa1a68731 then 0xa0a68731, with an equal prefix CRC.

   Each term has 32 cases:
   - 16 cold boots and 16 writer restarts;
   - both orientations;
   - sequences 1, 0x5A5A5, 0x80000000 and 0xFFFFFFFF with the other slot blank;
   - both-valid 0x5A5A5 and the wrap, with the newer or the older slot faulted.

   Every case goes through the gate's own `grade_fault_case`, so it keeps the exact read-count, hold, window, changed-record and other-record assertions.
3. **One control per term, rejected by its own diagnostic on three shapes.** In full count over the 128 class cases per shape (`probe_controls.log`), each of `r_omit_verdict`, `r_omit_byte_count`, `r_omit_prefix_crc` and `r_omit_trailer` is caught by 32 of 32 cases of its own class, with its own words. It is caught by 0 cases of the other three classes. This holds on `endstation_arty_4x4`, `endstation_ax7101_1x1_tdm8` and `endstation_ax7101_8x8`. The shipped firmware gives 0 findings on the same 384 cases. I also wrote five variants of my own that break a term's computation rather than its comparison:
   - tail read 4 bytes early;
   - digest 4 bytes short;
   - digest over the header only;
   - verdict compared by blank/non-blank class;
   - byte count compared by non-zero.

   Each is caught 32 of 32 by the right class on all three shapes, and by no other class.
4. **A missing class or control fails a check.** The gate's self-test fails the check by name in 9 arms (`gate_selftest.log`). Beyond those arms, `probe_check.py` makes it fail when:
   - a single place is removed for any term;
   - a class case's window is moved off the judgement;
   - the function is renamed;
   - a term is dropped;
   - the terms are reordered;
   - `&&` becomes `||`;
   - a control's plant is not the term removed.

   That is 21 of 21 assertions.
5. **Production comparison unchanged.** `git diff --quiet 0c276b62 HEAD -- sw/firmware/milan_baremetal tb/verilator/nvm_capture_cpu` holds. The firmware sha256 is `497845e6243b919638285ce4de18e6687beff6a509d72c8e2e2f2d45ba7b1bed` (`delta_facts.log`). No STOP was due, and capture and size are not re-owed.
6. **Prior probes now produce named findings on three shapes.**
   - R603-5's `probe_comparison.py` (published blob `7ada1dd7`): rc 0, with its own assertions. The omission plant gives **78 standing findings per shape**, 32 of which name the trailer class (32 distinct cases), on all three shapes (`r603_5_probe_comparison.log`, `prior_probe_named_counts.log`).
   - R602-5's `probe_r602_5.py --mutants no_tail,digest_short --sets none --standing` (published blob `9b8b38db`): **78 findings per shape for each plant**, on all three shapes. Named lines read "which differ only in their trailer" or "... prefix CRC" (`r602_5_probe_standing.log`).

## Findings

### R602-6-R1 - RESIDUE - Docs - `sw/firmware/nvm_hosttest/README.md:165-168` - the term-class sentence's parenthetical names only the blank-other sequences

- **Evidence.** The text reads: "Each class runs at every sequence of each group whose faulted slot holds a container (1, 0x5A5A5, 0x80000000 and 0xFFFFFFFF with the other slot blank), both ways round and on both entry paths: 32 cases per term."
  - The 32 cases per term also include the both-valid layouts: 0x5A5A5 and the wrap, with the newer or the older slot faulted (`term_class` over `GROUPS`; counted in `probe_check.log` and `probe_terms.log`).
  - From the parenthetical alone, a reader computes 16.
  - The PR body states the both-valid layouts correctly.
- **Why RESIDUE.** The main clause, the figure 32, the code, the tests and every measurement are correct. Only the example list is incomplete. This is purely wording.
- **Exact fix.** Replace the parenthetical with "(1, 0x5A5A5, 0x80000000 and 0xFFFFFFFF with the other slot blank, and 0x5A5A5 and the wrap with both slots valid, the newer or the older one faulted)".

### Retained SUGGESTIONs (optional, not blocking)

- **R602-4-S1** (Tests): the boot line's `read faults=` count is still not graded numerically.
- **R602-4-S2** (Tests, Robustness): still no generated case faults both slots in one boot.

## Lens results

`[R602] PASS Conformance - read_fault_cases.py:24-27,145,299-371 and milan_baremetal.c:742-779 at c7d0ad63 against the round-6 ruling items and #671 Required/Acceptance 1-3; receipts/probe_terms.json, probe_controls.log, probe_check.log, delta_facts.log, gate_selftest.log`

- **Acceptance 1 and 2.** The unchanged firmware meets them. This is re-proven at this head by the full gate:
  - rc 0 on five shapes at 3,550 cases each;
  - all 18 #671 controls caught by name on three shapes, including `restart_at_zero`.
- **Acceptance 3** (A/B power-loss guarantees). The write path is unchanged, and the co-simulation passes 465/465.
- **Ruling items** are met as stated under Verdict. The production comparison is byte-identical.
- **Terms differing alone.** That each class's two refusals differ in their own term only is measured on every class case, not taken from the model.

`[R602] PASS RTL - git diff --name-only e8454e27..c7d0ad63 over hdl, protocol-processor, gptp-processor, syn, constraints, third_party, external, .gitmodules, .github (empty, delta_facts.log); nvm_host.c:584-698 (host-model C); receipts/cosim.log; receipts/integrity_final.log`

- **No RTL in scope.** There is no RTL, gitlink, register-map, record-format or workflow change anywhere in the PR. The delta's C change is in the host model only.
- **`forge_crc` (`:584`).** It undoes 32 reflected-CRC shifts and XORs with the register before the four bytes, a correct construction. Measurements confirm it: the forged reads print the intended prefix-CRC values (`probe_terms.json`).
- **`fault_slot` (`:603`).**
  - Before any length-relative fault, it guards `len` in [48, 0x10000], `-off <= len` and `grown <= 0x10000`. Otherwise it exits 2, so a harness error never passes as a fault.
  - The forge offset `len-8` is at least 40, so header words are never overwritten.
  - The view is re-copied from flash before every faulty read (`:651-657`), so RF_LEN cannot compound across reads. The measured byte counts len+4 and len+8 confirm this.
- **`arm_read_fault`.** It moves to signed parsing, rejects a negative SKIP or COUNT, and bounds OFF to (-0x10000, 0x10000).
- **Co-simulation.** It imports the changed `test_nvm_firmware.py`, so I ran it here under the scoped simulator 5.050, after verifying the wrapper (sha256 `905795b99e0a8803383b198b118bafcbd87d20b877e3f09c39c31ea81979e92f`). Result: "465 checks: 465 PASS, 0 FAIL", "39 of 39 mutant(s) killed by their named check", rc 0, 384 s.

`[R602] PASS Robustness - read_fault_cases.py:299-348 (term_class, term_of, comparison_findings), nvm_host.c:603-635 at c7d0ad63; receipts/probe_check.log (21/21), probe_controls.log (reviewer variants), probe_terms.json`

The check fails closed in each of these cases:
- the comparison function is renamed or not found ("nothing found");
- the comparison is reordered, a term is dropped, or `||` replaces `&&`;
- a single sequence, orientation or entry-path place is missing;
- a class case's window does not open the judgement (the model's "ffc" is required);
- a control's text is not the term removed.

The classes catch a broken term computation, not only a missing comparison term: the five reviewer variants were each caught by the right class on three shapes. The harness's malformed-length guards are covered under RTL. The existing groups, windows, sealed class, hold, wipe and retire paths are unchanged and green in the gate.

`[R602] PASS Tests - test_nvm_firmware.py:969-990, read_fault_cases.py:140-146,350-371 at c7d0ad63; receipts/gate_selftest.log (rc 0, 180 s at --jobs 8), probe_controls.log, r603_5_probe_comparison.log, r602_5_probe_standing.log`

- **Gate self-test.**
  - "saved-state writer gate: OK across 5 shape(s), and every planted defect reddened".
  - 61 firmware plants were caught: 5 writer controls, 18 #671 controls × 3 shapes, and 2 boot-walk controls.
  - The 9 comparison-check arms failed by name. The disabled-writer mutant and the 4 PHY mutants were caught.
- **New controls.** Each can fail for the defect it names, as the full-count 32/0 isolation above shows. Both prior reviewers' plants now redden the standing suite.
- **The 14 earlier #671 controls** are still caught by name on all three shapes. `r_fill_from_flash` is now first caught by a `--read-verdict` case, still by its own words ("want exactly").
- **Harness equivalence.** The refactored `fault_slot` keeps the RF_XOR, RF_SEAL, RF_FF and RF_OTHER behaviour by construction: the same XOR value, the same seal, the same fill and the same copy. I did not repeat the author's 10,641-run twin campaign.

`[R602] PASS Docs - docs/design/SAVED_STATE_FASTCONNECT.md:128,800; docs/integration/BAREMETAL_FIRMWARE.md:2033-2036,2187-2197; sw/firmware/nvm_hosttest/README.md:12,55-67,154-183,209-267; test_nvm_firmware.py module docstring; PR body Round 6 at c7d0ad63; receipts/docs_check.log, probe_check.log, gate_selftest.log`

- **Counts.** These match the generator and the transcript:
  - twenty-three planted writer defects, eighteen #671;
  - 3,550 of 3,636 cases, 1,839 cold, 1,711 restart, 128 term-class cases;
  - 32 cases per term;
  - 9 comparison-check arms;
  - the PR body's 61 plants.
- **Fault descriptions.** The `--read-length` and `--read-verdict` descriptions match the measured verdicts and byte counts.
- **Other checks.** No stale "nineteen", "fourteen #671" or "3,422" remains in any page. `docs_check.py` returns rc 0 with 0 findings, scrub 23/23. No added line contains U+2014.
- **Not run here.** The pinned-renderer contents check is not installed in this clone. I did not install it, so its result rests on the hosted `docs-check`, which was still running at my last poll.
- **RESIDUE.** R602-6-R1 is wording only and leaves the lens clean.

## Completion ledger (reviewer-owned)

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `read_fault_cases.py:24-27,145,299-371`; `milan_baremetal.c:742-779` (byte-identical to `0c276b62`); #671 acceptance 1-3; round-6 ruling items; `probe_terms.json`, `probe_controls.log`, `probe_check.log`, `gate_selftest.log`, `delta_facts.log` | R602-6 | `c7d0ad63510cf1aaee41ef440675d110ad2730d7` |
| RTL | CLEAN | empty RTL/infra name-only diff since `e8454e27`; `nvm_host.c:584-698`; `cosim.log` (465/465, 39/39); `integrity_final.log` | R602-6 | `c7d0ad63510cf1aaee41ef440675d110ad2730d7` |
| Robustness | CLEAN | `term_class`, `term_of`, `comparison_findings`; `fault_slot` guards; `probe_check.log` (21/21); reviewer variants in `probe_controls.log` | R602-6 | `c7d0ad63510cf1aaee41ef440675d110ad2730d7` |
| Tests | CLEAN | `test_nvm_firmware.py:969-990`; `read_fault_cases.py:140-146,350-371`; `gate_selftest.log`; `probe_controls.log`; `r603_5_probe_comparison.log`; `r602_5_probe_standing.log`; `prior_probe_named_counts.log` | R602-6 | `c7d0ad63510cf1aaee41ef440675d110ad2730d7` |
| Docs | CLEAN (RESIDUE R602-6-R1 carried) | FASTCONNECT `:128,800`; BAREMETAL_FIRMWARE `:2033-2036,2187-2197`; host README; gate docstring; PR body Round 6; `docs_check.log` | R602-6 | `c7d0ad63510cf1aaee41ef440675d110ad2730d7` |

## Prior public findings: disposition at this head

| Prior IDs | Disposition | Evidence at this head |
|---|---|---|
| R602-5-F1 (MAJOR), R603-5-F1 (MAJOR) | RESOLVED | The trailer and the bytes before it (prefix CRC) now have standing classes. `no_tail` and `digest_short` give 78 named standing findings per shape. `r_omit_trailer` and `r_omit_prefix_crc` are caught by their own words on three shapes. Term isolation is measured over 384/384 cases. The ruling's widening to all four terms holds as well. |
| R603-4-F1 (MAJOR) | RESOLVED (unchanged) | `r_digest_with_trailer` is caught by name on three shapes (`gate_selftest.log`). In R603-5's probe, `inclusive_crc` fails 32 of 48 focused (sealed) cases per shape, and the head fails none. |
| R602-4-S1, R602-4-S2 | RETAINED, optional | Not taken up. |
| R602-3-F1 / R603-3-F1, R602-3-F2, R603-3-S1, R602-3-S1; R603-2-F1 / R602-2-F1, R603-2-S1, R603-2-S2, R603-2-R1, R602-2-S1, R602-2-R1; R603-1-F1, R603-1-F2, R603-1-S1 to S3, R603-1-R1; R602-1-F1, R602-1-S1 to S3, R602-1-R1 to R4 | RESOLVED (unchanged since the round-5 dispositions) | Round 6 does not touch the firmware or their docs. Their controls are all still caught by name on three shapes in `gate_selftest.log`. |
| R603-2-OBS-1 / R602-2-S2 (prefill) | RETAINED OUTSIDE SCOPE | It is #717. |

## Execution receipts (this packet)

| Run | Result | Receipt |
|---|---|---|
| `test_nvm_firmware.py --self-test --jobs 8` | rc 0, 180 s, 5 shapes, 61 plants plus 9 comparison arms | `receipts/gate_selftest.log`, `.rc`, `.secs` |
| `probe_terms.py REPO WORK --part terms --jobs 8` | rc 0; all 384 class judgements differ in their own term only | `receipts/probe_terms.log`, `.rc`, `probe_terms.json` |
| `probe_terms.py REPO WORK --part controls --jobs 8` | rc 0, 4 controls with 32/0 isolation, 5 reviewer variants caught, shipped 0, on all 3 shapes | `receipts/probe_controls.log`, `.rc`, `.secs`, `probe_controls.json` |
| `probe_check.py REPO` | rc 0, 21/21 | `receipts/probe_check.log`, `.rc` |
| R603-5 `probe_comparison.py REPO --jobs 8` | rc 0, omission gives 78 standing findings per shape, 32 naming the trailer | `receipts/r603_5_probe_comparison.log`, `.json`, `.rc`, `.secs`; `prior_probe_named_counts.log`; `prior_probe_provenance.txt` |
| R602-5 `probe_r602_5.py REPO WORK --jobs 8 --mutants no_tail,digest_short --sets none --standing` | rc 0, 78 findings per shape per plant | `receipts/r602_5_probe_standing.log`, `.rc`, `.secs` |
| `make -C tb/verilator/nvm_cosim run JOBS=8 POOL=8` (scoped simulator 5.050) | rc 0, 465/465, 39/39 | `receipts/cosim.log`, `.rc`, `.secs`, `cosim_tool.log` |
| `scripts/docs_check.py` | rc 0, 0 findings | `receipts/docs_check.log` |
| `verify_clone.py REPO c7d0ad63...` | rc 0, see the line after this table | `receipts/integrity_final.log` |

The final integrity check covers 1,272 parent blobs with their index records, kinds and modes, and the registered submodules at their gitlinks:
- processor `2ad2f845`: 562 files;
- time-synchronization processor `5dce647a`: 104 files;
- stream library `48ff7a7e`: 213 regular files.

Two unused submodules are uninitialised. Nothing is untracked or ignored, because every cache and build product the runs created was removed first.

Absolute host paths in the two co-simulation logs were replaced with placeholders before publication (`receipts/SANITISATION.txt`). No other receipt carried any.

**Probe-run correction.** My first `--part terms` run reported 48 deviations per shape (`receipts/probe_terms_run1_window_artifact.log`, rc 1). These came from my own probe, not the product. When the faulted slot is judged last and picked, its re-stage read follows its judgement directly, and my window included that read. Every one of the 144 lines has exactly that shape. I ended the judgement window at its first VD_OK read and re-ran; that run is the cited result.

## Hosted evidence at this head (read-only snapshot, manager-owned)

`receipts/hosted_summary.txt` and `hosted_checkruns_final.json` hold the snapshot taken at 2026-10-11T21:14:44Z. Of 21 check runs:
- **Success (15):** `full-ci-gate`, `changes`, `bdd-conformance`, `verilator-lint`, `wire-accountability`, `docs-check-no-git`, `yosys-elaboration`, `firmware-unit`, `elaborate`, `rtl-fast`, Yosys shards 0-3, Verilator shard 3/5.
- **Skipped (1):** `Physical gPTP (nightly and manual)`. A skip is not hardware evidence.
- **Still in progress (5):** `docs-check` (it holds the builder's writer gate), Verilator shards 0, 1, 2 and 4.

None had failed. The PR is not a draft, and its head is this commit. Hosted and local-replica acceptance belong to the manager.

## Limits

- **Physical calibration NOT RUN.** No hardware was used. Field skips, the host model and the co-simulation are not hardware proof.
- **Constructed faults.** The verdict and byte-count classes are constructed CRC-32 collisions in the host model, as the PR states. They pin the comparison terms; they make no claim about field fault rates.
- **Host toolchain.** CPython 3.14.7 and host GCC 16.2.1, on a shared host. The wall times are not comparable to the hosted limits.
- **Not reproduced here:**
  - the builder bank and the firmware-unit/Mark II suites (no delta input);
  - the 10,641-run twin equivalence campaign;
  - capture and size, which are not re-owed because the firmware is byte-identical;
  - R602-5's trailer and sealed-alternative sets;
  - the pinned-renderer contents check.
- **Source banks.** No manager source bank runs at this exact head, and none is claimed or inferred. Source-head execution evidence is the author's published receipts plus this packet's focused runs.

## Pending manager duties

- Carry RESIDUE R602-6-R1 to the residue checklist.
- Accept the hosted evidence once the five in-progress contexts finish, and the local-replica evidence.
- File the Mark II (`sw/firmware/ctrl_nvm`) refusal-comparison collapse as its own Issue, as round 5 item 2 ruled, if not yet filed.
- At the merge turn, validate the current-dev merge candidate: source base `e8454e27`, live dev `cfadd767a7ad47aaee68de655e1066cc000fb8a0`, with the builder and native banks. Link its receipts.
- Merge still requires:
  - the external independent positive at this head;
  - clean five-lens coverage at the merge head;
  - no review in flight;
  - explicit maintainer merge authorization;
  - post-merge containment and Issue/Project completion.

  This report does not authorize a merge.

Only `REPORT.md` and the files listed in `MANIFEST.sha256` are for publication; `scratch/` is not.

R602-6 FINISHED
