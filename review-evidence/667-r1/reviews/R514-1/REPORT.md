[R514] POSITIVE - exact head 41bc9dac031526c1fd637ff1e801d3c6dc1260b4

Round R514-1. Internal cleared-context independent review of issue #667 / PR #680.
Tree: `1a233401c2f5d585b7a0a2d1a7db16daff6d29b6`; parents `5d6164a2` (author) and `bd884631` (live dev).
All five lenses were applied with executed evidence. No BLOCKER, MAJOR or MINOR finding is open.
Two SUGGESTIONs are recorded. The one prior public finding on this PR (R515-1-F1) is resolved at this head.

## Scope and reconstruction

Read in order: AGENTS.md, CONTRIBUTING.md, docs/README.md, the #667 thread
(B12 evidence 5994857089, B13 assignment 6009837251, fix assignment
6011846710, STOP 6012826048, ruling 6012843714, REVIEW READY 6015760986,
ruling 6016181662), IEEE 1722-2016 4.3.2, 4.4.4.9 and 7.5 (primary text),
`docs/design/TIME_SYNC.md`, then the diff and history, then the public evidence
at `90d0bcbf` (`review-evidence/667-r1/author/*`).

The requested `423ac5d9..41bc9dac` diff (29 files) is dominated by inherited
dev content (#658 power-on maps, B13 findings page). The PR's own delta,
`bd884631..41bc9dac`, is seven paths: `KL_aaf_packetizer.sv` (+8 lines),
`docs/design/TIME_SYNC.md` (+12), `scripts/measure_test_evidence_readers.py`
(+3, the reader entry moved by the merge), and `tb/verilator/aaf/`
`Makefile`, `README.md`, `sim_start.cpp`, `start_mutants.py`. The packetizer is
byte-identical between `423ac5d9` and `bd884631`, so the base red run and the
dev red run exercise the same RTL. Submodule gitlinks are equal at dev and head.

## Root cause and fix (verified)

At base, with line numbers of `423ac5d9:hdl/ieee1722/aaf/KL_aaf_packetizer.sv`:
`:314` admits any owned pair as soon as `stream_en_i` is high; `:712` advances
`nsamp_r` on the last pair of a sample; `:720` captures the timestamp only for
sample zero AND pair zero; `:651` reads the epoch timestamp from TCTX w4, which
`:734` (disable) and reset do not refresh. An enable landing after pair zero
lets pairs 1..3 in, the last pair moves `nsamp_r` 0 -> 1 without a capture, and
the first PDU carries the previous stream's (or reset-time zero) w4 value.

The fix (`KL_aaf_packetizer.sv:274`, `:319`, `:591`, `:715`, `:742` at head)
adds one `started_r` bit per talker. It is cleared by reset and by
`!stream_en_i`, and set by any accepted pair. Admission requires
`started_r || pown_o_w == 0`, so the first accepted pair after enable is pair
zero at `nsamp_r == 0`, which takes the unchanged PHC-plus-own-offset capture
at `:727-733`. No port, parameter or register-map declaration changed (diff
inspection). The disable clear is placed after the `pair_ok_w` set in the same
always block, and `pair_ok_w` already requires `stream_en_i`, so the two writes
can never conflict.

The -494821316 ns first-to-second step is the signed modulo-2^32 view of a
retained timestamp 3.8 s old (3.8e9 - 2^32 = -494967296, plus the sample-phase
offset). The bench's -280..-544 ms steps fit retained values about 3.75..4.0 s
old, consistent with 2 s binds. This matches the mechanism; it is not a proof
of the bench incidence (14/100), which depends on pair-delivery spacing in the
integrated capture path. That is the manager's bench repeat.

IEEE 1722-2016 7.5 (sp = 0: every AAF AVTPDU sets tv = 1 with valid data; the
timestamp is the presentation time of the first sample frame) is the governing
clause. The assignment's 5.4.4 is the IEC 61883 encapsulation and 7.3.4 is
`bit_depth`; the PR's re-citation is correct and changes no required behaviour.
After the fix tv = 1 is always paired with a first-sample timestamp, which is the
assignment's "tv=1 only then".

## Findings

**R514-1-S1 | SUGGESTION | Docs**
Artifact: `CHANGELOG.md` (no entry in `bd884631..41bc9dac`).
Evidence: every recent product behaviour change has an "Unreleased" entry (for example
"CRF unbind counts its unlock"); this PR changes on-wire behaviour (a mid-frame
enable now starts at the next pair zero, and the first PDU carries a current
presentation time). No rule found in CONTRIBUTING.md, AGENTS.md or docs/README.md
requires an entry, so this is optional.
Impact: release readers do not see the #667 fix in the product record.
Suggested outcome: add an "Unreleased - talker first PDU timestamp" entry citing #667.
Verification: `check_doc_style.py` and `check_em_dash.py --base <dev>` pass with the entry.

**R514-1-S2 | SUGGESTION | Tests**
Artifact: public `author/area.csv` (packetizer 868 -> 864 LUT, 1344 -> 1344 FF);
reviewer `receipts/yosys_area_{dev,head}.log`.
Evidence: the change adds one state bit per talker. A reviewer flattened xc7 synthesis
of the packetizer alone at N_TALKERS_P=1, WIRE_CHANS_P=8 gives FF 1367 -> 1368 (+1)
and LUT 1380 -> 1418 (+38; excluding LUT1, 1310 -> 1386). This is a different
synthesiser with heuristic mapping, so it does not contradict the Vivado figure as a
measurement, and both are inside the 40/40 limit. A net-zero FF delta can arise from
unrelated register merging.
Impact: none on the verdict. The only hardware proof is the post-flash bench, and that
depends on the bit surviving synthesis.
Suggested outcome: when the manager builds the flashed candidate, confirm the
synthesised netlist contains the `started_r` register (one cell query) and record it
with the bench evidence.
Verification: the netlist query output in the bench receipts.

## Prior public findings on this PR

**R515-1-F1 (MAJOR, Conformance/Tests/Docs) - RESOLVED at this head.**
It said the #657 base-equality condition of ruling 6012843714 was shown only for
`423ac5d9` vs author head `5d6164a2`, not for the published merge head. Ruling
6016181662 sets the equality base to the merge parent `bd884631`, and the PR body
now carries the merge-parent figures. Independent reviewer evidence at the merge
parent and the exact head:

| Comparison (dev `bd884631` vs head `41bc9dac`) | Result | Receipts |
|---|---|---|
| Render `--epoch-only` clean leg | byte-identical stdout: 3746 bytes, 127 checks / 4 failures, SHA-256 `3ef42e34ca3874e90fd2929f869dd0f37343e04b9cb2cb0c5f294262448c1c6b`; rc 1 at both; the four failures are the #657 T30 CRF lines | `render_epoch_{dev,head}.stdout`, `.rc` |
| Render default leg | byte-identical log, 258 checks / 0 failures, rc 0 at both | `render_full_{dev,head}.log`, `.rc` |
| Full render mutation campaign (`make tdm8render-mutants`) | identical judgments at both: 32 checks, 28 PASS / 4 FAIL, the four being the #657-ruled findings (clean `--epoch-only` control, its two clean skew controls, the surviving uncounted-repeat mutant); campaign exit 1 under make (rc 2) at both; normalised logs identical (491 lines, 34 judgment lines); raw logs differ only in build timing/source-size statistics | `render_mutants_{dev,head}.log`, `.rc`, `render_campaign_compare.log` |

So the remaining ruling condition, "every other check and every mutant in that
campaign gives the same result at base and head", is also independently established
for the merge parent. The #657 failures and the surviving uncounted-repeat mutant
remain open under their explicit exception and are not claimed fixed.

## Lens results

```text
[R514] PASS Conformance - hdl/ieee1722/aaf/KL_aaf_packetizer.sv:319,:727-733 at 41bc9dac; receipts/startup_head.log; receipts/startup_red_devbd88.log - first PDU after every graded start carries (sample time + own offset) with tv=1, per IEEE 1722-2016 7.5 / 4.4.4.9; red at dev reproduces -494821316 ns (108 of 486 starts), head has first step = steady = 125000 ns in all 486; ruling 6012843714 conditions hold at the merge parent (table above); no port/register/parameter change
[R514] PASS RTL - hdl/ieee1722/aaf/KL_aaf_packetizer.sv:274,:319,:591,:715,:742 - one reset-cleared flop per talker, single clock domain, no new CDC; set and clear mutually exclusive (pair_ok_w requires stream_en_i); per-talker indexing by pown_t_w; nsamp/pend/bank logic and capture path unchanged; base root-cause lines :314,:651,:712,:720,:734 confirmed at 423ac5d9 and identical at bd884631
[R514] PASS Robustness - scripts/probe_start.cpp; receipts/probe_h_*.log, probe_d_*.log - reviewer probe over 1/2/3/4 pairs per sample, 1 and 2 talkers (talker 0 streaming while talker 1 restarts), strides 1/26/130/260, dense enable phases, 0 and 0xffe00000 origins, cold/3.8 s idle, disable and reset restarts, bounded and 1500-cycle output stalls: 1,461,024 checks, 0 failures at head; the three dev configurations run (4 pairs: 1 talker, 1 talker with long stalls, 2 talkers) all fail
[R514] PASS Tests - tb/verilator/aaf/sim_start.cpp:113-153, start_mutants.py:22-79, Makefile:22-31 - oracle uses stimulus sample times and payload identity, not DUT internals; 486 starts x 70 checks = 34,020; 8/8 planted defects caught with their named assertion (receipts/start_mutants_head.log); default target runs the startup leg and its controls; a reviewer talker-index mutant (started_r[0]) is caught by the standing chmap_capture suite (receipts/mutidx_chmap_capture.log); reader entry passes measure_test_evidence --check and --selftest; affected suites at head all rc 0 (table below)
[R514] PASS Docs - docs/design/TIME_SYNC.md:501-511, tb/verilator/aaf/README.md, KL_aaf_packetizer.sv:271-274 comments, PR body - descriptions match the RTL and sweep (dimensions, counts, stall pattern, limits); doc style, em-dash (vs bd884631), doc-path and hygiene gates pass; PR body labels the pre-merge comparison and now records the merge-parent figures
```

## Executed evidence (reviewer)

| Execution | Result | Receipt |
|---|---|---|
| Startup sweep + 8 controls, exact head | 34,020 checks, 0 failures; 8/8 caught; rc 0 | `startup_head.log`, `start_mutants_head.log` |
| Same harness, packetizer at dev `bd884631` / base `423ac5d9` | 33,804 checks, 864 failures; first step -494821316 ns in 108 starts; make rc 2 | `startup_red_devbd88.log`, `startup_red_base423.log` |
| Reviewer generalised probe, head | 8 configurations, 1,461,024 checks, 0 failures | `probe_h_*.log` |
| Reviewer generalised probe, dev | fails (3,900 / 3,900 / 2,580 failures in the three 4-pair configurations run) | `probe_d_*.log` |
| Talker-index mutant against standing N=2 legs | caught by chmap_capture; aaf legs and tdm do not catch it | `mutidx_*.log` |
| Suites at head: aaf (flat 27, NxN 42, startup, controls), aaf_audio_loop (10), tdm (58), chmap_capture, capture_coherence (with its mutants), milan_dp, milan_dp_mclk (with its mutants), milan_dp_render default (258) | all rc 0, no failing check | `suite_*_head*.log`, `.rc`, `render_full_head.log` |
| Mutation-context search over 293 tracked Python/patch files | no existing campaign plants in the packetizer; the 9 count changes are the PR's own new sites and generic words | `mutation_context.log` |
| Static: measure_test_evidence --check/--selftest, check_py_idiom, check_cpp_idiom, check_sv_idiom, lint_rtl, check_doc_style, check_em_dash --base bd884631, check_doc_paths, check_hygiene, check_port_contracts, check_wire_accountability, check_todo_ownership, check_rtl_source_lists | all rc 0 | `static_*.log`, `.rc` |
| Packetizer-only xc7 area (different synthesiser) | dev 1380 LUT / 1367 FDRE, head 1418 / 1368 | `yosys_area_{dev,head}.log` |
| Hosted contexts at exact head, point-in-time read (14:23 UTC) | 21 completed success (incl. rtl-fast, Verilator shards 0-4/5, Yosys shards 0-3/4); physical gPTP skipped and not counted | `hosted_checks_41bc9dac.txt` |
| Tree identity | clone worktree/index/tree = 1a233401, gitlinks ead80360/5dce647a/48ff7a7e; scratch head 1113/1113 blobs equal; scratch dev 1110/1110 equal to bd884631 | `clone_integrity.txt`, `scratch_*_identity.txt` |

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | KL_aaf_packetizer.sv:319, :727-733; IEEE 1722-2016 7.5, 4.4.4.9; issue assignment 6011846710, rulings 6012843714 / 6016181662; startup red/green receipts; render dev/head comparisons | R514-1 | 41bc9dac031526c1fd637ff1e801d3c6dc1260b4 |
| RTL | CLEAN | KL_aaf_packetizer.sv:274, :319, :591, :715, :742 (head); :314, :651, :712, :720, :734 (base); milan_datapath.sv aaf_stream_en_w composition | R514-1 | 41bc9dac031526c1fd637ff1e801d3c6dc1260b4 |
| Robustness | CLEAN | sim_start.cpp sweep dimensions; reviewer probe_start.cpp over 8 configurations incl. two talkers and long stalls | R514-1 | 41bc9dac031526c1fd637ff1e801d3c6dc1260b4 |
| Tests | CLEAN | sim_start.cpp:113-153; start_mutants.py:22-79; aaf Makefile:22-31; measure_test_evidence_readers.py:21-23; suite, campaign and mutant receipts | R514-1 | 41bc9dac031526c1fd637ff1e801d3c6dc1260b4 |
| Docs | CLEAN | TIME_SYNC.md:501-511; tb/verilator/aaf/README.md; packetizer comments :271-274; PR body incl. manager notes; CHANGELOG.md (S1) | R514-1 | 41bc9dac031526c1fd637ff1e801d3c6dc1260b4 |

## Real limits

- No Vivado run (forbidden here); the -4 LUT / 0 FF own-area figure is the author's
  public measurement, checked for arithmetic only; S2 records a cross-check.
- Not run here: the other default suites, portability tops, builder bank, native
  banks, aggregates and physical-rate simulation. Those are the author's and the
  manager's public evidence, not this reviewer's.
- The startup sweep and the reviewer probe drive the packetizer's post-bind enable
  directly; neither runs ACMP traffic, the TDM capture engine or the capture map.
  The bench incidence is not modelled.
- Hosted results are a point-in-time read; skipped contexts are not counted.
- Physical calibration NOT RUN; no hardware, no flashing.

## Pending manager duties

- Final current-dev candidate validation at the merge turn (source base `423ac5d9`,
  live dev `bd884631` or later), and hosted/act acceptance (the exact-head hosted
  contexts read green here are evidence for the source head only).
- S2 netlist check on the flashed build, then the B13-style repeat of 100 binds:
  first ten PDUs per bind, first-to-second steps, peer EARLY/LATE counters.
- Second positive review (external lane), post-merge containment, issue closure.

## Packet

Portable drivers are in `scripts/`; raw command outputs and return codes are in
`receipts/`. Install, home and checkout path prefixes in receipts are redacted to
`<SIMROOT>`, `<HOME>`, `<PACKET>`, `<CLONE>`, `<TOOLS>`; the render `--epoch-only`
stdout files contain no paths and keep their raw bytes (SHA-256 above). The
`suite_{milan_dp,mclk,chmap_capture,capture_coherence}_head.log` files are first
attempts cut off when an earlier session of this round was terminated for memory;
they are superseded by the `*_head2` receipts and carry no verdict. Disposable trees
are under `scratch/` and are not published. Only `REPORT.md` and the files listed in
`MANIFEST.sha256` are publication inputs. No source fix, commit, push, GitHub write,
hardware action, synthesis with the vendor tool, or edit to another checkout was made;
the review clone was verified byte-identical to the exact head after all probes.

R514-1 FINISHED
