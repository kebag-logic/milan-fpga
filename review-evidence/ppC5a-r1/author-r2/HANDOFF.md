# [A466] HANDOFF — lane C5a round 2 (PR #140)

Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, branch `c5a-aecp-deadlines`.
Round-2 start head `f963fe9ac591b8a42547700468fc875db27ae5ab` (round 1, base `0451d83d`). Assignment:
issue #81 comment 5923634905, on the reviews R418-1 (PR #140 comment 5921631179) and R419-1 (comment
5921721080), both NEGATIVE. TAKEN posted as issue #81 comment 5923637418; REVIEW READY with the head as
comment 5927089371.

Status: REVIEW READY. Head `44a6bb9082d31dbf933087ef007ad78a110e7053` (eight commits on `f963fe9`, not
pushed). The session was cut once by a restart at 07:41, with the tree clean and seven commits in. The run
it cut, the processor's other mutation campaigns, was re-run in full. Every gate, suite and campaign is
rc 0. No STOP condition was met: no port, parameter or parent-visible interface change.

| Commit | Item | Subject (short) |
|---|---|---|
| `44db34b` | 1 | every class and key pair that can conflict with ACMP graded (HZ9 to HZ12), 19 arms; the false statement removed |
| `9f0299a` | 2 | an MVU response whose memory fails answers NOT_IMPLEMENTED with the command echoed (DL8), 2 arms |
| `a2d2a24` | 3 | every non-AEM message type forced to NOT_IMPLEMENTED with the command echoed (DL9), 1 arm |
| `5107327` | 4 | the registry and lock exemptions and the owner clear on an honoured kill proven (DL10, DL11, DL1), 3 arms |
| `bf9b32d` | 5 | the deadline checks of `tb/ucpu` renamed P20; the HZ banner and single HZ prefixes |
| `49041e6` | 6 | the cheap suggestions taken |
| `88e3459` | — | `tb/pp_top/README.md`: the campaign record at the head (no gate reads it) |
| `44a6bb9` | 6 (R419-1 S3) | `syn/ooc/README.md`: the complete processor's Vivado area at base and at the change (no gate reads it but `make check`'s link scan) |

Environment: Verilator 5.050 (the CI pin, `hdl.yml`) from the host's pinned tool directory, first on PATH;
yosys 0.66. Every build ran under an 8-CPU affinity mask, under which Verilator's `-j 0` resolves to
`make -j 8` (checked by capturing the make command line). The service is capped at 12 GiB, so the D3
campaign ran with `--jobs 2`. Runs longer than one foreground call were started detached and waited on in
the foreground until they ended, and their exit status was read from a file; nothing was piped into a
verdict. Scratch trees and logs: `$VALIDATION_STORAGE/a466-*`. The working tree was clean after every run.

## 1. Item 1 — R418-1 F1 / R419-1 F1 (MAJOR): every reachable conflict graded, the statement removed

Clauses: 03 §6 F03.7 (RO_SNAPSHOT "blocked only vs in-flight write on the same key", NAME_WR, CLOCK_CFG,
MAP_CFG, LOCK_OP, CFG_BARRIER rows) and the scoreboard's rules (1) to (6)
(`hdl/packet_engine/KL_pp_scoreboard.sv:133-157`); IEEE 1722.1-2021 §7.4.17 (SET_NAME names any named
descriptor, STREAM_INPUT and STREAM_OUTPUT included), §7.4.21.1 (SET_SAMPLING_RATE: AUDIO_UNIT,
VIDEO_CLUSTER or SENSOR_CLUSTER), §7.4.25.1 (SET_CONTROL: CONTROL), §7.4.45.1 (ADD_AUDIO_MAPPINGS:
STREAM_PORT_INPUT or STREAM_PORT_OUTPUT), Table 7-141 (NOT_SUPPORTED: the target is not supported).

Reachability at this top (ACMP presents RO_SNAPSHOT for its state reads and STREAM_CFG for every other step,
always on a stream key; the AECP engine is single-issue):

| AECP class | against ACMP RO_SNAPSHOT (same key) | against ACMP STREAM_CFG | graded by |
|---|---|---|---|
| CFG_BARRIER | yes (global) | yes (global) | HZ2, HZ3, HZ11a |
| LOCK_OP | no (key 0 is no stream key) | yes | HZ4, HZ11b, HZ11c |
| STREAM_CFG | yes | yes, per key | HZ5, HZ10a-d |
| MAP_CFG | yes, only through a command naming a stream descriptor | yes, class-wide cross-lock | HZ7, HZ11d-e, HZ12c |
| CLOCK_CFG | yes, only through a command naming a stream descriptor | no (rule 6) | HZ8, HZ12a |
| NAME_WR | **yes, with a legal command** | no (rule 6) | HZ8, HZ9a-f |
| IDENTIFY | yes, only through a command naming a stream descriptor | no (rule 6) | HZ8, HZ12b |
| REGISTRY_OP | **no reachable pair**: its key is the registry's, which no ACMP transaction presents | no (rule 6) | HZ1, HZ8 |
| RO_SNAPSHOT | no (two reads) | yes, per key | HZ6, HZ10e-f |

Found while doing it: both reviewers' talker-side probe was inconclusive because section HZ ran with no
MAAP allocator, so the talker sat in its MAAP request wait (`S_EV_MAAP`) and took no command. And the talker
returns its RX slot once it has read a frame, so a talker transaction holds its key a few clocks only. So:
HZ now runs with the allocator answering (`io.maap_on = true`, justified at the line); talker-side pairs are
graded with the AECP command held by the same TX-pool stall (`hold_aecp`); and every "waits" check
requires the scoreboard to have refused the head at least once (new wrapper taps `dbg_sb_ref_aecp_o`,
`dbg_sb_ref_acmp_o`), so a head that waits for its engine rather than its key cannot pass.

Tests (`tb/pp_top` section HZ, `make -C tb/pp_top hazards`: 83 -> 176 checks):

| Check | Grades |
|---|---|
| HZ8 (added) | REGISTER runs beside a held GET_RX_STATE: REGISTRY_OP has no reachable conflict |
| HZ9a | SET_NAME STREAM_INPUT 1 waits for a held GET_RX_STATE of sink 1, then SUCCESS; GET_NAME reads it back byte-exact |
| HZ9b, HZ9c | SET_NAME STREAM_INPUT 0 beside that read; SET_NAME STREAM_INPUT 1 beside a held UNBIND_RX of sink 1 |
| HZ9d, HZ9e, HZ9f | held SET_NAME STREAM_OUTPUT 1 holds back GET_TX_STATE source 1 (SUCCESS), not source 2; held SET_NAME STREAM_INPUT 1 holds back GET_RX_STATE sink 1 |
| HZ10a-f | STOP_STREAMING STREAM_INPUT 1 vs a read of sink 1; held STOP_STREAMING STREAM_OUTPUT 1 vs GET_TX_STATE and DISCONNECT_TX of source 1 and DISCONNECT_TX of source 2; held GET_STREAM_INFO STREAM_OUTPUT 1 vs DISCONNECT_TX and GET_TX_STATE of source 1 |
| HZ11a-e | held SET_CONFIGURATION vs GET_TX_STATE; held LOCK_ENTITY vs DISCONNECT_TX and GET_TX_STATE; held ADD_AUDIO_MAPPINGS vs DISCONNECT_TX and GET_TX_STATE |
| HZ12a-c | SET_SAMPLING_RATE, SET_CONTROL, ADD_AUDIO_MAPPINGS naming STREAM_INPUT 1 wait for a read of sink 1 and are then refused NOT_SUPPORTED; naming STREAM_INPUT 0 they run beside; held naming STREAM_OUTPUT 1 they hold back GET_TX_STATE of source 1 |

New arms (19, all KILLED; failing-check counts in `tb/pp_top/README.md`): `hz-name-key-none` (named HZ9a,
and as `-talker` HZ9d, `-held` HZ9f), `hz-name-as-stream` (HZ9c), `hz-stream-key-none-vs-read`,
`-talker-read`, `-talker-step` (HZ10a-c, the existing patch), `hz-talker-keyed-as-listener` (HZ10c),
`hz-reads-keyed-none-talker` (HZ10e), `hz-setcfg-not-barrier-talker` (HZ11a), `hz-lock-not-lockop-talker`
(HZ11b), `hz-map-as-ro` (HZ7, which had no arm in round 1) and `-talker` (HZ11d), `hz-clock-key-none` and
`-talker` (HZ12a), `hz-identify-key-none` and `-talker` (HZ12b), `hz-map-key-none` and `-talker` (HZ12c).
Six patch files are new (`hz-name-key-none`, `hz-name-as-stream`, `hz-clock-key-none`,
`hz-identify-key-none`, `hz-map-key-none`, `hz-map-as-ro`, `hz-talker-keyed-as-listener`: seven).

The statement is removed: 03 §6 now states the reachability above; 09 §8.3 lists HZ8 to HZ12; the HZ8
banner says what rule (6) makes true; the PR body's What remains and parent-visible list are corrected.

#84 acceptance 2 re-judged: every class with a reachable conflict at this top is graded against ACMP
(CFG_BARRIER, STREAM_CFG, MAP_CFG, LOCK_OP, RO_SNAPSHOT, NAME_WR, CLOCK_CFG, IDENTIFY). REGISTRY_OP has no
reachable admission conflict at this top, so it cannot be graded by one; it is graded by HZ1 (its class and
key) and HZ8 (it never over-serializes). With acceptance 4 also not done, #84 stays "Relates to".

## 2. Item 2 — REQ-MVU-005 on the fault path (R418-1 F3, R419-1 F3), fixed

Clause: Milan v1.2 §5.4.3.3 Table 5.19 (MVU statuses SUCCESS and NOT_IMPLEMENTED; 2 to 31 reserved); IEEE
1722.1-2021 Table 9-6 (Vendor Unique: 0 and 1 common, 2 to 31 vendor-defined).

RTL (`hdl/aecp/KL_aecp_engine.sv`, at the head): the fault rebuild at A_ALLOC (`:3696`) and A_WR (`:3726`)
answers a command that is not an AEM_COMMAND (`st_echo_w`, `:1705-1707`, generalized in item 3; in item 2
it was MVU alone) NOT_IMPLEMENTED with the command echoed from its RX slot, the same frame the deadline
forces. The failure can come after the TX slot is granted, so such a response requests the oversize slot
whenever its echo would need it (`echo_len_w`, `txs_oversize_o`, `:2548-2554`); a legal command (cdl at
most 524) always fits the standard slot, an over-long one (a GET_MILAN_INFO padded past cdl 524) does not.
Banner `:227-240` and the `rsp_fail_w` comment updated.

Check: `tb/pp_top` DL8 — GET_MILAN_INFO under a response-memory read error, a write error and a tied-off
master, and padded to 540 payload bytes under a read error (a 578-byte echo in the oversize slot), answers
MVU NOT_IMPLEMENTED with the command echoed, byte-exact, each void counted; an AEM GET_CONFIGURATION under
the read error still answers ENTITY_MISBEHAVING header only; afterwards RX slots free and GET_MILAN_INFO
SUCCESS byte-exact. Arms: `mvu-fault-status-10` (4: DL8 under every fault, status 10, 60 bytes),
`mvu-echo-slot-std` (1: the 578-byte echo clipped to 576). Docs: 06 §6.9 GET_MILAN_INFO row, 00 REQ-MVU-005
and GAP-03 rows, operator and integrator guides.

## 3. Item 3 — R418-1 F2: the deadline-killed residual-bucket types

Clauses: IEEE 1722.1-2021 Table 9-2 (SUCCESS and NOT_IMPLEMENTED are the codes every message type shares),
Table 7-141 (status 10 is AEM's), Table 9-4 (ADDRESS_ACCESS 0 to 7), Table 9-5 (AV/C 0 to 2), Table 9-8
(HDCP APM 0 to 2), §9.4.2.5 (ADDRESS_ACCESS within 240 ms).

RTL: `st_echo_w` (`KL_aecp_engine.sv:1696-1707`) is true for every message type but AEM_COMMAND (the
validator's residual bucket carries AVC, HDCP APM, the reserved band and EXTENDED, so message_type 0 is the
test). The A_RUN remap (`:3644`) answers a preempted such command NOT_IMPLEMENTED with the command echoed
(round 1 did this for MVU only); the fault path of item 2 uses the same signal.

Check: DL9 — an ADDRESS_ACCESS, an AVC, an HDCP_APM and an EXTENDED command each answer NOT_IMPLEMENTED with
the command echoed idle, and the same frame byte-exact when queued behind a stall past their deadline and
preempted, inside T-AECP-RESP. Arm: `dl-non-aem-forced-status-10` (the round-1 MVU-only rule; 4: DL9);
`dl-mvu-forced-status-10` now fails DL3 and DL9 x4. Docs: 03 §6, 06 §8.1, both guides, 09 §8.3.

## 4. Item 4 — R419-1 F2: the two surviving kill-seam mutants

- Registry and lock exemption (`KL_aecp_engine.sv:1719-1720`). DL10: a REGISTER_UNSOLICITED_NOTIFICATION
  and a LOCK_ENTITY, each queued behind a stall past its own deadline, answer their own SUCCESS byte-exact
  with no redirect; the lock is then held (`dbg_lock_held_o`), and after the unlock a SET_NAME by another
  controller is pushed to the registered one (u = 1). Arms (split so each exemption is proven alone):
  `dl-registry-preempted` (2: DL10), `dl-lock-preempted` (2: DL10); `dl-edit-preempted` (all three) now
  fails DL6 and DL10 x4.
- Owner clear on an honoured kill (`protocol_processor_top.sv:3581`). New wrapper taps `dbg_sb_rel_o`,
  `dbg_sb_rel_id_o` (the scoreboard's normal release port). DL1 checks the RX-slot return after the kill
  releases no hold id again; DL11 checks that across the whole section every normal release named a live
  hold. Arm `dl-kill-ack-keeps-owner` (2: DL1, and DL11 with 19 releases of a freed id). Note: at this
  topology the stray release is harmless (the only possible new owner of the freed id is granted in the same
  clock as the stray release, which the scoreboard then ignores), so the check grades the release port's
  contract, which is what keeps it safe when a second AECP client exists.
- The reviewers' own script (`reviewer_mutants.py` from the R419-1 packet, read-only) re-run at the head:
  see section 7.

## 5. Item 5 — R418-1 F4 / R419-1 F4

- `tb/ucpu`: the deadline checks P19a-P19h are now P20a-P20h (P19 stays GET_AUDIO_MAP's; P20 was unused);
  the campaign names `P20a completes: one redirect`, `P20c`, `P20d`, `P20e`, `P20f`; `tb/ucpu/README.md`,
  09 §8.3, 06 §8.1 and the `tb/pp_top` README follow.
- The HZ banner now describes the TX-pool stall (`fill_tx_pool`, `hold_acmp`, `hold_aecp`); the vestigial
  `io.maap_on = false` line was replaced in item 1 by `io.maap_on = true` with its reason at the line (a
  talker with no allocator takes no command); the doubled `HZ HZ5` prefixes are now single (`HZ5`).

## 6. Item 6 — suggestions

| Suggestion | Taken / retained | Where, or why |
|---|---|---|
| R418-1 S1 (MVU preempt trade-off) | taken (recorded) | 06 §8.1: kept uniform with rule (e); exempting MVU would leave only its own program length as the bound |
| R418-1 S2 (LOCK_OP key 0 = {ENTITY,0}) | taken | comment `protocol_processor_top.sv:1453-1458` |
| R418-1 S3 (ACMP waiting on a conflicting AECP hold) | taken (stated, not measured) | 08 §4: up to T-BUDGET-AECP-WC plus the forced response, past the 50 ms design budget, inside T-ACMP-CMD |
| R418-1 S4 (fan-out row contradiction, tracking issue) | partly: the F08.3 row now says "not met as written" | the tracking issue is retained for the manager: this round may post only TAKEN / REVIEW READY / STOP |
| R419-1 S1 (equivalent arms as defence in depth) | taken | comments `KL_aecp_ucpu.sv:480-484`, `KL_aecp_engine.sv:1709-1712`; the effect-set claim checked by scanning every µprogram (only E_AMADD leads with COMMIT, and it is exempt) |
| R419-1 S2 (TB2 wording) | taken | TB2/TB3 check names "with all thirteen getters", 08 §4 table note |
| R419-1 S3 (Vivado figures) | taken (correction: an earlier draft of this file said Vivado is not installed; Vivado 2026.1 is, outside PATH) | `44a6bb9`, `syn/ooc/README.md`; section 7 |

## 7. Validation at the head

Which commit each receipt was taken at: `49041e6`, `88e3459` and the head `44a6bb9` differ only in
`tb/pp_top/README.md` and `syn/ooc/README.md`, which no build, suite, campaign or parent consumer reads
(checked: no campaign script or Makefile opens a README). Each detached run is dated by its start against
the commit times.

Processor suites and gates (all rc 0):

| Gate | Commit | Result |
|---|---|---|
| `./scripts/run_suites.sh` | `49041e6`, again at `44a6bb9` | rc 0 both: 33 suites, 1,017,487 checks, 0 failing; µPC map gate PASS (57 constants, 81 entry points) |
| `tb/pp_top` | same | 8,240 checks (round 1: 8,112): DL 29 -> 64, HZ 83 -> 176, TB 56, D3 133 |
| `tb/ucpu` | same | 415 (P19a-h renamed P20a-h, count unchanged) |
| `./scripts/lint_hdl.sh` | `49041e6`, `44a6bb9` | rc 0, 41 modules LINT OK |
| `make check` | `49041e6`, `88e3459`, `44a6bb9` | rc 0: 41 mermaid + 18 wavedrom, 1,003 links, 115 REQ rows and 17 GAP findings, 94 module rows 0 untested, parameters 26/26/26 |
| `make stale`, `scripts/gen_matrix.py --check` | `49041e6`, `44a6bb9` | rc 0; matrix OK (94 rows, 0 untested) |
| `syn/yosys/run.sh` | `49041e6` | rc 0, every top YOSYS OK, `KL_aecp_engine` YOSYS XILINX OK |
| `git diff --check 0451d83d..HEAD` and `f963fe9..HEAD` | `44a6bb9` | rc 0, empty |
| commit messages | `44a6bb9` | every round-2 commit a one-line subject, no body, no trailer |

Vivado (R419-1 S3): `syn/ooc/protocol_processor_ooc.tcl` from the head, Vivado 2026.1, default 8x8,
`xc7a100tfgg484-2`, 10 ns, run alone in the service (peak 3.2 GB; the unit hit its cap only with page
cache, `oom_kill 0`), each tree a `git archive` in an empty build directory, 165 s and 156 s:

| Resource | Base `0451d83d` | Lane RTL `88e3459` | Delta |
|---|---:|---:|---:|
| Slice LUTs | 30,334 | 30,645 | +311 |
| Registers | 31,820 | 31,994 | +174 |
| LUT as distributed RAM | 1,206 | 1,222 | +16 |
| RAMB36 / RAMB18 / DSP | 23 / 2 / 4 | 23 / 2 / 4 | 0 |
| WNS at 10 ns, OOC | -10.114 ns | -8.922 ns | (area only) |

Hierarchy: `u_scoreboard` 101/73 -> 137/169, `u_dispatch` 890/903 -> 904/926, `u_normalizer` 27/366 ->
91/384 (LUT/registers; unedited modules whose class, key and kill inputs are now live); the top's own
358/4,689 -> 365/4,722 (+33: the 32-bit deadline register and the boot-hold bit); `u_aecp` 6,430 -> 6,584
LUTs, registers 4,528 both (engine's own 1,439 -> 1,504; `u_ucpu` 2,033/490 -> 2,016/493; `u_d3`, the
unedited `KL_aecp_nvm_writer`, 1,006 -> 1,132). Recorded in `syn/ooc/README.md` (`44a6bb9`). Reports kept
in `$VALIDATION_STORAGE/a466-viv/{0451d83,88e3459}/build/` (`util.rpt`, `util_hier.rpt`, `timing.rpt`).

Resource cost (round 2 changes `KL_aecp_engine` only; the `KL_aecp_ucpu` and top edits are comments), yosys
`synth_xilinx -family xc7 -flatten`, out of context, `f963fe9` -> `49041e6`:

| Recipe | LUT | FF |
|---|---|---|
| LUT-only (`-nowidelut`, the round-1 figure) | 8,135 -> 8,130 (-5) | 4,583 -> 4,583 |
| default | 8,123 -> 9,231 | 4,583 -> 4,583 |

The default recipe's jump is ABC's wide-mux choice (MUXF7 574 -> 1,592, MUXF8 112 -> 642), not logic: the
LUT-only recipe, which cannot use them, is 5 LUT smaller. The Vivado figures above are the instrument of
record.

## 8. Mutation campaigns

`make -C tb/pp_top aecp-mutants` at `49041e6` (Verilator 5.050): 5 controls PASS, 55 arms KILLED (round 1:
5 and 30). Round 2's 25 new arms (failing-check counts; every arm fails its named check):

| Item | Arm | Fails |
|---|---|---|
| 1 | `hz-name-key-none`, `-talker`, `-held` | 7, 7, 7 (HZ9a; HZ9d; HZ9f) |
| 1 | `hz-name-as-stream` | 2 (HZ9c) |
| 1 | `hz-stream-key-none-vs-read`, `-talker-read`, `-talker-step` | 12, 12, 12 (HZ10a-c) |
| 1 | `hz-talker-keyed-as-listener` | 18 (HZ10c) |
| 1 | `hz-reads-keyed-none-talker` | 13 (HZ10e) |
| 1 | `hz-setcfg-not-barrier-talker`, `hz-lock-not-lockop-talker` | 7 (HZ11a), 7 (HZ11b) |
| 1 | `hz-map-as-ro`, `-talker` | 10 (HZ7), 10 (HZ11d) |
| 1 | `hz-clock-key-none`, `-talker` | 6, 6 (HZ12a) |
| 1 | `hz-identify-key-none`, `-talker` | 5, 5 (HZ12b) |
| 1 | `hz-map-key-none`, `-talker` | 6, 6 (HZ12c) |
| 2 | `mvu-fault-status-10`, `mvu-echo-slot-std` | 4 (DL8), 1 (DL8) |
| 3 | `dl-non-aem-forced-status-10` | 4 (DL9) |
| 4 | `dl-registry-preempted`, `dl-lock-preempted`, `dl-kill-ack-keeps-owner` | 2 (DL10), 2 (DL10), 2 (DL1, DL11) |

Round-1 arms whose counts moved because the new checks also see them: `dl-kill-tied-off` 16 -> 28,
`dl-armed-at-admission` 2 -> 6, `dl-edit-preempted` -> 6, `dl-mvu-forced-status-10` -> 5; all in
`tb/pp_top/README.md`.

The reviewers' own scripts at the head (read-only copies from the R419-1 packet, sha256 checked against its
manifest, run on a `git archive` of `88e3459`):

| Arm (R419-1 `reviewer_mutants.py`) | R419-1 at `f963fe9` | at `88e3459` |
|---|---|---|
| `r-registry-lock-preempted` | SURVIVED | **KILLED** (pp_top: 4, DL10); `tb/ucpu` run still passes (the exemption is the engine's, not the µCPU's) |
| `r-kill-ack-keeps-owner` | SURVIVED | **KILLED** (2: DL1, DL11) |
| `r-mvu-no-echo` | KILLED | KILLED (DL3) |
| `r-effects-short`, `r-queued-counts-unsolicited`, `r-kill-latched-unsolicited` | SURVIVED (R419-1 S1: equivalent) | SURVIVED, equivalent; now commented as defence in depth at the guards |

R419-1 `probe_hz_reachability.py`, with only its anchor moved from the HZ8 call to the HZ12 call (the run
list grew): P0 status 0 (SUCCESS beside), P1 status 0 after waiting (NAME_WR conflicts, as HZ9a grades),
P3 and P4 status 11 (NOT_SUPPORTED, as HZ12a-b grade). P2 still fails its own premise ("the ACMP command
(message 4) is admitted and held"): a talker transaction keeps its key a few clocks only, so a talker-side
ACMP command cannot be held by the TX-pool stall; HZ9d/HZ9e grade the same key pair held from the AECP side.

Other processor campaigns, at `88e3459`, all rc 0:

| Campaign | Result |
|---|---|
| `tb/pp_top/d3_mutants.py --jobs 2` | 83 of 83 KILLED by their named checks; goldens PASS |
| `make -C tb/adp_engine mutants` | 32/32 |
| `tb/pp_top/gsi_mutants.py` | 20 detected; golden and restored PASS |
| `tb/pp_top/name_wr_mutant.py` | decode killed; golden and restored PASS |
| `tb/acmp_talker/retry_mutants.py` | 62 killed, 7 equivalence controls, 1 performance control |
| `tb/srp_admission/mutants.py` | controls PASS, every stale-evaluation and discarded-round arm rc 2 |
| `tb/desc_mem_guard/mutate.py` | hold-deleted mutant detected |
| `make -C tb/nvm_port figures` | rc 0 |
| `make -C tb/srp_top mutants` | 90/90 KILLED, assertion coverage 65/65 |

(adp_engine, gsi, name_wr and retry ran 07:10-07:36, before the restart; srp_admission, desc_mem_guard
and the nvm_port figures were re-run after it, srp_top after the parent gates.)

## 9. Parent consumer gates

Scratch parent `$VALIDATION_STORAGE/a466-parent`: a `git archive` of the trusted checkout at milan-fpga dev
`e4b771f9`, blob-identical to it (gitlinks aside), submodules at their pins (external `efeb541`,
gptp-processor `5dce647`, third_party/verilog-axis `48ff7a7`); `protocol-processor` a clone of this lane,
checked out at `88e3459` and then at `44a6bb9`, with the gitlink set to it each time (scratch commits
`c640b93`, `166c222`). No parent adaptation is applied or needed at `e4b771f9`. The trusted checkout was
not modified, and the scratch parent had 0 changed paths after each run. Verilator 5.050 (the parent's
`elaborate.yml` pin). Gates in round-1 order, one at a time, heavy builds at `-j8`. Receipts:
`$VALIDATION_STORAGE/a466-pg/` (`88e3459`) and `$VALIDATION_STORAGE/a466-pgF/` (`44a6bb9`).

| # | Gate | `88e3459` | `44a6bb9` |
|---|---|---|---|
| 1 | `scripts/check_cpp_idiom.py` | rc 0, every ratchet held | rc 0 |
| 2 | `scripts/check_py_idiom.py` | rc 0 (288 modules) | rc 0 |
| 3 | `scripts/xvlog_gate.py --check` | rc 0, 4 findings == ratchet, none new (138 s) | rc 0, same |
| 4 | `scripts/check_rtl_source_lists.py` | rc 0, 36/42 tops, 6 recorded | rc 0 |
| 5 | `scripts/pp_srcs.py --check --selftest` | rc 0, 46 sources | rc 0 |
| 6 | `sw/builder/test_builder.py` | rc 0, ALL GATES PASS EXCEPT 1 NOT RUN (gate 11 needs a board implementation report not on this host), 987 s | not re-run |
| 7 | `make -C tb/verilator/pp_shadow -j8` | rc 0, 311 checks | not re-run |
| 8 | `scripts/check_port_contracts.py` | rc 0: 48 literal-bound, 59 without a rationale, the ratchet lowerable by 3 | rc 0, same |
| 9 | `scripts/measure_naming.py --check` | rc 0, 96 recorded | rc 0 |
| 10 | `scripts/measure_test_evidence.py --check` | rc 0 (73 <= 77, 10 <= 10, 0 <= 0, 3 <= 3; lowerable to 73) | rc 0, same |
| 11 | `scripts/docs_check.py` | rc 0, 0 findings | rc 0 |
| 12 | `scripts/lint_rtl.py --check` | rc 0, 90 <= 90 | rc 0 |
| 13 | `make -C tb/verilator/nvm_cosim lint` | rc 0 | rc 0 |
| 14 | `make -C tb/verilator/nvm_cosim quick` | rc 0, 315/315 | rc 0, 315/315 |
| 15 | `make -C tb/verilator/milan_dp -j8` | rc 0, every RESULT PASS (1,440 s) | not re-run |
| 16 | `make -C tb/verilator/milan_dp_render -j8` | rc 0, leg defects 5/5 | not re-run |

The four heavy builds were not re-run at `44a6bb9`: it adds only `syn/ooc/README.md`, which no parent
build reads. The lane needs no parent adaptation of its own.

## 10. Parent-visible list, issue closure, what remains

Parent-visible list (round 2):

- No top-level port, parameter or register-map change; no RTL port or parameter line changed in round 2
  (only `KL_aecp_engine` logic, and comments in `KL_aecp_ucpu` and the top). No new or renamed RTL file.
- Behaviour, both on the AECP wire:
  - a command of any AECP message type but AEM_COMMAND (MVU, ADDRESS_ACCESS, AVC, HDCP APM, EXTENDED,
    reserved) whose response memory fails, or which is preempted past its deadline, is answered
    NOT_IMPLEMENTED with the command echoed (round 1: status 10 header only on both paths, MVU's deadline
    path excepted);
  - such an answer to an over-long command (cdl past 524) takes the oversize TX slot. A legal command's echo
    always fits the standard slot.
  The parent's `tests/features/aecp_response_contract.feature` already expects NOT_IMPLEMENTED for every
  non-AEM message; none of the consumer gates reads either path.
- Added to round 1's list (behaviour landed in round 1, first graded and stated now): SET_NAME and an ACMP
  read of the stream it names exclude each other at admission, either order; a SET_SAMPLING_RATE,
  SET_CONTROL or ADD_AUDIO_MAPPINGS naming a stream descriptor waits likewise before it is refused
  NOT_SUPPORTED.
- Test-only: `tb/pp_top/pp_top_wrap.sv` gains taps `dbg_sb_ref_aecp_o`, `dbg_sb_ref_acmp_o`, `dbg_sb_rel_o`,
  `dbg_sb_rel_id_o` (hierarchical observation inside the processor's own testbench).
- Entry points unchanged (`make -C tb/pp_top deadline | hazards | budget | d3 | aecp-mutants`); the campaign
  grows to 55 arms. Section HZ now runs with a MAAP allocator answering.
- Parent ratchets at `e4b771f9`, confirmed by the gate table above: port contracts 48 literal-bound and 59
  without a rationale (the ratchet lowerable by 3), suites without a mutation arm 73 <= 77 (lowerable to
  73); naming, draws, DUT readers, wall-clock files and lint unchanged.
- Area: +311 Slice LUTs and +174 registers on the complete processor (Vivado, section 7).

Issue closure (round-2 rulings):

- #57: **Closes.** Acceptance 1 to 3 as round 1, and the ruled fault-path fix (item 2, DL8, two arms).
- #81: Relates. Acceptance 1 to 3 met; acceptance 4 (F08.1 rows T-IDENT-BURST, T-IDENT-REARM, T-CTR-OBSERVE
  and a check pinning 300 s / 60 s) not done.
- #84: Relates. Acceptance 1 and 3 met. Acceptance 2: every class with a reachable admission conflict at
  this top is graded against ACMP (eight of nine); REGISTRY_OP has none (its key is the registry's, which
  no ACMP transaction presents, and rule (6) puts it beside every other ACMP class), so it is graded by its
  class and key (HZ1) and by never over-serializing (HZ8) only. Acceptance 4 (02 §2 rule 5, the
  synchronous active-low reset) not done.

What remains (unchanged from round 1 unless said): #81 acceptance 4; #84 acceptance 4 and the REGISTRY_OP
remainder above; F03.3's kill count and trace (a register-map change); no kill consumer for ACMP's stamped
deadline; `KL_aecp_notify` holding solicited commands behind a whole notification class (08 §4 finding);
GET_DYNAMIC_INFO and READ_DESCRIPTOR keeping the none key; R418-1 S4's tracking issue (this round may post
only TAKEN / REVIEW READY / STOP on #81); hosted CI, review and hardware. The round-1 REQ-MVU-005 latent
(the MVU fault path's status 10) is fixed by item 2, and the Vivado figures are taken (R419-1 S3).

PR-BODY.md: `[A462]` first line kept; Closes #57, Relates to #81, Relates to #84; round-1 sections kept as
the round-1 record with three corrections (the Vivado sentence, the old "four classes cannot conflict" and
"MVU fault path not acted on" bullets of What remains, both superseded); a "Round 2" section with the six
items and their clauses, the Vivado table, validation, the 16 parent gates and the round-2 parent-visible
list; one current "What remains". No absolute home path, no attribution footer.

Not done by rule: no push, no PR edit, no comment but TAKEN and REVIEW READY on #81.
