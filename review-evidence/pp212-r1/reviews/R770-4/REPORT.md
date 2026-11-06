[R770] POSITIVE - exact head 6162885ffee5d8e8897732be6479982b8dceaec9

# R770-4: external independent review of PR #213 (issue #212), round 4

- **Head:** `6162885ffee5d8e8897732be6479982b8dceaec9`, tree `16b9d3fa90901d34a1225ae6821b693218431061`. Both were checked in the detached clone before and after the probes.
- **Delta judged:** `834cc88..6162885`. It is one commit, two blobs, 7 insertions and 4 deletions (`receipts/delta-raw.txt`, `receipts/delta.diff`). The delta's sha256 equals the author's published `round4.diff`: `85c571f2…f3be3f`.
- **Scope (round 4 assignment, issue comment 6676602877):** split each multi-declarator declaration this PR added, one declarator per statement, Rule 11, and change nothing else. Then run the gates: `tb/pp_top` and `tb/srp_stream_fsms` at full count; the parent's `scripts/check_cpp_idiom.py` with this gitlink, rc 0 and 0 for the rule; `git diff --check`.
- **Rest of the PR:** the delta touches no HDL, documentation, README, mutant patch, campaign driver or build file. The round-3 lens verdicts (both POSITIVE at `834cc88`) carry for everything outside the two test-bench blobs.

## Verdict

**POSITIVE.** No BLOCKER, MAJOR or MINOR finding is open at this head.

- The three splits keep behaviour. Types, initial values and the values the check reads are all unchanged. A byte-level rebuild proves that no other line changed.
- Both suites keep their full counts on the pinned Verilator 5.050: pp_top 11,064 of 11,064 and srp_stream_fsms 1,512 of 1,512.
- With this head as the gitlink on a scratch parent at live dev `cc204c6f`, the parent's `check_cpp_idiom.py` returns rc 0, `multi-declarator declaration: 0 <= 0`. The round-3 pin still refuses it with "3 > ratchet 0", which reproduces the gate failure the round answers.

The report records one new SUGGESTION. Two RESIDUE items from my round 3 are retained, because the delta was barred from touching them. The prior SUGGESTIONs are carried.

## What was checked, and how

### 1. The split is behaviour-identical (Conformance, Tests)

| Site at head | Before (`834cc88`) | After (`6162885`) | Equivalence |
|---|---|---|---|
| `tb/pp_top/sim_main.cpp:10619-10620` (`listener_is`) | `int e = -1, q = -1;` | `int e = -1;` / `int q = -1;` | Same type (`int`), same initialisers (-1). Both are still lvalues bound to `listener_value(..., int& ev, int& fp)` (`:10584-10585`). |
| `tb/pp_top/sim_main.cpp:10625-10626` (`listener_any`) | `int e = -1, q = -1;` | `int e = -1;` / `int q = -1;` | Same as above. |
| `tb/srp_stream_fsms/sim_main.cpp:2895-2896, :2899` (PS12) | `const int sinks[] = {0, 3};`, read as `sinks[0]`, `sinks[1]` | `const int sink_a = 0;`, `const int sink_b = 3;`, read as `sink_a`, `sink_b` | Element type `const int` is unchanged. The values 0 and 3 are unchanged. They are the only two reads, both arguments of `l_decl(int s)` (`:325`). No other use of `sinks[` existed or remains, and the new names are used only at `:2899`. |

- **Byte-level rebuild** (`scripts/delta_equiv.py`, `receipts/delta-equiv.log`, PASS): the round-3 blobs, with only these three textual substitutions applied (each found exactly the expected number of times), are byte-equal to the round-4 blobs.
- **Clean build:** neither file draws a compiler warning under `-Wall -Wextra` in either build (`receipts/pp_top-r4.log`, `receipts/srp_stream_fsms-r4.log`).
- **`git diff --check 834cc88 6162885`:** rc 0 (`receipts/diff-check.txt`).
- **Mutation probe, Tests:** the renamed constant still feeds the PS12 check. In a disposable copy, `sink_b = 3` → `sink_b = 1` (`receipts/probe-ps12-sink_b.diff`) fails exactly `PS12: both register at the settle, one applicant (sink 0) declares Ready for both ...`, with 1,511 PASS and 1 FAIL, rc 2 (`receipts/probe-ps12.log`). The `listener_is` / `listener_any` initialisers are only read after `listener_value` returns true (short-circuit `&&`), so the split cannot change their result. A probe there would not be informative, so I ran none.
- **Comment rule:** the delta adds no comment line, no bench lane label, no review round and no reviewer ID.

### 2. The suites keep full counts (Tests)

Each suite ran on a `git archive` of the exact head with the pinned Verilator. Its identity was verified first: `Verilator 5.050 2026-07-01 rev v5.050` (`receipts/tool-versions.txt`). The two suites ran concurrently.

| Suite | Command | rc | Tally | Round 3 (PR body, both round-3 reviews) |
|---|---|---|---|---|
| `tb/pp_top` | `make run` (7 builds) | 0 | `11064 checks: 11064 PASS, 0 FAIL` | 11,064 |
| `tb/srp_stream_fsms` | `make` (walk shapes, then suite) | 0 | `1512 checks: 1512 PASS, 0 FAIL` (walk shapes 48/64/96/176 all PASS) | 1,512 |

The delta adds or removes no `CHECK`, so equal counts are expected. They hold. The author's published receipts give the same two tallies with rc 0.

### 3. The parent idiom gate passes with this gitlink (Conformance, Robustness)

- **Scratch parent:** `kebag-logic/milan-fpga` at live dev `cc204c6fd2349b543d73f15c97162a2c4434c86e`, with `gptp-processor` at its pin `135afd04`. `protocol-processor` was checked out and staged as the gitlink at each pin in turn. `git submodule status` shows a leading space (on pin) for each run (`receipts/idiom-*.status`). The scope helper refuses an off-pin or absent processor, so a pass is not a false zero.

| Pin | `check_cpp_idiom.py` | `--list` |
|---|---|---|
| main `a9e84b66` | rc 0, `multi-declarator declaration: 0 <= 0` | rc 0 |
| round 3 `834cc88` | rc 1, `FAIL: multi-declarator declaration 3 > ratchet 0 ... Rule 11` | rc 1. Rows: `protocol-processor/tb/pp_top/sim_main.cpp ... =2`, `protocol-processor/tb/srp_stream_fsms/sim_main.cpp ... =1` |
| **round 4 `6162885`** | **rc 0**, 351 first-party translation units (165 C), every rule 0, `multi-declarator declaration: 0 <= 0` | **rc 0**, no per-file row |
| `--selftest` | rc 0, `75 checks: 75 PASS, 0 FAIL` | |

- **Parent base:** the author's scratch parent was based at dev `604899c0`, not `cc204c6f`. `scripts/check_cpp_idiom.py`, `scripts/code_quality_scope.py` and `scripts/cpp_idiom.budget` are byte-identical between the two (`git diff --stat` empty). My run at `cc204c6f` therefore checks the same gate at the base the manager's refusal used. The ROM digests the author re-recorded are equal to main's. `check_cpp_idiom.py` does not read them.

### 4. Published evidence (Docs, Tests)

- **Evidence locations:** the link in the assignment points at `kebag-logic/milan-fpga@c5661216`, the round-3 author packet. The round-4 author packet is the next author commit on the same public branch: `pp212-review-evidence` at `d7250b05`, "processor #212 author round 4 packet". I read only its `author-r4/` files, not the archived reviews.
- **Manifest:** `scripts/verify_manifest.py` checks all 68 `author-r4/` entries of `MANIFEST.json` against the blobs at `d7250b05`. Result: 0 mismatches, 0 unlisted files (`receipts/manifest-author-r4.log`). The commits are unsigned (`%G?` = N), so the integrity evidence is the manifest hashes, not a signature.
- **Spot-checks:**
  - `processor/head-6162885/{pp_top,srp_stream_fsms,git_diff_check}`: rc 0, the same tallies as mine.
  - `parent/pin-6162885/check_cpp_idiom{,_list,_selftest}`: rc 0, `0 <= 0`.
  - `parent/pin-834cc88-repro`: the refusal reproduced.
  - `records/parent-records.txt`: the gitlink is `6162885…`, on pin.
- **PR body:** the published `author-r4/PR-BODY.md` is byte-identical to the live PR body (sha256 `bbc81cb1…09f1a`). The round-4 sections ("Round 4", the Changes bullet, the Validation lead and the `check_cpp_idiom.py` lines) match what I measured.
- **Gate list:** the published handoff now lists `check_cpp_idiom.py` among the consumer gates (author-r4 `HANDOFF.md:61-66`), as the assignment asked.

## Findings

### S1 - SUGGESTION - Robustness, Docs (parent gate, outside this PR)

- **Where:** parent `milan-fpga` `scripts/check_cpp_idiom.py:269-270` (`MULTI_DECL_RE`), at dev `cc204c6f`. In this PR: the PS12 line that was `tb/srp_stream_fsms/sim_main.cpp:2895` at `834cc88`.
- **Evidence:** `scripts/multidecl_probe.py` runs the gate's own regex (`receipts/multidecl-probe.log`):
  - It counts `int e = -1, q = -1;` as 1. That is correct: two declarators, ES.10.
  - It also counts `const int sinks[] = {0, 3};` as 1. That declaration names one entity, and the comma is inside a braced initialiser. Core Guidelines ES.10 does not cover it.
  - It counts all four split forms as 0.
- **Impact on this PR:** none. The split is harmless and behaviour-identical (section 1), and the assignment required it. The PR body's "refused three multi-declarator declarations" reproduces the gate's own category and count, so it is not wording residue.
- **Impact elsewhere:** a later braced array initialiser in any first-party C or C++ file will be refused under Rule 11 as well.
- **Suggested outcome:** a parent follow-up could exclude commas inside `{...}` from `MULTI_DECL_RE`, with a selftest fixture (`const int a[] = {0, 3};` → 0). Otherwise, Rule 11 could say that braced aggregate initialisers are counted on purpose.
- **Verification:** rerun `scripts/multidecl_probe.py` against the changed parent. The third line should give 0.

No other new finding. The delta has no RTL, documentation or README text in which a defect could be found.

## Prior public review findings at this head

| Finding (round 3) | Status at `6162885` | Evidence |
|---|---|---|
| R770-3 R1, RESIDUE: `tb/srp_top/README.md:901` "(the exception before this row)" | **Retained.** The round-4 assignment barred every other change, and the delta does not touch the README. | `:901` still reads "(the exception before this row)". The exact fix is unchanged: replace it with "(the settled-sink exception the listener had before PS24)". |
| R770-3 R2, RESIDUE: PR body Validation, "(README cells re-recorded)" for eight arms where seven have a cell | **Retained.** The PR body's round-3 paragraph is unchanged. | The text is still present. The exact fix is unchanged: replace it with "(the seven README cells that record a count re-recorded; the issue #188 table, which holds `listener-reprobe-abandons-leave`, records none)". |
| R770-3 S1 to S4, R769-3 S1 to S4 (the LINK_UP strobe wording; adopting probe cases; an end-to-end link row; settled-sink Begin! and Talker Failed variants of PS24; the talker-side link gap; the late Lv; the `msrp_fail_bridge_o` note) | **Carried as suggestions, not taken.** | The delta does not touch the HDL, `10_srp_engine.md`, PS24 or `tb/pp_top`'s link rows. Nothing these suggestions depend on has changed. |
| R769-2 F1 = R770-2 F1 and the round 1 findings | **Still resolved.** | The delta changes no RTL and no test that grades them. PS16 to PS24 are inside the 1,512 passing srp_stream_fsms checks, and the pp_top rows are inside the 11,064 passing pp_top checks. |

## Lens summary

- **Conformance - CLEAN.** The delta changes no protocol behaviour and no test oracle. The split satisfies Rule 11 / ES.10 as the parent gate enforces it. S1 concerns the parent's regex, not this PR.
- **RTL - CLEAN.** No HDL changed in the delta (`receipts/delta-raw.txt`). The round-3 RTL verdict and the round-3 area figures stand.
- **Robustness - CLEAN.** On pin, the parent gate passes at this head and refuses at the round-3 head, and the off-pin refusal makes a false zero impossible. S1 is a suggestion.
- **Tests - CLEAN.**
  - Both suites run at full count with rc 0 and no new warnings.
  - The renamed PS12 constant is shown live: the mutation probe fails PS12 by name.
  - The delta removes no check.
- **Docs - CLEAN (R1, R2 RESIDUE retained).**
  - The PR body's round-4 text and the published handoff match the receipts.
  - The two round-3 residues are carried to the residue checklist unchanged.

## Ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `tb/pp_top/sim_main.cpp:10584-10627`, `tb/srp_stream_fsms/sim_main.cpp:325, 2886-2903`; parent `check_cpp_idiom.py` Rule 9 / `MULTI_DECL_RE`; issue #212 acceptance and the round 4 assignment | R770-4 (delta), R770-3 (rest) | 6162885ffee5d8e8897732be6479982b8dceaec9 |
| RTL | CLEAN | `git diff --raw 834cc88 6162885` (no `hdl/` path); round-3 RTL verdict carried | R770-4 (delta), R770-3 (rest) | 6162885ffee5d8e8897732be6479982b8dceaec9 |
| Robustness | CLEAN (S1 suggestion) | scratch parent at `cc204c6f`, gate at the main, round-3 and round-4 pins, `--list`, `--selftest`, on-pin status; the regex probe | R770-4 | 6162885ffee5d8e8897732be6479982b8dceaec9 |
| Tests | CLEAN | `pp_top-r4.log` (11,064/11,064), `srp_stream_fsms-r4.log` (1,512/1,512), `probe-ps12.log` (PS12 killed by name), `delta-equiv.log`, `diff-check.txt` | R770-4 | 6162885ffee5d8e8897732be6479982b8dceaec9 |
| Docs | CLEAN (R1, R2 RESIDUE retained) | PR body (round-4 sections, Validation), author-r4 `HANDOFF.md`, `PR-BODY.md` and manifest (68/68), `tb/srp_top/README.md:901` | R770-4 (delta), R770-3 (rest) | 6162885ffee5d8e8897732be6479982b8dceaec9 |

## Real limits

- **No full banks:** I ran no full processor or parent bank, no campaign driver, no Yosys or area run and no lint run at this head. For the parts the delta does not touch, round 3's evidence and verdicts are relied on. The delta is two test-bench C++ blobs, so none of those depend on it.
- **One parent gate only:** of the parent consumer gates I ran only `check_cpp_idiom.py`, at live dev `cc204c6f` with `gptp-processor` at its dev pin. The other consumer commands, and the ROM-digest recording, I did not run.
- **No signature:** the evidence commits are unsigned. Integrity rests on the manifest hashes.
- **Physical calibration:** NOT RUN. No hardware was used, and field skips are not hardware proof.
- **No manager bank at this head:** no manager source bank exists at this exact head, and none is claimed or inferred here.

## Pending manager duties

- Build and validate the current-dev merge candidate (source base `a9e84b66`, live dev `cc204c6f`) on the builder and native banks, including the parent consumer gate with `check_cpp_idiom.py`, and link the receipts on the PR.
- Carry R770-3 R1 and R2, retained here, to the residue checklist.
- Hosted/act acceptance.
- Optionally, route S1 to a parent follow-up.

## Integrity after probes

- Clone `HEAD` = `6162885…`, tree `16b9d3fa…`.
- Status is empty, the index equals the HEAD tree for every mode, blob and path, and the worktree bytes equal HEAD after a forced refresh (`receipts/clone-integrity.txt`).
- The processor tree has no submodule gitlinks. The required `protocol-processor` gitlink was exercised only in the scratch parent.
- Every build and probe ran under `scratch/` on copies.

Reproduction: `scripts/run_gates.sh <processor-clone> <work-dir> <verilator>`, plus `scripts/delta_equiv.py`, `scripts/verify_manifest.py` and `scripts/multidecl_probe.py`. Usage is in each file's header.

R770-4 FINISHED
