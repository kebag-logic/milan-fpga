# [A510] Lane C7 (counters), round 2: handoff

Branch `c7-counters` from `e2c7d97d` (pushed, the round-1 head after the manager's merge
of main `c74711d4`). Issues #44, #78, #79. PR #147.
Assignment: #79 comment 5963890173; addendum (item 5): #79 comment 5963896239.
Reviews: R442-1 (#147 comment 5963845095, NEGATIVE, 2 MINOR) and R443-1 (#147 comment
5963886063, NEGATIVE, 1 MINOR). Ruling on the tick: #79 comment 5963704232.
TAKEN was already posted (#79 comment 5963893132) and is not repeated.

Status: DONE. Head `81edaaa` (local branch, nine commits on `e2c7d97d`, not pushed; the PR
body is handed over as `PR-BODY.md`, "Round 2" section). Code head `274b424`; `81edaaa`
adds only the campaign record to `tb/pp_top/README.md`. Every gate rc 0 (below).
REVIEW READY posted on #79 (comment 5965053895, 2026-10-03 05:26 CEST) with head
`81edaaa74f688081ad34c1e2f392612f46eb558c`.

| Commit | Item |
|---|---|
| `459f2fd` | 5 (addendum, done first as it says): `.gitattributes` entry for `tb/pp_top/ctr_mutations/*.patch` |
| `9078094` | 1. R442-1 F1: the GPTP_GM_CHANGED rule as the identity comparison alone |
| `5599879` | 2. R442-1 F2 / R443-1 F1: no removed op and no in-processor counter block in 01, 05, 06 |
| `52bf47b` | 3. R442-1 S1: the stale GET_COUNTERS paragraph (and the two phrases S1 names) |
| `d3f9e0f` | 3. R442-1 S2 = R443-1 F3: `ctr_mutants.py --jobs N` through `tb/common/mutant_pool.py` |
| `e27c070` | 3. R443-1 F2: the notify slot decode graded (K17) with four arms |
| `a34c505` | 3. R443-1 F4: STREAM_INPUT quadlets 6 and 7 under `0x00000FFF` |
| `274b424` | 4. R443-1 F5 and F6, the reviewer's exact text |
| `81edaaa` | the ctr campaign's record at `--jobs 1` and `--jobs 8` (`tb/pp_top/README.md`) |

No STOP condition met: no RTL change beyond comments (two files, comment lines only,
proved below), no port, no parameter, no register.

## 0. Design

Round 2 changes text, one test section and one campaign driver. Nothing the parent drives
or reads changes; the processor's preprocessed RTL is byte-identical to `e2c7d97d`.

Decisions taken where the findings left a choice, with their evidence:

1. **GPTP_GM_CHANGED (item 1).** The rule is one identity comparison: at each update the
   integrator publishes, count one when the grandmaster identity on `gm_id_i` differs from
   the identity in force before it; the identity in force out of reset is the first one
   published, which counts nothing. Neither `gm_change_i`, nor `gsi_asp_chg_i`, nor their
   coincidence identifies a grandmaster change. Clauses: Milan v1.2 §5.3.6.3 Table 5.1
   ("Number of gPTP GM changes, since boot"); IEEE 1722.1-2021 §7.4.42.2.2 Table 7-152
   (counters_valid bit 26, mask `0x20`) and Table 7-153 (offset 20, "gPTP grandmaster
   change count"). The assignment and the ruling cite "Table 7-112"; in the printed IEEE
   1722.1-2021, Table 7-112 is "IEEE 802.3 Passive Optical Network Media Subtype Options"
   (the media_subtype tables of §7.2), so the guide cites Tables 7-152/7-153, the tables
   the repository already uses for the AVB_INTERFACE counters. The rule is the one the
   rest of the tree states and grades:
   - `docs/guides/integrator.md:466` (the table row) and `06_aecp_engine.md:612` (F06.15);
   - the harness store, `tb/pp_top/sim_main.cpp:930-937`: at each `gm_change_i`, count when
     `gm_id_i != itf.gm_q`, then take it in force; `itf.gm_q` resets to the identity the
     bench drives at reset (`:1918-1920`), so the first identity counts nothing;
   - K11 (`counters_phases.hpp`): five identity changes count five, a domain-only strobe
     counts nothing; K13/K14 carry the count in the push;
   - the reference parent at `cdf49d1a`, `hdl/milan/milan_datapath.sv:7267`:
     `pp_gm_id_edge_w = (|pp_gm_id_q_r) & (pp_gm_id_q_r != cfg_adp_gptp_gm)`, a change only
     against a prior identity, counted at `:3514`; consistent with the ruling (#79 comment
     5963704232): a domain-only change is not a grandmaster change.
2. **A8 in F05.3's legend (item 2).** Both reviews suggest A8 say the bound view drops
   (`acmp_bound_o` falls). In the RTL it does not drop at A8: A8 drives the `srp`
   WITHDRAW_LISTENER request (`protocol_processor_top.sv:2615-2621`, op 3) and clears the
   record's settled fields (`KL_pp_acmp_listener.sv:1162-1169`); the top's bound view
   (`bound_r` and the stream identity) is cleared by A9's discovery disarm
   (`protocol_processor_top.sv:1808-1819`, `lstn_disc_disarm_w`), and `acmp_bound_o` is
   its debounced copy (`:945-954`). A8 without A9 is a settled sink re-probing
   (SETTLED_* to PRB_W_DELAY/PRB_W_AVAIL on T-ACMP-NOTK or EVT_TK_UNREGISTERED), which keeps
   its binding. So A8 now says it issues no stream-datapath request and that the bound
   view follows the binding and is withdrawn with A9, and A9 says what it withdraws
   (`acmp_bound_o` falls unless A4 re-arms in the same transaction, a re-bind). The
   reviewers' wording is exact for the UNBIND_RX teardown (A8 then A9, F05.6), which
   `tb/pp_top` AS6 grades ("the bound view is cleared with the binding").
3. **The notify slot decode (item 3, R443-1 F2): graded, not only stated.** K17 strobes
   four objects the notification block keeps no slot for (AVB_INTERFACE 1, CLOCK_DOMAIN 1,
   STREAM_INPUT 8, STREAM_OUTPUT 8; the default shape is 8 by 8), each alone, and requires
   no unsolicited GET_COUNTERS of any object at either controller for 1.5 s, longer than
   the one-second window K13 to K16 leave open; then a slotted strobe still pushes. Four
   arms remove each term of the decode (`KL_aecp_notify.sv:491-506`): the AVB_INTERFACE
   index test (the reviewer's probe P3), the CLOCK_DOMAIN index test and the two stream
   range tests.
4. **R443-1 F5 and F6 (item 4): the exact text.** The posted comment renders F6's link as
   `https://github.com/kebag-logic/milan-fpga/blob/a49faa38.../review-evidence/ppC7-r1/reviews/R443-1/11_maap_engine.md`,
   a relative link rewritten against the evidence directory; that path does not exist
   (the GitHub contents API answers 404). The reviewer's packet
   (`ppC7-r443-1-packet/REPORT.md`) carries the exact text with the relative link
   `[11](11_maap_engine.md)`, which is what 02 now carries, so the visible text is
   identical and the link resolves in this repository (`make check` links gate).

## 1. Item 5 (addendum): `.gitattributes` (commit `459f2fd`)

| Change | Where |
|---|---|
| `tb/pp_top/ctr_mutations/*.patch whitespace=-blank-at-eol,-blank-at-eof`, next to the other campaigns' entries | `.gitattributes:7` |

Before: `git diff --check c74711d4 HEAD` rc 2 (three patches: blank context lines as a single
space, one blank line at EOF). After: rc 0 against `c74711d4` (= `origin/main`).

## 2. Item 1: R442-1 F1 (commit `9078094`)

| Change | Where | Clause |
|---|---|---|
| the AVB_INTERFACE duty bullet states the rule only as the identity comparison, the reset case, and that neither strobe nor their coincidence identifies a grandmaster change; the strobe-coincidence appositive is gone | `docs/guides/integrator.md:486-498` | Milan v1.2 §5.3.6.3 Table 5.1; IEEE 1722.1-2021 §7.4.42.2.2 Tables 7-152, 7-153 |

Agrees with `integrator.md:466`, F06.15 (`06_aecp_engine.md:612`), `sim_main.cpp:930-937`
and the ruling. Test: the existing K11 and its arm `store-counts-domain-strobes` (the store
counts every `gm_change_i`), KILLED, 7 failures (K11 x2 named).

## 3. Item 2: R442-1 F2 and R443-1 F1 (commit `5599879`)

| Change | Where |
|---|---|
| F01.3: the `ctrs["counters"]` node and `adapters --> ctrs` edge removed; the 02 node renamed to the landed faces (`faces["srp/maap faces · gptp/avtp/mclk levels · gsi/ctr read faces · side-port · nvm port"]`), with an edge `faces -- "gsi / ctr read words" --> ucpu` | `docs/architecture/01_overview.md:240, :253` |
| 01 block table, Event router: no event feeds a counter here | `01_overview.md:98` |
| 01 §2: the external engines are reached through the faces of 02 §4 (srp/maap class B; gPTP, AVTP, media clock as levels and read faces), not "adapter interfaces"; scope rows: GET_COUNTERS reporting, the banks out of scope | `01_overview.md:9, :36, :42-46` |
| 01 §7 profile mechanism: the STREAM_OUTPUT counter-mask table is no processor ROM | `01_overview.md:196-200` |
| F05.1 edge: `srp declare/withdraw; the bound view` to `srp face + acmp_bound levels` | `05_acmp_engine.md:106` |
| F05.3 legend A8 (no `avtp` op) and A9 (what it withdraws); F05.6 node `A8 withdraw SRP + clear settled`, `A9 disarm discovery + withdraw the bound view` | `05_acmp_engine.md:286-287, :350-351` |
| F06.14 SET_CLOCK_SOURCE: `mclk.SET_CLOCK_SOURCE` replaced by the committed index on the `aecp_clk_src_index_o` level (02 §4.5) | `06_aecp_engine.md:469` |
| same rule beyond the three: 03's state-RAM list (no counters), the guide index row for 06, docs/README's GPTP/AVTP/MCLK participants | `03_packet_engine.md:31`, `docs/guides/README.md:34`, `docs/README.md:141` |
| the RTL comments R442-1 F2 names (optional there), comment lines only | `hdl/acmp/KL_pp_acmp_listener.sv:25, :184, :188, :1162` |

Verification: R442-1's `stale_names.sh` over `docs hdl tb` prints nothing; R443-1's
`grep -rnE 'avtp\.[A-Z_]+|srp \+ avtp adapters|gptp · avtp · mclk adapters' docs` rc 1 (no
match); `make check` rc 0. Tests: none (text and figures; `make check` renders every
mermaid block).

## 4. Item 3: suggestions

### 4.1 R442-1 S1 (commit `52bf47b`)

| Change | Where | Clause |
|---|---|---|
| "GET_COUNTERS keeps no counters": the landed `E_GCTRS` (locate; 17-µop hit path with eight four-beat `READ_CTRS`; an 11-µop miss arm laying the zero body from an iterator loop; `E_GCTRSNS` two µops into it), ENTITY refused NOT_SUPPORTED, and Tables 5.1/5.4/5.6/5.7 rather than 5.6 alone | `06_aecp_engine.md:1136-1154`; program `hdl/aecp/ucode/gen_ucode.py:823-861` | IEEE 1722.1-2021 §7.4.42.2, Table 7-150 |
| "the µCPU serves and latches counters" corrected | `docs/10_RESOURCE_AND_EFFORT.md:404-407` | — |
| the top's face comment names Tables 5.1/5.4/5.6/5.7 (comment line only) | `hdl/top/protocol_processor_top.sv:369` | Milan v1.2 |

### 4.2 R442-1 S2 = R443-1 F3 (commit `d3f9e0f`)

`tb/pp_top/ctr_mutants.py` adopts `tb/common/mutant_pool.py` (`add_jobs_argument`,
`in_order`, `:33, :126, :149`): each unit (the positive control, then each arm) runs in a
scratch copy of its own (`trial`, `:85`), the control first and alone, the arms up to N at
once, results printed in the declared order. The serial restore-with-fresh-timestamps
scheme is gone (each copy is fresh). README section updated (`tb/pp_top/README.md`, the
campaign section).

### 4.3 R443-1 F2 (commit `e27c070`)

| Change | Where |
|---|---|
| K17: four unslotted strobes push nothing for 1.5 s each; a slotted one still pushes, byte-exact | `tb/pp_top/counters_phases.hpp:354-388` (helper `any_pushes` `:107`, constants `:36-40`), run at `:157`; the deregistration check is now labelled K17 (`:160`) |
| four arms | `tb/pp_top/ctr_mutations/ctr-notify-{avb,ckd}-any-index.patch`, `ctr-notify-{stri,stro}-past-shape.patch`; `ctr_mutants.py:55-59` |
| docs | 06 §6.6 push paragraph (`06_aecp_engine.md:632`), 09 §8.6 table and arm count, 00 GAP-05 Verified by, `tb/pp_top/README.md` section K table and campaign record, Makefile and `sim_main.cpp` comments |

| Check | Its failing mutant (named) |
|---|---|
| K17: AVB_INTERFACE 1 pushes nothing | `ctr-notify-avb-any-index` (1 failure) |
| K17: CLOCK_DOMAIN 1 pushes nothing | `ctr-notify-ckd-any-index` (1 failure) |
| K17: STREAM_INPUT 8 pushes nothing | `ctr-notify-stri-past-shape` (1 failure) |
| K17: STREAM_OUTPUT 8 pushes nothing | `ctr-notify-stro-past-shape` (1 failure) |
| K17: AVB_INTERFACE 0's own strobe still pushes, byte-exact | also fails under `ctr-notify-avb-dropped`, `-avb-as-clock`, `-one-window`, `ctr-change-type-from-index`, `ctr-index-from-type`, `ctr-block-beats-swapped` and both `store-*` arms |

### 4.4 R443-1 F4 (commit `a34c505`)

| Change | Where | Clause |
|---|---|---|
| STREAM_INPUT quadlets 6 TIMESTAMP_VALID and 7 TIMESTAMP_NOT_VALID named (under `0x00000FFF` only, zero under `0x00000F3F`); a counts row: per received stream data AVTPDU with tv set / clear, per frame, reset with the input bank | `docs/guides/integrator.md:456, :470` | IEEE 1722.1-2021 Tables 7-156, 7-157 (offsets 24, 28); Milan v1.2 §5.3.8.10 (the bank reset) |

The reference parent keeps them per frame and wipes them with the bank
(`KL_avtp_rx_monitor_ctx.sv:988, :770` at `cdf49d1a`).

## 5. Item 4: residue R443-1 F5 and F6 (commit `274b424`)

| Finding | Exact text, where |
|---|---|
| F5 | "`DESC_MEM_TMO_CYC_P` (the engine's `MEM_TIMEOUT_CYC_P`, 06 §8.1)" at `02_interfaces.md:209` and `:435` |
| F6 | appended to the §5 `LINK_UP/DOWN` row's Consumers cell: "the internal MAAP engine (PortOperational!, [11](11_maap_engine.md)); the PRNG seed latch (first rise)", `02_interfaces.md:481` |

## Parent-visible list

- **No interface change.** No port, parameter or register of `protocol_processor_top`
  changes; the `ctr_*` face, `KL_pp_shadow` and the parent's GET_COUNTERS path are
  untouched. Both adoption patches are unchanged and apply (c4c6 then c8).
- **RTL:** comment lines only (`KL_pp_acmp_listener.sv:25, :184, :188, :1162`;
  `protocol_processor_top.sv:369`); preprocessed source identical (below). Gate 8 counts
  the same 1,756 processor ports as round 1.
- **Text the parent cites moves:** integrator guide §7.1 (the GPTP_GM_CHANGED rule;
  STREAM_INPUT quadlets 6 and 7 and their row); 01 F01.3 (the 02 node is now `faces`,
  `ctrs` is gone), the block table, §2, §7; 05 F05.1, F05.3 A8/A9, F05.6; 06 F06.14's
  SET_CLOCK_SOURCE row, §6.6's push paragraph, the GET_COUNTERS design paragraph; 02 §4,
  §4.6, the §5 `LINK_UP/DOWN` row; 03's state-RAM row; 09 §8.6; 00 GAP-05 Verified by;
  docs/README participants; `docs/10_RESOURCE_AND_EFFORT.md` item 3. No anchor removed;
  the `tb/pp_top` README heading "K9 to K16" became "K9 to K17" (no in-tree link to it).
- **Tallies the parent may quote:** `tb/pp_top` 9,191 -> 9,196 (+5, K17; the counters
  build 23 -> 28); sweep 1,019,111 -> 1,019,116; every other suite unchanged; the ctr
  campaign 13 -> 17 arms.
- **New processor files the parent's gates see:** four patches in
  `tb/pp_top/ctr_mutations/`; `ctr_mutants.py` imports `tb/common/mutant_pool.py` (gates 2
  and 10 pass).

## Gates

All with the pinned Verilator 5.050 (wrapper sha256 `905795b9…`), every command run
directly with its own log and rc in scratch (`$VALIDATION_STORAGE/c7-a510/`), heavy runs under a
memory guard that records the service's peak memory (none tripped).

### Processor suites and entry points

| Command | Where | Result |
|---|---|---|
| `./scripts/run_suites.sh` | `git archive` of `274b424` (all code) | rc 0: 33 suites, **1,019,116** checks, 0 failing; `tb/pp_top` **9,196** (+5); `tb/adp_engine` 1,328; every other suite as round 1; 819 s, peak anon 7.0 GB |
| `./scripts/run_suites.sh` | `git archive` of `81edaaa` (final) | rc 0: the same 33 suites and per-suite tallies, 1,019,116 checks, 0 failing; 809 s |
| `./scripts/lint_hdl.sh` | `274b424`, `81edaaa` | rc 0, 41 of 41 |
| `make check` | in-tree after each item; `81edaaa` archive | rc 0 each: 41 mermaid + 18 wavedrom, 1,095 links, 115 REQ / 17 GAP, 94 rows 0 untested, 27 parameters |
| `python3 scripts/gen_matrix.py --check` | `274b424`, `81edaaa` | rc 0 |
| `git diff --check c74711d4 HEAD` | tree | rc 2 before item 5, rc 0 from `459f2fd` to `81edaaa` |
| `git apply --check`, every campaign patch in `tb/` | `274b424`, `81edaaa` | 224 of 224 |
| R442-1 `stale_names.sh`; R443-1's grep | tree at `81edaaa` | no hit; no match |

### Mutants

| Campaign | Result |
|---|---|
| `ctr_mutants.py --jobs 1` (archive of `274b424`, pinned to CPUs 0-3, alone) | rc 0: control PASS, 17 of 17 KILLED; 940 s; peak anon 1.5 GB |
| `ctr_mutants.py --jobs 8` (same archive, pinned to CPUs 0-3, alone) | rc 0: control PASS, 17 of 17 KILLED; 699 s; peak anon 9.1 GB; printed record byte-identical to `--jobs 1` (sha256 `0fd23cc6151456be…`, 11,104 B, both) |
| a first `--jobs 8` count run on the working tree before `e27c070` was committed | 17 of 17 KILLED, the same counts (the source of the README record) |
| other campaigns | not re-run: the RTL is preprocessed-identical, no patch or exact-edit anchor touches a changed comment line (searched), every patch applies |

Per-arm record (identical at both `--jobs`; the named check first):

| Arm | Failing checks |
|---|---|
| `ctr-avb-not-supported` | 9: K9, K10 x4, K11 x3, K12 |
| `ctr-ckd-not-supported` | 3: K16 x3 |
| `ctr-index-from-type` | 18: K9, K10 x4, K11 x3, K13, K14, K15 x3, K16 x4, K17 |
| `ctr-block-beats-swapped` | 9: K11 x3, K13, K14, K15 x3, K17 |
| `ctr-locate-ignored` | 1: K12 |
| `ctr-notify-avb-dropped` | 6: K13, K14 x2, K15 x2, K17 |
| `ctr-notify-avb-as-clock` | 8: K13, K14 x2, K15 x2, K16, K17 x2 |
| `ctr-notify-ckd-dropped` | 1: K16 |
| `ctr-notify-one-window` | 3: K15, K16, K17 |
| `ctr-notify-no-window` | 5: K14 x3, K15 x2 |
| `ctr-change-type-from-index` | 8: K13, K14 x2, K15 x3, K16, K17 |
| `ctr-notify-avb-any-index` | 1: K17 (AVB_INTERFACE 1) |
| `ctr-notify-ckd-any-index` | 1: K17 (CLOCK_DOMAIN 1) |
| `ctr-notify-stri-past-shape` | 1: K17 (STREAM_INPUT 8) |
| `ctr-notify-stro-past-shape` | 1: K17 (STREAM_OUTPUT 8) |
| `store-counts-domain-strobes` | 7: K11 x2, K13, K14, K15 x2, K17 |
| `store-link-detector-resets-up` | 11: K9, K10 x4, K11, K13, K14, K15 x2, K17 |

### Parent consumer gates (dev `cdf49d1a` + c4c6 + c8)

Scratch parent `$VALIDATION_STORAGE/c7-a510/parent`: `git archive` of the trusted checkout,
`git init` and commit; `external` `efeb541a`, `gptp-processor` `5dce647a`,
`third_party/verilog-axis` `48ff7a7e` cloned from round 1's local mirrors of their GitHub
origins (each pin verified present), `git submodule init`; `protocol-processor` a clone of
this branch at `81edaaa` with its gitlink committed (`274b424` for the first light run);
then `parent-adoption-c4c6-ea3fb388.patch` (sha256 `67bcd698…`) and
`parent-adoption-c8-cdf49d1a.patch` (`aa5a88eb…`) with `git apply`, in that order. The
trusted checkout is untouched (HEAD `cdf49d1a`, `git status` empty).

| # | Gate | Result at `81edaaa` |
|---|---|---|
| 1 | `check_cpp_idiom.py` | rc 0, every ratchet held; 168 translation units; multi-declarator 0 <= 0 |
| 2 | `check_py_idiom.py` | rc 0, every ratchet held |
| 3 | `xvlog_gate.py --check` (alone, last) | rc 0, 4 findings == ratchet (the same four) |
| 4 | `check_rtl_source_lists.py` | rc 0: 107 files; protocol-processor 36/42 tops, 6 recorded |
| 5 | `pp_srcs.py --check --selftest` | rc 0 |
| 6 | `sw/builder/test_builder.py` (alone) | rc 0: ALL GATES PASS EXCEPT 1 NOT RUN (gate 11, a board report not on this host); 1,183 s |
| 7 | `make -C tb/verilator/pp_shadow -j16` | rc 0: 606, 606, 646 and 311 checks, 0 failures |
| 8 | `check_port_contracts.py` | rc 0: protocol-processor 1,756 ports |
| 9 | `measure_naming.py --check` | rc 0, 96 recorded |
| 10 | `measure_test_evidence.py --check` | rc 0, 0 <= 0 unexplained DUT-source readers |
| 11 | `docs_check.py` | rc 0, 0 findings |
| 12 | `lint_rtl.py --check` | rc 0, 90 <= 90 |
| 13 | `make -C tb/verilator/nvm_cosim lint` | rc 0 |
| 14 | `make -C tb/verilator/nvm_cosim quick` | rc 0, 315/315 |
| 15 | `make -C tb/verilator/milan_dp -j16` | rc 0, 9 RESULT PASS, 0 FAIL; `[CTRS2]` reads mask 0x23 and LINK_UP = LINK_DOWN + 1 |
| 16 | `make -C tb/verilator/milan_dp_render -j16` | rc 0, leg defects 5/5 |

Gates 1, 2, 4, 5 and 8 to 12 also ran at `274b424`, all rc 0 with the same figures.

## Out-of-context cost

The two RTL files changed only comment lines. `verilator -E -P` (pinned 5.050, comments
stripped) gives byte-identical preprocessed source at `e2c7d97d` and at head:

| File | Preprocessed bytes | sha256 (base = head) |
|---|---:|---|
| `hdl/acmp/KL_pp_acmp_listener.sv` | 41,467 | `5134a80a98d3be56…` |
| `hdl/top/protocol_processor_top.sv` | 155,115 | `dc511d2d4b283715…` |

Identical source to the elaborator means an identical netlist: the out-of-context cost is
0 by construction, so no synthesis run was made. Round 1's measured record (0 for the tick
removal) stands.

## Housekeeping

- The two ignored entries this session created in the tree (`.venv-wavedrom/` from an
  in-tree `make check`, `tb/common/__pycache__/` from an in-tree driver run, both created
  after the session started) were removed with `git clean -fdX`; `git status --ignored`
  is empty at `81edaaa`.
- Scratch, logs and the parent copy: `$VALIDATION_STORAGE/c7-a510/` (nothing large here).
- The trusted parent checkout was only read (HEAD `cdf49d1a`, status empty).
