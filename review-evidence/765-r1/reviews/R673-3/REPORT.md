[R673] POSITIVE - exact head 87a2b77d1ed49f634c616f2d27b6aa9b9f5d786d

Internal cleared-context independent review, round R673-3, issue #765 / PR #769.

- Head `87a2b77d1ed49f634c616f2d27b6aa9b9f5d786d`, tree `95076a30447b31a37d02298bf87b4fdd6a809d89`.
- Delta reviewed: `d4a27e63..87a2b77d`, one commit, `87a2b77d`, whose parent is `d4a27e63` (the R673-2 head). No rebase and no amend.
- The commit changes four files: `KL_avtp_rx_monitor.sv` (comment only), the avtp_rxmon `[28]` banner, `fuzz_aaf.py` (rationale, docstring, section title), and the regenerated `hdl/ieee1722/avtp/doc/TEST_RESULTS.md`.
- All five lenses were applied to the delta. Lens results from earlier rounds are carried forward only where the delta does not touch what they depend on.

This is a source review verdict. It is not merge authorization and not hardware qualification.

## Summary

R673-2-F1 is resolved at its cause:
- The six assigned texts and the PR body's known limitations now say what the flat test instrument does. It reads only `channels_per_frame[7:0]` (`KL_avtp_rx_monitor.sv:178`) and accepts a nonzero value there (`:197`), so a count of 256 is rejected.
- The campaign's section title names the counts it probes. Its parenthesis now says the device listener rejects a count other than its current format's. It no longer says the listener rejects every probed count.
- `TEST_RESULTS.md` matches a fresh campaign run at the CI tsn-gen pin, apart from the timestamp.
- The reviewer's own boundary probe agrees with the new wording, and so does the R673-2 probe as the author re-ran it:
  - 256 and 512 are rejected and counted UNSUPPORTED_FORMAT;
  - 257, 520 and 1023 are accepted.

With comments stripped, the delta changes no SystemVerilog token. The avtp_rxmon leg and the AAF campaign pass at this head in this reviewer's own runs.

No BLOCKER, MAJOR or MINOR finding is open. Two inherited wording RESIDUE items and the retained optional SUGGESTIONs are listed below. They do not affect the verdict.

## Findings

### R673-3-RES1: RESIDUE | Tests, Docs

- **Where:** `tb/verilator/avtp_rxmon/sim_main.cpp:453`. The inherited `[27e]` stimulus comment reads `// any count matches now`.
- **Evidence:**
  - The stimulus is a 2-channel PDU under the 8-channel `FMT`.
  - The flat instrument would reject a count of 0 or 256 here (`KL_avtp_rx_monitor.sv:197`; `receipts/probe_cpf_hi.log`).
  - This is the same overgeneralisation that R673-2-F1 removed from the six assigned texts. The author's REVIEW READY and the PR's known limitations already disclose it.
  - The line predates the delta. It is a source comment only: no check, label, console output or generated record carries it.
- **Impact:** a reader of the `[27]` case is told that the flat instrument accepts any count. The `[28]` banner 12 lines below says otherwise.
- **Exact fix:** `// a 2-channel PDU matches again: this flat instrument does not compare the count`.
- **Verification:** read the line. Run `make -C tb/verilator/avtp_rxmon`, which should still give flat 97/0.

### R673-3-RES2: RESIDUE | Docs, Tests

- **Where:** `tb/verilator/milan_dp/gen_divergent_shape.py:9-10`. The module docstring reads "channels alone would be masked by the listener family compare".
- **Evidence:**
  - The obj_nxndv leg elaborates `milan_datapath`, whose listener is `KL_avtp_rx_monitor_ctx`.
  - Since #765 that listener compares the full 10-bit channel count against the current format (`KL_avtp_rx_monitor_ctx.sv:512-528`; FR-STR-03). So channels alone would no longer be masked.
  - This PR does not touch the file, and the generator's choice of the 96 kHz base remains valid. Only the parenthetical reason is stale. It is a docstring and changes no generated header or expectation.
- **Impact:** a reader is told that the shipping listener still uses the family compare that #765 retired.
- **Exact fix:** replace the parenthesis with `(the 96 kHz family member the builder's own encoder produces, so the row differs in rate as well as in channel count)`.
- **Verification:** read the docstring. Run `python3 -I scripts/docs_check.py` and expect rc 0.

### R673-2-S1 (retained): SUGGESTION | Tests

- **Where:** `tb/verilator/avtp_rxmon/sim_main.cpp:83,459`, the method `channel_freedom_accepts_every_count()`.
- **Issue:** the name now contradicts its own banner at `:460-464`, which says a count whose low eight bits are zero is rejected.
- **Suggested change:** rename it, for example to `flat_family_compare_accepts_other_counts`. No check changes. This was not assigned and is optional.

### Comment-rule scan of the delta: no RESIDUE

I scanned every added line in `d4a27e63..87a2b77d` for a lane label, lane name, review round, reviewer ID or issue-comment ID, and found 0 (`receipts/static_gates.log`). The new comments cite only `#765`, FR-STR-03 and Milan v1.2 clauses.

## Prior public findings at this head

I read these after this round's independent pass over the diff.

| prior finding | status at 87a2b77d | evidence |
|---|---|---|
| R673-2-F1 (MINOR; Docs, Tests, RTL) | **Resolved** | See the table below. |
| R673-2-S1 (SUGGESTION; Tests) | **Retained, optional** | Not assigned. The method name is unchanged (`sim_main.cpp:83,459`). |
| R673-2-N1 (note) | **Unchanged** | `sim_main.cpp:433` still holds inherited identifiers, outside the delta. #746 tracks them. |
| R673-1-F1, R673-1-F2 (MINOR) | **Stay resolved** | The delta does not touch `KL_avtp_rx_monitor_ctx_ref.sv`. The F2 texts were reworded only toward R673-2-F1, and each still says that the flat instrument keeps the family compare on purpose and that the device listener rejects another count (#765, FR-STR-03). |
| R673-1-S1, S2, S3 (SUGGESTION; Tests) | **Retained, optional** | Their artifacts, `KL_avtp_rx_monitor_ctx.sv` and `tb/verilator/milan_dp/sim_main.cpp`, are untouched by the delta. |
| R674-1-RES1 (RESIDUE; Docs) | **Stays resolved** | The PR body at review contains no U+2014 (`receipts/pr769_body_at_review.md`). |

R673-2-F1, text by text:

| assigned text | at 87a2b77d | agrees with the RTL and the probe |
|---|---|---|
| `KL_avtp_rx_monitor.sv:183-184` | `:182-192`: "a channel count whose low eight bits are nonzero accepted (this instrument reads only channels_per_frame[7:0], so a count of 256 is rejected)" | yes. `:178` is `p_chans = fsh_i[47:40]` (O+18, the low byte of the 10-bit field per IEEE 1722-2016 7.3). `:197` is `p_chans != 8'd0`. Probe: 256 and 512 rejected, 257 accepted. |
| `[28]` banner, `sim_main.cpp:460-461` | `:460-464`: "a channel count whose low eight bits are nonzero is accepted here (this instrument reads only channels_per_frame[7:0])" | yes. No check, label or expectation changed (`receipts/delta_d4a27e63_87a2b77d.diff`). |
| `fuzz_aaf.py:143` (rationale) | `:141-150`: "accepts a channel count whose low eight bits are nonzero (it reads only channels_per_frame[7:0])" | yes |
| `fuzz_aaf.py:176-177` (docstring) | `:177-180`: "accepts each probed channels_per_frame: it reads only channels_per_frame[7:0] and accepts a nonzero value there. The device listener rejects a count other than its current format's (#765)" | yes |
| `fuzz_aaf.py:178-179` (section title) | `:181-185`: the title is built from `counts = (1, 2, 3, 4, 8)` and reads "flat instrument family compare: channels_per_frame 1, 2, 3, 4, 8 accepted (the device listener rejects a count other than its current format's, #765)" | yes. It claims only the probed counts. The campaign's format has 8 channels (`cosim_aaf.cpp:26`, `FMT[31:22] = 8`), so the parenthesis is right for all five probes: the listener would accept 8 and reject 1 to 4. The same 20 checks are graded, with unchanged labels and expectations. |
| `TEST_RESULTS.md:29,96` (generated) | regenerated, with the same title | yes. The reviewer's fresh run differs from the committed file only in the timestamp (`receipts/test_results_regen.diff`). The author's in-clone run reports freshness 1 PASS, and that receipt's hash matches the published manifest (`receipts/author_r3_spotcheck.txt`). |
| PR body, known limitations | "reads only the low eight bits of the 10-bit channels_per_frame ... a count of 256, 512 or 768 is rejected as if it were zero ... rejects a count other than its current format's (#765)" | yes. The reviewer probe covers 256 and 512, and 768 has the same zero low byte. The Round 3 table's line ranges match the head. |

## Lens results

### Conformance: CLEAN

[R673] PASS Conformance - `tb/verilator/tsn_fuzz/fuzz_aaf.py:141-150,177-185`; `hdl/ieee1722/avtp/KL_avtp_rx_monitor.sv:182-192`; `hdl/ieee1722/avtp/doc/TEST_RESULTS.md:29,96`; `receipts/avtp_rxmon_full.log` ([UF], `format_mutants.py` 6/6) - every statement in the delta about the device listener was checked against the shipping compare, the clauses of issue #765 and FR-STR-03.

- **The listener statement is true.** "The device listener rejects a count other than its current format's" describes `KL_avtp_rx_monitor_ctx`, which compares the full 10-bit count with the current format. This head's run grades it:
  - `[UF2a]` 2 channels against 8, `[UF3a]` 264 against 8, and `[UF1a]` a matching count accepted;
  - all five format mutants caught, including "low byte".
- **No clause is misstated.** The delta cites only Milan v1.2 4.4.2.2, Table 5.6 and Table 6.2, which are the clauses of #765.
- **The flat module is not shipped.** Its width behaviour is a property of a test instrument.
- **Carried forward.** R673-1's acceptance-criteria evidence for the shipping engine and `KL_crf_rx` stands. The delta changes no code token (`receipts/strip_compare.txt`).

### RTL: CLEAN

[R673] PASS RTL - `hdl/ieee1722/avtp/KL_avtp_rx_monitor.sv:178,182-192,197`; `receipts/strip_compare.txt` (1221 tokens at `d4a27e63` and at `87a2b77d`, identical); `receipts/probe_cpf_hi.log` - the module's contract comment was checked against the expression below it and against a boundary probe.

- The comment now states the 8-bit read and the 256 rejection. That is exactly `p_chans = fsh_i[47:40]` and `p_chans != 8'd0`.
- No port, parameter, register-map or gitlink change. All six gitlinks are recorded in `receipts/clone_integrity.txt`.
- The route, Yosys and xvlog evidence that R673-1 examined at `75db4b57` stands for the logic, because no logic token changed in rounds 2 or 3.

### Robustness: CLEAN

[R673] PASS Robustness - `receipts/probe_cpf_hi.log` (flat instrument at counts 256, 257, 512, 520, 1023 and 8); `receipts/avtp_rxmon_full.log` ([UF2f-g], [UF3]-[UF5], the "low byte" mutant caught by [UF3a]) - the delta's boundary claims were tested at the 8-bit and 10-bit edges.

- **The flat instrument behaves as the new text says:**
  - a count whose low byte is zero (256, 512) gives frames_rx +0 and UNSUPPORTED +1;
  - a count whose low byte is nonzero (257, 520, 1023) gives frames_rx +1 and UNSUPPORTED +0.
- **The shipping engine's 10-bit boundary** is graded and mutation-tested at this head.
- The delta changes no reject, recovery, reset or boundary behaviour. R673-1's Robustness result is carried forward.

### Tests: CLEAN

[R673] PASS Tests - `receipts/avtp_rxmon_full.log` + `.rc`; `receipts/tsn_fuzz_aaf.log` + `.rc`; `receipts/test_results_regen.diff`; `receipts/author_r3_spotcheck.txt`; `tb/verilator/tsn_fuzz/fuzz_aaf.py:176-196`; `tb/verilator/avtp_rxmon/sim_main.cpp:459-482` - this head was executed and the changed harness text was checked against what it grades.

- **avtp_rxmon (reviewer run, pinned Verilator 5.050), rc 0:**
  - flat 97/0 and NX 147/0;
  - lockstep N=1 116/0 and N=8 119/0;
  - `lockstep_mutants.py` 14/14 and `format_mutants.py` 6/6.
- **AAF campaign (reviewer run, rc 0):** tsn-gen built by the reviewer at `deca300c`, the CI pin. Result: 164 pass, 0 fail, 0 known gaps.
- **Record freshness.** The regenerated record differs from the committed file only in the timestamp. The campaign's freshness gate itself reported SUITE-SKIP in the reviewer's export, which has no git metadata, so the direct diff stands in for it.
- **The checks are unchanged.** The delta adds or removes no check. The 20 count checks keep their labels and expectations, and only the section title changes in the record's check-set.
- **Author receipts.** I spot-checked ten files of the round-3 author receipts at `71b87fde` (`r3-aaf`, `r3-probe`, `r3-rxmon`, `r3-scripts/probe_flat_cpf256.sh`, `r3-misc`), and all ten match `MANIFEST.json`.
  - Each carries head `87a2b77d` with rc 0.
  - The probe script's hash, `4598ce13...`, is the one the author's `HEAD.txt` records.
- **Wording.** RES1 (an inherited comment) and S1 (a method name) are wording only and do not leave the lens unclean.

### Docs: CLEAN

[R673] PASS Docs - `receipts/static_gates.log`; `receipts/pr769_body_at_review.md`; `hdl/ieee1722/avtp/doc/TEST_RESULTS.md:7,29,96`; `receipts/delta_d4a27e63_87a2b77d.diff` - the changed and generated texts and the PR body were checked against the head.

- **Static gates:**
  - `git diff --check d4a27e63 87a2b77d`: clean;
  - U+2014 added by the delta: 0;
  - `check_em_dash.py --base d4a27e633`, run with the pinned Markdown renderer available: 0 findings over 3 added lines;
  - `docs_check.py`: rc 0, 0 findings across 210 md files;
  - `lint_rtl.py --check`: PASS, 90 against a ratchet of 90.
- **The commit message** is one line with no trailers.
- **The PR body** has a Round 3 section whose line ranges match the head, and its known limitations are corrected as assigned.
- **Retired reading.** A repository-wide search for the retired "any nonzero channel count" and "any channel count accepted" readings, outside the history archive, finds only RES1 (`sim_main.cpp:453`). The search also surfaced RES2, a stale docstring that predates the PR. Both are wording RESIDUE.

## Reviewer-owned completion ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `fuzz_aaf.py:141-150,177-185`; `KL_avtp_rx_monitor.sv:182-192`; `TEST_RESULTS.md:29,96`; `receipts/avtp_rxmon_full.log` ([UF], format mutants); `cosim_aaf.cpp:26` | R673-3 | 87a2b77d1ed49f634c616f2d27b6aa9b9f5d786d |
| RTL | CLEAN | `KL_avtp_rx_monitor.sv:178,182-192,197`; `receipts/strip_compare.txt`; `receipts/probe_cpf_hi.log`; `receipts/clone_integrity.txt` | R673-3 | 87a2b77d1ed49f634c616f2d27b6aa9b9f5d786d |
| Robustness | CLEAN | `receipts/probe_cpf_hi.log`; `receipts/avtp_rxmon_full.log` ([UF2f-g], [UF3]-[UF5], "low byte" mutant) | R673-3 | 87a2b77d1ed49f634c616f2d27b6aa9b9f5d786d |
| Tests | CLEAN | `receipts/avtp_rxmon_full.log`; `receipts/tsn_fuzz_aaf.log`; `receipts/test_results_regen.diff`; `receipts/author_r3_spotcheck.txt`; `sim_main.cpp:459-482`; `fuzz_aaf.py:176-196` | R673-3 | 87a2b77d1ed49f634c616f2d27b6aa9b9f5d786d |
| Docs | CLEAN | `receipts/static_gates.log`; `receipts/pr769_body_at_review.md`; `TEST_RESULTS.md:7,29,96`; `receipts/delta_d4a27e63_87a2b77d.diff` | R673-3 | 87a2b77d1ed49f634c616f2d27b6aa9b9f5d786d |

Each row covers the round-3 delta at this head. Behaviour the delta does not touch is carried forward from R673-1 at `75db4b57`, and R673-2 at `d4a27e63` adds no code token change. None of that scope has changed since: the shipping RTL, `KL_crf_rx`, milan_dp and the route inputs.

## Real limits of this round

**Not run by this reviewer:**
- Vivado route-1x1 and the resource gate;
- Yosys and xvlog;
- the full suite sweep, crf_rx, milan_dp, the builder bank and `make dynmap-mutants`.

The delta changes no logic token, so the author's round-1c figures at `75db4b57` stand for them.

**Freshness gate.** In the reviewer's run the campaign's freshness gate reported SUITE-SKIP, because the run used a `git archive` export with no git metadata. The direct diff of the regenerated record against the committed blob, which differs only in the timestamp, stands in for it. The author's exact-head freshness PASS was verified by hash only.

**Interpreter.** The reviewer's Python gates ran on the host CPython 3.14. The author's ran on 3.12.3.

**Hosted CI.** A snapshot at review time is in `receipts/hosted_checks_snapshot.tsv`: 1 completed/success, 2 in progress, 15 queued. No hosted acceptance is claimed, and no queued or skipped context is counted as executed.

**Evidence context:**
- No manager source bank exists at this head, and none is inferred.
- Physical calibration NOT RUN. No hardware or field proof is claimed.
- The other reviewer's round-3 report was not read.

**Receipt redaction.** Home-directory and packet paths in the build logs are replaced with `<home>`, `<verilator-root>` and `<packet>`. No other byte was changed.

**Probe hygiene:**
- All runs used a `git archive` export of the head and probe copies under this packet's scratch area. The tsn-gen clone and build are also there.
- The only write into the review clone was a `scripts/__pycache__` directory from one gate run. I removed it.
- After that, `git status --porcelain --ignored` is empty, the index equals HEAD, `git write-tree` equals tree `95076a30`, and the six submodule gitlinks are unchanged (`receipts/clone_integrity.txt`).

## Pending manager duties

- **Merge candidate:** build and validate the current-dev merge candidate at the merge turn, with the builder and native banks, on live dev `78ca9bdf`.
- **Hosted acceptance:** own hosted and replica acceptance at the exact head (`rtl-fast`, `verilator-suites`, `yosys-portability`).
- **Residue checklist:** carry R673-3-RES1 and R673-3-RES2.
- **Optional:** R673-2-S1, and R673-1-S1 to S3.
- **New issues:** file the work the lane recommended:
  - the pruned 1x1 short-frame depacketizer window;
  - inputs above 0 read their current format only from LCTX words 2/3;
  - optionally, whether the flat instrument should read the full 10-bit `channels_per_frame`.

## Packet contents

- `scripts/strip_compare.py`: compares a SystemVerilog file token by token, with comments stripped, at two revisions.
- `scripts/probe_cpf_hi.py`: patches a copy of the flat avtp_rxmon harness to set `channels_per_frame[9:8]`, and adds the `[P]` boundary case.
- Raw receipts are under `receipts/`. Every published file is listed in `MANIFEST.sha256`.

R673-3 FINISHED
