[R369] NEGATIVE - exact head c64f8cd896a4462bd42c4b90b32861ac7fd35176

# R369-2 external independent review: PR #609 (#590, #592, #599), round 2

- Round: R369-2, external reviewer, cleared context. Delta focus `792a57b0..c64f8cd8` (`ececc631c` fix, `c64f8cd89` capture and service re-measure); all five lenses applied at the exact head.
- Exact head `c64f8cd896a4462bd42c4b90b32861ac7fd35176`, tree `d83fe0c35f7675c7408dd19c18fd3094f0044a3b`. Source base `8bc97021f28fb7f729418d3a00851c84ea0b50fd`. Processor pin `16be6768f710e79450aace277abacd6c2c3336e5`.
- Scope sources: #590 body, assignment 5859537529, scope correction 5859930453, findings-page scope 5857603294, round-2 assignment and decision 5862495507 (option (a)), round-2 REVIEW READY 5865308902; #592 and #599 bodies; PR #609 body and its Round 2 section; AGENTS.md, CONTRIBUTING.md, docs/README.md.
- Prior public findings (R368-1, R369-1) were read only after this round's own pass over the diff. Their disposition is below.
- Overall result: the three round-2 technical repairs hold. F1 (MDIO phase), F2 (dispatch hook) and R368-1 F3 (edge test) are resolved, and I re-ran my own probes and mutants against them. Three MINOR findings are open: a stale design authority for the capture figures, an understated residual threshold, and native round-2 service evidence that was not retained. Conformance, Tests and Docs are unclean. RTL and Robustness are clean.

## Findings

### F4 - MINOR - Docs, Conformance - the design authority still states the replaced capture receipt

- **Where:**
  - `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1590-1631` (section 18 "Cost", Timing).
  - `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1776-1786` (section 20, item 6).
- **Authority:**
  - AGENTS section 6, Docs: "Changed contracts are reflected in authoritative docs."
  - #592 acceptance 2: "Report the new 8x8 maximum and the margin gained."
  - Precedent in this tree: the #580 re-measure, `d02db63c3`, replaced `measurements.json` and updated this section in the same commit.
- **Evidence:**
  - The section still gives the measured parent `499b15f97...` and says "Firmware and hold behavior are unchanged by this remeasurement".
  - It still gives "The worst 8x8 measurement is 24.30246 ms", "0.19754 ms below the assigned limit", 1x1 6.60642 ms, the 100 MHz figure 19.79024 ms, and the full six-row table.
  - The committed receipt at this head (`tb/verilator/nvm_capture_cpu/measurements.json`) binds firmware `2e715af6...`, tree `dab60a36` (= `ececc631^{tree}`) and maxima 3.88578 / 13.22872 / 9.94948 ms. `check_nvm_capture.py` passes against it (`receipts/check_nvm_capture.log`).
  - The lane replaced the receipt twice (`ba3a47811`, `c64f8cd89`) and never touched this section. This defect was already present at the round-1 head, and R369-1 missed it.
  - For the final figures, the margin gained (24.30246 - 13.22872 = 11.07374 ms) and the margin to the 24.5 ms limit (11.27128 ms) appear in no current text. The receipt states only the floor ratio (3.704x). The PR body's one margin sentence, 11.06984 ms, describes the superseded round-1 figure.
- **Impact:** the hold-sizing authority tells a reader that the 8x8 copy sits 0.2 ms under its limit on byte-copy firmware. It contradicts the receipt it cites, and it records neither the word-copy remedy's result nor the margin it gained.
- **Required outcome:**
  - Sections 18 and 20 item 6 describe the committed receipt: measured tree, firmware digest, six maxima, floor ratios, and the 8x8 margin to 24.5 ms. Alternatively, they explicitly mark the old figures as historical and point to the receipt.
  - The final 8x8 maximum and the margin gained are stated.
- **Verification:** `rg '24\.30246|0\.19754|6\.60642|19\.79024' docs/design` returns only lines marked historical, and the section's figures equal `measurements.json`.

### F5 - MINOR - Docs - the long built-in residual understates when backing can lapse

- **Where:**
  - `docs/integration/BAREMETAL_FIRMWARE.md:1908`: "Beyond 2,000 ms without service, saved-state backing can lapse."
  - `docs/findings/397_SERVICE_BUDGET.md:195`: "After 2000 ms without service, saved-state backing can lapse."
- **Authority:**
  - Round-2 decision 5862495507: long built-ins are a **documented residual**.
  - `SAVED_STATE_FASTCONNECT.md:1096`: T-NVM-WRITER-ALIVE re-arms on every heartbeat (2,000 ms, `:1247`).
  - `milan_baremetal.c:918-931`: a heartbeat is written only when 250 ms have passed since the last one.
- **Evidence:**
  - Consider an opportunity taken at the dispatch hook 249 ms after the last written heartbeat. It writes nothing. A built-in body that starts there lapses backing after about 1,751 ms with no opportunity, not 2,000 ms.
  - The lane applies this same phase everywhere else ("The 500 ms heartbeat limit includes the 250 ms phase"), but it is missing from this sentence.
  - The surrounding "can exceed 500 ms heartbeats and 250 ms PHY publication" is correct but gives no body length.
- **Impact:** an operator who times a built-in, for example a `mem_read` range, at under 2 s would read it as safe for liveness when it is not.
- **Required outcome:** both pages state the lapse threshold in terms of the built-in body, net of the 250 ms rate-limit phase (about 1,750 ms). A body-length statement for the 500 ms heartbeat and 250 ms publication bounds is optional.
- **Verification:** text review of both pages against `nvm_heartbeat_tick` and section 9.4.

### F6 - MINOR - Conformance, Tests, Docs - the round-2 native service and control evidence is not retained

- **Where:**
  - Round-2 REVIEW READY 5865308902: "A host restart cleared the scratch area after the measurements and regrades. The raw logs and native builds are lost, but their size and SHA-256 bindings remain."
  - `tb/verilator/fw_service_budget/README.md:90`: "Raw per-run receipts belong in the public evidence packet."
- **Authority:**
  - Round-2 assignment item 2: the built-in plan must be "graded with `--enforce-service`, showing zero unbacked cycles; removing the hook fails it".
  - AGENTS section 5: an executor posts reproducible evidence.
  - AGENTS section 6, Docs: "enough evidence for another cold reviewer".
- **Evidence:**
  - At review time the only public evidence tree is `0f817be1:review-evidence/590-r1`, round-1 evidence for `792a57b0`. No round-2 packet exists (`590-review-evidence` tip `a1c4d79f`, rechecked at the end of this round).
  - The claims have no retained raw log or receipt a reviewer could regrade: `queued-builtins` passing on both shapes, the 1051-of-1051 serviced lines, the `remove-dispatch` gap of 8238.99363 ms, the target `late-sample` kill, the 1.83666x byte-only ratio, and the refreshed service tables.
  - The committed code is consistent with them. The plan, the per-line oracle (`run.py:353-355`), the mutation anchors (`build.py:110-121`) and the verdicts (`run.py:527-537`) all exist, and I exercised the per-line oracle portably (`receipts/builtin-oracle-probe.log`).
  - I could not run the native harness in this round (see limits).
- **Impact:** item 2 of the round-2 assignment and #590 acceptance 2 at this head rest on unretained output. `--regrade` is impossible without the bound logs.
- **Required outcome:** at the candidate head, run the native `queued-builtins` positive arm on both shapes, the `remove-dispatch` control on `queued-builtins`, and the target `late-sample` control, and retain their raw logs and JSON receipts in the public packet. The byte-only control receipt should also be retained. A manager-run bank with published receipts satisfies this equally.
- **Verification:** `run.py --regrade` with identical arguments passes on the published logs, each control prints its named PASS line, and receipt hashes match the packet manifest.

## Suggestions (do not affect coverage)

- **S5 (Robustness, Docs) - the dispatch hook fails silently if patch 0006 is absent from the LiteX environment.**
  - The weak BIOS default plus the whole-archive strong override is correct (`receipts/weak-link-probe.log`; LiteX `ALWAYS_LINK_LIBS` uses `--whole-archive`).
  - An environment that applied only 0002/0004/0005, which is every environment set up before this PR, still builds, and #590 regresses with no signal. Every earlier series patch fails loudly when absent.
  - Builder gate 23h catches such an environment, but the product build path (`milan_soc.py`, `build.sh`) does not.
  - Consider a link-time guard: the patch defines a marker symbol that the firmware references. Also note the 0006 dependency where `BAREMETAL_FIRMWARE.md:1896` introduces the hook.
- **S6 (Docs) - the in-file records of the patch series are stale.**
  - The `sw/litex/patches/apply.sh:6-12` header describes 0002/0004/0005 but not 0006.
  - `sw/builder/test_builder.py:23296` still says "six patches" (pre-existing).
  - `SERIES` and the README are consistent.
- **S7 (Tests) - the per-line oracle is not pinned portably.**
  - The queued-builtins check "console line lacks a dispatch opportunity" (`run.py:353-355`) has no portable control.
  - `report_verdict` for `remove-dispatch` requires only "continuous backing lost" (`run.py:530`).
  - Consider a portable control and requiring the named per-line finding in the dispatch control.
- **S8 (Tests) - the MDIO acknowledgement guard is not independently exercised.**
  - An "ack-ignored" mutant passes the host PHY test (`receipts/mdio-mutants.log`). A missing acknowledgement also yields 0xffff, which the BMSR/ID filters already refuse.
  - A NAK part-way through the negotiation reads would distinguish the two. This is pre-existing #599 scope.
- **S9 (Docs) - two traceability gaps on the findings page.**
  - `397_SERVICE_BUDGET.md:267` cites "the unchanged phase probe", a review-evidence script, without a locator.
  - The duty tables give a 500 ms deadline for empty and unknown lines (`:94-95`) but N/A for `mem_read` and Milan commands, without explanation.
- **S10 (Tests) - reviewer note, no change needed.**
  - An off-by-one `next - i >= 3u` survives the partial-ownership test.
  - Every shipped shape's record boundaries have residue 0 or 2, so it is behaviorally equivalent today (`receipts/edge-residue-probe.log`).
  - A fixture with an odd-length record would pin it.
- **Retained from R369-1, not taken:**
  - S1: a single NAK or undiscovered PHY republishes link down each opportunity (`milan_baremetal.c:873-908`, unchanged).
  - S3: the builder literal 4.
  - S4: no `CHANGELOG.md` entry for this lane. Its #580 capture lines now describe a replaced receipt, like F4.

## Verification of the round-2 items (evidence for what holds)

1. **F1 (MDIO phase): resolved.**
   - `phy_mdio_bit` (`milan_baremetal.c:791-803`) now does three things in order: it drives with MDC low and waits `cdelay(32)`, samples, then raises MDC.
   - `phy_mdio_read` (`:806-823`) clocks 32 preamble and 14 command bits, discards turnaround bit 46, takes the acknowledgement from bit 47 (sampled before rising edge 47, driven by the PHY after edge 46), then reads 16 data samples.
   - This matches IEEE 802.3 22.3.4 and the pinned LiteX `libliteeth/mdio.c` at `a1e1c365`. I extracted that file from the pinned revision: after two turnaround clocks, `raw_read` samples before each rising edge.
   - The sample point is at least 64 CPU cycles after the previous rising edge. That exceeds the 300 ns maximum clock-to-output plus the `LiteEthPHYMDIO` MultiReg (`liteeth 276c9e37`).
   - Both peers now launch frame bit k+1 at edge k: `phy_host.c:55-58` and `phy.hpp:26-27`. That is TA zero at 46, D15 at 47, D0 at 62 and release at 63. Each peer is derived from the clause, not from the reader.
   - My unchanged round-1 probe now reports the following under the IEEE phase (`receipts/probe_mdio_phase-head.out`): firmware BMSR `0x796d`, PHYID1 `0x001c`, `link_status=13`, identical to the LiteX reference. Under the old convention the firmware now fails, as it should.
   - Host mutants (`receipts/host-selftest.log`, `receipts/mdio-mutants.log`):
     - `late-sample` is killed on its named assertion.
     - My one-turnaround, three-turnaround, fifteen-data and write-opcode mutants are killed.
     - The settle-free sample passes, as an equivalent.
   - The target `late-sample` kill is covered by F6.
2. **F2 (every dispatch): resolved in code, with F5 and F6 open.**
   - `0006-bios-dispatch-hook.patch` applies with no offset or fuzz to the pristine pinned LiteX `a1e1c365`, after 0004. It reverse-applies, and the result is byte-identical to the patched BIOS `main.c` (`receipts/patch-0006-apply.log`). The pin is from `litex_pins.txt:53`. The hosted `elaborate` job, which runs `apply.sh` and gate 23h on a fresh environment, succeeded at this head.
   - The hook follows `readline` (patched `main.c:352-353`) and precedes the `buffer[0]` test, so Milan commands, built-ins, unknown and whitespace-only lines, and empty lines all reach it.
   - The firmware override (`:935-938`) is one rate-limited heartbeat plus a PHY opportunity. It performs no idle auto-commit, and the five per-handler entry ticks are removed.
   - The host bench mirrors the hook (`nvm_host.c:636`). `SERIES` lists 0006, and the README entry matches.
   - The plan is `('mem_read 0x40000000 128', '', 'unknown_command') * 350 + ('milan_status',)`: 1051 lines and 14363 bytes. The pinned `CMD_LINE_BUFFER_SIZE` is 128, which supports applying the 133-byte figure to the queue.
   - The per-line oracle fires only for queued-builtins and only when a line has zero ticks (`receipts/builtin-oracle-probe.log`).
   - The portable self-test passes 43 grading and 14 flash checks (`receipts/service-selftest.log`).
   - The residual is documented in both pages for the heartbeat and the PHY bound. Its lapse threshold is F5.
3. **R368-1 F3 (partial ownership): resolved.**
   - `nvm_host.c` carries an independently driven ownership vector, `--open-record` (`:724`) and `--dump-stage`. `grade_partial_ownership` poisons an open record beside an unaligned closed predecessor and checks both the stage and the committed slot.
   - My own mutant runner (`receipts/edge-mutants.log`) plants the `>= 1u` edge-cross on all five shapes, Arty included. Each shape is caught by the named finding "open record changed across unaligned predecessor edge".
   - `>= 2u`, a removed edge guard and an ownership-ignoring copy are also caught on all five. The byte-only equivalent passes on all five.
   - The committed self-test plants its mutants on the first shape only. The all-shape claim is established by my runner.
4. **S1/S2 as taken (R368-1): resolved.**
   - `grade_byte_only` (`nvm_capture_cpu/run.py:85-96`) requires every byte-only sample to exceed 1.5 times a matched-scenario maximum. `byte_only_controls` (`:99`) pins the boundary and a mismatch before each run.
   - The capture README states that the capture SoC has no `milan_mac`, so the PHY path is compiled out. I confirmed `soc.py` has no `milan_mac`. Without its CSR the firmware compiles the `#else` stub (`milan_baremetal.c:909`).
5. **Capture re-measure: binding holds.**
   - `product_firmware_sha256` `2e715af6...` equals the head's `milan_baremetal.c`, and `tree` equals `ececc631^{tree}`.
   - `ececc631..c64f8cd8` touches no firmware or capture-harness file. All six `harness_sha256` values equal the head files, and `bios_dispatch_patch_sha256` equals the head 0006 patch.
   - All six arms have 16 rows. 8x8 at 50 MHz: 13.22872 ms against 24.5 ms (margin 11.27128 ms, floor ratio 3.704x).
   - `check_nvm_capture.py` returns rc 0 at head. The stated margin is F4.
6. **No RTL change.**
   - The round-2 diff touches no `hdl`, `configs`, processor, `milan_soc.py` or builder file. 0006 is BIOS C.
   - Gitlinks equal the source-validation pins.

## Prior public findings: disposition at this head

| Finding | Disposition |
| --- | --- |
| R369-1 F1 = R368-1 F1 (BLOCKER) | Resolved. See item 1. R368-1's "independent peer" wording is replaced by the IEEE-peer text. |
| R369-1 F2 = R368-1 F2 (MAJOR) | Resolved by the option (a) hook. The residual accuracy is retained as F5, and the evidence as F6. |
| R368-1 F3 (MINOR) | Resolved on all five shapes. See item 3. |
| R368-1 S1, S2 | Taken and verified. See item 4. R369-1 S2 is the same point as R368-1 S1 and is resolved. |
| R369-1 S1, S3, S4 | Not taken. Retained as suggestions. |

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | UNCLEAN (F4, F6) | `milan_baremetal.c:791-823,918-938,1184` against IEEE 802.3 22.3.4 and the pinned LiteX `mdio.c`; 0006 patch against pinned `main.c`; #590/#592/#599 acceptance and decision 5862495507; `measurements.json`; `check_nvm_capture.log` | R369-2 | `c64f8cd896a4462bd42c4b90b32861ac7fd35176` |
| RTL | CLEAN | Round-2 diff (no `hdl`/`configs`/processor/`milan_soc.py`); `LiteEthPHYMDIO` (liteeth `276c9e37`: MDC from CSR storage, MultiReg on `mdio_r`) against the firmware sample point; `milan_soc.py:1760-1800` `link_status` CSR; gitlinks | R369-2 | `c64f8cd896a4462bd42c4b90b32861ac7fd35176` |
| Robustness | CLEAN (S5, S8 optional) | Hook path for empty, whitespace, unknown and built-in lines (patched `main.c:350-360`); 128-byte line buffer; weak/strong link (`weak-link-probe.log`); PHY-compiled-out capture and Arty builds; NAK/absent peer cases; `--open-record` refusals (`nvm_host.c:724-730`); edge residues on all shapes | R369-2 | `c64f8cd896a4462bd42c4b90b32861ac7fd35176` |
| Tests | UNCLEAN (F6) | `test_nvm_firmware.py --self-test` rc 0; `test_phy_firmware.py` with 3 mutants; reviewer mutants `edge-mutants.log`, `edge-residue-probe.log`, `mdio-mutants.log`, `probe_mdio_phase-head.out`; `fw_service_budget/run.py --self-test` (43+14); `builtin-oracle-probe.log`; `ci_scope.py --selftest` | R369-2 | `c64f8cd896a4462bd42c4b90b32861ac7fd35176` |
| Docs | UNCLEAN (F4, F5, F6) | `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1590-1631,1776-1786`; `BAREMETAL_FIRMWARE.md:1896-1911,1933-1937,1958-1963`; `397_SERVICE_BUDGET.md` round-2 diff; both harness READMEs; `nvm_hosttest/README.md`; patches README and `apply.sh`; `docs_check`, `check_doc_paths`, `check_doc_style`, `check_archive`, `check_em_dash --base 8bc97021`, `gen_toc --check`, `git diff --check` all rc 0 | R369-2 | `c64f8cd896a4462bd42c4b90b32861ac7fd35176` |

## Receipts (listed in MANIFEST.sha256)

**Scripts:**
- `scripts/probe_mdio_phase.py` and `scripts/probe_mdio_phase.c`: the round-1 probe, byte-identical to the round-1 packet.
- `scripts/edge_mutants.py`, `scripts/edge_residue_probe.py`, `scripts/mdio_mutants.py`, `scripts/builtin_oracle_probe.py`, `scripts/weak_link_probe.sh`.
- `scripts/verify_head_bytes.py`.

**Receipts:**
- `receipts/probe_mdio_phase-head.out`, `receipts/host-selftest.log`, `receipts/edge-mutants.log`, `receipts/edge-residue-probe.log`, `receipts/mdio-mutants.log`.
- `receipts/patch-0006-apply.log`, `receipts/weak-link-probe.log`, `receipts/builtin-oracle-probe.log`.
- `receipts/service-selftest.log`, `receipts/check_nvm_capture.log`, `receipts/ci-scope-selftest.log`.
- Docs gate logs (`receipts/*.py.log`) and `receipts/diff-check.log`.
- `receipts/hosted-checks-snapshot.txt`.
- `receipts/verify-head-bytes.log`: HEAD, tree, 945 file blobs/modes and 4 gitlinks match the exact head. Porcelain including ignored files is empty, and the three required submodules are clean at their pins. All probe builds ran under this packet's `scratch/`. The shared LiteX tree was only read.

## Real limits

- **No native product-CPU simulation was run.**
  - The scoped Verilator path in the assignment does not exist on this host, so no Verilator was used.
  - A SoC build plus the Verilator compile and a multi-second simulation cannot finish inside this session's 10-minute foreground bound, and no reusable build exists.
  - Target-side claims (queued-builtins, remove-dispatch, late-sample, service tables, capture arms) are therefore unverified by me beyond the committed receipt and the gates above. This is F6.
- **MDIO correctness rests on host evidence.** It rests on the clause text, the pinned reference reader and host peers. Physical calibration was NOT RUN, and field skips are not hardware proof. The silicon confirmation is #599 acceptance 4 after merge.
- **Builder banks were not run** (outside allowance). Patch applicability was checked on an extracted pristine pinned tree, plus the hosted `elaborate` success.
- **Manager banks were in progress** under the manager's work area at report time, with no results. No round-2 manager evidence is published.
- **Hosted snapshot** (07:38:54Z): `rtl-fast`, `elaborate`, Yosys shards and Verilator shards 0 and 3 SUCCESS; Verilator shards 1, 2 and 4 and `docs-check` IN_PROGRESS; Physical gPTP SKIPPED. This is not acceptance evidence.

## Pending manager duties

- Route F4, F5 and F6 to the executor, or run and publish the F6 native receipts under manager ownership. Then re-review the corrected head across all five lenses.
- Hosted/act acceptance at the corrected head. Publish the builder and native bank receipts.
- The final current-dev candidate build and merge validation (source base `8bc97021`, live dev `54ce8773`).
- The internal review (R368-2) remains independent. Merge needs two positive reviews and the full completion bar.
- #599 acceptance 4 (bench switch cycles, which also confirms the MDIO phase on silicon). The bench environment must carry patch 0006 (S5). Post-merge containment.

R369-2 FINISHED
