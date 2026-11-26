[R937] NEGATIVE - exact head a6864a49293ba3d0df37029abfa581468ef78dce

Round R937-1, internal cleared-context review of kebag-logic/milan-fpga PR #1016 (Closes #1013) at exact head `a6864a49293ba3d0df37029abfa581468ef78dce`, tree `282773485cda391903a7e3bf8b1a0374bb882563`, on source base `dev-soft-core` `c34e7d8b06739a22cc79997a9a1f4cbcd9bd0350`. All five lenses applied. Two MINOR findings are open, under Tests and Docs, so the verdict is NEGATIVE. Conformance, RTL and Robustness are covered clean at this head.

## Reconstruction

- Contract: AGENTS.md, CONTRIBUTING.md sections 2 to 6, docs/README.md.
- Task: the #1013 body (objective, scope, acceptance 1 to 4). The pin ruling on #1013 (comment 7178757153, by the manager identity) replaces the gPTP target `3009f9a2` with `3ce71b768a2f6f6a5274c127080146e755d02275`, the merge of FPGA-gPTP PR #110. I accept that ruling as the public change to acceptance 1. The issue body was not edited, and the ruling is the record.
- Standards: I read the text of each cited clause.
  - IEEE 802.1AS-2020 11.2.13.7: asCapable is cleared only when meanLinkDelay exceeds the threshold.
  - Milan v1.2 4.2.6.1.1 sets the 800 ns threshold.
  - Milan v1.2 4.2.6.2.7: a Pdelay between -80 and 0 ns shall not clear asCapable. That is a minimum tolerance.
  - IEEE 1722.1-2021 6.2.2.6: control_data_length "is set to 56".
  - IEEE 1722.1-2021 6.2.7.1.3 (rcvdDiscover) and Milan v1.2 5.6.3.1 (entity_id filter).
  - Accepting a control_data_length above 56 by its first 56 octets is the stack's ruling (tsn-c-stack #37), adopted by #1013's scope. I raise no conflict.
- Diff: `c34e7d8b..a6864a49` (7 commits, each a one-line message with no trailer), plus both donor deltas:
  - FPGA-gPTP `1213ac5b..3ce71b76`: under `hdl/`, only `hdl/ucode/gen_gptp_ucode.py` changes.
  - tsn-c-stack `715589c1..a795471c`: outside tests and docs, only `src/adp.c` (one comparison) and `examples/rv32/smoke.c` change.
  - Both pins are on their donors' `main`, and each is a descendant of the previous pin.
- Evidence read: the author packet at `86ac1ed8:review-evidence/pins1125-r1/author`, all 82 blobs, fetched by blob id. I also took a snapshot of the hosted check runs at the exact head.
- Prior public review findings: none. At the time of this round the PR carries only the two review-start comments and no reviews or review comments. There is nothing to resolve or retain.

## Findings

### R937-F1 MINOR - Tests, Docs - `tb/verilator/gptp_shadow/sim_main.cpp:3040-3043`, `tb/verilator/gptp_shadow/README.md:38` - two of phase 22's named checks cannot fail when the graded Follow_Up is not used

- **Authority/evidence:**
  - AGENTS.md section 6, Tests: "Each new test can fail for the defect it claims to detect".
  - The `gm_pair` background pairs (`:3014`, via `gm_pair_on_link`) and the graded pair (`:3040`) are all built for an offset of 0.
  - `:3041` grades `near(pub_offset_o, 0, 64)`. A Follow_Up the plane refuses or ignores therefore leaves the previous pair's offset of about 0 published, and the check passes. `:3043` ("no PHC step") also passes when no pair is used.
  - Two measurements show this:
    1. **The graded pair never sent:** a disposable copy of the harness with `:3040` removed still prints `483 checks: 483 PASS, 0 FAIL` (`receipts/probe_shadow_unsent_pair.*`, `scripts/probe_shadow_unsent_pair.sh`).
    2. **The previous engine (1213ac5b image):** at -81 ns phase 22 fails `asCapable kept`, so the plane drops the Follow_Up. That engine's not using it is shown by `gptp_plane`'s `link delay -81: the next Follow_Up is used` failing on the same image. Yet `#109 -81 ns: the next Follow_Up is used with the delay floored at -800 ns` does not fail (`receipts/oldgen/old_gen_shadow_1213ac5b.log`, `old_gen_plane_ldonly_1213ac5b.log`).
  - README row 22 states that each negative trial's "next Follow_Up is used with the delay floored at -800 ns, without a PHC step".
  - `gptp_plane` phase 6 does discriminate here. Its background pairs carry `kBackgroundOffsetNs = 11` (`tb/verilator/gptp_plane/sim_main.cpp:99`) and it counts the adjfine update.
- **Impact:** an engine or transport defect that keeps asCapable but drops or ignores the Sync/Follow_Up after a negative-delay exchange passes this phase. The README records as proven through the slice a property the slice does not grade. Overall coverage of that property rests on `gptp_plane` alone, which has no tap, FIFO or ledger.
- **Required outcome:** in phase 22, a graded pair that is not used must fail by name. Either make the stale value distinguishable (for example a nonzero background offset, as in `gptp_plane`) or grade a use counter. Alternatively, rename the checks and restate README row 22 to claim only what is graded.
- **Verification:** `scripts/probe_shadow_unsent_pair.sh <repo> <out>` reports a named FAIL of the renamed or strengthened check. `make -C tb/verilator/gptp_shadow` stays at 0 FAIL with 14/14 controls. The 1213ac5b image also fails that check at -81 ns.

### R937-F2 MINOR - Docs - `docs/design/GPTP_PLANE.md:158` - "`gptp_plane`'s phase 6 grades every row to the nanosecond" overstates the coverage of the new table

- **Authority/evidence:**
  - The table at `:137-142` has four columns, the last of them "Public word".
  - Phase 6 grades the engine's signed word, not the public word. `tb/verilator/gptp_plane/README.md:25` says so: "the public clamp to 0 is `gptp_shadow`'s and `milan_dp`'s".
  - Phase 6 grades no published value for the bad exchange: `check("the engine publishes the used delay", ...)` is under `if (kept)` (`tb/verilator/gptp_plane/sim_main.cpp:686`).
  - So the "Public word" cells (0 for every negative row, the measured delay above 800 ns) are graded by `gptp_shadow` phase 22 and the `milan_dp` legs, not by phase 6.
  - This is a statement about what a test grades. Under the residue rule I classify it MINOR, not RESIDUE.
- **Impact:** the authoritative design page attributes public-face coverage to a suite that has no public bank. A reader who checks or changes the clamp is pointed at the wrong suite.
- **Required outcome:** the sentence names what each suite grades. For example: phase 6 grades the asCapable and Sync-path columns to the nanosecond, and `gptp_shadow` phase 22 and the `milan_dp` legs grade the public word.
- **Verification:** read the sentence against `gptp_plane/sim_main.cpp:675-712` and `gptp_shadow/sim_main.cpp:3022-3045`. The docs gates (`check_gptp_docs.py`, `check_doc_style.py`, `docs_check.py`, `check_em_dash.py --base <merge-base>`) pass.

### R937-R1 RESIDUE - Docs - `tb/verilator/gptp_plane/README.md:24` - a blank line splits the phase 6 row out of the phase table

- **Evidence:** the pinned renderer (cmark-gfm) ends the table after row 5 and renders row 6 as a paragraph with literal pipes. The text itself is intact.
- **Exact fix:** delete the empty line 24, between `| 5 | ...` and `| 6 | ...`.

### R937-R2 RESIDUE - Docs - `docs/design/GPTP_PLANE.md:150` - "Two over-stated latency constants then cancel in the offset." has no antecedent for "then"

- **Exact fix:** "Because the Sync path uses the delay signed, two over-stated latency constants cancel in the offset."

### R937-R3 RESIDUE - PR body - its first two lines are both `[A850]`

- **Exact fix:** delete one of the two lines.

### R937-S1 SUGGESTION - Tests - `tb/verilator/milan_dp/sim_gptp.cpp:1705` - "the peer's exchange is negative" is a harness-model check

- `pd_expect + pd_bias < 0` is a precondition on the harness's own prediction, not a reading from the DUT. The product faces are clamped, so the leg cannot tell -263 ns from -5,000,000 ns by design.
- Optionally, label it as a harness precondition. The leg's real checks are live: at the 1213ac5b image it fails exactly `asCapable kept` at -81, -263 and -5,000,000 ns, 3 of 242 (`receipts/oldgen/old_gen_milan_dp_gptp.log`).

### Not a finding against this PR

The firmware gate's sharded dispatch self-check writes an untracked `dispatch-build/` into the caller's working directory (`sw/firmware/ctrl/test/test_ctrl_firmware_shards.py:42`). That file is not in this delta. I removed the directory after my runs. The manager may decide whether to file it.

## Lens coverage, with evidence

- `[R937] PASS Conformance - #1013 acceptance 1-4 and ruling 7178757153 against a6864a49 - acceptance criteria and standards:`
  - **Acceptance 1:** both gitlinks sit at the ruled commits: index `160000 3ce71b76...` and `160000 a795471c...` (`receipts/restore_check.txt`).
  - **Acceptance 1, generators:** `check_submodule_docs.py`, `submodule_boundaries.gen.py --check`, `timesync_chain.gen.py --check` and `check_diagram_pngs.py` each return rc 0 (`receipts/ratchets/`).
  - **Ruling inputs:** `hdl` `48cb0525` and `syn` `ae1d026c` are identical at `3ce71b76` and `3009f9a2`, and PR 112 touches only 4 test-runner and doc files (`receipts/gptp_pin_identity.txt`).
  - **Acceptance 2:** discovers of 57, 84, 102, 256 and 2047 are accepted, and 0 and 55 are refused, with valid_time 0 and 31 (`AdpAdapter.*`, 69/69). Negative delays keep asCapable and the public value reads 0 in `gptp_shadow` and `milan_dp`. Each rule has a caught plant (5 ADP plants, 8 `link_delay.py` plants, and the clamp control).
  - **Acceptance 3:** reproduced at this head (see Tests below). The egress and platform ledgers come from the author's receipts at `d0483d08`: rows and points equal the base's, and only command paths and ELF digests differ.
  - **Acceptance 4:** the author's route receipts. All 9 head/base signoff and identity receipts are byte-identical apart from their header lines. Utilization figures are equal. At the #818 floor (+0.030 setup, 0 hold), 1x1 ExtraPostPlacementOpt has a worst WHS of +0.021 and 8x8 ExtraTimingOpt is +0.283/+0.036, both as on the base.
  - **Clauses:** all cited clauses were read and match the stated behaviour.
- `[R937] PASS RTL - hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:770-771, hdl/milan/milan_datapath.sv:1848,2930,6460,6877, gptp-processor 1213ac5b..3ce71b76:hdl - integration:`
  - **No parent HDL change:** the diff touches no file under `hdl/`.
  - **Engine change:** the engine's only HDL-tree change is the microcode generator. The ROM stays word-neutral at 1,013 of 1,024 at both pins (generator logs in `scratch`, summarised here).
  - **Floor arithmetic:** the floor is branch-free and its sum cannot overflow (|D| < 2^62).
  - **Clamp:** the public 32-bit word is clamped to 0 on bit 31 at `KL_gptp_shadow.sv:770`. Every parent consumer (CSR `A_GPTP_PDELAY`, GET_AVB_INFO snapshot, change detector) reads only that clamped bank.
  - **ROM ledger:** the row `3ce71b76 gptp_ucode.hex 52293128...` equals the reviewer's regeneration with `ooc.sh`'s generator call, and equals the donor's `syn/ooc/work/gptp_ucode.hex` at both 3ce71b76 and 3009f9a2 (`receipts/rom_digest_check.txt`).
  - **Untouched:** no port, parameter, register, CDC or reset change.
- `[R937] PASS Robustness - sw/firmware/ctrl/test/test_adp.cpp:896-930, tb/verilator/gptp_plane/sim_main.cpp:675-712, tb/verilator/gptp_shadow/sim_main.cpp:3022-3071 - boundaries and malformed input:`
  - **ADP length:** control_data_length 0, 55, 56, 57, 84, 102, 256 and 2047, with valid_time bits set, in complete and truncated frames up to the 128-octet channel limit (frames above it are out of scope).
  - **Reviewer plants, all caught by the named tests** (`receipts/runs/fw_adp_probe.log`, 9 of 9 with the PR's 5):
    1. require the whole declared PDU in the frame;
    2. an upper bound at 102;
    3. an upper bound at 2046;
    4. the bound moved to 55.
  - **Delay:** -3, -80, -81, -263, -800, -801 and -5,000,000 ns, then 800 and 801 ns, plus requalification after 801.
  - **Previous engine:** it goes red at every face. `gptp_plane` fails 32 of 102, `gptp_shadow` 15 of 483 and `milan_dp` `gptp` 3 of 242, each from -81 ns on (`receipts/oldgen/`).
- `Tests` - UNCLEAN (R937-F1). Reproduced at this head with the scoped Verilator 5.050 (`Verilator 5.050 2026-07-01 rev v5.050`, wrapper sha256 `905795b9...`), GCC 16.2.1 and GoogleTest 1.14.0:
  - `gptp_plane`: 102/102, phc-step campaign 8/8, `link_delay.py` 9/9 with each named check.
  - `gptp_shadow`: 483/483, controls 14/14 including `public_bank_publishes_a_negative_delay: caught by "#109 -263 ns: the public bank reads 0"`, and lifecycle PASS ("fourteen named defects").
  - `milan_dp` `gptp` and `gptp-lat`: 242/242 each, with five `[#109]` lines each.
  - `gptp_tables`: 36 checks, 26/26 controls. `gptp_txts`: 95 checks, 13/13 controls.
  - Firmware gate shard 0/4: PASS, rc 0. Shard 1/4: `mutants: 847 of 847 caught`, PASS, rc 0, with the per-plant failure counts equal to the author's.
  - The new tests fail for the old behaviour (the previous-engine runs above). F1 is the exception.
- `Docs` - UNCLEAN (R937-F1, R937-F2). Gates at this head, each rc 0 (`receipts/ratchets/`):
  - `check_py_idiom.py`, with every count at its budget (`too many parameters: 7 <= 7`);
  - `measure_test_evidence.py`, host-time suite files 3;
  - `check_doc_style.py`, `check_gptp_docs.py` and `check_submodule_docs.py`;
  - `check_em_dash.py --base c34e7d8b`: 0 findings over 198 added lines, arms 339/339;
  - `docs_check.py`: 0 findings, scrub 23/23;
  - `gen_toc.py --check`.
  - The two ratchet budget files are byte-identical to the base: blobs `008f7fd7` and `fc044548` (`receipts/ratchets/budget_blobs.txt`).
  - The comment rule: the added source comments carry no bench lane label, lane name, review round, reviewer ID or issue-comment ID. No new instance.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #1013 body, acceptance 1-4 and ruling 7178757153; both donor deltas; clause texts of 802.1AS-2020 11.2.13.7, Milan v1.2 4.2.6.1.1, 4.2.6.2.7 and 5.6.3.1, 1722.1-2021 6.2.2.6 and 6.2.7.1.3; author route, ledger and firmware receipts; `receipts/gptp_pin_identity.txt`, `restore_check.txt` | R937-1 | a6864a49293ba3d0df37029abfa581468ef78dce |
| RTL | CLEAN | `KL_gptp_shadow.sv:770-771`; `milan_datapath.sv` public-delay consumers; donor `hdl/` delta (generator only); ROM word count; `syn/yosys/rom_digests.tsv:33` with `receipts/rom_digest_check.txt` | R937-1 | a6864a49293ba3d0df37029abfa581468ef78dce |
| Robustness | CLEAN | `test_adp.cpp:896-930` boundaries and 9 caught plants; delay trials in `gptp_plane` and `gptp_shadow`; previous-engine runs on three suites | R937-1 | a6864a49293ba3d0df37029abfa581468ef78dce |
| Tests | UNCLEAN (R937-F1) | `gptp_plane`, `link_delay.py`, `gptp_shadow` with controls and lifecycle, `milan_dp` `gptp` and `gptp-lat`, `gptp_tables`, `gptp_txts`, firmware shards 0 and 1, ADP probe, the unsent-pair probe | R937-1 | a6864a49293ba3d0df37029abfa581468ef78dce |
| Docs | UNCLEAN (R937-F1, R937-F2) | CHANGELOG, `SUBMODULES.md`, `GPTP_PLANE.md`, guides, traceability AS-8, both suite READMEs, `ctrl_mutants.py` and `mutants.py` docstrings, diagrams; 11 docs gates | R937-1 | a6864a49293ba3d0df37029abfa581468ef78dce |

## Real limits

- **Not re-run at this head; relied on the author's receipts at `d0483d08` and the exact-head hosted contexts:**
  - firmware shards 2/4 and 3/4 (hosted `firmware-aecp-mutants` and `firmware-srp-mutants` concluded success at this head);
  - both stack boundary legs (hosted `firmware-boundary` success);
  - `tsn_fuzz`, `milan_dp_gm_steps` and the physical `milan_dp_gptp` leg;
  - the egress ledger and `plat_ledger`;
  - all routes.
  - The image inputs at this head equal `d0483d08`'s (identical `hdl/` and `syn/` trees, identical ROM digest). That is why those receipts carry over.
- **Not run:** Yosys, Vivado, `ooc.sh --record-rom-digests` (a Yosys sweep), the full docs workflow replica and any act or Docker replica. The named docs gates were run one by one instead.
- **Hosted snapshot** (`receipts/hosted_checks_snapshot.tsv`): 40 success, 1 skipped (Physical gPTP, nightly and manual), 29 queued or in progress. The `verilator-suites` and `yosys-portability` aggregates had not concluded. They are not claimed here.
- **No manager source bank** ran at this head, and none is claimed. Physical calibration was NOT RUN, and no result here is hardware evidence.
- **Process incident:** during the round, one of my cleanup commands was too broad. It interrupted the first firmware shard-0 run and the first probe chain, and duplicates ran briefly. Every result reported here comes from a complete re-run: the shard 0 and shard 1 receipts are the second chain's, and the probe summary notes which lines are repeats (all agree).
- **Clone state:**
  - I fetched remote-tracking refs inside the `gptp-processor` and `tsn-c-stack` submodules to check that the pins are on `main` and to compare `3009f9a2`.
  - I removed an ignored bytecode cache my runs wrote in `protocol-processor`, plus the untracked `dispatch-build/` and my probe directories.
  - Tracked bytes, index, modes and all gitlinks match the head (`receipts/restore_check.txt`).
  - Ignored build outputs (object directories and generated images) remain in the clone.

## Pending manager duties

- Have R937-F1 and R937-F2 fixed, then re-cover `Tests` and `Docs` at the new head. Conformance, RTL and Robustness stay banked only if the fix touches nothing in their scope.
- Carry R937-R1, R937-R2 and R937-R3 to the residue checklist.
- The hosted `verilator-suites` and `yosys-portability` aggregates must conclude success on the exact head. The PR records that `suite_shards.py`'s figures for `gptp_shadow` (393 s) and `gptp_plane` (784 s) are not re-measured, and that phase 22 and `link_delay.py` add time, so the shard windows want the hosted measurement.
- Build and validate the current-dev merge candidate at the merge turn: source base `c34e7d8b`, live dev `e275d795`, with the builder and native banks.
- External review, containment after merge, and the bench after merge.

R937-1 FINISHED
