# [A475] Round 3 handoff: lane C5a (AECP deadlines), PR #140

Status: DONE at head `d4ca85c60e1e12b9fa0923e83bdfe39ce16e7d59`.
- The three items are committed in the ruled order.
- Every processor suite, entry point and campaign is rc 0 at the merge commit and at the head.
- The 16 parent consumer gates are rc 0 at milan-fpga dev `ea3fb388`, with #137's disposition line.
- No STOP was needed.

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, branch `c5a-aecp-deadlines`.
- Start head: `44a6bb9082d31dbf933087ef007ad78a110e7053`. New head: `d4ca85c60e1e12b9fa0923e83bdfe39ce16e7d59`.
  Not pushed: pushing is not this role's.
- REVIEW READY: issue #81 comment 5936548637.
- Assignment: issue #81 comment 5929634478, on R418-2 (POSITIVE, comment 5928299930) and R419-2 (NEGATIVE on
  F5, comment 5928298648). TAKEN: issue #81 comment 5929644465.

| Commit | Item | What |
|---|---|---|
| `97fe22f` | 1 | the merge of processor main `3f3ea56b` (#135 C2, #137 C4); parents `44a6bb9` and `3f3ea56b` |
| `e4c70b5` | 2 | R419-2 F5 as ruled: the classifier comment made true, and the limitation recorded in 03 §6 |
| `d4ca85c` | 3 | R418-2 S1 with R419-2 S6 (08 §4), and R418-2 S2 (DL8's label) |

Every commit has a one-line subject, no body and no trailer. The merge was made with `git merge --no-ff`, and
nothing was rebased.

Environment:
- Verilator 5.050 (the CI pin, `hdl.yml`), first on PATH. yosys 0.66. Every build ran under an 8-CPU affinity
  mask, so Verilator's `-j 0` resolves to 8 jobs. Heavy runs went one at a time, with D3 at `--jobs 2` and ACMP
  at `--jobs 1`.
- Runs longer than one foreground call were started detached and waited on in the foreground, and their exit
  status was read from a file. Nothing was piped into a verdict.
- Scratch trees and logs are under `$VALIDATION_STORAGE/a475-*`. The working tree held no tracked change after any
  run, and its ignored build products were deleted before each full run and at the end.

## Item 1: merge processor main `3f3ea56b`

- Merge commit `97fe22f4bda14eda7a2f940ef74deafb44bf6292`, made with `git fetch origin main; git merge --no-ff`.
  Its parents are `44a6bb90` (this branch) and `3f3ea56b` (main).
- Main brings #135 (C2, MAAP) and #137 (C4, ACMP), 48 files.
  - Its only RTL change is `hdl/maap/KL_pp_maap.sv`. At the head that file is byte-equal to main's.
  - It changes no top port or parameter, and no generator.
  - The top's port and parameter header, and `KL_pp_maap`'s, are byte-identical at `0451d83d`, `3f3ea56b` and the
    head (header sha256 compared).
- Eight files changed on both sides. Six merged cleanly: `.gitattributes`, `.github/workflows/hdl.yml`, docs 00
  and 09, `tb/pp_top/README.md` and `pp_top_wrap.sv`. Two conflicted, and both resolutions keep both sides:
  - `tb/pp_top/Makefile` `.PHONY`: main's `maap-internal` beside this lane's `deadline d3 hazards budget
    budget-build aecp-mutants`.
  - `tb/pp_top/sim_main.cpp`, the section switch: `one_section` ORs main's `acmp_only` and `maap_only` with this
    lane's `dl_only` and `hz_only`, and keeps main's `if (maap_only) run_maap_internal(h);`. The default build
    runs Suite, GI, NW, D3, AC, AD, DL and HZ. MP stays opt-in, as on main.
- Generated ROMs and tables:
  - `ucode.hex` and `ltn_rom.hex` are build products, never committed. Every ignored build product was deleted
    before each full run, so both were regenerated from `gen_ucode.py` and `gen_ltn_rom.py`.
  - The one committed generated table, `docs/traceability/MODULE_MATRIX.md`, was regenerated with
    `scripts/gen_matrix.py`. It came out byte-identical (94 rows, 0 untested).
  - The wavedrom SVGs pass `wavedrom-check`.
- No port, parameter or parent-visible change was needed, so there was no STOP.
- Measured at the merge commit (detail in the tables below):
  - `run_suites.sh` rc 0: 33 suites, 1,018,218 checks. `tb/pp_top` has 8,288: this lane's 8,240 plus main's +48.
    Main went from 7,944 at the shared base `0451d83d` to 7,992 at `4e55849`.
  - All twelve campaigns rc 0.
  - The AECP table and the ACMP table were re-measured, with every count equal to its record and no arm lost.
  - Before the merge commit, the merged bench ran DL 64/0, HZ 176/0, MP 34/0 and AC 43/0.

## Item 2: R419-2 F5, as ruled (`e4c70b5`)

This is the ruling's first outcome. It changes no RTL logic: the edit is a comment and docs.

Clauses:
- F03.7: RO_SNAPSHOT is keyed by the addressed descriptor and "blocked only vs in-flight write on the same key".
- IEEE 1722.1-2021 §7.4.76.1: each GET_DYNAMIC_INFO element is handled "as if it were an independent command".
  §7.4.76.2 lists GET_STREAM_INFO among the fixed-size members.
- Milan v1.2 §5.4.2.10, Figure 5.1: GET_STREAM_INFO's probing and ACMP status.

Established before the edit:
- READ_DESCRIPTOR serves the descriptor image. Its only live overlays are ENTITY's current_configuration
  (`E_RDESCENT`) and the name overlay. AECP's SET_CONFIGURATION and SET_NAME write them, and no ACMP step does.
  So the NONE key costs READ_DESCRIPTOR nothing, and the ruling's "READ_DESCRIPTOR holds" stands.
- GET_DYNAMIC_INFO's GET_STREAM_INFO records use the stand-alone getter's word table (`gen_ucode.py` E_GSTRI:
  "shared by solicited, unsolicited and GDI responses").
  - For a STREAM_INPUT, selector 7 is the committed probing and ACMP status byte. It is
    `lstn_gsi_status_r` (`protocol_processor_top.sv:3342`, read at `:3391`), written only by the listener record
    write `lstn_recwr_w`, that is, by ACMP listener steps.
  - The batch takes the NONE key, so it is not serialized against them.

Edits:
- `hdl/top/protocol_processor_top.sv:1464-1471`, the classifier banner, which was `:1464-1466`:
  - READ_DESCRIPTOR's NONE key is stated as harmless, with the reason.
  - GET_DYNAMIC_INFO's NONE key is stated as a known gap, naming the field and its writer, and the contrast with
    the stand-alone getter.
- `docs/architecture/03_packet_engine.md:229-237`, beside the no-descriptor-key sentence: the same limitation,
  with the clauses, the HZ6 contrast, the probe's result, and serialization left to a later #84 item.
- The PR body's #84 remainder names it.

Verification: R419-2's `probe_gdi_stream_info.py` (sha256 `6cfd0162…`, equal to the R419-2 manifest) ran unchanged
on a `git archive` export of `e4c70b5`, rc 0:
- G0: a stand-alone GET_STREAM_INFO STREAM_INPUT 1 against a held UNBIND_RX of sink 1 WAITED (refused 498
  clocks) and answered status 0.
- G1: a GET_DYNAMIC_INFO carrying GET_STREAM_INFO STREAM_INPUT 1 against the same hold was ADMITTED BESIDE
  (class 0, key 0xFC00, refused 0 clocks) and answered status 0.
- G2: the same batch beside a held GET_RX_STATE was admitted beside.
- HZ: 179 checks, 0 failures (176 plus the probe's 3).

These equal the reviewer's results line for line. So the comment and 03 §6 match the probe. No test was added
and no arm applies: the ruling asks for a record, not a fix.

## Item 3: suggestions (`d4ca85c`)

- **R418-2 S1 and R419-2 S6: taken together.** They rewrite the same 08 §4 paragraph
  (`docs/architecture/08_timing.md:187-210`).
  - It lists every AECP hold an ACMP transaction can meet: the barrier, LOCK_ENTITY against a stream step,
    ADD/REMOVE_AUDIO_MAPPINGS against any stream step (the MAP_CFG class-wide cross-lock, F03.7 rule 5), and a
    command on the same stream key.
  - It bounds each hold:
    - A preemptible command holds until its forced response.
    - LOCK_ENTITY and ADD/REMOVE_AUDIO_MAPPINGS are never preempted (`ucpu_preempt_w`,
      `KL_aecp_engine.sv:1719-1720`). They run the rest of their own program.
    - Every face wait in such a program is bounded by the shared gather watchdog (`KL_aecp_engine.sv:2342`,
      `MEM_TIMEOUT_CYC_P` = `DESC_MEM_TMO_CYC_P` = 4,096 clocks at the top, `protocol_processor_top.sv:3666`).
  - Derived figures:
    - LOCK_ENTITY (`E_LOCKEN`) makes 2 registry-face waits: 8,192 clocks, about 82 µs at `P-CLK-HZ`.
    - A mapping edit (`E_AMADD`) makes at most 2N + 3 edit-face waits: begin, N validations, commit-begin, N
      commit records, and finish.
    - The engine refuses cdl > 524 BAD_ARGUMENTS before dispatch (`KL_aecp_engine.sv:3212-3215`), so N ≤ 63:
      129 × 4,096 = 528,384 clocks, about 5.3 ms.
    - REGISTER and DEREGISTER are also never preempted, but they meet no ACMP transaction (03 §6).
  - The conclusion is unchanged: later than the 50 ms design budget, inside T-ACMP-CMD (200 ms).
- **R418-2 S2: taken.** The DL8 label is now "a read error under a command padded to 540 payload bytes". It
  changed in three places:
  - `tb/pp_top/sim_main.cpp`;
  - the named check of `mvu-echo-slot-std` in `tb/pp_top/aecp_mutants.py`;
  - the 09 §8.3 DL8 row, which also names the 578-byte echo.
  - Verified at once: `make -C tb/pp_top deadline` 64/0. `aecp_mutants.py --only mvu-echo-slot-std,mvu-fault-status-10`
    gave control PASS, with the arms KILLED (1 and 4, the new label named).
- **R418-2 S3** (the `KL_aecp_notify` fan-out tracking item): the manager's, by the assignment. It goes to the
  residue checklist at merge, not done here.

## Parent-visible list (round 3)

- This round changes no top-level port, parameter or register-map. The top's header is byte-identical to the
  round-2 head and to the base. No RTL file is added or renamed. The only RTL edit of the round is a comment.
- The merge brings main's #135 and #137. Their own parent-visible lists apply at pin adoption, as their PR bodies
  record:
  - #137 owes one parent registry entry: `protocol-processor/tb/pp_top/acmp_mutants.py` in
    `DUT_READER_DISPOSITIONS` of the parent's `scripts/measure_test_evidence.py`.
    - It was applied in the scratch parent as `parent-adaptation-137-acmp-disposition.patch`, beside this file
      (1,064 bytes, sha256 `e4be68ac635eb803cadf20bb5506d3e3c07399c6a47a8ce4748513335332feaa`, +4 lines).
    - It is a parent adaptation owed by the pin bump, not a change of this lane.
  - #135 owes none. Its MAAP fix acts only with `cfg_maap_internal_i = 1`, which the parent ties to 0.
  - New entry points from main: `make -C tb/maap mutants`, `make -C tb/pp_top maap-internal`,
    `./obj_dir/Vpp_top_sim --acmp-only`, and `tb/pp_top/acmp_mutants.py`.
- Tallies the parent might quote: `tb/pp_top` 8,288 (default build 8,212, fixture 20, timebase 56), and
  `run_suites.sh` 1,018,218.
- Docs: 03 §6 records the GET_DYNAMIC_INFO limitation (F5), and 08 §4 bounds the ACMP wait per hold kind. The
  DL8 label is renamed. No wire behaviour changes in this round.

## Suite and entry-point table

| Command | Merge commit `97fe22f` | Head `d4ca85c` |
|---|---|---|
| `./scripts/run_suites.sh` (µPC map gate first) | rc 0, 33 suites, 1,018,218 checks, 0 failing | rc 0, 33 suites, 1,018,218 checks, 0 failing (`tb/pp_top` 8,288, `tb/ucpu` 415) |
| `./scripts/lint_hdl.sh` | — | rc 0, 41 LINT OK |
| `make check` (lint, wavedrom-check, links, matrix, modmatrix, params, stale) | rc 0 (1,003 links) | rc 0 (1,004 links) |
| `make stale` | — | rc 0 |
| `python3 scripts/gen_matrix.py --check` | rc 0 (94 rows, 0 untested) | rc 0 |
| `git diff --check` from `0451d83d`, `44a6bb90` and `3f3ea56b` | — | rc 0 each |
| `make -C tb/pp_top gsi-build / name-writes / gsi-internal / maap-internal / adp-config / deadline / d3 / hazards / budget` | — | rc 0 each: 85, 6,182, 34, 55, 64, 133, 176, 56 checks, 0 failures |
| `tb/pp_top/obj_dir/Vpp_top_sim --acmp-only` | 43/0 | rc 0, 43/0 |
| `make -C tb/ucpu run` | — | rc 0, 415/415 |
| `./syn/yosys/run.sh` | — | rc 0, 36 tops YOSYS OK |

## Mutant tables

Campaigns, all from the tree root, each rc 0 at both commits:

| Campaign | Merge commit `97fe22f` | Head `d4ca85c` |
|---|---|---|
| `make -C tb/pp_top aecp-mutants` | 5 controls PASS, 55/55 KILLED | same, every arm's count equal to the merge commit's and to the README |
| `python3 tb/pp_top/acmp_mutants.py --jobs 1` | 3 goldens PASS, 19/19 KILLED | same, every record equal |
| `make -C tb/maap mutants` | 32/32: controls maap 196, pp_top MP 34, rx_validator 555; 29 arms KILLED | same |
| `make -C tb/adp_engine mutants` | 32/32: 2 controls, 30 arms KILLED | same |
| `make -C tb/srp_top mutants` | 90/90: controls PASS, 78 arms KILLED, assertion coverage 65/65 | same |
| `make -C tb/nvm_port figures` | rc 0, all measured figures agree with the tree | same |
| `python3 tb/pp_top/d3_mutants.py --jobs 2` | 83/83 KILLED, goldens PASS; `hold_released_at_go` 17, `dispatch_not_held` 6 (as recorded) | same, every record equal |
| `python3 tb/pp_top/gsi_mutants.py` | 20 detected, golden and restored PASS | same |
| `python3 tb/pp_top/name_wr_mutant.py` | decode killed, golden and restored PASS | same |
| `python3 tb/acmp_talker/retry_mutants.py` | 62 killed, 7 equivalence and 1 performance control, baseline and restored rc 0 | same |
| `python3 tb/srp_admission/mutants.py` | 12/12 | same |
| `python3 tb/desc_mem_guard/mutate.py` | hold-deleted mutant detected | same |

AECP arms, failing checks at the head (identical at the merge commit and to `tb/pp_top/README.md`: 38 rows parsed,
the 17 shared-row arms checked by hand):
`dl-kill-tied-off` 28, `dl-released-before-queued` 3, `dl-armed-at-admission` 6, `dl-boot-hold-not-exempt` 1,
`dl-gdi-runs-on` 4, `dl-edit-preempted` 6, `dl-registry-preempted` 2, `dl-lock-preempted` 2,
`dl-kill-ack-keeps-owner` 2, `dl-preempt-after-effect` 4, `dl-preempt-after-effect-top` 2,
`ucpu-preempt-cuts-a-wait` 2, `ucpu-preempt-keeps-the-body` 1, `ucpu-preempt-repeats` 18,
`dlkill-always-misbehaving` 1, `dl-mvu-forced-status-10` 5, `dl-non-aem-forced-status-10` 4,
`mvu-fault-status-10` 4, `mvu-echo-slot-std` 1, `mvu-silent` 12, `fanout-never-ends` 23, `acmp-waits-for-aecp` 2,
`hz-stub-restored` 74, `hz-setcfg-not-barrier` 7, `hz-lock-not-lockop` 7, `hz-stream-key-none` 12,
`hz-reads-keyed-none` 13, `hz-clock-as-ro` 6, `hz-clock-as-lock` 3, `hz-name-as-ro` 8, `hz-registry-as-ro` 2,
`hz-identify-as-ro` 5, `hz-acmp-reads-as-steps` 23, `hz-barrier-no-priority` 127,
`hz-foreign-target-classified` 1, `hz-response-classified` 1, `hz-name-key-none` / `-talker` / `-held` 7 each,
`hz-name-as-stream` 2, `hz-stream-key-none-vs-read` / `-talker-read` / `-talker-step` 12 each,
`hz-talker-keyed-as-listener` 18, `hz-reads-keyed-none-talker` 13, `hz-setcfg-not-barrier-talker` 7,
`hz-lock-not-lockop-talker` 7, `hz-map-as-ro` / `-talker` 10 each, `hz-clock-key-none` / `-talker` 6 each,
`hz-identify-key-none` / `-talker` 5 each, `hz-map-key-none` / `-talker` 6 each.

ACMP mutants, failing checks at both commits (equal to #137's table at `4e55849`):

| Mutant | Suite | Failing |
|---|---|---|
| `msg_ok_forced` | acmp_listener / pp_top AC | 93 of 2988 / 1 of 43 |
| `guard_ctlr_dropped`, `guard_talker_eid_dropped`, `guard_talker_uid_dropped` | acmp_listener | 50 / 40 / 30 of 2984 |
| `cdl_not_44_rejected` | rx_validator / pp_top AC | 27 of 555 / 19 of 43 |
| `st_ls_settle_as_withdraw`, `st_ls_sid_da_swapped`, `st_ls_state_none`, `st_ls_vid_dropped` | pp_top AC | 7 of 43 each |
| `st_ls_index_zero` | pp_top AC | 6 of 43 |
| `st_ls_teardown_as_declare`, `bound_view_not_cleared` | pp_top AC | 1 of 43 each |
| `st_ls_teardown_lost`, `bound_view_not_latched`, `bound_dmac_from_sid` | pp_top AC | 2 of 43 each |
| `matcher_da_ignored`, `matcher_vid_ignored` | pp_top AC | 5 of 43 each |

## Parent consumer gate table

Scratch parent `$VALIDATION_STORAGE/a475-parent`:
- It is a `git archive` of the read-only trusted checkout at milan-fpga dev `ea3fb388`. The index was rebuilt to
  equal the checkout's (981 entries, tree `bae15aec` identical) and committed as a scratch baseline.
- Submodules:
  - `gptp-processor` `5dce647` and `third_party/verilog-axis` `48ff7a7` are cloned from their recorded URLs at
    the pins.
  - `external` `efeb541` is recorded and uninitialized, as in the checkout.
  - `protocol-processor` is a clone of this branch, checked out detached at `d4ca85c`. The gitlink is set to it,
    and `git submodule status` shows no `-` or `+` for the three initialized ones.
- #137's disposition line is applied first and committed in the scratch parent:
  `parent-adaptation-137-acmp-disposition.patch`, +4 lines in `scripts/measure_test_evidence.py`. With the
  gitlink, it is the only change against `ea3fb388`.
- The trusted checkout was never modified: 0 changed paths, HEAD `ea3fb388` at the end. The scratch parent had
  0 changed paths after the run.
- The gates ran in the round-2 order, one at a time, with heavy builds at `-j8` and Verilator 5.050 (the parent's
  pin too). Receipts: `$VALIDATION_STORAGE/a475-pg-head/`.

| # | Gate | rc | Result at head `d4ca85c` |
|---|---|---:|---|
| 1 | `python3 scripts/check_cpp_idiom.py` | 0 | every ratchet held |
| 2 | `python3 scripts/check_py_idiom.py` | 0 | every ratchet held |
| 3 | `python3 scripts/xvlog_gate.py --check` | 0 | 4 findings == ratchet (0 hdl/, 4 pinned processors), pinned at protocol-processor@d4ca85c6, gptp-processor@5dce647a (143 s) |
| 4 | `python3 scripts/check_rtl_source_lists.py` | 0 | 107 files in the milan_datapath closure; protocol-processor 36/42 tops, 6 recorded |
| 5 | `python3 scripts/pp_srcs.py --check --selftest` | 0 | OK |
| 6 | `python3 sw/builder/test_builder.py` | 0 | ALL GATES PASS EXCEPT 1 NOT RUN: gate 11 needs the mf48 board implementation report, not on this host (1,038 s) |
| 7 | `make -C tb/verilator/pp_shadow -j8` | 0 | builds of 606, 606, 646 and 311 checks, 0 failures |
| 8 | `python3 scripts/check_port_contracts.py` | 0 | 48 literal-bound, 59 without a local rationale, 196 test-only hierarchical observations; the ratchet is lowerable by 3 |
| 9 | `python3 scripts/measure_naming.py --check` | 0 | 96 recorded |
| 10 | `python3 scripts/measure_test_evidence.py --check` | 0 | 72 <= 77 suites without a mutation arm (round 2: 73; `tb/maap` is now armed; lowerable to 72), 10 <= 10, 0 <= 0 unexplained DUT readers, 3 <= 3 wall-clock files |
| 11 | `python3 scripts/docs_check.py` | 0 | 0 findings |
| 12 | `python3 scripts/lint_rtl.py --check` | 0 | 90 <= 90 |
| 13 | `make -C tb/verilator/nvm_cosim lint` | 0 | |
| 14 | `make -C tb/verilator/nvm_cosim quick` | 0 | 315/315 |
| 15 | `make -C tb/verilator/milan_dp -j8` | 0 | 9 RESULT PASS, 0 FAIL (1,546 s) |
| 16 | `make -C tb/verilator/milan_dp_render -j8` | 0 | leg defects 5/5 |

## What remains

- #81 acceptance 4 (T-IDENT-BURST, T-IDENT-REARM and T-CTR-OBSERVE have no RTL; the 300 s and 60 s defaults
  are not pinned): unchanged, so the PR relates to #81.
- #84 is not closed, so the PR relates to #84:
  - REGISTRY_OP has no reachable conflict (graded by HZ1 and HZ8).
  - Acceptance 4 (02 §2 rule 5) is not done.
  - New this round, F5: a GET_DYNAMIC_INFO's GET_STREAM_INFO record of a sink is not serialized against that
    sink's ACMP listener steps (03 §6). Serializing it is a later #84 item.
- The `KL_aecp_notify` fan-out tracking item (R418-2 S3, R418-1 S4) is the manager's, for the residue
  checklist at merge.
- Push, hosted CI, the re-review of the merge head and hardware: none of them is this role's, and none was run.
