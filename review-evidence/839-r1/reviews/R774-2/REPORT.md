[R774] NEGATIVE - exact head ba56827bbfe4acadb84ca220616a76ad74611e7d

External independent review, round R774-2, of PR #841 (issue #839). Exact head `ba56827bbfe4acadb84ca220616a76ad74611e7d`, tree `72b663ff0c6a45d2fe95606b9cdb7d40303e8bec`. Base and live `dev`: `604899c08ff1cd1830e1dd08b733109ef852400c`.

Scope: the round-2 delta `992c3d7b..ba56827b`, four commits. It touches `sim_boot_sa.cpp`, `gen_boot_fw.py`, `bootsa_probes.vlt`, `bootsa_mutants.py`, `scripts/measure_test_evidence_readers.py`, the milan_dp `README.md`, `TESTING.md` and `CHANGELOG.md`. Nothing under `hdl/`, `syn/`, `sw/`, `configs/` or any submodule changed (`receipts/delta_scope.txt`). I also checked each round-1 finding at its cause. Code the delta does not touch keeps its round-1 lens verdict.

The verdict is NEGATIVE on one open MINOR finding (F1, Docs). The README still credits the leg with checks it does not make, in the list that round 1's F2 required to match the leg exactly. Every round-1 finding is resolved at its cause, and the RTL stands. Every new check can fail, and each new control fails by name, both in my rerun and in the author's receipts.

## Round-1 findings, resolved or retained

| Finding | Status at ba56827b | Evidence |
|---|---|---|
| R773-1 F1 = R774-1 F1 (MINOR, Tests): no test of the MAAP/AAF/CRF hold | **Resolved.** `early_enable()` (`sim_boot_sa.cpp:549-618`) writes `MAAP_CTRL`, `AAF_CTRL` (with the `[1]` bypass) and `CRFT_CTRL` at reset release, using the firmware's own boot words (`0x201`, `0x20001`, `0x3`; offsets `0x6CC`, `0x654`, `0x750`, generated from `milan_baremetal.c`). It then holds the pair unwritten for 400 ms and grades the frames that follow. In the MAAP-on boot, MAAP and CRF offer. In the MAAP-off boot, AAF and CRF offer (`receipts/bootsa_tree.log`: "MAAP yes, AAF no, CRF yes" and "MAAP no, AAF yes, CRF yes"; "0 frames left" in both). The control that removes all three holds is the same plant as my round-1 `plant_noxtra.py` (`bootsa_mutants.py:76-89,116-118`), and it is caught with 10 failures. Each single-source control is caught by its own name. The README gives the reason the AAF talker cannot offer while MAAP is held, with RTL lines. I checked every cited line: `milan_datapath.sv:2214-2217` (`aaf_gate` needs `~cfg_maap_enable` or `maap_addr_valid`), `KL_maap.sv:189` (claim only in ANNOUNCE), `:307` (`tvalid = tx_busy_r`), `:392-395` (busy clears only on accepted beats), `:477` (next PROBE only when not busy), `:487-489` with `PROBE_SENDS_C = 4` at `:123` (fourth PROBE goes to ANNOUNCE), and `milan_datapath.sv:8818` (MAAP `tready` gated). The claim holds. | `receipts/par_mutants.log`, `receipts/mut_no_hold_*.log` |
| R773-1 F2 (MINOR, Docs/Tests): the leg did not check that the stamp touched nothing but octets 6 to 11 | **Resolved at the leg (option a).** `stamp_edge()` (`sim_boot_sa.cpp:429-452`) compares the gasket's output (`ctlg_src_tdata_w`) with the stamp's output (`ctlg2_tdata`) for every kept octet outside 6 to 11, on `ctlg2_tvalid & ctlg2_tready`. It samples before the clock edge (`tick()`, `:296-311`) and skips reset edges (`:431`), in every boot. The stamp is combinational (`milan_datapath.sv:8934-8941`), so comparing both sides in the same cycle is sound. Clean run: 93 frames, 3,556 octets, 0 changed. The wrap control (round-1 PM3 shape) fails `every control-lane octet outside 6 to 11 leaves the stamp as it entered` (got=126) and **nothing else**. So this check alone is what now guards that property. `TESTING.md:277` matches what the controls fail. One residual README scope problem is F1 below. | `receipts/par_mutants.log`, `receipts/mut_the_stamp_s_beat_position_wraps_past_the_source_.log` |
| R773-1 S1 / R774-1 S1 (SUGGESTION): CRF and MVRP | **Taken.** CRF is required where `kCrfOutputDeclared` is set (generated from `boot_policy.crf_output_declared()`; `true` for the shipping config). MVRP is driven by `probe_tx()` (`sim_boot_sa.cpp:731-757`) and required. My probe removes the `probe_tx()` call and fails exactly one check, `MVRP frames were sent and graded`, out of 65 (`receipts/bootsa_nomvrp.log`). So the MVRP requirement is live and is not met by accident. I checked the probe PDU layout: subtype 0xFC, message_type 0, control_data_length 44, FAST_CONNECT 0x0002, status read from `rsp[16] >> 3`. | `receipts/bootsa_nomvrp.log`, `receipts/probe_nomvrp.diff` |
| R773-1 S2 (SUGGESTION): link the decision record | **Taken.** The PR body links issuecomment-6655611611. | PR body, "Maintainer decision" paragraph |
| R773-1 RES-1 = R774-1 R2 (RESIDUE): area-run commit | **Applied with the exact texts.** R773-1's text is in the PR body's area paragraph. R774-1's text is in the issue's round-2 REVIEW READY comment ("Residue from round 1: Area at `8d2dfb65` ..."). | PR body area paragraph; issue #839 REVIEW READY of round 2 |
| R774-1 R1 (RESIDUE): "pending a maintainer" | **Applied with the exact text** in Known limitations ("Acceptance 3" item) and in the Definition of Done. No stale phrase remains outside the residue table's quotation. | PR body |

## Findings

### F1 - MINOR - Docs - the README's "It grades every frame" list claims checks the leg makes only on the first boot

- Where:
  - `tb/verilator/milan_dp/README.md:1183-1197`, with `:1204` ("In each early-enable boot it **also** grades").
  - `README.md:1206-1210` (CRF described unconditionally).
  - The code: `sim_boot_sa.cpp:759-830` (`grade()`), called once at `:861`, before `pair_order()` (`:862-863`) and `early_enable()` (`:864-865`); `early_enable()`'s CRF checks run only under `if (kCrfOutputDeclared)` (`:608`).
- Authority and evidence:
  - The round-2 assignment, item 2, asks that the README "match exactly what the leg checks". R773-1 F2 records a README claim about what a test proves as MINOR, not as wording. I am not certain this is wording only, so under the owner rule it is MINOR.
  - `README.md:1183` comes after the descriptions of all five boots. It reads "It grades every frame on valid/ready at `m_axis_mac_tx`", and its list includes the destination-address, known-protocol (EtherType and subtype), sent-and-graded and processor-offered checks.
  - Those checks are `grade()`'s, and `grade()` iterates `sent_` only as it stands after the first boot and the listener's probe.
  - The pair-order boots' frames, and the two early-enable boots' frames, get no destination or known-protocol check. In this run the early-enable boots alone send 850 frames ("847 frames after the pair" and "3 frames after the pair", `receipts/bootsa_tree.log`).
  - `:1204`'s "also" tells the reader that the first list applies to the early-enable boots too.
  - `:1206-1210` say the MAAP-on boot requires the CRF talker, and that CRF frames leave, without the condition the code applies.
- Impact: no defect ships. In every boot, the stamp's own integrity is guarded by the octet comparison. But a reader is told that every frame of every boot has its destination and EtherType checked, and that CRF is graded in every config. Neither is true, and the README is the place round 1 asked to make exact.
- Required outcome, either:
  - (a) The text states what the leg checks. For example, `:1183` becomes "It grades every frame of the first boot (through the controller's and the listener's exchanges) on valid/ready at `m_axis_mac_tx`:". `:1204` becomes "In each early-enable boot it grades instead:". `:1207-1210` add "(CRF where the config declares the CRF Media Clock Output)". Or:
  - (b) `grade()`'s destination and known-protocol checks also run over the later boots' frames, and the text stays.
- Verification: the README lists match `sim_boot_sa.cpp:759-830` and `:549-618` line by line. For (b), `make -C tb/verilator/milan_dp bootsa` and `bootsa-mutants` stay green.

### S1 - SUGGESTION - Tests - name every check a control is known to fail

- `bootsa_mutants.py:116-118` names `[ON_MAAP, ON_CRF, OFF_AAF]` for the all-three control. It also fails `OFF_CRF` (got=10; my probe that names all four is caught, `receipts/mut_PROBE_together_all_four_early_enable_source_chec.log`).
- The destination-octet control and the last-beat control also fail `OCTETS` (`receipts/mut_the_stamp_lands_on_the_destination_octets_0_to_5.log`, `receipts/mut_the_stamp_s_beat_position_survives_a_frame_s_las.log`).
- Naming those checks would make each control assert everything it covers.

### S2 - SUGGESTION - Tests - use the exported offsets

- `gen_boot_fw.py` now exports `kMacAddrLo`/`kMacAddrHi`.
- `sim_boot_sa.cpp:862-863` still pass `0x108`/`0x10C`.
- `:617` and `:827` read `0x784` (`A_TXARB_DIAG`) as a literal.

### S3 - SUGGESTION - Tests - formatting

- `gen_boot_fw.py:112` reads `body ="".join(...)`. A space is missing after `=`.

### S4 - SUGGESTION - Tests - check label

- The check name `every frame is a known protocol's (octets 12 and 13 untouched)` (`sim_boot_sa.cpp:815`) predates this round.
- The classifier also reads octets 16 and 17 behind a C-TAG, and the AVTP subtype. The README now says so, but the label does not.

No new RESIDUE in the delta. The comment-rule scan of the added lines found no lane labels, round or reviewer IDs, or comment IDs. `TESTING.md`'s "every reviewer of a change" is the table's existing role wording.

## Per-lens results

```text
[R774] PASS Conformance — issue #839 acceptance 1-2 against sim_boot_sa.cpp:549-618 (early-enable boots) and :731-757 (probe PDU fields), receipts/bootsa_tree.log (67/0; first boot 868 frames and early-enable boots 850, all from the station MAC, none all-zero); README RTL citations checked against milan_datapath.sv:2214-2217,8818 and KL_maap.sv:123,189,307,392-395,477,487-489; acceptance 3-4 per the maintainer record issuecomment-6655611611; hdl/ unchanged (receipts/delta_scope.txt)
[R774] PASS RTL — receipts/delta_scope.txt (no hdl/, syn/, sw/, configs/ or submodule change in 992c3d7b..ba56827b, so round 1's RTL verdict carries); milan_datapath.sv:8916-8941 re-read for the comparison's soundness (combinational stamp, saturating position); probes "saturates one beat early" (got=799) and "never advances" caught, showing the saturation bound matters
[R774] PASS Robustness — sim_boot_sa.cpp:496-497 (reset clears the offered flags and the octet position), :431 (no transfer on a reset edge); early-enable boots = invalid order against configure_fabric(), MAAP on and off, config-dependent CRF (kCrfOutputDeclared); A_TXARB_DIAG 0 in both boots (receipts/bootsa_tree.log); probe retry bounded at five tries
[R774] PASS Tests — receipts/par_mutants.log: clean pass, all 12 shipped controls caught by name, plus 3 reviewer probes caught; receipts/bootsa_nomvrp.log (MVRP requirement live); author receipt author-r2/receipts/gates/lane/bootsa_mutants.log (sha256 prefix bf448e8d2e6887bc, matches its INDEX.md; 13 of 13) agrees; S1-S4 optional
[R774] MINOR Docs — tb/verilator/milan_dp/README.md:1183-1210 — F1; TESTING.md:277, CHANGELOG.md:70-76, bootsa_mutants.py banner, measure_test_evidence_readers.py:171-176 and the PR body's residue rows checked and accurate
```

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue acceptance and decision record; `sim_boot_sa.cpp` early-enable and probe code; README RTL citations against `milan_datapath.sv` and `KL_maap.sv`; `receipts/bootsa_tree.log` | R774-2 | ba56827bbfe4acadb84ca220616a76ad74611e7d |
| RTL | CLEAN | `receipts/delta_scope.txt` (RTL unchanged since R774-1's clean RTL lens at 992c3d7b); `milan_datapath.sv:8916-8941`; stamp-position probes | R774-2 | ba56827bbfe4acadb84ca220616a76ad74611e7d |
| Robustness | CLEAN | early-enable boots (MAAP on and off); reset handling in `reset()`/`stamp_edge()`; config-dependent CRF; `A_TXARB_DIAG` | R774-2 | ba56827bbfe4acadb84ca220616a76ad74611e7d |
| Tests | CLEAN | `sim_boot_sa.cpp`, `gen_boot_fw.py`, `bootsa_probes.vlt`, `bootsa_mutants.py`; `receipts/par_mutants.log`, `mut_*.log`, `bootsa_nomvrp.log`; author `gates/lane/bootsa_mutants.log` | R774-2 | ba56827bbfe4acadb84ca220616a76ad74611e7d |
| Docs | UNCLEAN (F1 MINOR open) | milan_dp `README.md`, `TESTING.md:277`, `CHANGELOG.md`, `bootsa_mutants.py` banner, `measure_test_evidence_readers.py`, PR body, issue REVIEW READY | R774-2 | ba56827bbfe4acadb84ca220616a76ad74611e7d |

## What I ran (pinned simulator Verilator 5.050 rev v5.050, identity checked)

| Run | Result | Receipt |
|---|---|---|
| `make bootsa`, head copy | rc 0, 67 checks, 0 failures | `receipts/bootsa_tree.log` |
| Head leg without `probe_tx()` | 65 checks, 1 failure: MVRP sent and graded | `receipts/bootsa_nomvrp.log`, `receipts/probe_nomvrp.diff` |
| Leg's 12 controls + 3 probes, 6 in parallel (`scripts/par_mutants.py`, using the tree's own `build`/`run_leg`/`verdict`) | clean pass, 15 of 15 caught | `receipts/par_mutants.log`, `receipts/mut_*.log`, `receipts/probe_mutant_extra.txt` |
| Head leg against the base-RTL datapath | does not build: the base lacks the nets the leg now probes (`crft_txs_tvalid_w`, `ctlg_src_tdata_w`); not evidence | `receipts/bootsa_base.rc`, `receipts/bootsa_base.log` |
| Exact-head hosted checks snapshot | 32 success, 1 skipped, 7 in progress, 0 failed at snapshot time | `receipts/hosted_checks_snapshot.txt` |
| Clone integrity after the review | HEAD, tree and index-tree are 72b663ff; no status lines; six gitlinks as recorded | `receipts/clone_integrity.txt` |

The round-1 probes, rerun at this head:
- The `plant_noxtra` plant is the shipped all-three control, and it is caught.
- The `plant_early_enable` shape is now the leg's own early-enable boots.
- PM3 (wrap) is the shipped wrap control, caught by the octet comparison alone.

No probe falsified a claim of the delta. All probe trees were copies under the packet's `scratch/`; the review clone was only read. Home-directory paths in the three build logs were replaced with `<home>` or `<pinned-verilator>`. `scripts/reproduce.sh` reruns everything.

## Real limits

- No manager source bank ran at this head, and I claim none. The source-head gate set (four sweep shards, firmware self-tests, builder, behave, docs gates) is the author's published receipts. I spot-checked only the `bootsa-mutants` receipt hash and tally.
- I did not rerun the full sweep, the builder, behave, Yosys or the docs gates; none is in this round's allowance.
- The base-RTL comparison is not possible with this leg, because it probes nets the fix introduced. The round-1 base run (9 of 40 failures) stands for that.
- I did not re-read the Milan v1.2 4.3.2, 4.3.3.1 and 5.5.2.2 or IEEE 1722.1-2021 8.2.1.4 clause texts the probe's comment cites. I checked the probe's behaviour and PDU layout, not the clause numbering.
- Physical calibration was not run. There is no hardware capture of a boot's first frames; per the maintainer record, the issue stays open for it.
- The hosted contexts were partly in progress at the snapshot. I report them; I do not accept them.

## Pending manager duties

- Carry F1 to the author. It needs a fix (a wording correction of `README.md:1183-1210`, or extending `grade()`) and a re-review of the Docs lens at the new head.
- The other lenses stay covered if the fix touches only the README. A change to `sim_boot_sa.cpp` un-covers Tests and Robustness.
- Optional: S1 to S4.
- The current-dev merge candidate (builder and native banks) at the merge turn, and hosted/act acceptance at the final head.
- The hardware capture for issue #839 at the next bench or lab run.

R774-2 FINISHED
