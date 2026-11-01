[R761] NEGATIVE - exact head 4cda0aa03b11462f4f8750289f0999d5288b3546

Tree `63924b8ce668a9e4e21cb0701a8586fb085551d9`, issue #829, PR #831, round R761-1, base and live dev `1f29f189279f9fc0132f4918e47342b87d22f33a`.

**The logic is right; the head does not pass the gates.** The fault, the fix, the 3770 ns correction, the bound table, the receive distances and the generated chain all reproduce independently, and GMII behaviour is unchanged. Two mandatory documentation-workflow gates that are green on the base are red at this head: `check_doc_style.py` and `check_cpp_idiom.py`. The first one already failed the hosted run and cancelled the exhaustive jobs. There are also five MINOR findings: a false statement about GMII `ready`, two test weaknesses on the MII shape, a false check label, and evidence figures that do not trace to this head.

## Findings

### F1. MAJOR. Lenses: Docs, Tests
- **Where:** `docs/design/GPTP_PLANE.md:276-342`, `CHANGELOG.md:11,56-63`. Gate: `.github/workflows/docs.yml:227`.
- **Evidence:** `python3 scripts/check_doc_style.py` gives rc 1, `documentation style: FAIL (28 findings)`, all on lines this PR adds. The base gives rc 0, `OK (23 current documents)`. Hosted `docs-gates-0` failed on the same gate at this head, and fail-fast cancelled the Verilator shards and elaborate legs. Receipts: `receipts/gates/check_doc_style-head.log`, `check_doc_style-base.log`, `receipts/hosted-status.txt`, `receipts/hosted-docs-failure-tail.txt`.
- **Why it is not residue:** the fix is rewording, but the defect changes a required gate's verdict, so the wording exception does not apply. The PR's "GREEN locally" table lists `docs_check`, `gen_toc --check` and `check_gptp_docs`, not this gate.
- **Impact:** the head cannot merge, and no exhaustive hosted evidence exists for it.
- **Required outcome:** the added text passes the gate with its facts unchanged, and the complete documentation workflow is recorded in the PR.
- **Verification:** `check_doc_style.py` and its `--selftest` rc 0, and hosted `docs-gates-0` green on the new head.

### F2. MAJOR. Lens: Tests
- **Where:** `tb/verilator/gptp_txts/Makefile:90`, `-CFLAGS "-DGPTP_TXTS_MII"`. Gate: `.github/workflows/docs.yml:391`.
- **Evidence:** `python3 scripts/check_cpp_idiom.py` gives rc 1, `build without warnings 1 > ratchet 0`. The base gives rc 0, `0 <= 0`. `makefiles_without_warnings()` names this one file with `-Wall -Wextra`. The hosted run was cancelled before reaching this gate, so only this local run shows it. Receipts: `receipts/gates/docsyml/cppidiom.log`, `receipts/gates/cppidiom-base.log`.
- **Impact:** a second red gate would stop the head once F1 is fixed. The compile itself still gets the warning flags through `VFLAGS`, so this is a gate failure and not lost compiler coverage.
- **Required outcome:** the recipe satisfies the Rule 11 ratchet, and the ratchet is not raised.
- **Verification:** `check_cpp_idiom.py` rc 0 at `build without warnings: 0 <= 0`.

### F3. MINOR. Lenses: RTL, Docs
- **Where:** `sw/litex/milan_soc.py:2085`, `docs/design/GPTP_PLANE.md:282`, `CHANGELOG.md:62`, `hdl/ieee8021as/gptp_plane/KL_gptp_gmii_launch.sv:362`, `sw/builder/test_builder.py:18266` ("the AX7101 image cannot move"), and the PR's change table.
- **Evidence:** GMII `ready` is not a constant. LiteEth's `LiteEthPHYGMIITX` assigns it in `sync`. The AX7101 export declares `reg milansoc_milanmac_phy_sink_ready = 1'd0`, sets it to 1 and clears it on reset, and now connects it with `.gmii_tready_i (milansoc_milanmac_phy_sink_ready)`. Synthesizing the observer with that registered `ready` keeps the flop. The export differs from the base by exactly that one functional line, once paths and the comment tree are normalized. Receipts: `receipts/run/ax-export-ready-lines.txt`, `receipts/run/ax-export-base-vs-head.diff`, `receipts/yosys/stat_*.txt`.
- **Impact:** the statements are false about the shipping netlist, and they are the stated reason the AX7101 "cannot move". The behaviour is still safe (see check 2), so this is a false claim and not a fault. It is a claim about hardware, and I could not settle it as wording only, so it is MINOR under the rule.
- **Required outcome:** the text says `ready` is a flop that is 1 from the first clock after reset, whose reset is covered by the observer's own, so no octet is held on GMII. The "cannot move" sentence goes.
- **Verification:** read against the export lines above.

### F4. MINOR. Lens: Tests
- **Where:** `tb/verilator/gptp_txts/sim_main.cpp:926`, `records_[target].abort != 0 || records_[target].delta != 45`.
- **Evidence:** a whole MII frame measures 90, so `delta != 45` is always true on that shape and the check named "fragment: the observer refused it, by measurement" cannot fail there. A planted cut of the record's refusal bit leaves the MII run at 0 failures. In a probe run where the bubble fragmented nothing, this check still passed while the two result checks failed. The control `delta_forced_not_measured` runs only on GMII. Receipts: `receipts/run/bubble/refusal-bit-cut.trim`, `receipts/run/bubble/stuck.trim`.
- **Impact:** the check claims a measured refusal on MII and proves nothing there. The later result checks still catch a lost record.
- **Required outcome:** the expected distance scales with `kEthCycPerOctet`, and an MII control shows the check can fail.
- **Verification:** that control is caught on `run-mii`.

### F5. MINOR. Lens: Tests
- **Where:** `tb/verilator/gptp_txts/sim_main.cpp:942` and the `pad_idx_ == 22` arm of `prove_phc_load_inside_the_window`.
- **Evidence:** the comment says the guard has to cover the whole longer interval, but the load lands 1120 ns in, leaving about 132 fabric cycles to the capture. A guard of 150 where 203 is needed passes all 89 checks. The same guard fails 2 checks once the load moves to octet 1, and the shipped 203 passes there. Receipts: `receipts/run/boundary/guard-150-load-at-octet-14.log`, `guard-150-load-at-octet-1.log`, `shipped-load-at-octet-1.log`.
- **Impact:** the design is correct, but the test only bites below about 133 cycles, so a wrong derivation between that and 203 stays green.
- **Required outcome:** the arm also loads at the window's early end on the MII shape.
- **Verification:** a control with the guard just below 203 is caught.

### F6. MINOR. Lens: Docs
- **Where:** the #829 `[A725b] REVIEW READY` comment and `author/REPORT.md` row g, with `author/receipts/ax7101/checksums.txt` and `gate-axhead.log`.
- **Evidence:** "14 planted controls are caught" is stated against this commit. This head has 10: `mutants.py --list` shows 10 and the run ends `controls: 10 failures: 0`. The 14 come from `txts-mutants-bench.txt`, the bench branch, with four writable-pair controls that are not here. Also, "126 implementation checksums" cannot be counted from public receipts, because `checksums.txt` publishes three lines per run and the logs are not published. It compares head to the bench branch, not to the base. `gate-axhead.log` does not name its head. Receipt: `receipts/run/gptp_txts-all.log`.
- **Impact:** a cold reviewer cannot trace these figures to this head. These are wrong or untraceable figures, so they are not residue.
- **Required outcome:** the record says 10 controls at this head and 14 on the bench branch, publishes the checksum comparison with the head identity of each route, and says what the comparison covers.
- **Verification:** the figures reproduce from the published files.

### F7. MINOR. Lens: Tests
- **Where:** `tb/verilator/gptp_txts/sim_main.cpp:859` and the matching `expect` strings in `tb/verilator/gptp_txts/mutants.py`.
- **Evidence:** the check reads "the mean error is within one nanosecond of zero", while the MII limit is 1.754 ns and the measured mean is 1.35 ns.
- **Impact:** the check's name is false on that shape. The limit itself is justified and documented.
- **Required outcome:** the name states the shape's limit, and the controls follow it.
- **Verification:** `make -C tb/verilator/gptp_txts`, every control caught.

### Residue
- **RES1.** `tb/verilator/gptp_txts/sim_main.cpp:14`, "at both system clocks that board has carried". This head's Arty configs state 83.333 MHz, a third clock. Exact fix: "at 80 MHz and at 100 MHz". The 83.333 MHz run passes all 89 checks (`receipts/run/mii-q24.log`).

### Suggestions (no effect on coverage)
- **S1. File a new Issue: the MII inter-frame gap looks short of the standard.** The converted chain and its migen source both put 12 low samples between frames on the MII pads. That is 480 ns, against 96 bit times (960 ns) in IEEE 802.3. LiteEth counts the gap in clocks, and nothing sets `tx_gap_cycles` on this PHY. This predates the PR and does not affect the observer, whose close count is 4 clocks. Receipt: `receipts/run/pad-gap-census.txt`.
- **S2. File a new Issue: the lifecycle failure's cause is still unknown** (see check 6).
- **S3. Reconcile the clause citation.** The PR and issue cite IEEE 802.1AS-2020 11.3.2 for the timestamp point, and the RTL banners cite 11.3.9. 11.3.2 appears nowhere else in the repository's documents or RTL. I had no copy of the standard, so I did not judge which is right.
- **S4. `ci/image/command-table.json`** still pins the old hashes of `tb/verilator/gptp_txts/mutants.py` and `sw/litex/gen_mac_tx_model.py`, and has no entry for the new `obj_mii` and `mac_tx_chain_mii` command forms. No hosted workflow runs this gate, and dev already has 32 stale pins and refuses it, so this only adds to the next refresh. Receipt: `receipts/gates/table-pin-drift.txt`.
- **S5. The fragment arm's two-clock bubble** only bites when it covers the `ready` edge. A timing shift can leave one held clock masked and produce a false red (`receipts/run/bubble/stuck.trim`).
- **S6. `mutants.py` leaves the last control's binary in `obj_mii`.** The source is restored and the binary is not rebuilt, so running that binary directly after `make` gives false failures. This misled my first system-clock sweep. I discarded those logs and repeated the sweep on a clean build.

## The seven checks

1. **Root cause: confirmed.** With the fix cut, `chk_w` is 0 at seam cycle 7 and `cand_r` is low from cycle 8, because the octet is still `55`. The run produces 0 records and fails 38 of 62 checks, including `launch: an isolated exchange completes`. As shipped it passes 89 of 89 with delta 90. On GMII the delimiter is at cycle 7 and delta is 45. `make -C tb/verilator/gptp_txts` rc 0 with 10 of 10 controls, not 14 (F6). Receipts: `receipts/run/rootcause/`, `receipts/run/gptp_txts-all.log`.
2. **GMII behaviour: unchanged. AX7101 netlist: not shown unchanged.**
   - At defaults, the observer with `ready` high is formally equivalent to the base (423 of 423 cells), and so is the ledger (1492 of 1492). The correction stays 426 ns and the guard 64.
   - Over a full GMII run there were 116,709 transfers and no cycle of `valid` without `ready`.
   - The route receipts read LUT 51994 and WNS +0.236 as recorded, and the gate passes. Slices are 15841 of 15850.
   - The "byte-identical export" and the checksums compare head to the bench branch. Head and base differ by the `ready` connection (F3). No route of the base is published, so the routed effect of this PR alone is unknown.
3. **Arithmetic and receive distances: correct.** `(90+2+1)x40 + 2x20 + 10` is 3770, the guard is 203, 3770 ns x 200 ppm is 0.754 ns, and the bound sums to 12.52 and is published as 12.6. My own probe, with a separate time base over seven phases, gives MII 1109.4 and 1173.9 (1166.5 to 1182.5), and GMII 140.9 and 215.0 (206.5 to 225.0). These match the table. `rx_mac_filter` is combinational on `valid`, so it adds no stage before the stamp. Receipts: `receipts/run/arithmetic.txt`, `receipts/run/rx/summary.txt`.
4. **Generated chain: from its generator, cannot drift unseen.** Regeneration is byte-identical for both shapes, and `sha256` matches the manifest. A hand edit, a falsified manifest and a product-region change are each refused. `test_gptp_tx_timestamp.py` gives 36 of 36. The focused builder gates 1d, 1f, 1g and 23m, the source-list gate and the port-contract gate pass. Receipts: `receipts/run/gen-*`, `receipts/run/test_gptp_tx_timestamp.log`, `receipts/run/builder-focus.log`.
5. **Docs state what is shown, apart from F3.** 100 Mb/s is described by its simulation and bound, and other speeds as unqualified. The Arty declares zero corrections and has no shipping claim. I found no list of "16 NOT RUN arms" in public material at this head; the only NOT RUN I found is the builder legs' one gate each, so I could not check that item.
6. **The lifecycle failure: acceptable for this PR, but its cause is not established.** The test and its process-ownership helpers are unchanged. The failure is the helper's 4 s cleanup deadline, with no in-suite failure. I ran it 12 times on head and 12 on base, side by side at a host load of about 43 to 53, and all passed, so "load flake" remains an unreproduced hypothesis (S2). Receipts: `receipts/run/lifecycle-round1/`, `receipts/run/lifecycle-round2/`.
7. **Bench evidence: traces, and claims nothing owed.** Sampled rows, 64 polls with asCapable 1, the -234.9 and -231.5 ns offsets and 460,354 stream frames match their receipts. The tap-out check is stated as not run. This is bench-branch evidence only, under a compensation.

**Robustness probes on the MII shape.** With every frame forced to start on a stuck nibble phase, the state `eth_rst` can leave on this shape, the reconstructions stay inside the bound with a mean of 1.32 ns. The only failures were the fragment arm's result checks in the 100 MHz run, where the bubble masked no transfer (S5). The suite also passes at 12 system clocks from 50 to 111 MHz.

**Comment rule:** no new lane label, round, reviewer ID or comment ID in the delta. **Commits:** four, each one line with no trailer. **Prior public findings:** none on this PR at the time of reading, so none to resolve.

## Ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #829 acceptance and corrections; `receipts/run/rootcause/`; pad oracle on `run-mii`; `docs/design/GPTP_PLANE.md:202-345` | R761-1 | `4cda0aa03b11462f4f8750289f0999d5288b3546` |
| RTL | UNCLEAN (F3) | `KL_gptp_gmii_launch.sv`, `KL_gptp_txret.sv`, `KL_gptp_shadow.sv`, `milan_datapath.sv`, `milan_soc.py`; `receipts/yosys/` | R761-1 | `4cda0aa03b11462f4f8750289f0999d5288b3546` |
| Robustness | CLEAN | `receipts/run/boundary/`, `receipts/run/bubble/`, `receipts/run/mii-q*.log`, `receipts/run/gptp_txts-all.log` | R761-1 | `4cda0aa03b11462f4f8750289f0999d5288b3546` |
| Tests | UNCLEAN (F1, F2, F4, F5, F7) | `sim_main.cpp`, `mutants.py`, `Makefile`, `test_gptp_tx_timestamp.py`, `test_builder.py`; `receipts/gates/`, `receipts/run/` | R761-1 | `4cda0aa03b11462f4f8750289f0999d5288b3546` |
| Docs | UNCLEAN (F1, F3, F6) | `GPTP_PLANE.md`, `CHANGELOG.md`, `REQUIREMENTS.md`, `CLOCK_DOMAINS.md`, `TESTING.md`, suite README; PR and issue text; `receipts/gates/` | R761-1 | `4cda0aa03b11462f4f8750289f0999d5288b3546` |

## Real limits
- No full suite sweep, `behave`, full builder legs, Yosys bank or Vivado run here. Those results are the author's receipts, and I checked only their tallies and heads.
- Formal equivalence covers the observer and ledger modules at defaults with `ready` high, not the whole image.
- The stuck-phase probe forces the state in the generated chain. It does not drive a real `eth_rst` mid-octet.
- No hardware was used. The Arty results are read from receipts, and large captures are not published.
- The IEEE and Milan texts were not available, so clause wording was not checked against them.
- The clone was restored and verified: tree, index and gitlinks match (`receipts/clone-restored.txt`).

## Pending manager duties
- Hold the merge until F1 to F7 are fixed and re-reviewed at the new head.
- Hosted and act acceptance at the new head. At this head all four workflow runs ended cancelled, with `docs-gates-0` failed.
- The current-dev merge candidate, builder and native banks at the merge turn.
- The owner's tap-out check, which remains owed on the bench path through #583.
- Carry RES1 to the residue checklist, and file S1 and S2 as public Issues.

R761-1 FINISHED
