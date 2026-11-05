[R773] POSITIVE - exact head ba56827bbfe4acadb84ca220616a76ad74611e7d

Round R773-2, internal independent review of PR #841 (issue #839) at exact head
`ba56827bbfe4acadb84ca220616a76ad74611e7d`, tree `72b663ff0c6a45d2fe95606b9cdb7d40303e8bec`.
Base and live `dev`: `604899c08ff1cd1830e1dd08b733109ef852400c`. The delta reviewed is
`992c3d7b..ba56827b` (four commits). It changes eight files: the `bootsa` leg
(`sim_boot_sa.cpp`, `gen_boot_fw.py`, `bootsa_probes.vlt`), `bootsa_mutants.py`, the milan_dp
README, `TESTING.md`, `CHANGELOG.md` and `scripts/measure_test_evidence_readers.py`. Nothing
under `hdl/`, `syn/`, `sw/` or `configs/` changes, and no submodule gitlink moves
(`git diff --stat 992c3d7b HEAD -- hdl syn sw configs <six submodules>` is empty).

Scope, per the round 2 assignment on issue #839: the delta, and each round 1 finding judged
at its cause. RTL the delta does not touch keeps its round 1 verdict (R773-1, CLEAN at
`992c3d7b`), because nothing it depends on changed. All five lenses were applied to the delta.

Verdict: no open BLOCKER, MAJOR or MINOR. Both round 1 MINORs (F1, F2) are fixed at their
cause, and the reviewer probes confirm the fixes. Both suggestions were taken and both residue
texts applied. This round leaves one RESIDUE and four SUGGESTIONS.

## Round 1 findings, resolved or retained at this head

| Round 1 item | State at ba56827b | Evidence |
|---|---|---|
| R773-1 F1 = R774-1 F1 (MINOR, Tests): nothing can fail without the hold on MAAP, AAF and CRF | **Resolved** | See F1 below |
| R773-1 F2 (MINOR, Docs, Tests): README credits the leg with "the stamp touched nothing but octets 6 to 11" | **Resolved**, option (a) | See F2 below |
| R773-1 S1 / R774-1 S1 (SUGGESTION): require CRF, drive or exclude MVRP | **Taken** | `sim_boot_sa.cpp:816-826`: CRF is required when `kCrfOutputDeclared` (generated `true` for the leg's config, `obj_bootsa/boot/boot_fw.h:23`). MVRP is driven by `probe_tx()` (`:731-757`) and required. Clean leg: `MVRP 1`, `[ ok ] ... MVRP frames were sent and graded`, `... CRF frames were sent and graded` (`receipts/bootsa-head.log`) |
| R773-1 S2 (SUGGESTION): link the decision record | **Taken** | PR body, Linked Issue paragraph: `[issuecomment-6655611611](../issues/839#issuecomment-6655611611)`. That comment is the `[A10]` maintainer decision record |
| R773-1 RES-1 = R774-1 R2 (RESIDUE): area head | **Applied exactly** | PR body area paragraph: "The head synthesis ran at `8d2dfb65`. `992c3d7b` differs from it only in `tb/verilator/milan_dp_render/sim_tdm8_render.cpp`, which synthesis does not read." That is R773-1's text verbatim. The added claim also checks out: `git diff --stat 8d2dfb65 HEAD -- hdl syn configs protocol-processor gptp-processor third_party` is empty |
| R774-1 R1 (RESIDUE): the two "pending a maintainer" phrases | **Applied exactly** | Known limitations and Definition of Done both read "accepted by the maintainer on 2026-11-05 (no register-map generator; no hardware capture yet, so this PR relates to #839)". No "pending a maintainer" remains. No "close"/"closes" sits beside an issue number in the PR body or the four commit subjects |

### F1, resolved at its cause

- **The cause.** Nothing could enable MAAP, AAF or CRF while the pair was unwritten, so the
  hold at `milan_datapath.sv:8817-8822` was never exercised.
- **The fix.** `early_enable()` (`sim_boot_sa.cpp:549-618`) writes `MAAP_CTRL`,
  `AAF_CTRL | AAF_CTRL[1]` and `CRFT_CTRL` at reset release. It takes the firmware's own boot
  words and CSR offsets, which `gen_boot_fw.py` now exports from `milan_baremetal.c`. It then
  holds the pair unwritten for 400 processor ms before writing it.
- **Clean leg** (`receipts/bootsa-head.log:498-527`):
  - MAAP-on boot: offered while held "MAAP yes, AAF no, CRF yes; 0 frames left". 847 frames
    followed the pair, all from the station MAC.
  - MAAP-off boot: offered while held "AAF yes, CRF yes; 0 frames left". The AAF talker
    therefore does offer a frame inside the held window.
- **Why AAF cannot offer in the MAAP-on boot.** I checked every RTL line the README cites
  against this head's blobs:
  - `aaf_gate` needs `~cfg_maap_enable | maap_addr_valid` (`milan_datapath.sv:2214-2217`).
  - `addr_valid_o = (state_r == ANNOUNCE_S)` (`KL_maap.sv:189`).
  - The only `state_r <= ANNOUNCE_S` is at `:489`, inside the `timer_ms_r == '0 && !tx_busy_r`
    PROBE send (`:477`), after `PROBE_SENDS_C` = 4 probes (`:123`).
  - `tx_busy_r` is `m_axis_tvalid` (`:307`) and is cleared only on an accepted last beat
    (`:392-395`).
  - The hold gives MAAP `tready` 0 (`milan_datapath.sv:8818`).
  - So the README's statement that "a held MAAP never leaves PROBE" is true at this head.
- **The planted controls.**
  - My round 1 probe PM1 (hold removed from MAAP, AAF and CRF) now fails 10 checks, by name
    (`receipts/run-PM1_nohold_maap_aaf_crf.log`):
    - `early-enable, MAAP on: no MAAP frame leaves ...` got=1
    - `... MAAP on: no CRF frame ...` got=10
    - `... MAAP off: no AAF frame ...` got=62
    - `... MAAP off: no CRF frame ...` got=10
    - plus the all-zero, CSR-addressed and station-MAC checks of both boots.
  - In round 1 the same mutant passed 40 of 40.
  - The author's four new hold controls are caught by every check they name
    (`receipts/bootsa-mutants.log`).
  - R774-1's `plant_noxtra` has PM1's shape. `plant_early_enable` (a harness that enables the
    three early) is now the leg's own `early_enable()`, so the leg itself subsumes it.

### F2, resolved at its cause (option a)

- **The cause.** The leg compared only octets 0-5, 6-11 and 12-13, so a stamp that wrote
  payload octets went undetected.
- **The fix.** `stamp_edge()` (`sim_boot_sa.cpp:429-452`) runs on the stamp's own
  `ctlg2_tvalid && ctlg2_tready`, in every boot, and skips reset edges (`:431`). It compares
  each kept octet at frame position outside 6-11 between `ctlg_src_tdata_w` (the IFG gasket's
  output) and `ctlg2_tdata`.
- **Why the comparison is sound.** `ctl_sa_stamp` is `always_comb`
  (`milan_datapath.sv:8934-8941`), so its input and output on the same handshake are the same
  beat. `tick()` samples after the low-phase eval and before the posedge, as `tx_edge()` does.
  `reset()` zeroes the harness position (`:497`).
- **Clean leg:** 93 frames, 3556 octets compared, 0 changed.
- **The planted controls.**
  - PM3 (beat position wraps) fails `every control-lane octet outside 6 to 11 leaves the stamp
    as it entered` by name. It reports got=126, first at frame 1 octet 38, the octets round 1
    predicted (`receipts/run-PM3_stamp_wraps.log:99-101`). In round 1 the leg passed PM3,
    40 of 40.
  - New probe PM5 flips one bit of control-lane octet 15 and leaves the addresses and EtherType
    intact (`receipts/mutant-PM5_octet15_bitflip.diff`). It fails the same check by name:
    got=136, first at frame 0 octet 15 (`receipts/run-PM5_octet15_bitflip.log:100-102`). This
    shows the comparison is not tuned to PM3 alone.
- **The docs.**
  - The old README sentence is gone. No file in the tree or the PR body still says "touched
    nothing" or "nothing but octets".
  - README `:1183-1197` now states the EtherType/subtype check and the destination check per
    protocol, matching `grade()` (`sim_boot_sa.cpp:808-816`, `:150-169`).
  - README `:1199-1202` states the octet comparison exactly as `stamp_edge()` performs it.
  - `TESTING.md:277` now names both new control families and the check that catches each.

## Findings

### RES-1 - RESIDUE - Docs - tb/verilator/milan_dp/README.md:1183 - the graded-frame list reads as covering every boot

- **Evidence.** The list after "It grades every frame on valid/ready at `m_axis_mac_tx`:"
  follows the paragraphs describing all five boots. `grade()` runs once, after `probe_tx()`
  and before `pair_order()` (`sim_boot_sa.cpp:860-864`), so these items apply to the first
  boot's frames only:
  - the destination check;
  - the known-protocol check;
  - "sent and graded";
  - "the processor offered".

  The later boots grade their own lists: `pair_order()`, and the early-enable list at
  README `:1204`, which the word "also" ties to the main list.
- **Why it is only wording.** Every listed property is checked by the leg. The control lane of
  the later boots is still covered by the octet comparison, which the README correctly says
  runs "in every boot". No test, figure or verdict changes.
- **Exact fix.** At README `:1183`, replace "It grades every frame on valid/ready at
  `m_axis_mac_tx`:" with "In the first boot, up to and past the first ENTITY_AVAILABLE and
  the probe, it grades every frame on valid/ready at `m_axis_mac_tx`:". At `:1204`, replace
  "In each early-enable boot it also grades:" with "In each early-enable boot it grades:".

### S1 - SUGGESTION - Tests - tb/verilator/milan_dp/sim_boot_sa.cpp:812, :815 - check names still say "octets 0 to 5 untouched" / "octets 12 and 13 untouched"

The classifier also accepts a C-TAG and reads octets 16-17 (`:153`), as the README now
says. Since the octet comparison is the real guard of untouched octets, the parentheticals
could be dropped or made to say "destination" and "EtherType". The names are matched by
`bootsa_mutants.py`, so change both together.

### S2 - SUGGESTION - Docs - tb/verilator/milan_dp/README.md:1207-1208 - CRF's condition

The early-enable bullet requires "MAAP and the CRF talker" and "the AAF talker and the CRF
talker". The code requires CRF only when `kCrfOutputDeclared` (`sim_boot_sa.cpp:568`, `:608`).
The statement is exact for the leg's one fixed config (`BOOTSA_CFG`, which declares CRF).
Adding "(CRF where the config declares its Media Clock Output)" would keep it exact if the
config changes.

### S3 - SUGGESTION - Tests - tb/verilator/milan_dp/gen_boot_fw.py:112 - spacing

`body ="".join(...)` should read `body = "".join(...)`. This is cosmetic only.

### S4 - SUGGESTION - Tests - receipts/run-PM2_pp_tready_ungated.log - PM2 still passes, as expected

PM2 lets the processor lane's `tready` through while its `tvalid` stays held. The leg still
passes it, 67 of 67. Round 1 classified PM2 as an equivalent mutant (the arbiter's
`s_*_tready` needs an active grant), and the RTL behind that has not changed. This is recorded
only so a later reader does not mistake the pass for a gap. No change is required.

## Lens results (clean lines with artifacts)

```text
[R773] PASS Conformance — issue #839 acceptance 1-4 and the [A10] decision record (issuecomment-6655611611) against receipts/bootsa-head.log (main boot 868 frames incl. MVRP 1 and CRF 786; both early-enable boots: 0 frames before the pair, every frame from the station MAC), receipts/run-PM1_nohold_maap_aaf_crf.log, PR #841 body (Relates to #839, decision link, accepted wording), hdl/ unchanged 992c3d7b..ba56827b
[R773] PASS RTL — hdl/milan/milan_datapath.sv:2214-2217,8815-8822,8923-8941 and hdl/ieee1722/maap/KL_maap.sv:123,189,307,392-395,456-493 at ba56827b (no hdl change in the delta; every RTL line the README cites verified; the round 1 RTL verdict at 992c3d7b stands since nothing it depends on changed); bootsa_probes.vlt adds read-only public_flat_rd taps only
[R773] PASS Robustness — sim_boot_sa.cpp:549-618 early_enable (sources enabled at reset release, before any MAC write: the order configure_fabric() never uses), :477-500 reset() clears the per-boot flags and the stamp position, :431 stamp_edge skips reset edges; receipts/run-PM4_reclose_on_mac_ctrl.log (re-close caught, 16 failures); receipts/run-PM2_pp_tready_ungated.log (equivalent mutant, unchanged)
[R773] PASS Tests — receipts/bootsa-head.log (67/67, rc 0), receipts/bootsa-mutants.log (13 checks: 13 PASS, 0 FAIL; all five new controls caught by every named check), receipts/run-PM1…PM5 (PM1, PM3, PM5 fail the new checks by name; PM4 caught; PM2 equivalent), bootsa_mutants.py:69-132 against milan_datapath.sv fragments (each matched once)
[R773] PASS Docs — tb/verilator/milan_dp/README.md:1143-1237, docs/testing/TESTING.md:277, CHANGELOG.md:70-76, scripts/measure_test_evidence_readers.py:170-176, PR #841 body against sim_boot_sa.cpp checks; receipts/docs-check_doc_style.log, docs-measure_test_evidence.log, docs-docs_check.log (all rc 0); RES-1 is residue only
```

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #839 acceptance and decision record. Clean-leg frame tallies. Early-enable boots. PM1. PR body | R773-2 | ba56827bbfe4acadb84ca220616a76ad74611e7d |
| RTL | CLEAN | `milan_datapath.sv` gate, stamp and `aaf_gate`. The `KL_maap.sv` PROBE/ANNOUNCE path. `bootsa_probes.vlt` taps. No `hdl/` delta | R773-2 (delta). R773-1 for the unchanged RTL | ba56827bbfe4acadb84ca220616a76ad74611e7d (R773-1 at ancestor 992c3d7b; nothing in RTL scope changed since) |
| Robustness | CLEAN | `early_enable()`, `reset()`, `stamp_edge()` reset handling. PM2, PM4 | R773-2 | ba56827bbfe4acadb84ca220616a76ad74611e7d |
| Tests | CLEAN (S1, S3, S4 optional) | `sim_boot_sa.cpp`, `gen_boot_fw.py`, `bootsa_mutants.py`. Clean leg 67/67. Campaign 13/13. PM1-PM5 | R773-2 | ba56827bbfe4acadb84ca220616a76ad74611e7d |
| Docs | CLEAN (RES-1 is residue, S2 optional) | README `#839` section. `TESTING.md:277`. `CHANGELOG.md`. Evidence-reader disposition. PR body. Doc gates I could run | R773-2 | ba56827bbfe4acadb84ca220616a76ad74611e7d |

## What I ran (reviewer receipts, all at ba56827b, scoped Verilator 5.050)

Each run used a copy of the exact head (git metadata included) under the packet's
`scratch/`. The review clone was never built in.

| Run | Result | Receipt |
|---|---|---|
| `make bootsa` (clean leg) | 67/67, rc 0, 1m18s | `receipts/bootsa-head.log`, `.rc` |
| `python3 bootsa_mutants.py` (author campaign) | `13 checks: 13 PASS, 0 FAIL`, rc 0, 12m00s | `receipts/bootsa-mutants.log`, `.rc` |
| PM1 hold off MAAP/AAF/CRF | 10 failures, incl. the four early-enable source checks by name | `receipts/run-PM1_nohold_maap_aaf_crf.log` |
| PM2 processor `tready` ungated | 67/67 pass (equivalent mutant) | `receipts/run-PM2_pp_tready_ungated.log` |
| PM3 stamp position wraps | 1 failure, the octet comparison, got=126 | `receipts/run-PM3_stamp_wraps.log` |
| PM4 MAC_CTRL write re-closes the hold | 16 failures | `receipts/run-PM4_reclose_on_mac_ctrl.log` |
| PM5 (new) octet 15 bit flip in the stamp | 6 failures, incl. the octet comparison, got=136 | `receipts/run-PM5_octet15_bitflip.log` |
| `check_doc_style.py`, `measure_test_evidence.py --check`, `docs_check.py` | all rc 0 | `receipts/docs-*.log` |
| `gen_toc.py --verify-anchors/--check` | NOT RUN: the pinned Markdown renderer (html5lib) is not installed here, and installing it is out of scope | `receipts/docs-toc.log`, `.rc` (2) |
| Author round-2 receipts, sha256 against the published `MANIFEST.json` at f2049361 | 4 of 4 MATCH (`gates/lane/bootsa_mutants.log`, `gates/sweep/shard-0/bootsa-section-of-milan_dp.log`, `dev/run-mvrp-probe.log`, `dev-mutants/campaign-subset.log`) | `receipts/evidence-spotcheck.txt` |
| Hosted check runs at the exact head (snapshot) | 6 success, 1 skipped (Physical gPTP, nightly/manual), 44 queued or in progress | `receipts/hosted-checks.tsv` |
| Restore | Review clone HEAD, tree, index (`git write-tree` = `72b663ff`) and six submodule gitlinks match the exact head; 0 status entries | `receipts/restore-check.txt` |

Scripts: `scripts/plant_mutants_r2.py` (PM1-PM5), `scripts/run_pm.sh`,
`scripts/run_campaign.sh`.

## Real limits

- Hosted contexts were mostly queued or running at snapshot time. I claim no hosted verdict.
- I ran no full sweep, firmware, builder, behave or Yosys bank. For those, the source-head
  evidence is the author's published gate receipts, which I spot-checked only.
- I did not read the Milan/IEEE clause texts cited for the MVRP probe (Milan v1.2 4.3.2,
  4.3.3.1, 5.5.2.2, Table 5.33; IEEE 1722.1-2021 8.2.1.4). The probe's behaviour is shown
  executably (`SUCCESS`, then one MVRP frame, from the station MAC with the protocol's
  destination), not proven against the clause.
- I did not run the TOC gate (renderer missing).
- Physical calibration and a hardware boot capture were NOT RUN. Acceptance 4's hardware part
  stays open by the maintainer decision, and simulation is not hardware proof.

## Pending manager duties

- Hosted and act acceptance at the exact head.
- The current-dev merge candidate (builder and native banks) at the merge turn, with its
  receipts linked on the PR.
- Carry RES-1 to the residue checklist.
- The hardware capture for #839 at the next bench run. The issue stays open, and the PR
  relates to it.

R773-2 FINISHED
