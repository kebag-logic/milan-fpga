[R458] POSITIVE - exact head d18270d69eea9cdf35f846c77821d5488dab97cc

# R458-5: internal independent review of processor PR #154 (milan-fpga #230)

- **Round:** R458-5, the internal cleared-context review. It was started publicly at PR #154 comment 5981519171.
- **Head:** `d18270d69eea9cdf35f846c77821d5488dab97cc`, tree `5ff7ea39fc74c21be0d6a1df92f07496513c5fab`.
- **Verdict:** POSITIVE. All five lenses are covered clean at this head. No BLOCKER, MAJOR, MINOR or RESIDUE is open.
  One SUGGESTION is recorded below. It does not affect the verdict.
- **Order of work:** I wrote my verdict and ledger to this file as a draft before I read any prior review on this PR. Section 6 then resolves the prior findings. Reading them changed no verdict and no lens.

## 1. Reconstruction and scope

- **Governance.** I read the parent's `AGENTS.md` and `CONTRIBUTING.md` at `dev`: lenses, severities, the one-line commit rule, the em-dash rule, privacy and the verification bar. The processor repository has no copies of its own. I also read the processor's `README.md` and `docs/README.md`.
- **Frozen acceptance (issue #230 body).**
  1. SRP tests pass at 1x1 and 8x8.
  2. Before-and-after hierarchical Vivado reports show a material reduction.
  3. At 1x1 no logic exists for seven inactive slots.
  4. WNS stays at zero or above.
  5. Scaling and latency trade-offs are documented in #229.
- **Public scope decisions** (manager comments on #230):
  - 5967853024: the timer-arm FIFOs join the issue.
  - 5974045353, the lane: behaviour identical, with no port, parameter or register change and no protocol-visible timing change. Equivalence is proved by suites, campaigns and lockstep. The 100 MHz criterion is judged at the declared 50 MHz.
  - 5977836860, the ruling on the STOP: lever 4's shared evaluator is (b), parallel evaluation, final for #230. Option (a) goes to #640, and #230 closes by hand at the processor merge.
  - 5978448959 (round 2) and 5980793710 (round 3).
- **The PR's own delta.** PR base `main` is `c050d971`, which is merged into this head. `git diff c050d971..d18270d6` spans 50 files:
  - four SRP HDL files (+112/-43);
  - two docs;
  - two new benches with their wraps and Makefiles;
  - `mutants.py` and 35 patches;
  - two READMEs.

  The rest of the range `c4cb84ff..d18270d6` (ADP, AECP notify, nvm_port, the top's declaration reorder, Yosys `run.sh`) came in through the merges of `main` PRs #149, #150, #152 and #153. I read it for context and did not re-review it here.
- **SRP HDL stability.** These diffs are empty:
  - `git diff 25847d0 d18270d6 -- hdl/srp`;
  - `git diff 65324390 d18270d6 -- hdl/srp`;
  - `git diff c4cb84ff c050d971 -- hdl/srp`.

  So the round-1 Vivado runs (milan-fpga `06fe795b`) measured exactly this head's SRP RTL against base `c4cb84ff`.

## 2. Evidence executed at this head

All runs used the scoped Verilator. Its wrapper reports `Verilator 5.050 2026-07-01 rev v5.050`, sha256 `905795b9...e92f`, and it is first on PATH for `lint_hdl.sh`. The run tree is a `git archive` export of the head, and all 554 of its tracked files hash to HEAD's blobs (`receipts/clone-integrity.txt`). Every rc is 0 unless stated.

| Run | Result | Receipt |
|---|---|---|
| `tb/srp_stream_fsms` `make`: walk arms then suite | 35, 46, 67, 123 checks at 1/1, 2/2, 3/5, 9/9; suite 1,219/1,219 | `receipts/runs/walk.log` |
| `tb/srp_top` `make`: FIFO arms then suite | 15/15 at each of the four shapes; suite 2,200/2,200; the STORE lines equal the README table cell for cell | `receipts/runs/store.log` |
| `tb/srp_admission` `make` | 1,138 / 12,615 / 41,012 / 201,073 / 991,231, all PASS | `receipts/runs/admission.log` |
| `tb/pp_top` `make` (integration at the default 8/8) | 10,416/10,416 | `receipts/runs/pp_top.log` |
| `scripts/lint_hdl.sh` | 41/41 LINT OK | `receipts/runs/lint.log` |
| root `make check` | lint, wavedrom, 1,131 links, matrix, parameters: OK | `receipts/runs/check.log` |
| `tb/srp_top/mutants.py --jobs 8` | 14 positive controls PASS; 113 arms KILLED; **128 checks: 128 PASS**; assertion coverage **80/80** | `receipts/runs/campaign.log`, `receipts/runs/campaign-receipts/` |
| Control table recount (`scripts/control_table.py`) | all 31 walk/FIFO rows of `tb/srp_top/README.md` equal the receipts' per-shape FAIL counts | `receipts/control_table_recount.txt` |
| Slope controls at N = 3, 5, 8, re-measured one shape per copy | all 12 cells equal the README (for example `slope-read-source-0`: 1,683 of 41,009; 6,125 of 201,068; 22,202 of 991,223) | `receipts/slope-shapes.txt` |
| Walk arms at 8 shapes the Makefile does not run (4/4, 8/8, 16/16, 1/9, 9/1, 2/3, 3/2, 5/16) and at 8 further random-reset seeds per committed shape | all PASS (2/3 elaborates the listener's smallest RAM arm, N = 3) | `receipts/walk-extra.txt` |
| Default `make` with a planted walk defect | rc 2, so `run_suites.sh`, which reads make's status, would mark the suite FAIL | `receipts/default-make-with-probe.log` |
| Vivado re-derivation from `06fe795b` (`scripts/vivado_rederive.py`) | every whole-design, `u_srp`, per-block, per-context and WNS/WHS figure in the PR body and in 10 §5.1 equals the published reports | `receipts/vivado-rederive.txt` |

**Reviewer probes.** `scripts/make_probes.py` generates the patches in `probes/`, and `scripts/run_probes.py` runs each one in a scratch copy of its own. None of them is in the committed set.

| Probe | Edit | Result |
|---|---|---|
| `r5-wid-write-ignores-ready` | RAM `{stream_id, DA, VLAN}` written on `gate_valid_i`, not `gate_acc_w` (RAM arm only) | caught: WK9 at 3/5 and 9/9 (n/e at 1/1, 2/2) |
| `r5-wtsp-mfs-mif-swapped` | MaxFrameSize and MaxIntervalFrames swapped in the `wtsp_r` write | caught: WK1-WK5 and WK9 at 4/4 shapes |
| `r5-wid-ram-vid-from-da` | RAM VLAN written from DA bits | caught: WK1-WK5 and WK9 at 3/5 and 9/9 |
| `r5-wsid-read-xor-1` | listener RAM read at `wsrc_r ^ 1` | caught: WK6-WK8 and WK10 at 3/5 and 9/9 |
| `r5-wsid-written-at-walk-index` | listener RAM written at `wsrc_r` | caught: WK6-WK8 and WK10 at 3/5 and 9/9 |
| `r5-tf-tk-written-at-ls-pointer` | talker FIFO written at the listener write pointer | caught: TF1 and TF4 at 4/4 |
| `r5-tf-ls-read-at-tk-rptr` | listener FIFO head read at the talker read pointer | caught: TF2 and TF5 at 4/4 |
| `r5-granted-slope-at-stage-index` | granted slope read at `cidx_q2_r` | caught: admission suite, 559 FAIL at N = 2 |
| `r5-eq-slope-write-only-when-valid` | expected equivalent: slope write also gated by `valid_q2_r` | survives `srp_stream_fsms`, `srp_top` and `srp_admission` with every tally unchanged, as an equivalent edit must |
| `r5-eq-wtsp-write-in-reset` | expected equivalent: the `rst_n` term dropped from the walk-copy write | survives all three suites, tallies unchanged |

All 8 defect probes are caught at every shape where the edited arm is elaborated. Both equivalent probes leave every suite green, which confirms my reading that their terms cannot be observed. Receipts: `receipts/probes/summary.txt` and the per-probe logs.

## 3. Lens results (clean-lens format, each with the artifact examined)

- `[R458] PASS Conformance` -- issue #230 acceptance 1-5 and the lane rules (5974045353, 5977836860), checked against the evidence below.
  - Criterion 1: the SRP suites pass. The new arms run the product's 1x1 shape (2/2) and 8x8 shape (9/9). `baseline_chparam.txt` binds `N_STREAM_*_P` = 2 and 9, and `KL_srp_top` gets them directly (`protocol_processor_top.sv:2485-2486`).
  - Criterion 2: `u_srp` falls from 4,558 to 3,988 LUT and 6,438 to 3,979 FF at 1x1, from 8,705 to 7,313 LUT and 11,192 to 7,747 FF at 8x8, and from 4,340 to 3,711 LUT and 6,263 to 3,839 FF in the route.
  - Criterion 3: no fixed eight-slot structure remains in `hdl/srp/*.sv`. Every per-stream array is sized by `N_SOURCES_P` and `N_SINKS_P`.
  - Criterion 4: the head route gives WNS +0.354 and WHS +0.036 at the declared 50 MHz, all constraints met. Base gave +0.079 and +0.014.
  - Criterion 5 is a manager duty (section 8).
  - No port, parameter or register meaning changes. The walk copies do not move any output cycle (RTL lens).
  - The IEEE 802.1Q F10.7/F10.8 FirstValue layout is unchanged. The walk arms check it byte for byte against an independent builder (`walk_main.cpp:132-154`).
- `[R458] PASS RTL` -- `hdl/srp/KL_srp_talker_fsm.sv:353-372,495-537,587-596`, `KL_srp_listener_fsm.sv:534-558,621-636`, `KL_srp_admission.sv:111-169,195-210` and `KL_srp_top.sv:944-985`, read against the base flops. The base's own flops were the reference for each point below.
  - Each copy's write enable equals the enable of the flop record it mirrors:
    - talker: `rst_n && gate_acc_w && gate_open_i` against `:587-592`;
    - listener: `rst_n && ctl_acc_w && ctl_settle_i` against `:622-626`;
    - admission: stage 3 every non-reset cycle, as at base;
    - FIFOs: an unchanged push term, split one memory per FIFO.
  - Every read address is a registered index (`wsrc_r`, `aidx_r`, `tf_rptr_r`). An asynchronous read returns the pre-edge value on a same-cycle write, exactly as the flops did. The FIFO head keeps its registered `tf_q_r`.
  - A copy is consumed only under its valid bit:
    - `rec_valid_r[wsrc_r]` at `talker:615` and `listener:655`; it is set only by the write that fills the copy and cleared only by reset;
    - `slope_valid_r` at `admission:196-210`, written in the same edge as the slope;
    - the FIFO count.

    So the removed resets cannot be observed.
  - Widths: `WTSP_W_C` = 68 and `WID_W_C` = 124, with field slices `wid_w[123:60]`, `[59:12]`, `[11:0]` and `wtsp_w[67:52]`, `[51:36]`, `[35:32]`, `[31:0]`. They match the write concatenations.
  - The generate split at N > 2 is functionally equivalent at every N (R459-1's two threshold edits survive, as noted in the README).
- `[R458] PASS Robustness` -- the same RTL, together with `walk_main.cpp` WK1, WK5, WK6, WK9 and WK10 and `store_main.cpp` TF4/TF5.
  - Unreset memory starts random in the walk arms, and 8 further seeds per shape pass.
  - Mid-run reset (WK5) is covered.
  - An idle face is parked on an out-of-range index: index 15 at 1, 3 and 9 sources (WK1, WK6).
  - An offer held under back-pressure from a busy decoder bus (WK9, WK10) is taken exactly once.
  - The FIFO full boundary is held by the one documented test-only force (TF4/TF5).
  - The arms also pass at 1/9, 9/1, 2/3, 3/2, 5/16 and 16/16.
- `[R458] PASS Tests` -- `tb/srp_stream_fsms/walk_main.cpp`, `srp_walk_wrap.sv` and `Makefile:18-61`; `tb/srp_top/store_main.cpp`, `srp_store_wrap.sv` and `Makefile:24-70`; `tb/srp_top/mutants.py:110-152,245`; and the 35 `tb/srp_top/mutations/*.patch`.
  - Expectations are built independently. FirstValues and MRPDUs come from the 802.1Q layouts, and the FIFO model from the contract. None is read from the DUT.
  - Each new check fails for the defect it names: 128/128 and 80/80 at this head, and 8 of 8 of my own defect probes caught.
  - Preconditions are checked.
  - Both elaboration arms run in the default `make`, and a failure propagates to the exit status.
- `[R458] PASS Docs` -- `docs/architecture/10_srp_engine.md:194-252` (§5.1), `docs/guides/hdl-engineer.md:88-94`, `tb/srp_stream_fsms/README.md:5-10,171-216`, `tb/srp_top/README.md:14-17,497-632` and the PR body as fetched at review time (`receipts/pr154-body.md`).
  - The storage table matches the RTL (68/124/104-bit widths, `41 + SLOT_AW_P` FIFO words).
  - The marginal-cost table matches the reports: talker 129/168 (base 213/221), listener 208/278 (227/278), admission 69/69 (73/101), engine 475/538 (592/679).
  - The two README tables match the receipts.
  - The PR body's Vivado table, its LUT/FF deltas (-37/-168 and -791/-762) and its 19/1/7/4 shape summary recount.
  - Added Markdown has no U+2014 and no host, path or bench identifiers.
  - The lane's 14 non-merge commits are one line each with no trailers.

## 4. Findings

No BLOCKER, MAJOR, MINOR or RESIDUE.

### R458-5-S1: SUGGESTION. Lenses: RTL, Docs. The FIFO comment's flip-flop formula is the pre-trim size

- **Where:** `hdl/srp/KL_srp_top.sv:947-950`. The comment says the two-dimensional array "mapped to 2 x 32 x TFW_C flip-flops".
- **Evidence:**
  - `TFW_C` = 41 + `SLOT_AW_P`, which gives about 3,000 bits at the product shapes.
  - The base synthesis kept 2,304 flip-flops at 1x1, and #638 reports 2,688 at 8x8, after constant bits were trimmed.
  - `docs/architecture/10_srp_engine.md` §5.1 states the measured 2,304 correctly.
- **Impact:** none on behaviour, tests or any published figure. This is the same observation as R459-4-S1, reached independently.
- **Optional outcome:** "up to 2 x 32 x TFW_C flip-flops (2,304 after synthesis at 1x1)".
- **Verification:** re-read the comment.

## 5. Ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #230 acceptance 1-5 and lane rulings; `06fe795b` hierarchy, timing and chparam reports; `protocol_processor_top.sv:2485-2486`; suites at 2/2 and 9/9 | R458-5 | d18270d69eea9cdf35f846c77821d5488dab97cc |
| RTL | CLEAN | `KL_srp_talker_fsm.sv:353-372,495-537,587-596`; `KL_srp_listener_fsm.sv:534-558,621-636`; `KL_srp_admission.sv:111-169,195-210`; `KL_srp_top.sv:944-985` | R458-5 | d18270d69eea9cdf35f846c77821d5488dab97cc |
| Robustness | CLEAN | valid-bit gating of the unreset memories; WK1/WK5/WK6/WK9/WK10; TF4/TF5; 8 extra shapes; 32 extra seeds; 2 equivalent probes | R458-5 | d18270d69eea9cdf35f846c77821d5488dab97cc |
| Tests | CLEAN | `walk_main.cpp`, `store_main.cpp`, both wraps, both Makefiles, `mutants.py`, 35 patches; campaign 128/128 (80/80); 8/8 defect probes caught; table recount 31/31 rows plus 12 slope cells | R458-5 | d18270d69eea9cdf35f846c77821d5488dab97cc |
| Docs | CLEAN | `10_srp_engine.md:194-252`; `hdl-engineer.md:88-94`; both READMEs; PR body at review time; commit messages | R458-5 | d18270d69eea9cdf35f846c77821d5488dab97cc |

## 6. Prior public findings at this head (read after my verdict and ledger were drafted)

| Finding | Status at `d18270d6` | Basis |
|---|---|---|
| R459-1-F1 = R458-1-F2 (MINOR): Vivado receipts unpublished | RESOLVED | Published at `06fe795b`. Every figure re-derives (`receipts/vivado-rederive.txt`). |
| R459-1-F2 = R458-1-F3 (MINOR): control-coverage overclaim | RESOLVED | Row-by-row tables; 31/31 rows and 12 slope cells equal my receipts; the 19/1/7/4 summary recounts. |
| R458-1-F1 (MINOR): new storage paths and the N <= 2 arm untested | RESOLVED | WK1-WK10 and TF1-TF5 at 1/1, 2/2, 3/5 and 9/9 in the default `make`; probes killed in the campaign. |
| R459-1-R1, R459-1-R2 (RESIDUE) | RESOLVED | The body names `docs/architecture/10_srp_engine.md` section 5.1 in full; the Validation header carries the gate-16 exception. |
| R459-1-S1, R458-1-S1 (SUGGESTION) | TAKEN | `hdl-engineer.md:88-94`; TF4/TF5 exercise the full guard. |
| R459-1-S2 (SUGGESTION) | Answered by committed arms | WK/TF arms; the round-1 bench is published with digests. |
| R459-2-F1 = R458-2-F1 (MINOR): the 1/1 zero of `wsid-flops-of-control-sink` | RESOLVED | `tb/srp_top/README.md:571-576,607,623-628` and the body say "equivalent in simulation". The receipt shows 0 at 1/1 and 5 at 2/2. |
| R459-2-R1, R458-2-R2-R1, R458-2-R2-R2 (RESIDUE) | RESOLVED | The body's head line names `d18270d6`; `hdl-engineer.md:88-90` attributes the slopes to the admission walk. |
| R458-3-F1 (MINOR): ready term of the walk-copy writes unpinned | RESOLVED | WK9/WK10. The committed controls fail WK9 at 4/4 and WK10 at 3/5 and 9/9. My RAM-arm-only probe `r5-wid-write-ignores-ready` is caught by WK9 at 3/5 and 9/9. |
| R458-3-R1 (RESIDUE): hdl-engineer lead-in | RESOLVED | `hdl-engineer.md:88-94` carries the lead-in as written; no line exceeds 86 columns there. |
| R458-4-F1 (MINOR): body said "no HDL" / "this processor" for the Vivado head | RESOLVED | Body lines 91, 123, 244 and 307 now read as its required outcome. `git diff --stat 65324390 d18270d6 -- hdl` lists the 4 non-SRP files, and `-- hdl/srp` is empty, as the body states. |
| R458-2-S1 = R459-3-S1 = R459-4-S2 (SUGGESTION): randomise unreset memory in the FIFO arms | Open, optional | The `tb/srp_top/Makefile` storage build still lacks `--x-initial unique`. TF1/TF2 already fail on an invented or stale word. |
| R458-2-S2 = R459-3-S2 (SUGGESTION): name the 1/1 alias beside WK6 | Open, optional | It is named in `tb/srp_top/README.md` only. |
| R459-3-S3 (SUGGESTION): rewrap `hdl-engineer.md:90` | TAKEN | `d18270d`. |
| R459-4-S1 (SUGGESTION): FIFO comment formula | Open, optional | Same as R458-5-S1. |
| R459-4-S3 (SUGGESTION): listener RAM arm at N = 3 not built by a committed suite | Open, optional | My 2/3 run elaborates it and passes 51/51 (`receipts/walk-extra/walk-2x3.log`). |

No prior MINOR, MAJOR, BLOCKER or RESIDUE remains open.

## 7. Real limits

- **No Vivado run at this head.** The area and timing figures are the round-1 runs (`65324390`), re-derived from the published reports. SRP HDL is byte-identical since then. The whole-design rows reflect the round-1 tree, and the body says so. At this head the merges of `main` changed non-SRP HDL, so a rebuild would change those rows (manager duty).
- **No lockstep bench re-run.** I did not re-run the round-1 lockstep. My equivalence position rests on three things:
  - the RTL reading;
  - the committed arms;
  - the two equivalent probes that survive while 8 of 8 defect probes are caught.
- **No banks.** I ran no full processor, parent, gPTP, Yosys or builder bank, no xvlog/xelab, no act and no hosted CI. Of the processor suites I ran only the SRP suites and `pp_top`.
- **Physical calibration NOT RUN.** Field skips are not hardware proof.
- **Unprobed corner.** Out-of-range valid gate/control indices are undefined in base and head alike. `KL_srp_top` never offers them, as R459-4 observed. I did not probe them.
- **Path placeholders.** The receipts were rewritten so that local absolute paths read `<packet>`, `<pinned-verilator-5.050>`, `<pinned-verilator-root>` or `$HOME`. The raw copies are kept, unpublished, in scratch.

## 8. Pending manager duties

- Build and validate the final current-dev candidate at the merge turn. The source base is `c4cb84ff`, and live dev is `fea346e7`.
- Hosted and act acceptance (exact-head `rtl-fast`, `verilator-suites`, `yosys-portability`), plus the parent consumer set with the c8, p2-p1 and c10 patches. Gate 16's T30 checks are recorded against #643.
- Acceptance 5: document the scaling and latency trade-offs in milan-fpga #229. The figures are in `docs/architecture/10_srp_engine.md` §5.1, and the shared-evaluator trade-off is in ruling 5977836860. The lane did not post to #229.
- Close #230 by hand at the processor merge. The PR says "Relates to", per 5977836860.
- Optionally, carry R458-5-S1 and the open prior suggestions to the residue checklist.

## 9. Packet

Everything published is listed in `MANIFEST.sha256`:

- `scripts/`: `run_focused.sh`, `make_probes.py`, `run_probes.py`, `walk_shapes_seeds.sh`, `slope_shapes.sh`, `control_table.py`, `vivado_rederive.py`;
- `probes/*.patch`;
- `receipts/`.

The clone was restored and verified (`receipts/clone-integrity.txt`):

- HEAD is `d18270d6` and the tree is `5ff7ea39`; `write-tree` equals the tree;
- status, `diff-index` and `diff-files` (after `--really-refresh`) are all empty;
- there are no skip-worktree or assume-unchanged entries;
- there are 0 gitlinks: this repository has no submodules.

R458-5 FINISHED
