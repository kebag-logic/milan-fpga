[R893] NEGATIVE - exact head 64d539f12532b2591f734b8e756f8a9358bb742c

Round R893-2, internal independent review of kebag-logic/milan-fpga PR #975 (issue #584), cleared context. This is a delta re-review.

- Head `64d539f12532b2591f734b8e756f8a9358bb742c`, tree `761862ef4b05e0284a6150036ea85709466bbeb5`.
- Delta: `2b295a44..64d539f1`, 5 commits, 17 files, all in tests, docs, the builder's comments and one YAML comment. No RTL, firmware or model change.
- Lenses applied: Conformance, RTL, Robustness, Tests, Docs.
- Open: two MINOR findings (F6, F7), four RESIDUE items and three SUGGESTIONs.
- Lens state: Conformance and RTL are clean. Robustness, Tests and Docs are unclean.

The round-1 findings are closed at this head (F1 for its statement only, see below), apart from one sub-item. F2's "cover reset/bind freshness" is only partly met; F6 below covers it. The owner's scope disposition of the 8x8 backing has **not** been posted, so it remains **open**. That is a pending owner/manager decision, not a defect of this round.

## Reconstruction (public state only)

- AGENTS.md sections 2-8. Issue #584 body (acceptance 1-4) and its public decisions:
  - the September proposal, approval, one-cluster fallback and parking (5854191783, 5854199817, 5857155362, 5857540091);
  - the executor's TAKEN+DECISION (7077045073);
  - both REVIEW READY comments (7083459655, round 1; 7085448602, this round).
- PR #975 body at this head, and the manager's review-start (7085482945).
- Authorities: Milan v1.2 5.3.3.8 (each stream port owns at least one AUDIO_CLUSTER), 5.3.3.9, and 5.4.2.26-28 (GET_AUDIO_MAP, ADD_AUDIO_MAPPINGS, REMOVE_AUDIO_MAPPINGS). IEEE 1722.1-2021 7.4.44-7.4.46 (payload layouts as the leg encodes them) and 6.2.2.8.
- Interface authorities: `docs/ENDSTATION_BUILDER.md` D2, D7, D8 and D10; `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md`; `docs/testing/TESTING.md`; `sw/litex/milan_soc.py` `add_milan_datapath()` (the render-parameter rules); `hdl/milan/milan_datapath.sv` (the edit face, epoch and freshness logic, adapter); `hdl/ieee1722/aaf/KL_tdm_render_master.sv`.
- Diff and history `2b295a44..64d539f1` (and `dd163e41..` for context).
- Public evidence: `review-evidence/584-r1` at `e3127c9139ae456ef671b098eab55bed6d41d0f4`, author-r1 and author-r2 receipts and `MANIFEST.json`. I read the receipts only, not the HANDOFF files.
- Prior public findings: the round-1 reports R894-1 (7083745128) and R893-1 (7083855570), read after my own pass over the diff.

**Disclosure.** While listing the PR thread to find the round-1 reports, a `grep` printed the headline lines of another reviewer's round-2 report at this head (7085655489). I read no further than those lines.
- One headline names a freshness-collection finding at `sim_ship8_render.cpp:1095/:1128`. It prompted my look at that path. F6's analysis, probes and figures are my own.
- One headline names a changelog wording item. I had not examined the changelog closely before seeing it. RS2 is my own wording.
- F7 was established before that listing: `receipts/packet_verify.txt` was produced first.

## Prior findings: resolved or retained at this head

| Prior finding | State at 64d539f1 | Evidence |
|---|---|---|
| R894-1 F1 / R893-1 F1 (backing vs. the owner's 2026-11-22 wording) | **Closed for its statement. Scope disposition OPEN** (owner/manager duty, not a defect of this round). | The deviation is stated plainly as pending in every place required: the PR body (Description, "Pending owner disposition", and the open-risks bullet "both are pending the owner's disposition"); D8 (`docs/ENDSTATION_BUILDER.md:759-776`); D10 (`:886-890`); the ownership page (`docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:171-173`); and the changelog (`CHANGELOG.md:79-81`, loopback half only, see RS2). It names no loopback-backed input cluster, a lane that stays off at 8x8, and TDM32 slot 0 standing for the first TDM8 channel. `Unrouted S<p>` is never called loopback (D10 `:886`). The YAML and builder deltas are comment-only. Not yet public: the owner's disposition, and the decision in the owner's own words on #584 (R893-1's first gap). |
| R894-1 F2 / R893-1 F2 (mapping to wire at the shipping 8x8) | **Closed**, except freshness, retained as **F6**. | Detailed after this table. |
| R894-1 F3 / R893-1 F3 (memory growth) | **Closed** | `SPLIT_CONTROL_MEMORY.md:313` now gives per-point growth, and the unbalanced breakdown is dropped. Recomputed from the published image sizes:<br>• product 8x8/1if: rom 139,208->140,544 (+1,336), sram 98,160->99,904 (+1,744);<br>• product 8x8/2if: rom 140,784->142,120 (+1,336), sram 115,504->117,312 (+1,808);<br>• fixture 8x8/1if: rom 130,032->131,368 (+1,336), sram 96,928->98,672 (+1,744);<br>• fixture 8x8/2if: rom 131,536->132,880 (+1,344), sram 114,320->116,064 (+1,744).<br>Sources: `author-r1/receipts/firmware/ledger-base-dd163e41.log` and `ledgerF.log` (POINT lines), and `fixture-base-dd163e41.log` and `variants-head.log` (unplanted lines). Every figure matches the page. |
| R894-1 F4 (stale waiver summaries) | **Closed** | Rule L1 (`PP_DESCRIPTOR_OWNERSHIP.md:86`) names `validate_cluster_minimum` (`sw/builder/endstation_builder.py:1836`) and `test_stream_port_cluster_minimum` (`sw/builder/test_declarations.py:658`). Row 45 (`ENDSTATION_BUILDER.md`) says no tracked config declares a waiver. The 32x32 census prose (`SAVED_STATE_FORMAT_32X32.md:90-92`) states one cluster per listener port (figure `p32_in_cl` = 1) and labels 11 + 12 x N as history. `check_nvm_format_32x32.py` reports 0 findings (`receipts/check_nvm_format_32x32.log`). |
| R894-1 F5 (round-1 index vs. published bytes) | **Closed for the round-1 index**; recurs as **F7** | `author-r2/receipts/f5/round1-INDEX-corrected.md`: 80 of 80 rows match the published blobs (`receipts/packet_verify.txt`). The original `author-r1/receipts/INDEX.md` is left as published, still 77/80, and the corrected index supersedes it. The new round-2 index repeats the defect for two rows (F7). |
| R893-1 R1 ("an 8x8 talker") | Fixed | `ENDSTATION_BUILDER.md:780` |
| R893-1 R2 (`render_ports: first` wording) | Fixed, and true to the code | `_role_pool` gives input port 0 `max(0, ph_render - 0)`, so port 0 takes every render channel. The wording matches in D2 (`:736-738`), row 16f (`:1115`), the builder comments (`:196`, `:1596-1597`, `:1660-1665`, `:4457`) and the YAML comment (`:222-225`). |
| R893-1 R3 (`obj_nxn8` README row) | Fixed | `tb/verilator/milan_dp/README.md:77` |
| R893-1 R4 (generated `build_plan.md` name list) | Retained as RESIDUE | Left deliberately, because fixing it changes every config's `build_plan.md`. Carried to the residue checklist. |

**F2 in detail.** The new `milan_dp_render` case `ship8` (`tb/verilator/milan_dp_render/sim_ship8_render.cpp`) meets the F2 outcome except for freshness.

- **Shape and parameters.** It elaborates at the tracked generated 8x8 shape. The recipe `cmp`s it against the builder's output (`Makefile:206-214`). The render `-G` flags come from the builder's own `soc_params.json` argv through `ship8_params.py`.
- **`ship8_params.py` derives, it does not mirror.** It reads the argv values. Its rules match `milan_soc.py:1110-1170`: `AUDIO_IF_CLK_HZ_P = 2*slots*32*48000`, render and master only on a TDM master, and `LOOPBACK_P` only with `--loopback-lane`. It refuses unmapped `--audio-*`, `--render-*` and `--i2s*` flags. The geometry header `static_assert`s the leg's constants.
- **Derived values** (`receipts/ship8_derived_params.txt`): `N_STREAMS=8`, `TALKER_WIRE_CHANS_P=8`, `AUDIO_IF_SLOTS_P=32`, master, `AUDIO_IF_CLK_HZ_P=98304000`, `AUDIO_IF_RENDER_SLOTS_P=1`, `LOOPBACK_P=0`, `I2SPB_P=0`, `LPF_P=0`.
- **What it drives and checks.** It drives identifiable audio (`{1,s,c,e}` words) from eight bound listeners through the real acceptance, depacketizer, render stage, crossbar, adapter and serializer. It decodes the three TDM pins and checks:
  - slot 0 carries the selected source in every frame, at its presentation time;
  - slots 1-31 are zero and the pad byte is zero;
  - REMOVE gives 119 silent frames on all 32 slots;
  - ports 1-7, mapped while their streams are live, change no routing;
  - D7's power-on map holds;
  - bind and reset (see F6 for the freshness part).
- **Control face.** The split control face's equivalence is structural. With `CTRL_SPLIT_P = 1`, `milan_datapath.sv:10193-10200` assigns `ppo_amap_edit_*` from `i_ctl_edit_*`.
- **CI and controls.** The loopback-on control `nxn8` is kept (README row). The fourth CI piece is wired: `RUN_CASES`, `ci-prepare`, `build-ship8`/`exec-ship8`, and `PIECE_SECONDS` `(549, 83, 812, 240)`. The piece self-tests pass.
- **Mutants.** `ship8-mutants` catches all four plants (two projection, the adapter, the bus binding) and the elaboration refuses the mis-tie by its guard's words.

My reruns:
- `make ship8`: 124 checks, 0 failures, every one named `[ ok ]`. Every graded window has 119 frames, and the largest presentation error is 11.8 ns against a 1041.7 ns band (`receipts/ship8_clean.log`).
- `ship8_mutants.py`: 6/6 PASS (`receipts/ship8_mutants.log`).
- My own DUT plants, all caught (`receipts/reviewer_probes.log`):
  - slots 1-31 copying slot 0: 8 failures;
  - an unqualified epoch mask: 3 failures, B1/B2/B3;
  - REMOVE taken as ADD: 35 failures, X2 SILENCE among them.

## Findings

### F6 - MINOR - Tests, Robustness, Docs - the B3 and Z3 FRESHNESS checks never see the frames in which a stale sample would render

- Artifacts:
  - `tb/verilator/milan_dp_render/sim_ship8_render.cpp:1095-1102` (B3) and `:1128-1135` (Z3);
  - `decode_a_window` at `:850-857`, which collects only inside its own `run_pdus`;
  - `docs/testing/TESTING.md:748`, the `ship8` row: "the rebind rendering only post-loss events ... only post-reset audio after the rebind";
  - `CHANGELOG.md` and the PR body state the same.
- Authority/evidence:
  - AGENTS.md section 6, Tests: "Each new test can fail for the defect it claims to detect".
  - R894-1 F2's required outcome: "Cover reset/bind freshness there".
- How the leg runs:
  - After `bind(0, "B3 REBIND")` the leg runs `run_pdus(kLeadPdus)` (19 PDUs, about 113 frames) with the decoder off. It opens the graded window only after that.
  - The check `w.first_event >= events_at_loss` is then made on a window whose first event is necessarily far past the loss: 1245 against about 1092 in my run. The check is named "the first event after the rebind", but it does not observe that event.
  - Z3 does the same after the post-reset bind.
  - A pre-loss (or pre-reset) word presented in the 113 skipped frames, which is exactly where a freshness defect would show, cannot fail either check.
- Measured:
  - In a disposable instrumented copy of the bench (`receipts/probe_bench_instrumentation.diff`), I decoded from the rebind itself. At this head the span is 93 silent frames, then the first rendered event 1224 against 1092 at the loss (B3). For Z3 it is 81 silent frames, then 1698 against 1458 at the reset (`receipts/probe_bench_clean.log`).
  - So the stronger check is practical, and the head passes it. The behaviour is not in doubt; the check's power is.
  - Two DUT plants that disable the post-bind freshness gate both pass all 124 checks (`receipts/reviewer_probes_fresh.log`):
    - `tdmr_fresh_w` forced to 1;
    - `tdmr_fresh_r` not cleared on a bind fall.
  - In this scenario those plants put no stale word on the pins even from the rebind on (`receipts/probe_bench_fresh.log`). They are not a demonstrated escape, but nothing in the leg shows its freshness checks can fail.
- Impact: a defect that renders a retained or pre-loss sample right after a rebind or a reset would pass `ship8` green. The documentation says the leg grades exactly that.
- Required outcome:
  - From the rebind, and from the post-reset bind, grade every frame up to and through the window.
  - Allow leading digital silence. Any rendered word in that span must be the routed source, with an event at or past the loss/reset cursor.
  - Show the check can fail, either with a planted gateware defect that really renders a pre-loss word, or with a leg-side defect arm. For example, re-send stream 0's pre-loss events with fresh timestamps after the rebind. The DUT renders them correctly, and the freshness check must fail.
  - If the gate is unreachable at this shape, say so in the leg's comment and the TESTING.md row instead of claiming the property.
- Verification: the strengthened checks pass at the corrected head (they pass at this one per my probe), and the defect arm or plant fails them by name.

### F7 - MINOR - Docs - the round-2 receipt index is itself indexed before publication normalization (the F5 defect, again)

- Artifact: `review-evidence/584-r1/author-r2/receipts/INDEX.md:19-20` at `e3127c9139ae456ef671b098eab55bed6d41d0f4`. The two rows index `f5/index-check.md` and `f5/round1-INDEX-corrected.md`.
- Evidence: `MANIFEST.json` records both files as normalized at publication (`original_sha256 != published_sha256`), and the index carries the original hashes:
  - `index-check.md`: indexed `1eb005c3...`, published `2028461c...`;
  - `round1-INDEX-corrected.md`: indexed `8fe24e66...`, published `d132b10e...`.
  - The other 14 rows match (`receipts/packet_verify.txt`).
- Cause: both files quote the raw path forms that publication rewrites. The normalization also left `index-check.md`'s Cause sentence unreadable: "'<scratch><home-path>' and '<scratch><home-path>' to '<scratch><home-path>'". `round1-INDEX-corrected.md`'s introduction has the same problem.
- Manifest integrity: 189 entries, 0 mismatches, 0 unlisted blobs. No measurement is affected.
- Lens: Docs only. These rows index the F5 explanation files, not execution receipts.
- Impact: the index that exists to authenticate the publication fails to authenticate two of its own files. A cold reader of the F5 explanation cannot tell which path form was rewritten.
- Required outcome:
  - Index the bytes as published: regenerate after normalization, or keep raw path forms out of the receipt text.
  - Word the cause so it survives normalization, for example "a home-directory path under the scratch root".
  - Either the author's packet or the publisher's step may make the fix. It belongs to whichever produces the next index.
- Verification: every row of the round's INDEX.md hashes to its published blob.

### RESIDUE (wording only; does not block and does not unclean a lens)

- **RS1** - `docs/testing/TESTING.md:431-437`. The #584 paragraph (lines 432-436) was inserted between "These measurements cover `8e4b1e53`; later heads still require hosted acceptance." (line 430) and its follow-on "That requires `follow_ring` within 1260 s and successful `verilator-suites`." (line 437). "That" now reads as a condition on the `ship8` piece's hosted window. Exact fix: move line 437 up to directly after line 430, so the #584 paragraph follows it.
- **RS2** - `CHANGELOG.md:72-85`:
  - Line 81, "Both points await the owner's disposition", covers only the loopback half (lines 79-80). Add the TDM half before line 81, for example "- `TDM32 Out 0`, the TDM32 bus's slot 0, stands for the decision's first TDM8 channel." Then change line 81 to "- All three points await the owner's disposition on #584."
  - Line 85, "Slots 1-31 and ports 1-7 stay silent": ports 1-7 are not silent; their mappings route nothing. Change it to "- Slots 1-31 stay zero; ports 1-7's mappings reach no slot."
  - Optionally, line 72 "binds the render channel." -> "binds the render channel to STREAM_PORT_INPUT 0."
- **RS3** - `tb/verilator/milan_dp_render/sim_ship8_render.cpp:42-44`. The rule comment says internal taps are "timestamp and counter sources only". The P2 checks also grade the stream table's enable mask (`strtbl_en_w`) and stream ids (`strtbl_sid_w`). Exact fix: append "and the stream table's enable mask and stream ids, graded in P2 against the ids the bench's own answers carried".
- **R4** (carried from R893-1) - the generated `build_plan.md` cluster-name sentence omits `Unrouted S<p>`.

Comment rule: no new bench-lane label, lane name, review round, reviewer ID or issue-comment ID appears in source comments in the delta. `(sim_tdm8_render T22)` at `:1091` cites another bench's check identifier, not a lane label. The `P1`, `R1`, `U1`, `X1`, `B1` and `Z1` tokens are runtime check names. "a later round" (D8) and the issue-comment link are in docs prose, which the rule allows.

### SUGGESTION (optional)

- **S1** - `scripts/suite_shards.py:122` (`"milan_dp_render": 1264`) and the Makefile's DEFAULT WALL CLOCK header (`Makefile:47-62`) predate `ship8` in the default `run` target.
  - Projection: the 1218.7 s hosted window plus `ship8`'s share (196-240 s at the 1.324-1.58 ratios) is about 1415-1459 s. That straddles the 1440 s 80% line and stays under the 1800 s guard. Hosted CI runs the suite as pieces, so the serial figure governs only the local serial gate.
  - When the owed hosted window lands, update both figures as the `follow_ring` bind round did (TESTING.md:440-458).
- **S2** - `ship8_params.py` ignores every argv flag outside its refused prefixes. The header names the observability levers. `--ctrl-mailbox` (`CTRL_SPLIT_P`) and `--milan-clk-freq` are also ignored, and that is intended. An explicit list of ignored flags would turn a future render-relevant flag outside `--audio-`, `--render-` and `--i2s` (say a `--tdm-*`) into a refusal instead of a silent default.
- **S3** - Bank the three plants this round ran (zero-fill, unqualified epoch mask, REMOVE-as-ADD) in `ship8_mutants.py`. The leg catches all three, so they cost one table row each.

## Lens results (PASS lines carry their artifacts)

```text
[R893] PASS Conformance - sim_ship8_render.cpp:567-658 (ADD/REMOVE/GET payloads, 7.4.44-7.4.46 field offsets), receipts/ship8_clean.log (R1-R2, U1-U3, X1, X3: SUCCESS, BAD_ARGUMENTS for cluster_offset 1 past port 7's one cluster, GET_AUDIO_MAP number_of_maps 1 and the issued rows on all 8 ports); docs/ENDSTATION_BUILDER.md:759-776, :886-890; PP_DESCRIPTOR_OWNERSHIP.md:86, :171-173; PR body; configs/endstation_ax7101_8x8.yaml and sw/builder/endstation_builder.py deltas (comment-only) - Milan 5.3.3.8/5.3.3.9 and 5.4.2.26-28 behaviour at the shipping shape over the wire to the pins; the deviation from the owner's wording is stated as pending everywhere required. The disposition itself is open (owner/manager), not a defect of this round.
[R893] PASS RTL - git diff --stat 2b295a44..64d539f1 (no hdl/ path); hdl/milan/milan_datapath.sv:8641, :8650-8662, :8695-8712, :10193-10200; hdl/ieee1722/aaf/KL_tdm_render_master.sv:430-443; receipts/reviewer_probes.log, ship8_mutants.log - no RTL changed since R893-1's clean RTL lens at 2b295a44 (an ancestor). The narrow lane's zero tail, the stream-qualified epoch, the adapter's first write, the bus binding and the edit face were exercised at the shipping parameters through the new leg; each planted fault is caught, and the split face's equivalence is structural.
```

## Reviewer-owned completion ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN (scope disposition open, owner/manager) | issue #584 decisions; PR body; D8/D10/ownership/changelog statements; YAML and builder deltas; `ship8` AECP and pin results | R893-2 | 64d539f12532b2591f734b8e756f8a9358bb742c |
| RTL | CLEAN | no RTL delta; datapath epoch, freshness, adapter and edit face; render master narrow arm; plants | R893-2 (and R893-1 at the ancestor 2b295a44) | 64d539f12532b2591f734b8e756f8a9358bb742c |
| Robustness | UNCLEAN (F6) | `ship8` reset, bind-fall, rebind, REMOVE, unrouted and out-of-range offset phases; freshness probes | R893-2 | 64d539f12532b2591f734b8e756f8a9358bb742c |
| Tests | UNCLEAN (F6) | `sim_ship8_render.cpp`, `ship8_params.py`, `ship8_mutants.py`, Makefile and CI piece wiring, `suite_shards.py`, `measure_test_evidence_readers.py`; reruns and 5 extra plants | R893-2 | 64d539f12532b2591f734b8e756f8a9358bb742c |
| Docs | UNCLEAN (F6, F7) | ENDSTATION_BUILDER D2/D8/D10/16f/45; PP_DESCRIPTOR_OWNERSHIP; SPLIT_CONTROL_MEMORY; SAVED_STATE_FORMAT_32X32; TESTING.md; CHANGELOG; milan_dp README; DOCUMENTATION_AUDIT; PR body; published packet and indexes | R893-2 | 64d539f12532b2591f734b8e756f8a9358bb742c |

## Commands run here (foreground; pinned Verilator 5.050, identity in `receipts/verilator_identity.txt`)

| Command | Result | Receipt |
|---|---|---|
| `make -j16 ship8` | rc 0; 124 checks, 0 failures; 2 m 12 s | `ship8_clean.log`, `.rc` |
| `ship8_mutants.py --jobs 4` | rc 0; 6 checks, 6 PASS | `ship8_mutants.log`, `.rc` |
| `scripts/reviewer_probes.py` (zero-fill, unqualified epoch, REMOVE-as-ADD) | caught: 8, 3 and 35 failures | `reviewer_probes.log`, `*.run.log` |
| `scripts/reviewer_probes.py --fresh` (two freshness-gate plants) | both survive, 124/0 | `reviewer_probes_fresh.log` |
| instrumented bench copy (decode from the rebind and the post-reset bind), clean and with the open freshness gate | no stale word either way; B3: 93 silent frames, then event 1224 against 1092; Z3: 81 silent frames, then 1698 against 1458 | `probe_bench_*.log`, `probe_bench_instrumentation.diff` |
| `docs_inventory.py --check`, `check_doc_style.py`, `measure_test_evidence.py --check`, `suite_shards.py --selftest`, `ci_suite_pieces_selftest.py` | all report OK/PASS | `docs_checks.log` |
| `check_nvm_format_32x32.py` | 0 findings | `check_nvm_format_32x32.log` |
| `scripts/verify_packet.py` on `e3127c91` | manifest 189/189; r1 corrected index 80/80; r2 index 14/16 (F7) | `packet_verify.txt` |
| tree integrity after the probes | HEAD, tree and index exact; 0 blob or mode mismatches; 5 initialized gitlinks MATCH and clean; `external` uninitialized (gitlink only) | `tree_integrity.txt` |

Receipts have local paths normalized (`<packet>`, `<clone>`, `<home>`) before hashing; no result or rc was altered. The `docs_checks.log` `rc=` lines record the pipeline's last stage, so the tool verdict lines are the evidence there. Disposable trees (planted copies and builds) stayed under `scratch/`. The instrumented bench copy was a temporary untracked directory inside the clone, and I removed it before the integrity check.

## Real limits

- No manager source bank ran at this exact head, and none is claimed or inferred. Source-head execution evidence is the author's published receipts plus the focused runs above.
- Not rerun here:
  - the builder suite (113 gates);
  - the firmware banks;
  - the native sweep;
  - `make -C tb/verilator/milan_dp_render` (all four cases);
  - the `ci_make_cases.py --shard 3/4` cold timing (147.9 s);
  - `twin` and the control-memory ledger;
  - the routes and saved-state measurements.
- The author reports that all five configs' builder outputs are byte-identical to round 1's. I confirmed only that the YAML and builder deltas are comment-only.
- Hosted contexts at this head when inspected: 21 success, 1 skipped, 20 in progress, 15 queued (`hosted_checkruns_snapshot.txt`). The manager owns hosted and act acceptance. Physical calibration was NOT RUN and no hardware was touched. Skipped field contexts are not hardware proof.
- The published evidence commit `e3127c91` is not GPG-signed. Its integrity was checked against its own `MANIFEST.json` only.
- The pre-existing all-fabric `milan_nvm` listing overrun stays filed separately.

## Pending manager duties

- Obtain and publish the owner's disposition of the 8x8 backing on #584, in the owner's words. It must cover no loopback-backed input cluster, the lane off at 8x8, and TDM32 slot 0 standing for the first TDM8 channel. If the owner requires loopback-backed input clusters, the Conformance, RTL and Tests coverage above no longer applies.
- Route F6 and F7 to the lane (F7 possibly to the publication step), and RS1-RS3 and R4 to the residue checklist. Re-review at the corrected head: every lens whose artifacts change must be covered again.
- Record the `ship8` piece's hosted window (owed; S1).
- Validate the current-dev merge candidate at the merge turn: source base `dd163e41`, live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`, builder and native banks, with receipts linked. Hosted and local-replica acceptance at the exact head. Explicit maintainer authorization before any merge, then containment and closing the issue as Done.

R893-2 FINISHED
