[R773] NEGATIVE - exact head 992c3d7bb37f4ade0b151c17d718baed0e119753

Round R773-1, internal cleared-context review of PR #841 (issue #839), exact head
`992c3d7bb37f4ade0b151c17d718baed0e119753`, tree `06bd3e03aece23b59ff01ebd641d1f4e4515a840`,
source base `604899c08ff1cd1830e1dd08b733109ef852400c` (ten commits). All five lenses applied.
Verdict NEGATIVE on two open MINOR findings (Tests: F1, F2; Docs: F2). Conformance, RTL and
Robustness are clean: the fix is correct in the RTL, and every probe that tried to make it
emit a wrong source address failed to. What is missing is test evidence for part of what the
PR says it proves.

Prior public review findings on this PR: none. The only review-side comment at this head is
the review-start notice (issuecomment-6654919293), which carries no findings; nothing to
resolve or retain.

Receipts are listed in `MANIFEST.sha256`; paths below are relative to this packet unless
they name the repository (`path:line` at the exact head).

## Findings

### F1 - MINOR - Tests - the hold on MAAP, AAF and CRF has no test that can fail without it

- Where: `tb/verilator/milan_dp/sim_boot_sa.cpp:573-574` (check "no CSR-addressed
  transmitter starts a frame before the station MAC is written") and
  `tb/verilator/milan_dp/bootsa_mutants.py:68-98` (the seven controls), against the hold at
  `hdl/milan/milan_datapath.sv:8817-8822`.
- Authority/evidence: AGENTS.md section 5 ("self-checking tests for changed behavior") and
  the section 6 Tests lens ("Each new test can fail for the defect it claims to detect").
  The check names all four held transmitters, but it can fail only for the processor lane:
  firmware enables AAF, MAAP and CRF in `configure_fabric()` *after* its MAC writes
  (`sw/firmware/milan_baremetal/milan_baremetal.c:1824-1836`), so they never try to start
  while the hold is closed.
  - Probe mutant PM1 removes the hold from MAAP, AAF and CRF only, keeping the processor
    lane held (`receipts/mutant-PM1_nohold_maap_aaf_crf.diff`). The shipped leg passes it,
    40 of 40, rc 0 (`receipts/run-PM1_nohold_maap_aaf_crf-Vmilan_dp_bootsa.log`).
  - A probe boot (`receipts/probe-harness.diff`, built by `scripts/make_probe_harness.py`)
    runs the firmware's own `configure_fabric()` with its two MAC_ADDR writes dropped, opens
    the AAF bypass, runs 600 processor ms, then writes the pair. Under PM1 it catches 16
    frames with source 00:00:00:00:00:00 before the pair (1 MAAP, 15 CRF), failing by name
    (`receipts/run-PM1_nohold_maap_aaf_crf-Vmilan_dp_bootsa_probe.log`).
  - At the head the same probe passes 46 of 46: no early frame; after the pair MAAP 5,
    AAF 1, CRF 814, all from the station MAC; A_TXARB_DIAG 0
    (`receipts/run-head-Vmilan_dp_bootsa_probe.log`). The RTL hold works.
- Impact: three of the four held sources rely on a hold nothing in the tree exercises. The
  README and PR acknowledge this ("the hold covers it; this leg does not drive it") without
  evidence. A later change can drop or mis-wire the hold on MAAP, AAF or CRF with every gate
  green. For those three, the acceptance-1 statement "the fix holds each transmitter" rests
  on reading, not on a test.
- Required outcome:
  - the leg (or one more boot in it) enables MAAP, AAF and CRF before the pair is written;
  - it grades that none of them starts before the pair and that each sends with the station
    MAC afterwards;
  - a planted control that removes the hold from those three fails it by name.
- Verification: `make -C tb/verilator/milan_dp bootsa bootsa-mutants` with the new control
  caught; the clean leg green.

### F2 - MINOR - Docs, Tests - the README credits the leg with "the stamp touched nothing but octets 6 to 11", which it does not check

- Where: `tb/verilator/milan_dp/README.md:1157-1158`. `docs/testing/TESTING.md:277` directs
  reviewers of any `ctl_sa_stamp` change to `bootsa-mutants`.
- Authority/evidence: the leg compares octets 0 to 5 (destination), 6 to 11 (source) and
  12/13 (EtherType), and reads 14/15 to classify (`sim_boot_sa.cpp:123-160, 543-590`).
  - Probe mutant PM3 makes the stamp's beat position wrap instead of saturating
    (`milan_datapath.sv:8928`; `receipts/mutant-PM3_stamp_wraps.diff`). This overwrites
    octets 38 to 43, 70 to 75, ... of every long control-lane frame.
  - The leg passes PM3, 40 of 40, rc 0 (`receipts/run-PM3_stamp_wraps-Vmilan_dp_bootsa.log`).
  - The property is true at the head: the counter saturates at TX_SA_BEATS_C, outside the
    stamp loop's range (`milan_datapath.sv:8921-8941`). The default-sweep `obj_notify` leg
    catches PM3 with 146 failures (`receipts/run-notify-PM3_stamp_wraps.log`; head 499 of
    499, `receipts/run-notify-head.log`).
- Impact: no defect ships. But the README attributes to this leg a property it cannot
  detect, and TESTING.md routes future stamp reviewers to it, so the reader is told the
  wrong guard.
- Required outcome, either:
  - (a) the leg compares every control-lane octet outside 6 to 11 with what entered the
    stamp, and a beat-position-wrap control fails it by name; or
  - (b) README.md:1157-1158 (and the TESTING.md:277 row if it relies on it) states exactly
    which octets the leg compares and names the leg that guards payload integrity.
- Verification: (a) `bootsa-mutants` with the new control caught; (b) the text matches
  `sim_boot_sa.cpp`'s checks.
- Recorded MINOR rather than RESIDUE because the sentence is a claim about what a test
  proves, and I am not certain that counts as wording only.

### RES-1 - RESIDUE - Docs - the area figure's head is recorded as the review head

- Where: the issue's `[A731] REVIEW READY` comment (issue #839, issuecomment-6654836727)
  says "Validation (all at 992c3d7b, each on a clean clone of the head)" and lists the area
  delta. The published `review-evidence/839-r1/author/receipts/area/AREA.md` records the head
  run at `8d2dfb65`.
- Why it is only wording: `git diff --stat 8d2dfb6547 992c3d7bb3` changes only
  `tb/verilator/milan_dp_render/sim_tdm8_render.cpp`, which out-of-context synthesis does not
  read, so the figure is the head's. The figures match the reports exactly
  (`receipts/area-util-{base,head}-extract.txt`; source hashes in
  `receipts/area-util-source-sha256.txt`):

  | Resource | Base | Head | Delta |
  |---|---:|---:|---:|
  | LUTs | 45,176 | 45,275 | +99 |
  | Registers | 40,222 | 40,233 | +11 |
  | F7 muxes | 805 | 920 | +115 |
  | F8 muxes | 104 | 109 | +5 |
  | Block RAM | 27.5 | 27.5 | 0 |
  | DSP | 13 | 13 | 0 |

- Exact fix: add to the PR body's area paragraph, and as a correction under the REVIEW READY
  comment: "The head synthesis ran at `8d2dfb65`. `992c3d7b` differs from it only in
  `tb/verilator/milan_dp_render/sim_tdm8_render.cpp`, which synthesis does not read."

### S1 - SUGGESTION - Tests - make the coverage checks cover CRF and MVRP

`sim_boot_sa.cpp:591-597` requires MSRP, gPTP, ADP, AECP, ACMP, MAAP and AAF to be "sent and
graded", but not CRF or MVRP.

- CRF: 781 frames here, but a silent CRF would go unnoticed.
- MVRP: no frame leaves in the leg's window, so "every MVRP frame's source address is the
  station MAC" is vacuous. MVRP shares the stamped control lane, so it is covered
  structurally.

Requiring CRF where the config declares it, and driving or explicitly excluding MVRP, would
remove the vacuity.

### S2 - SUGGESTION - Docs - link the maintainer decision record

The PR body states "Maintainer decision (2026-11-05): both readings are accepted". No
maintainer-authored comment on the issue or PR carries it. A link to the record would let a
cold reviewer trace it.

## Lens coverage (clean results with their artifacts)

```text
[R773] PASS Conformance — issue #839 acceptance 1-4 against hdl/milan/milan_datapath.sv:3106-3115,8815-8822,8915-8941; hdl/common/csr/milan_csr.sv:1117-1145,1682-1683; sw/builder/endstation_builder.py:3280-3305,5931-5938; sw/litex/boot_policy.py:35-49; receipts/run-head-Vmilan_dp_bootsa.log; receipts/run-base-Vmilan_dp_bootsa.log; receipts/gptp_rom_vs_fw_mac.txt; PR body "Relates to #839"
[R773] PASS RTL — hdl/milan/milan_datapath.sv @992c3d7b (diff 604899c0..992c3d7b, every driver of the eight gated nets, generate tie-offs, reset and clock of mac_addr_seq vs milan_csr, stamp widths/indexing for TDATA_WIDTH/8 octets per beat), hdl/ieee17221/adp/adp_tx_arbiter.sv:125-126, protocol-processor/hdl/packet_engine/KL_pp_tx_arbiter.sv:33-43, published util/timing reports
[R773] PASS Robustness — receipts/run-head-Vmilan_dp_bootsa_probe.log (sources enabled before the pair), receipts/run-PM4_reclose_on_mac_ctrl-Vmilan_dp_bootsa.log (re-close caught, 12 failures), sim_boot_sa.cpp pair_order boots, sw/litex/milan_soc.py:857 (datapath reset = milan domain system reset), milan_baremetal.c:1894-1916 (identity-mismatch path holds), endstation_builder.py:3302-3305 (zero/group MAC refused)
```

What each clean lens rests on:

- **Conformance.**
  - *Acceptance 1.* All four CSR-addressed sources are held: `pp_tx_*`, `maap_tx_*`,
    `aaf_tx_*` and `crft_tx_*`, the only inputs of the two first-stage merges
    (`milan_datapath.sv:8832-8879`). The gPTP plane is the only other source into
    `gptp_ctl_mux`/`adp_tx_mux` (`:9083-9154`). It has no CSR MAC input; its source address
    is ROM constants built from `--mac` (`gptp-processor/hdl/ucode/gen_gptp_ucode.py:1537-1538`).
    The SoC MAC is a bare MAC core fed only by the datapath (`milan_soc.py:1601-1606, 1807`).
  - *gPTP ROM vs firmware MAC.* For each of the 5 tracked configs, the builder's
    `gptp_ucode.hex` is byte-identical to a ROM regenerated from the MAC that
    `fabric_constants()` hands the firmware, at the build's clock and priority1; a one-bit
    MAC flip makes it differ (`receipts/gptp_rom_vs_fw_mac.txt`). Both values come from
    `cfg["platform"]["mac_address"]` in one builder run (`endstation_builder.py:2677, 5933`).
  - *Acceptance 2.* Head leg 40 of 40, 831 frames, first frame MSRP at cycle 40112 after the
    MAC completes at 40088. The head leg against the base RTL fails 9 of 40, first
    `#0 MSRP cycle 20198 source 000000000000`, as the author claims. The author's seven
    controls are caught, 8 of 8 (`receipts/bootsa-mutants.log`).
  - *Acceptance 3.* No port change: the first hunk is at line 784, after the port list. No
    `milan_csr` change; VERSION unchanged.
  - *Acceptance 4.* The two maintainer-accepted readings (no register-map generator; no
    hardware capture yet, so the PR relates to #839 and does not close it) are stated in the
    PR body, the REVIEW READY comment and "Known limitations".
  - *Clause citations* are consistent with how the tree already cites 802.1Q 35.2.2.1 and
    Milan 5.6.3.5.2.
- **RTL.**
  - `mac_addr_seq` keys on `s_axi_awvalid && s_axi_awready`, which is exactly `milan_csr`'s
    `wr_fire` (AWREADY = wr_fire, same 16-bit decode, WSTRB ignored). Same clock and reset
    (axis_clk/axis_resetn), so flags and `mac_alo/ahi` update on the same edge.
  - The hold only rises, so it never cuts a frame. Arbiters see tvalid 0, so no watchdog
    counts; the processor's internal TX arbiter has no watchdog by design.
  - The tready half of the hold is redundant but harmless: PM2 is an equivalent mutant,
    because the arbiter's `s_*_tready` needs an active grant.
  - The stamp writes only lanes at frame position 6 to 11, with a saturating counter that
    resets on tlast. PM3 shows the saturation matters; the sweep catches its loss (F2).
  - Area figures match the reports (RES-1).
- **Robustness.**
  - With sources enabled before the pair, the hold keeps AAF, MAAP and CRF back. After
    release every frame carries the station MAC and A_TXARB_DIAG stays clean; no wedge after
    600 processor ms held.
  - Either-half-alone opens nothing, and a re-close mutant is caught.
  - Nothing re-closes the hold except the datapath reset, which is the milan domain's system
    reset (`milan_soc.py:857`), after which firmware writes the pair again.
  - The identity-mismatch boot never writes the pair, leaving the fabric disabled as its
    message says.
  - Rewriting the MAC after boot is not atomic across the two words; this is documented on
    the MAC_ADDR rows and in the PR.

## Harness edits (point 3)

The MAC writes added to `capture_coherence/sim_dp.cpp`, `milan_dp/sim_nxn.cpp`,
`milan_dp/sim_gptp.cpp` and `milan_dp_render/sim_tdm8_render.cpp` write the all-zero address
those legs already used. They stand in for `configure_fabric()`, which the product runs first
after the identity check on every system reset. None of those legs grades the source address,
so the writes mask no source-address defect.

The render leg's second write follows four datapath resets. The arms before it grade render
epochs, not processor TX (the author's receipt shows 263 of 263). The datapath resets only
with the system clock domain (`milan_soc.py:857`), so the product has no
reset-without-reboot path that would leave the hold closed.

Comment rule: the added source comments carry no bench lane label, lane name, review round,
reviewer ID or issue-comment ID ("lane" in them is the datapath's control/data lane). All ten
commit messages are one line with no trailers, and `git diff --check` is clean.

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #839 acceptance 1-4 and comments; `milan_datapath.sv` gate/seq/stamp; `milan_csr.sv` write path; builder MAC/ROM path; `boot_policy.py`; `receipts/run-head-*`, `run-base-*`, `gptp_rom_vs_fw_mac.txt`, `bootsa-mutants.log` | R773-1 | 992c3d7bb37f4ade0b151c17d718baed0e119753 |
| RTL | CLEAN | `hdl/milan/milan_datapath.sv` diff and nets; `adp_tx_arbiter.sv`; `KL_pp_tx_arbiter.sv`; `receipts/run-PM2_*`, `run-PM3_*`; area util/timing reports | R773-1 | 992c3d7bb37f4ade0b151c17d718baed0e119753 |
| Robustness | CLEAN | `receipts/run-head-Vmilan_dp_bootsa_probe.log`, `run-PM4_*`; pair-order boots; `milan_soc.py:857`; `milan_init()` | R773-1 | 992c3d7bb37f4ade0b151c17d718baed0e119753 |
| Tests | UNCLEAN (F1, F2) | `sim_boot_sa.cpp`, `gen_boot_fw.py`, `bootsa_probes.vlt`, `bootsa_mutants.py`, Makefile/pool wiring, four harness edits; `receipts/run-PM1_*`, `run-PM3_*`, `run-notify-*` | R773-1 | 992c3d7bb37f4ade0b151c17d718baed0e119753 |
| Docs | UNCLEAN (F2; RES-1 is residue) | `REGISTER_MAP.md` MAC_ADDR rows, `BAREMETAL_FIRMWARE.md`, `TESTING.md`, milan_dp `README.md`, `CHANGELOG.md`, PR body, REVIEW READY comment, published `AREA.md` | R773-1 | 992c3d7bb37f4ade0b151c17d718baed0e119753 |

## What I ran (reviewer receipts)

Verilator 5.050 (identity and wrapper hash in `receipts/builds-summary.txt`). Builds went
through the Makefile's own `bootsa-build`/`notify-build` recipes in the review clone, with
object directories and mutated sources outside it.

| Run | Result | Receipt |
|---|---|---|
| Clean `bootsa`, head | 40/40, rc 0, 831 frames | `receipts/bootsa-head.log`, `run-head-Vmilan_dp_bootsa.log` |
| Head leg on base datapath | 9/40 fail, first `#0 MSRP cycle 20198 source 000000000000` | `receipts/run-base-Vmilan_dp_bootsa.log` |
| `bootsa_mutants.py` (author's campaign) | 8 checks, 8 PASS | `receipts/bootsa-mutants.log` |
| Probe boot (early enables), head | 46/46 | `receipts/run-head-Vmilan_dp_bootsa_probe.log` |
| PM1, no hold on MAAP/AAF/CRF | leg 40/40 (survives); probe 1 FAIL, 16 zero-source frames | `receipts/run-PM1_*` |
| PM2, processor tready ungated | 40/40, identical frame list (equivalent) | `receipts/run-PM2_*` |
| PM3, stamp position wraps | bootsa 40/40 (survives); notify 146 failures | `receipts/run-PM3_*`, `run-notify-PM3_*` |
| PM4, MAC_CTRL write re-closes the hold | 12 failures | `receipts/run-PM4_*` |
| notify leg, head | 499/499 | `receipts/run-notify-head.log` |
| Builder gPTP ROM vs firmware MAC, 5 configs | all SAME; one-bit flip differs | `receipts/gptp_rom_vs_fw_mac.txt` |

- Scripts: `scripts/plant_mutants.py`, `scripts/make_probe_harness.py`,
  `scripts/build_variants.sh`, `scripts/gptp_rom_vs_fw_mac.py`.
- After the probes the clone is back to exact head bytes: HEAD, tree, index tree and the five
  submodule gitlinks match, with no tracked change and no untracked or ignored files
  (`receipts/restore-check.txt`).

## Real limits

- The full sweep, firmware self-tests, builder, behave, LiteX, Yosys and Vivado were not
  rerun. They are the author's published receipts at `992c3d7b` (area at `8d2dfb65`, RES-1).
  I spot-read behave (508 scenarios / 2330 steps, rc 0) and `bootsa_mutants` (8/8, rc 0).
- Simulation only. No hardware boot capture; physical calibration NOT RUN; field skips are
  not hardware proof.
- No manager source bank exists at this head, and none is claimed.
- The probe harness and mutants are reviewer artifacts, not tree content.
- Clause wording was checked against the tree's existing citations, not against the
  standards' text.

## Pending manager duties

- Hosted checks at this head were still running when sampled: rtl-fast queued, 20 in
  progress, 6 queued, 29 success, 1 skipped (`receipts/hosted-checks.tsv`). Hosted and act
  acceptance remain the manager's.
- The current-dev merge-candidate builder and native banks remain the manager's (base
  `604899c0` = live dev).
- RES-1 goes to the residue checklist; S1 and S2 are optional.
- F1 and F2 need a fix and re-review at a new head. A later commit touching
  `milan_datapath.sv` or the leg un-covers RTL, Robustness and Tests for that head.

R773-1 FINISHED
