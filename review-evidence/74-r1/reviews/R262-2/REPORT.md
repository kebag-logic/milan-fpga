[R262] POSITIVE - exact head 2accfadfd3d4d8a318e3e714ee0dc87fc84e4164

Round R262-2: internal cleared-context re-review of issue #74 ledger item 2
(junction-counter raced-lock chatter), PR #528.

- Head `2accfadfd3d4d8a318e3e714ee0dc87fc84e4164`, tree
  `37b72c34062ccf6c9370311cd2e203a64c65fdd0`. Lane base
  `ede8d48ecd7c7f589a14b957951f040d92c99c70`.
- My previous round, R262-1, reviewed `6d1572d6`. Since then there are two
  commits: `553edeb8` (generated matrix) and `2accfadf` (the Docs follow-up).
- Items 1, 3 and 4 of #74 are out of scope and were not reviewed.

## Verdict in brief

POSITIVE. All five lenses are covered CLEAN at this exact head.

- **R262-1 F1 (BLOCKER, Docs) is resolved.** The matrix was regenerated at
  `553edeb8`. It is still up to date here. The hosted `docs-check` at this
  head executed all 47 steps, and none were skipped.
- **R262-1 F2 / R263-1 F1 (the same MINOR, Docs) is resolved.** The
  rewritten `SLIP_TDM` paragraph and the aligner banner now claim what the RTL
  implements and what the arms grade. I checked every sentence against the
  RTL, the arms and my own probes on the real RTL.
- **The delta since my previous round touches only documentation.** The one
  `.sv` hunk is inside the banner comment. The preprocessed source is
  byte-identical at `6d1572d6`, `553edeb8` and `2accfadf`.
- **This round opens no MINOR or higher finding.** It has three optional
  suggestions.
- **Out-of-scope new work, N1.** `KL_media_nco` can drop two packet-grid
  ticks when the aligner's per-frame command reaches its terminal count. I
  found this independently during this round's probes. It is the same defect
  as R263-1's O1. It is pre-existing, and this PR reduces its exposure rather
  than causing it. It needs a new public Issue. The reasoning for keeping it
  out of this PR's coverage is in the N1 section.

## Reconstruction (public state only, in order)

1. `AGENTS.md`, `CONTRIBUTING.md` (sections 2, 3 and 6.1), and
   `docs/README.md` (requirements over interfaces, code, tests and
   summaries).
2. Issue #74:
   - the body;
   - the reopening ledger (issuecomment-5507453907), item 2;
   - the [A10] assignments (5794151797, 5797374041);
   - [A197] TAKEN, DECISION and REVIEW READY (5794228544, 5794560116,
     5795282366);
   - [A207] REVIEW READY (5797448207).
3. Interface authorities:
   - `docs/reference/REGISTER_MAP.md`, the 0x8D4 section (`SLIP_TDM`);
   - `docs/design/TIME_SYNC.md:114`;
   - the root wiring: the aligner at `hdl/milan/milan_datapath.sv:5562-5574`
     (`MILAN_CLK_FREQ_HZ` = 100 MHz, default keep-off), whose `u_o` drives
     the NCO's `servo_trim_i` at `:774`.
4. Diffs:
   - `git diff ede8d48e..2accfadf` (12 files);
   - the deltas `6d1572d6..553edeb8` and `553edeb8..2accfadf`.
5. Public evidence, read as claims to reproduce:
   - PR #528 body;
   - the [A10] source-validation comment (5795493487, at `6d1572d6`);
   - `review-evidence/74-r1/correction-a207/HANDOFF.md` and
     `author-a197/HANDOFF.md` at `0278bc39`.
6. After my own verdict and ledger were drafted, the prior reviews: R262-1
   (issuecomment-5796351579) and R263-1 (5797369587).

## The delta since my previous round (E2)

| Commit | Paths | Nature |
|---|---|---|
| `553edeb8` | `docs/traceability/MODULE_MATRIX.md:71`, `hdl/ieee1722/aaf/README-tests.md:20` | Generator output: +1/-1 each, adding `media_grid_align` to `KL_chan_map_capture` |
| `2accfadf` | `docs/reference/REGISTER_MAP.md` (+24/-9) | The `SLIP_TDM` paragraph, the ceiling row and the INTERNAL reading row |
| `2accfadf` | `hdl/ieee1722/crf/KL_media_grid_align.sv` (+6/-3) | One hunk at lines 84-89, inside the `/* ... */` banner (lines 3-101) |

**The `.sv` change is comment-only, by two methods:**

- `verilator -E -P` output sha256 is
  `e3a16b1811a1f117b9e54788e57333a72fcbc32761dbe6f939ec9e46630079a9` at all
  three heads (blobs `4d298a83`, `4d298a83`, `cc418322`).
- A comment-stripped text comparison of `553edeb8` and `2accfadf` is equal.

Nothing under `tb/` changed after `6d1572d6`. No other `hdl/` logic changed.

## Claim-by-claim check of the rewritten text

Each row is a claim at this head, the authority it rests on, and my
executable check.

| # | Claim (`REGISTER_MAP.md` unless stated) | Authority | Check | Result |
|---|---|---|---|---|
| C1 | `:1816-1818` A coincidence counts nothing; the tick takes the pending marker if any, and the coincident one pends in its place | `KL_chan_map_capture.sv:541-546`: `pend <= pend`, no count | E4 [T0] coincidence checks; E5 | holds (see S1 on wording) |
| C2 | `:1818-1821` From the first frame on and below the ceiling, dups minus skips follows ticks minus markers within one; the NET count is the slip count, +1 slow and -1 fast | Law at `:529-548`; fed gate `:531,538` | E5, P-LAW: 13,353,490 checked cycles in 6 scenarios, including 27,222 coincidences over a pending marker and runs to saturation. `(dups-skips)-(ticks-markers)` spans exactly width 1; there are 0 dups before the first frame. E6: net exactly +1 or -1 in 128/128 passages | holds |
| C3 | `:1822-1825` Each half counts once while the marker dithers between two adjacent cycles; that is what [G9] grades, with no jitter | `sim_main.cpp:363-378`; `anchor_grid()` clears `marker_jitter` (`:280`) | E6: 64 unjittered passages, dither depth exactly 1, each exactly 1/0 (slow) or 0/1 (fast). E3: [G9] 1/0 and 0/1 | holds |
| C4 | `:1825-1828` A wider dither, such as the suite's one-edge delivery jitter, adds balanced pairs; only the difference is the slip | the same law | E6: 64 jittered passages, depth exactly 2, dups 0-8 and skips 1-8, net exactly +1 or -1. E5: jittered scenarios 5/6 and 14/15 | holds |
| C5 | `:1828-1831` Before item 2: about a dozen dups per slip, skip-direction slips read as dups, and thousands of dups per 0.2 s at a lock on the tick | base law | E3 `MGA_MUT_COIN`: 11 dups; mirrored 10 dups, 0 skips. R262-1 E2 base [G7] windows up to 2431 per 0.2 s | holds |
| C6 | `:1831-1835` The engagement capture is clamped into [`LOCK_KEEPOFF_CYC_P`, `DIV_C - LOCK_KEEPOFF_CYC_P`]; default `DIV_C/128`, 16 cycles at 100 MHz, just under 1/128 sample | `KL_media_grid_align.sv:117,182-186,267`; 2083/128 = 16 < 16.28 | code read; not overridden at the root (`milan_datapath.sv:5562-5565`) | holds |
| C7 | `:1835-1837` and banner `:84-87` The marker dithers around that target, so clearance at lock is the keep-off less the lock's dither and the delivery jitter | the PI integrator drives the mean error to the reference (`:284-293`) | E7: 96 locks, both rates, 24 phases, 2 seeds. All count 0/0. Clearance is 13-15 on clamped targets and 13-16 at the band edges | holds |
| C8 | `:1837-1840` and banner `:87-89` [G7]/[G8], engaged on and just before the tick with one edge of jitter, grade clearance at 12 or more and count 0/0 over their lock windows; at the [G7] lock a held frame is 1 dup and a surplus 1 skip | `sim_main.cpp:50,296-360` | E3: [G7] 8 x 0.2 s 0/0, clearance 15, held 1/0, surplus 0/1; [G8] 0/0, clearance 14 | holds |
| C9 | `:1780` 35.6 h at one dup per slip; sooner under a wider dither | 65535 x 1.958 s = 35.6 h | arithmetic; C4 | holds |
| C10 | `:1850` INTERNAL row: dups minus skips climbing 0.51/s; dups alone at 0.51/s only under two-adjacent dither; a wider dither adds skips and as many dups | C2-C4; 1/1.958 s = 0.51/s | E5, E6 | holds |

## Findings of this round

No BLOCKER, MAJOR or MINOR finding.

### Suggestions (optional; they do not affect coverage)

- **S1, Docs, `docs/reference/REGISTER_MAP.md:1816-1818`.** The coincidence
  sentence can be read literally as "the coincident marker always pends".
  The RTL keeps `pend` unchanged, and the banner at
  `KL_chan_map_capture.sv:504` says "so pend carries over". Adding that
  clause, or "with none pending, the tick takes the coincident marker",
  removes the reading. The "always pends" law is R262-1's mutant MC1, which
  [G9] and [T0] reject.
- **S2, Docs, nominal "1/128 sample" wording.** The register page now states
  the precise value: `DIV_C/128`, 16 cycles at 100 MHz, just under 1/128
  sample. Three places still say "1/128 sample" flat:
  - `docs/design/TIME_SYNC.md:114`;
  - the parameter comment at `KL_media_grid_align.sv:116`;
  - `KL_chan_map_capture.sv:513`.

  Separately, the Contents description at `REGISTER_MAP.md:199` says "one
  dup per fed pair per beat period". Read for `SLIP_TDM`, that holds only
  under the two-adjacent-cycle condition. All four are nominal wordings from
  before this correction, and none is false at the resolution it states.
- **S3, Docs and Robustness, the PR body's "Known limitations".** It says
  acquisition crossings "count balanced dup/skip pairs". N1 shows that an
  acquisition crossing can also drop two real ticks and leave net -1. Once
  N1's Issue is filed, the PR body could cite it. This is a PR-body edit, so
  it does not move the head. It agrees with R263-1's note on R262 S1 and its
  S3 on [G8]'s seed margin. The [G8] geometry with jitter seed 4 drops ticks
  during acquisition (E8), although the committed seed does not.

## New work outside this diff: N1 (recommend a new public Issue; not attributed to PR #528)

**`KL_media_nco` drops two packet-grid ticks when its trim falls on the
lent cycle.**

- **Where:** `hdl/ieee1722/crf/KL_media_nco.sv:198-227`, unchanged by this PR
  (`git diff ede8d48e 2accfadf -- hdl/ieee1722/crf/KL_media_nco.sv` is empty).
- **Mechanism:**
  - `end_w` (`:206-208`) is combinational in `trim_r` through `ov_w`/`un_w`.
  - The terminal test is an equality, `32'(cnt_r) == end_w` (`:216`).
  - Suppose a speed-up command reaches `trim_r` on the cycle where `cnt_r`
    equals the lent-cycle end, and it lowers `end_w` below `cnt_r`. Then the
    equality never fires, and the 12-bit `cnt_r` runs through its wrap.
  - The next tick comes about 6179 cycles later, so two ticks are missing.
  - The premise at `:187-191` ("servo_trim_i moves at most once per servo
    tick", about 1 ms) no longer holds. At the root, `servo_trim_i`
    (`milan_datapath.sv:774`) is the aligner's `u_o` (`:5571`), rewritten on
    every frame at the marker's phase.
- **Evidence (all mine; found before I read R263-1):**
  - **E10, NCO alone, with no loop and no jitter:**
    - a step from -183 to +3200 LSB applied 2081 or 2082 edges after a tick
      drops ticks: 2 of 8364 trials, gaps 6178 and 6179;
    - the realistic loop step from -183 to -179 drops ticks 1 time in 6000
      trials;
    - slow-down steps and the no-step control drop 0.
  - **E9, closed loop at this head** (slow feed, engaged at phase 2060, which
    is not clamped, jitter seed 1):
    - frame 14067 is captured 4165 edges after a tick;
    - frame 14068 reads err -1991, and u goes to the +3200 rail;
    - the loop re-acquires by about 1.7 s.
    - The err/u trajectory is identical with the base aligner, so this PR
      plays no part at that phase.
  - **E8, acquisition sweep of 152 runs:**
    - 6 runs drop ticks during acquisition, all with one edge of jitter and
      none without;
    - 4 of the 6 lock onto a clamp bound, and 2 of those because this PR
      clamped them: fast phase 2, and slow phase 2082, which is [G8]'s
      geometry at jitter seed 4;
    - every run's last 0.5 s counts 0/0, with clearance at least 14;
    - without a drop, the acquisition net is always 0 (balanced).
  - **E11, base against head at raced-from-below phases 2079-2082 (16 runs
    each, one edge of jitter, 2.5 s):**
    - base drops ticks in 9 runs, and 6 base runs still count in their last
      0.5 s (up to 1381 dups and 221 skips). Those windows mix old-law
      chatter with drops, and this probe does not separate them;
    - head drops ticks in 1 run, during acquisition only, and every head lock
      is clean.
- **Classification:**
  - Pre-existing, in a module this PR does not change.
  - Exposure is reduced, not introduced: the keep-off moves every lock out
    of the hazard window, leaving only a bounded exposure during acquisition.
  - No claim this PR adds depends on it. Every rewritten claim is at lock, or
    is the net-count law, which counts N1's hole honestly as a real slip.
  - AGENTS.md section 7 says "a finding moved to another Issue is not
    resolved". That rule governs defects in the artifacts a PR ships under
    review; the protocol-processor #13 case was the PR's own
    `KL_pp_nvm_port.sv`.
  - Fixing an unchanged NCO in this lane would be the silent scope expansion
    that section 4 forbids.
  - So N1 needs its own Issue. I do not count it against a lens here. The
    manager or maintainer may overrule this classification.
- **Impact when it fires:**
  - under CRF selection, a real two-sample hole in `media_tick_p`;
  - the aligner mis-folds on the saturated capture and slews at the
    +/-200 ppm rail for hundreds of ms;
  - the junction words record net -1 honestly.
- **Concordance:** this matches R263-1 O1 in mechanism, location and
  classification. I did not re-verify R263-1 O2 (the unwrapper fold under a
  half-sample surplus marker); it stays theirs to route.

## Lens results (each against the exact head)

- [R262] PASS Conformance - `REGISTER_MAP.md:1780,1813-1840,1850`; `KL_media_grid_align.sv:72-89,117,182-186,267`; `KL_chan_map_capture.sv:502-546`; `milan_datapath.sv:5562-5574`; #74 item 2 (5507453907) and the [A10] Docs-only assignment (5797374041) - every rewritten claim holds against the RTL and the arms (C1-C10). Item 2's behaviour is unchanged from R262-1: E3 shows raced locks 0/0 and held/surplus 1/0 and 0/1, and E7 shows 96 of 96 locks at 0/0. The follow-up changed no logic (E2), and it matches the assignment's Docs-only scope.
- [R262] PASS RTL - `KL_media_grid_align.sv` blob `cc418322` against `4d298a83`, and the preprocessed sha256 `e3a16b18...79a9` at all three heads (E2); `KL_chan_map_capture.sv` unchanged since `6d1572d6` - the one RTL-file change is comment-only, so R262-1's RTL analysis at `6d1572d6` applies unchanged to identical preprocessed source. Lint at this head passes 90 <= 90; `check_sv_idiom`, `measure_naming --check`, `check_port_contracts`, `check_hygiene --check` and `check_todo_ownership` pass (E12). N1 is outside the diff.
- [R262] PASS Robustness - `receipts/probe_law_head.txt`, `passage_sweep.txt`, `lock_sweep.txt`, `acq_sweep.txt`, `acq_*_rtl_raced_below.txt`, `probe_nco_head.txt` - these checked random coincidence storms to saturation, jitter 0 and 1 on passages, every clamp boundary (15/16/17, 2066/2067/2068) and both rates at lock, and acquisition from both sides. The PR's logic is robust to all of them. N1 is pre-existing, reduced by this PR, and routed as new work.
- [R262] PASS Tests - `tb/verilator/media_grid_align/{sim_main.cpp,Makefile,media_grid_align_wrap.sv}` and `tb/verilator/chmap_capture/sim_main.cpp`, unchanged since `6d1572d6` (E2) - at this head, `media_grid_align` passes 45/45 and all three committed negative controls are red on their own arms (E3). `chmap_capture` passes 204/204 and the netlist leg 20/20 (E4). The arms the docs cite grade what the docs say: [G9] with jitter off, and [G7]/[G8] with a clearance floor of 12 (C3, C8). R262-1's six reviewer mutants (at `6d1572d6`) ran against identical harness and RTL logic.
- [R262] PASS Docs - `REGISTER_MAP.md:1780,1813-1840,1850`; `KL_media_grid_align.sv:84-89`; `MODULE_MATRIX.md:71`; `hdl/ieee1722/aaf/README-tests.md:20`; plus the untouched `TIME_SYNC.md:114`, `TESTING.md:428`, `tb/verilator/media_grid_align/README.md` and `KL_chan_map_capture.sv:502-515` - checked against the RTL and E3-E7. `docs_check` reports 0 findings, and `check_em_dash --base ede8d48e` 0 findings over 54 added lines. `check_doc_style`, `gen_toc --check`, `gen_toc --verify-anchors`, `gen_module_matrix --check` and `check_doc_paths` pass, and `git diff --check` is clean (E12). The hosted `docs-check` at this head ran 47 of 47 steps (E13). S1 and S2 are optional.

## Evidence (all at the exact head unless stated)

The simulator is the pinned Verilator 5.050. The launcher sha256 is
`905795b9...e92f` and `verilator_bin` is `44898b22...bfdd`
(`receipts/tool_identity.txt`). `scripts/vwrap.sh` caps every build at
8 jobs, and the sweeps use `xargs -P 8`. All builds and probes ran in
`git archive` extractions under the packet's `scratch/`. Only the read-only
gates of E12 ran in the review clone.

| ID | What | Result | Receipt |
|---|---|---|---|
| E1 | Clone state, start and end | HEAD/tree exact; index equals HEAD; 0 byte or mode mismatches; no untracked or ignored entries; no skip/assume flags; 3 gitlinks checked out clean, `external` uninitialised as at start | `receipts/clone_state_start.txt`, `receipts/clone_state_end.txt`, `scripts/verify_clone.sh` |
| E2 | Delta and comment-only proof | as in "The delta since my previous round" | `receipts/delta_proof.txt`, `scripts/delta_proof.sh` |
| E3 | `make -C tb/verilator/media_grid_align` | 45/45; G7 windows all 0/0, clearance 15; G8 0/0, clearance 14; G8 acquisition 84/84. `MGA_MUT_U_SIGN` fails [G2] (11040). `MGA_MUT_NO_KEEPOFF` fails [G7] (5203; windows 994-1422 pairs from window 4). `MGA_MUT_COIN` fails [G9] (11 dups; mirrored 10 dups, 0 skips) | `receipts/head_media_grid_align.log`, `receipts/head_mut_{usign,keepoff,coin}.log` |
| E4 | `make -C tb/verilator/chmap_capture` | 204/204, netlist 20/20, including the three carried-coincidence [T0] checks | `receipts/head_chmap_capture.log` |
| E5 | P-LAW, real `KL_chan_map_capture`, driven tick and marker | See C2. Width 1 in all 6 scenarios | `receipts/probe_law_head.txt`, `scripts/probe/probe_law*.{sv,cpp}` |
| E6 | Passage sweep: 128 runs, 8 start offsets per direction, jitter 0 and 1, 4 seeds | Jitter 0: depth 1, exactly one count in its direction (64/64). Jitter 1: depth 2, balanced extra pairs, net exactly +1 or -1 (64/64) | `receipts/passage_sweep.txt`, `scripts/run_sweeps.sh`, `scripts/probe/probe_loop.cpp` |
| E7 | Lock sweep: 96 runs, 24 phases x 2 rates x 2 seeds, one edge of jitter, 1 s settle then 1 s | 96/96 count 0/0. Clearance is 13-15 on clamped targets, 13-16 at the band edges and 14-22 inside the band. The exception, slow 2060 seed 1 at 3 cycles, was still re-acquiring after N1 (E9) | `receipts/lock_sweep.txt` |
| E8 | Acquisition sweep: 152 runs, 19 phases (the crossing side for each rate, plus [G7]'s phase 0), jitter 0 and 1, 4 seeds, 2.5 s | 6 NCO-drop runs, all jitter 1, none at jitter 0; every last-0.5 s window 0/0 with clearance at least 14; without a drop, acquisition net is 0 | `receipts/acq_sweep.txt`, `scripts/run_acq_sweep.sh` |
| E9 | N1 traces | Per-frame trace at frames 14058-14070; 0.1 s trace over 6 s for seeds 1 and 2; identical err/u with the base aligner | `receipts/ftrace_nco_tick_drop_slow2060_seed1.txt`, `receipts/trace_acq_*.txt`, `scripts/probe/probe_dbg.cpp` |
| E10 | P-NCO, `KL_media_nco` alone | See N1 | `receipts/probe_nco_head.txt`, `scripts/probe/probe_nco.cpp` |
| E11 | Base against head, raced-from-below acquisition | See N1 | `receipts/acq_base_rtl_raced_below.txt`, `receipts/acq_head_rtl_raced_below.txt` |
| E12 | Focused gates in the clone (exit codes captured per gate) | All rc 0, as listed in the Docs and RTL lines | `receipts/head_gates.log`, `scripts/run_gates.sh` |
| E13 | Hosted contexts at this exact head (observed, not accepted) | The seven required contexts succeeded: `rtl-fast`, `docs-check`, `wire-accountability`, `docs-check-no-git`, `elaborate`, `verilator-suites`, `yosys-portability`. Verilator shards 0-4 executed (6-34 min). `rtl-fast` is an aggregator step. Yosys shards restored a dev-seeded result cache. `Physical gPTP` was SKIPPED and is not evidence | `receipts/hosted_checks_observed.txt`, `receipts/hosted_job_steps_observed.txt`, `receipts/hosted_docs_check_steps_observed.txt` |

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Item 2 and the Docs-only assignment; C1-C10 against `KL_chan_map_capture.sv:502-546`, `KL_media_grid_align.sv:72-89,117,182-186,267`, `milan_datapath.sv:5562-5574`; E3, E5-E7 | R262-2 | `2accfadfd3d4d8a318e3e714ee0dc87fc84e4164` |
| RTL | CLEAN | The comment-only proof for `KL_media_grid_align.sv` (E2); `KL_chan_map_capture.sv` unchanged; lint and idiom, naming, port and hygiene gates (E12). The logic analysis is R262-1's, on preprocessed-identical source | R262-2 | `2accfadfd3d4d8a318e3e714ee0dc87fc84e4164` |
| Robustness | CLEAN | E5-E8, E10, E11; N1 is pre-existing, reduced, and routed as new work | R262-2 | `2accfadfd3d4d8a318e3e714ee0dc87fc84e4164` |
| Tests | CLEAN | Both suites and all committed negative controls re-run (E3, E4); cited arms graded as the docs say (C3, C8); `tb/` unchanged since R262-1's mutant campaign at ancestor `6d1572d6` | R262-2 | `2accfadfd3d4d8a318e3e714ee0dc87fc84e4164` |
| Docs | CLEAN | `REGISTER_MAP.md:1780,1813-1840,1850`; `KL_media_grid_align.sv:84-89`; `MODULE_MATRIX.md:71`; `README-tests.md:20`; `TIME_SYNC.md:114`; `TESTING.md:428`; bench README; `KL_chan_map_capture.sv:502-515`; E12, E13 | R262-2 | `2accfadfd3d4d8a318e3e714ee0dc87fc84e4164` |

Every lens was applied at this head. So the ledger does not rest on an
ancestor round, although R262-1 at `6d1572d6` supplied the unchanged RTL
analysis and the mutant campaign on identical logic. A later commit that
touches a lens's scope un-covers that lens.

## Prior public review findings on PR #528 (read after the verdict above was drafted)

| Prior finding | State at `2accfadf` | Basis |
|---|---|---|
| R262-1 F1 (BLOCKER, Docs): stale `MODULE_MATRIX.md:71` and `hdl/ieee1722/aaf/README-tests.md:20` | **RESOLVED** | Regenerated at `553edeb8`; neither file changed since. `gen_module_matrix --check` reports up to date, rc 0 (E12). The hosted `docs-check` here ran all 47 steps, and step 16 succeeded (E13) |
| R262-1 F2 = R263-1 F1 (MINOR, Docs): the `SLIP_TDM` paragraph overstates passage exactness and lock clearance | **RESOLVED** | Each required outcome is met. (a) C2-C4 state the passage law with its condition, dups minus skips as the slip count, and balanced pairs under a wider dither. The ceiling row (C9) and the INTERNAL row (C10) follow. (b) C6-C8 give the clamp, the 16-cycle default "just under 1/128 sample", the dither and jitter less the target, and the graded floor of 12, in both `REGISTER_MAP.md` and the banner `KL_media_grid_align.sv:84-89`. The one `.sv` edit is comment-only (E2) |
| R262-1 S1 (acquisition note), S2 (CHANGELOG), S3 (jittered [G9] net check) | Not taken; still optional | Any acquisition note must not promise balance (N1); see S3 above |
| R263-1 S1-S4 (Tests and CHANGELOG suggestions) | Not taken; still optional | E8 corroborates S3's point on [G8]'s seed margin |
| R263-1 O1 (`KL_media_nco` tick drop) | **Concordant with N1**; still new work to file | E8-E11 |
| R263-1 O2 (unwrapper fold under a half-sample surplus marker) | Not re-verified this round; still new work to file | It bounds only the surplus-injection offset, not a claim this delta makes |
| R262-1 observation: `verilator-suites` cancelled at `6d1572d6` | Superseded | Observed success at this head (E13) |

## Real limits

- **Not run:**
  - the full parent, protocol-processor, gPTP, Yosys and builder banks;
  - `act`, the host `act_ci` runner, and its self-test;
  - hosted re-runs;
  - `xvlog_gate` (no Vivado on this host);
  - `milan_dp aclk`: R262-1 ran it at `6d1572d6` on preprocessed-identical
    RTL, and the hosted Verilator shards passed at this head;
  - candidate-merge validation.
- **Physical calibration was NOT RUN.** Field skips and simulation are not
  hardware proof. Bench items 1 and 4 of #74 remain.
- **Jitter model.** The root's marker-delivery jitter is modelled as 0 or
  1 edge, as the suite models it. Its silicon width is unmeasured.
- **N1 characterisation.** It was measured in the unit loop and in the NCO
  alone, not at the root. Its rate on silicon is unknown.
- **Manager banks not observed.** I found no public record of the manager's
  source static/builder and native banks at this head. The only [A10]
  source-validation comment is at `6d1572d6`. This round makes no claim
  about them.

## Pending manager duties

- File a new public Issue for N1 / R263-1 O1, linked to #74, with E8-E11 and
  R263-1's receipts. Decide on R263-1 O2.
- Publish the source static/builder and native bank results for this exact
  head.
- Own hosted and `act` acceptance, and build and validate the current-dev
  candidate at the merge turn (source base `ede8d48e`, live dev
  `759da623`).
- Obtain the external re-review verdict at this head (R263-2 is in flight).
  Merge also needs maintainer authorization and the full completion bar.
- Keep #74 open for items 1, 3 and 4.

R262-2 FINISHED
