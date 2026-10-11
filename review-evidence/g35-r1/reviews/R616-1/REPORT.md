[R616] POSITIVE - exact head 5b4ce3974f7627d57b31167bde50cde8f4bdcdf3

# R616-1 internal independent review: FPGA-gPTP PR #80 (issue #35)

- Exact head: `5b4ce3974f7627d57b31167bde50cde8f4bdcdf3`, tree `9a2ecff812f209bf90eb6714690e864a4ec4f582` (verified in the reviewer's detached clone: HEAD, `HEAD^{tree}` and `git write-tree` all match).
- Base: main `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`. Four commits: a7c031f, fd1d6c9, 05cacb6, 5b4ce39.
- Diff: 11 files, +393/-18. Touched: `hdl/wire/KL_gptp_rx_parser.sv`, the parser bench (`sim_main.cpp`, `Makefile`, `README.md`, new `mutants.py`), and current docs (`README.md`, `docs/{HDL_DEVELOPER,INTEGRATION,MANAGER,SOURCE_EVIDENCE,TEST_DEVELOPER}.md`). No microcode, engine RTL, checker script, generated image or submodule is touched. The repository has no submodules, so there are no gitlinks to check.
- Verdict: **POSITIVE**. There are no open BLOCKER, MAJOR or MINOR findings. One RESIDUE (wording only) and two SUGGESTIONs are recorded.

## Reconstruction (order followed)

1. `AGENTS.md` / `CONTRIBUTING.md`: neither exists in this repository at head or base. The governing local sources are the root `README.md`, the `Makefile`, and the `docs/README.md` truth order: RTL, then executable tests, then current guides, then history.
2. Docs map, `docs/INTEGRATION.md` receive interface, `docs/SOURCE_EVIDENCE.md` and its checker.
3. Issue #35 body (frozen acceptance: four checkboxes), the manager lane ruling (comment 6104916029: the safer default, any byte latches into the drop state, one drop, first and eof byte included, port doc and module header state the contract, error-free frames unchanged, parent netlist/ROM digests unchanged, the four-type per-position proof, a planted control, and the donor gates), the author's REVIEW READY (6105359326), and the manager ruling on the 3567 -> 3568 hierarchical cell move (6105366046, accepted).
4. Interface authorities: engine port forwarding (`hdl/top/KL_gptp_engine.sv:72,167`, which feeds `rx_err_i` only to the parser), the engine's bank/Announce-context consumers of the parser write lane (`:180-310`, `:700-720`, `:895-912`), the bench gasket (`bench/arty/bench_mii_rx.sv:158`, which raises the error with the last byte only), and the parent tie-off `KL_gptp_shadow.sv:666 .rx_err_i (1'b0)` at dev `ac2c5e77`, whose gitlink is `5dce647a` (read from the public parent: `receipts/parent-tieoff-ac2c5e77.txt`).
5. `git diff 5dce647a..5b4ce397` and the commit history.
6. Public executable evidence: `kebag-logic/milan-fpga@2e32325/review-evidence/g35-r1`. All 60 blobs were fetched and each one's git blob hash matches the published tree (`receipts/evidence-index/g35-r1-tree.txt`). Also the PR body and the manager's comments on the issue and PR.
7. Prior public review findings on PR #80: none. The PR has no reviews and, apart from author and manager text, only the two review-start notices (R616-1, R617-1). The issue has no reviewer comments for this lane. Nothing needs to be resolved or retained.

## RTL change under review

`hdl/wire/KL_gptp_rx_parser.sv:645` adds `if (rx_err_i) bad_r <= 1'b1;` as the last statement inside `if (rx_valid_i)`:
- It comes after the sof arm (`:401-419`), so its non-blocking assignment overrides the sof arm's `bad_r <= 1'b0` on a flagged first byte.
- The eof byte's own flag still reaches `fin_ok_r` directly through the existing `!rx_err_i` term (`:625`), because `bad_r` settles on the same edge.
- Drops are counted once, at the deferred fin (`fin_drop_w`, `:650`). A one-byte frame is counted once by `runt_drop_w`.
- The line sits inside `rx_valid_i`, so a flag on an idle cycle is ignored. This is documented.
- A flag on a valid byte outside a frame (no sof, `run_r` low) sets `bad_r`, but the next sof clears it, so the next frame is unaffected. The reviewer probe confirms this.
- With `rx_err_i` tied to 0 the new line is dead logic. Equivalence is proven below.

## Lenses

### Conformance: CLEAN
- Ruling clause "rx_err_i on any byte latches into the drop state; exactly one drop; first and eof byte included". Code at `:645` and `:625`. Reproduced at every position of 9 frame shapes (below).
- Clause "port documentation and module header state the contract". Port comment `:109`, DROP-arm list `:32`, contract paragraph `:52-62`, `docs/INTEGRATION.md:47,60-66`. The header's bank-write sentence is imprecise; see RESIDUE R616-1-RES1.
- Clause "frames without an error behave exactly as before". Yosys equivalence of base and head parsers with `rx_err_i` tied 0: **748 of 748 proven**. With the port free: 747 proven and 1 unproven (`bad_r`), so the proof is not vacuous (`receipts/equiv/equiv_{tied,free}.summary`). The parser suite runs 268/268 at base and 298/298 at head, the extra 30 being the new checks.
- Issue acceptance checkbox 2 says "no bank write". The PR reads it as "no bank write after the flag" and discloses that reading. That matches the later manager ruling, which sets drop/event semantics and not bank-write semantics. A write already made before the flag cannot be retracted in a streaming parser without buffering. The words left behind land in the write bank, which no event names, exactly as for the pre-existing truncation and TLV refusal arms. The engine's Announce context path already handles a frame that is poisoned after staging (`KL_gptp_engine.sv:270-275`), and the published path is copied only by the owning handler (`:895-912`). Checkbox 4 (`feed_gap` drives `rx_err_i`) was already true at base (`sim_main.cpp:235` at base). Checkbox 3 ("README counts"): no current page carries a parser count. Checked by grep.
- Parent clause (as ruled on in 6105366046): see the RTL lens. No standard-clause claim is added or changed by this PR.

### RTL: CLEAN
- Independent focused identity probe (`scripts/equiv_parser.sh`, `receipts/equiv/`; parser module only, not the parent bank). sv2v, then Yosys hierarchical `proc; opt_clean` stat: base 529 cells, head 530. The only stat difference is `$mux` 306 -> 307 (`hier_free_stat.diff`). This is the module-local form of the ruled 3567 -> 3568 parent rollup.
- Wrapper with `rx_err_i` tied 0, then `flatten; opt; opt_clean`: **stat identical** (`flat_tied_stat.diff` empty). The `write_verilog -noattr` text differs, but only in the numbering and order of Yosys auto-named nets. Logical identity rests on the 748/748 equivalence proof, not on byte equality of the dump.
- ROM: `gen_gptp_ucode.py` output is byte-identical at base and head, `c496ed8af59edd424e7d980aa3442bb725c745f44469ce53ec3a4d219fa30371` (`receipts/equiv/rom.txt`). That equals the parent ledger row for the base pin shown in the author's `parent/romcheck/head-record.diff`.
- Author parent evidence (inspected, not re-run; the parent bank is out of this reviewer's allowance):
  - gate PASS at both pins, cells 3567 / 3568;
  - module-by-module sv2v input: 8 of 9 modules identical, only `KL_gptp_rx_parser` differs;
  - `flat.stat.txt` byte-identical at both pins (same blob `342dfb15`);
  - ROM bundle digest `018e9be9…6fd2` at both pins;
  - `flat.il` and `hier.il` sha256 differ between pins. This is consistent with the parser's shifted source lines and the extra cell. The PR body claims identical `stat` plus equivalence, not identical dump bytes, and that claim is supported.
- Lint: `make lint` rc 0 with Verilator 5.050.

### Robustness: CLEAN
The reviewer probe (`scripts/probe_rx_err.cpp`, `scripts/build_probe.sh`) is independent of the parser suite: its own frame builders, sampling and counters. Results are in `receipts/probe/probe-{head,base}.log`.
- **Head: 36/36 PASS.**
- **Base: 22 PASS, 14 FAIL.** The probe is not vacuous: base fails every mid-frame sweep, the zero-gap pairs with a mid-frame flag, and the flag-then-idle case.

What the probe covers:
- A per-position single-byte flag (drops +1, events 0, no write after the flagged byte's own edge), a flag on every byte (one drop), and a clean control after the errors. This is run for:
  - Sync (58 bytes), Follow_Up (90), Pdelay_Req (68), Pdelay_Resp (68), the four types the ruling names;
  - **plus** Pdelay_Resp_Follow_Up (68), Signaling (48), Announce without PathTrace (78), Announce with a one-hop PathTrace (90), and a Sync padded to 60 bytes (flags in the padding).
- Zero-gap neighbours:
  - a flagged Sync (flag at byte 0, 20 or 57) followed with no gap by a clean Pdelay_Req: one drop, one event, code 4;
  - a clean Pdelay_Req followed with no gap by a Sync flagged on byte 0 or 1: one drop, and the predecessor's event survives.
- A flagged stray valid byte outside any frame, then a clean frame: no drop, event raised.
- A flagged one-byte frame: exactly one drop, and the next frame dispatches.
- A flag on a byte followed by an idle gap that keeps the flag high: one drop.

Observation (feeds RES1): in every swept type, the word completed by the flagged byte itself is still written on that byte's own edge. Positions that do this:

| Frame | Positions writing on their own edge |
|---|---|
| Sync | 6 of 58 (bytes 29, 41, 43, 47, 53, 57) |
| Follow_Up | 7 of 90 |
| Pdelay_Req | 4 of 68 |
| Pdelay_Resp | 8 of 68 |

The same holds at base. The write goes to the unnamed write bank. Behaviour is safe; only the header sentence describing it is imprecise.

### Tests: CLEAN
- Donor gates at exact head, Verilator 5.050 (wrapper sha256 `905795b9…e92f`), run in disposable exports (`scripts/run_gates.sh`, `receipts/gates-head/`): `make tb` rc 0, `make contract` rc 0, `make lint` rc 0, `make docs` rc 0. Results:
  - ucpu 768/768
  - **parser 298/298 + parser mutants 8/8**
  - engine 1613/1613 x3 + engine mutants 34/34
  - gaskets 81/81 + 5/5
  - tsngen 288/288 + 4/4
  - bench MII tag PASS
  - docs: 20 exact anchors, 0 findings

  Every figure matches the PR body's validation table and the author's `gates-head` receipts. Base parser suite: 268/268 (`receipts/base-parser/`).
- New checks reviewed in `sim_main.cpp`:
  - `feed_err` drives every face signal each byte, and counts writes after the first flagged byte's own edge;
  - the sweep runs every position for four types, plus held from byte 20 to eof, plus a clean control, plus the gap-only flag;
  - the 30 new checks run last, so the earlier drop-total check is undisturbed.
- **Independent re-application of planted defects** (`scripts/indep_mutants.py --jobs 8`, `receipts/mutants/`). Each arm uses the reviewer's own edit forms against the head suite. An arm counts as caught only if every named check appears on a FAIL line. **8 of 8 arms behaved as expected.**

| Arm | Defect | Result |
|---|---|---|
| C0 | unmutated | 298/298 |
| R1 | latch deleted (re-applied control) | caught, 12 named |
| R2 | latch gated `!rx_sof_i` (other form of the first-byte defect) | caught |
| R3 | eof term removed from `fin_ok_r` (re-applied) | caught |
| R4 | latch only in the first 30 bytes (novel) | caught |
| R5 | eof flag also counted as a runt drop (novel) | caught (one drop / held one drop) |
| R6 | flag refuses at eof but bank writes continue (novel) | caught by exactly the 4 "no later write" checks, which shows that check is load-bearing on its own |
| R7 | latch gated `!rx_eof_i` (equivalent rewrite) | passes 298/298, as expected, because the eof term still refuses |

- The author's arm non-vacuity receipts were inspected: the repair reverted gives 2 PASS / 6 FAIL; one named check renamed gives 7 PASS / 1 FAIL ("missed its named check"). These match the PR body.

### Docs: CLEAN (one RESIDUE, one SUGGESTION)
- `docs/INTEGRATION.md` receive table and contract lines: accurate, including "Errors raised between valid bytes are ignored".
- `docs/HDL_DEVELOPER.md:29`, `docs/TEST_DEVELOPER.md:35,94-95` and the parser README describe the contract and the arm.
- The #35 risk bullets are removed from `README.md` and `docs/MANAGER.md`, and #35 is moved under closed work in `docs/SOURCE_EVIDENCE.md:42`. The tree describes the post-merge state, and the PR carries `Closes #35`.
- `SOURCE_EVIDENCE` anchors moved `#L374 -> #L386` and `#L456 -> #L468`. Both are verified EXACT by the checker and by direct line read at base and head.
- History pages are left as dated records, as the truth order allows.
- PR body line references `:32`, `:52-62`, `:109`, `:620-621`, `:625`, `:645` all match head.
- No hosted CI exists for this repository: there are no workflow files, and the exact head shows 0 check runs and an empty combined status (`receipts/gh/hosted-check-runs.txt`). There are therefore no executed or skipped hosted jobs to distinguish.

## Findings

### R616-1-RES1: RESIDUE (Docs)
- **Where:** `hdl/wire/KL_gptp_rx_parser.sv:60-62` ("No bank write follows the flagged byte; words written before it stay in the write bank …"). The same imprecision appears in the PR body's opening paragraph ("no bank write after the flagged byte") and Acceptance item 2 ("Words written before a later flag stay in the write bank").
- **Evidence:** reviewer probe `INFO *_flagged_edge_writes` lines. A word completed by the flagged byte (for example Sync byte 29 → w1, 57 → w5) is written on that byte's own edge. That write is neither "before" the flagged byte nor excluded by the sentence. The suite's "no later write" check and the PR's per-position section count writes *after the flagged byte's own edge*, so measurements, tests and code are all correct. Only the sentence is imprecise.
- **Impact:** wording only. The write lands in the unnamed write bank, like every other refused frame's words. No figure, test, code path, generated artifact or clause claim changes.
- **Exact fix:** replace the header sentence with "No bank write follows the flagged byte's own edge; words written up to and including it stay in the write bank like those of any refused frame, unnamed by any event." In the PR body, read "after the flagged byte's own edge" for "after the flagged byte", and "up to and including a later flagged byte" for "before a later flag".
- **Verification:** text review. `make docs` is unaffected (the comment is not an anchored construct).

### R616-1-S1: SUGGESTION (Docs, Tests)
- **Where:** `docs/SOURCE_EVIDENCE.md:12`. The new "Any-byte receive refusal" row links the whole parser file without a line anchor, so `scripts/check_source_evidence.py` skips it (rows outside `EXPECTED` with no anchor are ignored).
- **Status:** precedent rows of this kind exist, and the lane scope excludes checker edits, so this is not a defect.
- **Outcome when the checker is next touched:** anchor the row to `if (rx_err_i) bad_r <= 1'b1;` and add it to `EXPECTED`, so the claim is bound to its construct.

### R616-1-S2: SUGGESTION (Tests, Robustness)
- The suite's sweep covers the four ruled types. The reviewer probe shows the same behaviour for Pdelay_Resp_Follow_Up, Signaling, Announce with and without PathTrace, a padded Sync, zero-gap neighbours, a stray flagged byte and a flagged one-byte frame.
- Folding a subset into the parser suite would make that coverage permanent. Optional.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #35 body + manager rulings 6104916029 / 6105366046; parser `:32,:52-62,:109,:625,:645`; `docs/INTEGRATION.md:47,60-70`; equivalence tied/free; base/head parser suites | R616-1 | 5b4ce3974f7627d57b31167bde50cde8f4bdcdf3 |
| RTL | CLEAN | parser diff; engine forwarding and bank/Announce consumers; parent tie-off at ac2c5e77; focused sv2v+Yosys hier/flat stat and equivalence; ROM generator digest; author parent evidence (inspected); `make lint` | R616-1 | 5b4ce3974f7627d57b31167bde50cde8f4bdcdf3 |
| Robustness | CLEAN | reviewer probe, head 36/36 and base 22/36 (9 frame shapes per position, zero-gap pairs, stray byte, runt, flag-plus-idle) | R616-1 | 5b4ce3974f7627d57b31167bde50cde8f4bdcdf3 |
| Tests | CLEAN | `sim_main.cpp`, `mutants.py`, `Makefile`; `make tb`/`contract`/`lint`/`docs` all rc 0; reviewer mutants 8/8 (R1, R3 re-applied; R2 another form; R4-R6 novel; R7 equivalent); author non-vacuity logs | R616-1 | 5b4ce3974f7627d57b31167bde50cde8f4bdcdf3 |
| Docs | CLEAN | README, `docs/{HDL_DEVELOPER,INTEGRATION,MANAGER,SOURCE_EVIDENCE,TEST_DEVELOPER}.md`, parser README, module header and port comment, PR body line references; RES1 recorded (RESIDUE, does not unclean) | R616-1 | 5b4ce3974f7627d57b31167bde50cde8f4bdcdf3 |

## Real limits
- The parent elaboration, sv2v staging, ROM bundle digest and ROM-ledger gate were **not re-run** by this reviewer: full parent and Yosys banks are outside the allowance. Parent figures (3567/3568 cells, flat stat identity, bundle digest `018e9be9…`) come from the author's published receipts. The reviewer reproduced only the module-local form (parser hier 529 -> 530, one `$mux`; flat stat identical with the port tied; 748/748 equivalence; identical `gptp_ucode.hex`).
- No manager source bank ran at this head, and none is claimed or inferred. Source-head execution evidence is the author's published gate receipts plus this reviewer's own gate run.
- There is no hosted CI for this repository (0 check runs at head), and Docker/act was not used.
- Physical calibration was NOT RUN. Nothing here is hardware proof. The bench path raises the error with the last byte only, so it does not exercise mid-frame behaviour.
- No engine-level test drives `rx_err_i` (the engine and tsngen harnesses tie it to 0). The engine-side effect of a mid-frame refusal was assessed by code reading only.

## Pending manager duties
- Build and validate the current-dev merge candidate (source base `5dce647a`, live dev `ac2c5e77`) with the builder and native banks at the merge turn, and link the receipts on the PR.
- At the next batched parent adoption: record the new pin's ROM-ledger row (`./ooc.sh --record-rom-digests` adds `5b4ce397… gptp_ucode.hex c496ed8a…`; without it the author's receipt shows `ooc.sh` FATAL for the unrecorded pin) and review that diff with the bump.
- Carry R616-1-RES1 to the residue checklist.
- Merge still needs the second independent review (R617) and the full completion bar.

## Reproduction
Scripts live in `scripts/`, receipts in `receipts/`; all are listed in `MANIFEST.sha256`.
- `scripts/run_gates.sh <repo> <commit> <work> <out> <verilator-dir>`
- `scripts/build_probe.sh <hdl-dir> <obj> <log>` (with `scripts/probe_rx_err.cpp`)
- `scripts/indep_mutants.py <head-tree> <work> --jobs N`
- `scripts/equiv_parser.sh <base-tree> <head-tree> <work> <out>`

After the probes, the clone was verified at exact head: HEAD, tree and write-tree match; the index equals the HEAD tree in modes, blobs and paths; all 105 worktree blobs and modes match; there is no status output, including ignored files; and there are 0 gitlinks (none required). See `receipts/clone-integrity.txt`.

R616-1 FINISHED
