# [A660] processor #192 — GET_STREAM_INFO on a Stream Input's started/stopped change

Status: REVIEW READY at head `21855f6c` (resumed after the host resets of 2026-10-20 10:00
and 14:01). Every processor gate and all 13 campaigns are rc 0 at base and head. The
scratch-parent consumer gates are rc 0 at base. At the head they are rc 0 with one parent
adoption patch, and without it one gate fails on rows that pin the defect (see the parent
section). So the PR says "Refs #192", not "Closes".

- Repository: processor (`git remote get-url origin` checked before the first commit and
  again before the resumed session's commit), branch `192-started-notify`
- Base: processor main `24c7f85340437c7c5b9321c1f76e45c955324e2d`
- Head: `21855f6cce6d8771f5b1e84de3d875d7683e23f1`; the branch is not pushed and no PR exists
  (`PR-BODY.md` is the draft)
- Assignment: the [A10] comment 6284522415 on processor issue #192
- TAKEN: comment 6284530521 (posted by the first session; not repeated). REVIEW READY: see
  the last line of this file
- No top-level port, parameter or register-map change, so no STOP

## Resume note

The first session committed `aa5d28f`, `5398ef4` and `6127c6b` and left a clean tree. The
reset cut its base campaigns (d3, notify, acmp), its head campaigns at `5398ef4` (d3,
notify, acmp) and the parent base pass at g15. Its complete records are kept: the base
processor gates (`receipts/base/gates/`), the GSI campaign at `5398ef4`
(`receipts/cut-by-reset-1/head-5398ef4/`, 22 detected) and at `6127c6b`
(`receipts/head-6127c6b/`, 23 detected), the parent base pass g01 to g16 but g15
(`receipts/parent-base/`), the pre-change lint and make check (`receipts/pre/`) and the
development runs (`receipts/dev/`). Every cut run was set
aside and runs again from a fresh output directory. The resumed session found the
generated F06.14 row of START/STOP_STREAMING still naming its class-9 notification
"Table 5.22 started/stopped", fixed it in the registry and regenerated the table
(`42c6a5e`), so every head record is taken at `42c6a5e`.

### Second resume (after the 14:01 reset)

The 14:01 reset left a clean tree at `42c6a5e`. By then these records were complete: the
head processor gates at `42c6a5e`, and the notify campaign at base and at `42c6a5e`. The
parent base pass was also complete except g10 and g17, with g15 rerun from a clean
milan_dp at rc 0. The reset cut base and head d3 and acmp and the parent base g10; those
logs are kept under `receipts/cut-by-reset-2/`. The earlier sessions had run only d3, notify, acmp
and gsi. That falls short of the assignment: all 13 campaigns build or read a changed
file. name_state, maap and adp build pp_top; aecp_cmds reads `aecp_commands.json` and
06; elab_guards mutates the top and the listener. So all 13 run at base and head. A
re-read of 06 §7 against Milan v1.2 found "Table 5.22's 'asynchronously of any command'".
The phrase belongs to §5.4.5.2's last paragraph, which introduces Table 5.22. `21855f6`
cites that paragraph, and §5.4.5.1's "if any" for the requester; it is docs only. The
head campaigns and the parent head pass, minutes old, were restarted at `21855f6`, and
every processor gate runs again there. The head notify campaign stays at `42c6a5e`. The
diff `42c6a5e..21855f6` is one 06 §7 paragraph, which `notify_mutants.py` never copies or
builds; only `tb/aecp_cmds/mutants.py` copies 06, and it runs at `21855f6`. The partial logs
of the runs stopped for these restarts are in `receipts/killed-restarted/`. They are the
head d3 at `42c6a5e` (five minutes in), the parent base g10 (263 s in, restarted whole),
and the base and prescribed-head g17 runs, stopped while still waiting on the Vivado lock.

## Commits

| Commit | Subject |
|---|---|
| `aa5d28f` | GET_STREAM_INFO on every started/stopped change of a Stream Input, a START/STOP_STREAMING's requester included (#192) |
| `5398ef4` | Docs: the START/STOP_STREAMING started/stopped notification in 06 and 00, and the GI step and its GSI controls in tb/pp_top/README (#192) |
| `6127c6b` | tb/pp_top: a GSI control for the defect as reported, a START/STOP_STREAMING's own started change dropped (#192) |
| `42c6a5e` | F06.14: START/STOP_STREAMING's class 9 is its own unsolicited response, requester excluded; the started/stopped GET_STREAM_INFO is a separate event (#192) |
| `21855f6` | Docs: 06 section 7 cites 5.4.5.2's last paragraph for 'asynchronously of any command' and 5.4.5.1's 'if any' for the requester (#192) |

## Changes (head `21855f6`)

| File:line | Change | Clause |
|---|---|---|
| `hdl/top/protocol_processor_top.sv:3573` | `stri_events`: the started/stopped term is `(32'(lstn_act_sink_w) == k && lstn_act_strt_chg_w)`. The `&& !lstn_act_strt_cmd_chg_w` that dropped a START/STOP_STREAMING's own change is gone, so every started/stopped change of a bound input feeds the per-input OR, whatever made it. | Milan v1.2 Table 5.22 ("Started/stopped state (Stream Input only)"), 5.4.5.2 last paragraph; 5.4.2.19, 5.4.2.20 |
| `hdl/top/protocol_processor_top.sv:3552-3567` | The comment says the term covers START/STOP_STREAMING and the re-bind. The notification answers no command, so the requester is not excluded, and the command's own unsolicited response is a separate job. Causes that meet before the input's round is claimed share its one pending bit (`KL_aecp_notify.sv:1319`). | 5.4.5.1; #181 coalescing |
| `hdl/top/protocol_processor_top.sv:2106`, `:2199` (the lines after) | The `lstn_act_strt_cmd_chg_w` net and its connection are removed; the exclusion was their only reader. The started net and its connection stay. | — |
| `hdl/acmp/KL_pp_acmp_listener.sv:208-228` | The `act_strt_cmd_chg_o` output is removed, along with its two resets (old `:875`, `:937`) and its assignment (old `:1457-1459`). The `act_strt_chg_o` port comment no longer says the command's unsolicited response is unsent: the engine's command trigger sends it. It now names the two recipients. A submodule port, not a top-level one; `protocol_processor_top`'s ports, parameters and register map are unchanged. | IEEE 1722.1-2021 7.5.2; Milan 5.4.5.1, 5.4.5.2 |
| `tb/acmp_nvm/acmp_nvm_wrap.sv:521` | The open `.act_strt_cmd_chg_o ()` connection is removed. | — |
| `tb/pp_top/gsi_internal.hpp:399-604`, `:690` | Section GI gets a new last step, `started_notify` (below). | Table 5.22, 5.4.2.19, 5.4.2.20, 5.4.5.1, 5.4.5.2 |
| `tb/pp_top/sim_main.cpp:5393`, `:5499-5546` | Section G: G7f now requires the STOP requester, its only registered controller, to receive the u=1 GET_STREAM_INFO for sink 1. G7g requires nothing else (no unsolicited STOP_STREAMING); before the change it required nothing. | 5.4.5.1, 5.4.5.2 |
| `tb/pp_top/gsi_mutants.py:105-124` | Three variants: `command-started-change-dropped`, `started-trigger-removed`, `coincidence-hold-removed`. | — |
| `hdl/aecp/ucode/aecp_commands.json:257`, `:269`; `docs/architecture/06_aecp_engine.md:271-272` (F06.14, regenerated by `python3 scripts/check_aecp_commands.py --write`) | START/STOP_STREAMING's notify text is now "success with state change, requester excluded; the started/stopped GET_STREAM_INFO is a separate event". It used to read "Table 5.22 started/stopped", which named the command's own class-9 response as the Table 5.22 notification. | IEEE 7.5.2; Milan 5.4.5.2, Table 5.22 |
| `docs/architecture/06_aecp_engine.md:462` (F06.13), `:1202-1209`, `:1219-1230` (section 7 STREAM_INPUT triggers; `21855f6` corrects the clause citations there), `:1369` (START/STOP row) | The started/stopped change by START/STOP_STREAMING is a cause. A state-changing START/STOP gives two notifications, each with its own recipients. A coincident cause coalesces with it. | Table 5.22, 5.4.5.1, 5.4.5.2 |
| `docs/00_MILAN_COMPLIANCE_REVIEW.md:468` (REQ-NOT-003) | The #192 evidence. | Table 5.22 |
| `tb/pp_top/README.md:471-492`, `:553-555` | The GI step and the three GSI table rows. | — |

## New checks and planted mutants

GI's last step (`--gsi-internal-only`, `tb/pp_top/gsi_internal.hpp:590`) runs on a fresh
boot: sink 0 is discovered, bound and settled; A registers, then B (CTLR2, MAC
`02:02:C2:C2:C2:C2`). Each controller's sequence_id is modelled from the wire as the
count of unsolicited frames it was sent before.

- **STOP-BY-A** and **START-BY-A** (`started_step`, `:530`): A's STOP_STREAMING, then its
  START_STREAMING, each gives exactly one GET_STREAM_INFO for sink 0 at A (the requester)
  and exactly one at B. Each is byte-exact at its controller's own sequence_id, with
  STREAMING_WAIT set by the STOP and clear after the START. The command's own unsolicited
  response reaches B once and A never. The step sends 4 frames in all, and the solicited
  read agrees. A premise checks that the command answered SUCCESS and moved the state.
- **STOP-WITH-REGISTRATION** (`started_with_registration`, `:559`): a STOP from A
  coincides with sink 0's first Talker registration (Failed, code 7, bridge `BRIDGE0`).
  Each controller gets exactly one notification, carrying STREAMING_WAIT and the failure.
  The engine takes no command while a notification is pending (`amap_busy_o`,
  `KL_aecp_notify.sv:1206`), so the bench raises the integrator's GET_AVB_INFO change on
  the clock the engine takes the STOP. That round holds the notify block until the STOP
  has answered, so both sink 0 causes pend before the input's round is claimed. Premises
  check that order and the single GET_AVB_INFO at each controller. 6 frames are sent.
- **SN final**: no late or duplicate notification within 100 ms.
- **G7f/G7g** (section G, default build): see the table above.

| Mutant (`tb/pp_top/gsi_mutants.py`) | Planted | Required failing words | Result |
|---|---|---|---|
| `command-started-change-dropped` | the defect as reported: `act_strt_chg_o` gains `&& !src_strq_r` in the listener, so a START/STOP's own change is not driven and the re-bind's still is | `GI STOP-BY-A: exactly one GET_STREAM_INFO for sink 0 at A, the requester` | detected at `21855f6`: `FAIL: GI STOP-BY-A: exactly one GET_STREAM_INFO for sink 0 at A, the requester, got 0` (6 checks fail, below) |
| `started-trigger-removed` | the event not driven: the started term deleted from `stri_events` | `GI STOP-BY-A: exactly one GET_STREAM_INFO for sink 0 at A, the requester` | detected (KILLED) at `21855f6`: `..., the requester, got 0` (9 checks fail) |
| `coincidence-hold-removed` (premise control) | `gsi_avb_chg_i` dropped from the notify block's `ev_avb_i`, so no round holds the block | `GI STOP-WITH-REGISTRATION: exactly one GET_STREAM_INFO for sink 0 at A, the requester` | detected at `21855f6`: `..., the requester, got 2` (3 checks fail) |

The base has no such step. `command-started-change-dropped` puts the base's behaviour back
into the head's RTL: the listener does not drive the started/stopped change of a
START/STOP_STREAMING, and the re-bind's still notifies. The step then fails by name, with
`got 0` at A. `started-trigger-removed` is the assignment's "event not driven" mutant.
`coincidence-hold-removed` checks that the coincidence premise is load-bearing: without
the holding round, the STOP's change is claimed alone and the registration takes a second
round. Development run `dev/gsi1` (`receipts/dev/README.txt`) shows the same: an earlier
coincidence bench without the hold gave two notifications per controller.

## Base and head records

Base `24c7f853` runs in a scratch clone of the lane, detached and clean. Head `21855f6`
runs in two more scratch clones, each cleaned with `git clean -fdX` first: one for the
campaigns, one for the gates. Every gate and campaign is unpiped in the foreground of its
own detached job, with its own log, rc and duration (`receipts/base/`, `receipts/head/`).
The tools are Verilator 5.050 (pinned) first on PATH, then sv2v 0.0.12 and Yosys 0.33,
the CI pins; Yosys 0.66 from the host gives the second synthesis record. A wrapper lets at
most two Verilator builds run at once across every stream. The host was shared (load
average 20 to 60), so durations are long and vary.

Memory: this unit's MemoryCurrent was sampled every 15 s (`receipts/host-memory/memlog.txt`). A
guard reclaimed page cache through the cgroup's `memory.reclaim` (`receipts/host-memory/memguard.log`).
It started at 8 GB, sampling every 10 s. MemoryCurrent exceeded 9 GB once, as the parent
builder tests (g10) ended: 9.14 GB in the 15 s sample at 17:33:27, and 9.44 GB in the
guard's reading at 17:33:32, with process memory 6.1 GB and the rest page cache. That
reclaim brought it to 8.34 GB, and the next to 4.61 GB at 17:33:52. The guard was then
restarted (17:39) to reclaim past 7 GB every 3 s. The peak after that was 6.99 GB.

### Processor gates

| Gate | Base 24c7f853 | Head 21855f6 | Comparison |
|---|---|---|---|
| scripts/run_suites.sh | rc 0, 1,030,205 checks, 0 failing (2,213 s) | rc 0, 1,030,277 checks, 0 failing (2,070 s) | two lines differ: pp_top 10,634 → 10,706 (+72: the GI step and G7f/G7g), and the total |
| executed REQ-tag check (`scripts/check-req-tags.py`) | rc 0, 233 evidence lines | rc 0, 233 | log identical; the evidence identical but for 69 `sim_main.cpp` line numbers (+5) |
| scripts/lint_hdl.sh | rc 0 | rc 0 | identical |
| make check | rc 0 | rc 0 | identical |
| scripts/gen_matrix.py --check | rc 0 | rc 0 | identical |
| syn/yosys/run.sh, Yosys 0.33 (CI pin) | rc 0 | rc 0 | eight memory warnings' all.v line numbers (−5, the listener's removed lines) |
| syn/yosys/run.sh, host Yosys 0.66 | rc 0 | rc 0 | the same eight lines |
| tb/elab_guards/guards.py --frontend yosys | rc 0 | rc 0 | identical with source and all.v line numbers masked |

The same gates at `42c6a5e` (`receipts/head-42c6a5e/gates/`) are all rc 0, and every log
is identical to the `21855f6` log once tree paths are masked; so is the REQ-tag evidence.
`git status --short` is empty in each tree before its gates. After them it lists only
ignored build products, the same set at base and at head.

### Campaigns

All 13 campaigns build or read a changed file, so all 13 ran at base and at head. Each
ran from a fresh output directory outside the trees, with TMPDIR in scratch. Unless noted,
each ran with `--jobs 2`. The notify runs come from the first resumed session, which did
not record their `--jobs`; `tb/common/mutant_pool.py` gives the same summary at any N.
Comparison: the verdict log (`<name>.log`), byte for byte or sorted where a driver prints
in completion order, and every per-unit log's sorted FAIL lines (`receipts/scripts/failsets.py`;
the results are in `receipts/compare/campaigns/`).

| Campaign | Base 24c7f853 | Head 21855f6 | Comparison |
|---|---|---|---|
| `python3 tb/pp_top/d3_mutants.py` | rc 0, 110 of 110 KILLED, goldens PASS (6,876 s) | rc 0, the same (6,798 s) | verdict log identical (sorted); all 116 unit logs carry the same FAIL lines |
| `python3 tb/pp_top/notify_mutants.py` | rc 0, 135 of 135 KILLED, goldens PASS (5,260 s) | at `42c6a5e`: rc 0, the same (5,831 s) | 149 of 150 unit logs identical in FAIL lines. `entry_seq_not_advanced` fails the same 13 checks, but its NP6, NP7 and NP8 messages name sequence_ids one or two higher (8 → 9, 9 → 11, 2 → 4): each controller was also sent the started/stopped GET_STREAM_INFO frames before them. The README row (13, NP1b first) holds |
| `python3 tb/pp_top/acmp_mutants.py` | rc 0, 54 of 54 KILLED, goldens PASS (2,395 s) | rc 0, the same (2,610 s) | verdict log identical (sorted). Two unit logs move: `armq_ring_of_three` fails G7g instead of G7f, whose check the change rewords (12 failing checks at both, as its README row says), and `gsi_vlan_external` also fails GI SN-BIND's two byte-exact rows (50 → 52) |
| `python3 tb/pp_top/aecp_dispatch_mutants.py` | rc 0, 73 checks PASS (2,198 s) | rc 0, the same (2,000 s) | verdict log byte-identical; all 73 unit logs carry the same FAIL lines |
| `python3 tb/pp_top/gsi_mutants.py` | rc 0, 20 detected, golden and restored PASS (1,108 s) | rc 0, 23 detected, golden and restored PASS (1,206 s) | the three #192 variants added, each detected by its named check (below); the 20 base variants detected by the same named checks. Six of them also fail rows of the new step (`failure-bridge-zero` +4, `failure-code-zero` +4, `integrator-path` +15, `pbsta-zero` +20, `status-notification-zero` +26, `wrong-sink` +22), and no base FAIL line is lost. Verdict log identical to `6127c6b`'s |
| `python3 tb/pp_top/aecp_mutants.py` | rc 0, 67 checks PASS (1,553 s) | rc 0, the same (1,744 s) | verdict log byte-identical; all unit logs carry the same FAIL lines |
| `python3 tb/pp_top/ctr_mutants.py` | rc 0, 18 checks PASS (502 s) | rc 0, the same (505 s) | verdict log byte-identical |
| `python3 tb/pp_top/name_wr_mutant.py` | rc 0, decode killed, golden and restored PASS (122 s) | rc 0, the same (83 s) | verdict log byte-identical |
| `python3 tb/name_state/mutants.py` | rc 0, 16 KILLED (463 s) | rc 0, the same (381 s) | verdict log identical sorted (completion order); all 38 unit logs carry the same FAIL lines |
| `python3 tb/maap/mutants.py` | rc 0, 32 checks PASS (373 s) | rc 0, the same (403 s) | verdict log byte-identical |
| `python3 tb/adp_engine/mutants.py` | rc 0, 62 checks PASS (561 s) | rc 0, the same (529 s) | verdict log byte-identical; all 62 unit logs carry the same FAIL lines |
| `python3 -B tb/aecp_cmds/mutants.py` | rc 0, 17 of 17 detected, golden and restored PASS (743 s) | rc 0, the same (657 s) | verdict log byte-identical; all 57 unit logs carry the same FAIL lines |
| `python3 -B tb/elab_guards/mutants.py` | rc 0, 160 of 160 killed (1,338 s) | rc 0, the same (1,320 s) | verdict log identical with source and all.v line numbers masked; all 161 unit logs carry the same FAIL lines with line numbers masked |

The three #192 GSI variants at head, with every check each fails:

- `command-started-change-dropped` (6): STOP-BY-A and START-BY-A each fail "exactly one
  GET_STREAM_INFO for sink 0 at A, the requester, got 0", "... at B, got 0" and "nothing
  else is sent, got 2 frames". REBIND-SW and STOP-WITH-REGISTRATION pass, because the
  re-bind and the registration still notify. That is the defect as reported.
- `started-trigger-removed` (9): the same six, plus REBIND-SW's three, because the re-bind
  uses the same term.
- `coincidence-hold-removed` (3): STOP-WITH-REGISTRATION's GET_AVB_INFO premise, and
  "exactly one GET_STREAM_INFO for sink 0 at A, the requester, got 2" and "... at B, got 2".

## Scratch-parent consumer gates

Scratch parent: a local clone of milan-fpga dev `e26f1816e456dc8027924bc2e5d327a8aa6e46db`,
local branches only, never pushed. Each patch commit's `git patch-id --stable` equals its
patch file's.

| Parent commit | Subject | Patch sha256 (bytes) |
|---|---|---|
| `af16b7fc` | Scratch: parent-evidence-classification.patch (#180) | `7662517046007f77b0e3763814226a50af87e06d01261586bcaf32cd4a75495e` (2,689) |
| `0f5648a7` | Scratch: parent-adoption-milan_dp-67.patch (#176) | `e142e2e7d7aec88fdc0bb7b6443d296f671f06391712b214339a50b84acc66d3` (1,541) |
| `13bf00e1` | Scratch: parent-scratch-tspec-every-slot.patch (#190) | `37d1b76ec95e1b0d7de12ace14d8ade032bf8bb96a70eb5df21d11c1363234a8` (760) |
| `625c0e5c` | Scratch: protocol-processor at 24c7f853 (base pass) | — |
| `9d1dcf14` (on `13bf00e1`) | Scratch: protocol-processor at 21855f6c (head pass) | — |
| `57465d43` (on `13bf00e1`) | Scratch: parent-adoption-milan_dp-gsi-g9.patch (processor #192) | `5ed1656c0733ed64a890000ddc2d73c9435a0373a991ab0436c04c6e2009c9ab` (3,343) |
| `be4cd421` (on `57465d43`) | Scratch: protocol-processor at 21855f6c (head pass with the #192 milan_dp adoption) | — |

**Finding: the parent's milan_dp pins the old behaviour.** On the prescribed stack at the
head (`9d1dcf14`), `make -C tb/verilator/milan_dp` fails with rc 2. Its notify leg
(`sim_nxn.cpp` section GSI, G9) fails two rows:
`[FAIL] [GSI] G9 sink 1 stopped (no GET_STREAM_INFO push): unsolicited GET_STREAM_INFO(sink 1) to A got=0x1 exp=0x0`,
and the same row for B. The pool then does not start the later legs. G9 sends STOP_STREAMING
for sink 1 from A, and it requires that nobody gets GET_STREAM_INFO. That is the defect
#192 removes: Milan v1.2 Table 5.22 and §5.4.5.1 send one to A and to B. The two
STOP_STREAMING rows of G9 still pass (B gets it, A does not), as do the STREAMING_WAIT and
state rows. The parent change belongs to the pin adoption, as `parent-adoption-milan_dp-67.patch`
did for #176: `parent-adoption-milan_dp-gsi-g9.patch` (this directory) makes G9 require
exactly one GET_STREAM_INFO for sink 1 at each controller, equal to the solicited answer
from the body on, and updates the G9 comment and the README row. The pass with it is
`be4cd421`. Its C++ idiom counts are unchanged.

Each pass ran the 17 gates of the #196 bank in the scratch parent, unpiped, each with its
own log, rc and duration. Before each pass, the parent's `tb/verilator` and the
submodule's ignored products were cleaned (`git clean -fdX`). The base pass is the first
session's, and the resumed sessions completed it; see the resume notes. g17 runs under
the host-wide Vivado lock. Another lane held that lock for about an hour, so g17 ran last
in every pass. The prescribed head pass stopped at g17, when the change to the adopted
pass was made, and its g17 ran after the adopted pass. `receipts/parent-chain/chain.txt`
holds the commit chain, the gitlinks and the patch-ids. Every patch commit's
`git patch-id --stable` equals its file's.

| # | Gate | Base `625c0e5c` (24c7f853) | Head `9d1dcf14` (21855f6, prescribed stack) | Head `be4cd421` (21855f6, with the adoption) |
|---|---|---|---|---|
| g01 | `python3 scripts/check_cpp_idiom.py` | rc 0 | rc 0, identical | rc 0, identical |
| g02 | `python3 scripts/check_py_idiom.py` | rc 0 | rc 0; 259,221 → 259,241 lines (`gsi_mutants.py` +20) | rc 0, the same |
| g03 | `python3 scripts/check_rtl_source_lists.py` | rc 0 | rc 0, identical | rc 0, identical |
| g04 | `python3 scripts/pp_srcs.py --check --selftest` | rc 0 | rc 0, identical | rc 0, identical |
| g05 | `python3 scripts/check_port_contracts.py` | rc 0 | rc 0; protocol-processor ports 1,765 → 1,764 (`act_strt_cmd_chg_o` removed), undocumented 111 ≤ 111 | rc 0, the same |
| g06 | `python3 scripts/measure_naming.py --check` | rc 0 | rc 0; the same port, one fewer in each column it was counted in | rc 0, the same |
| g07 | `python3 scripts/measure_test_evidence.py --check` | rc 0 | rc 0, identical | rc 0, identical |
| g08 | `python3 scripts/docs_check.py` | rc 0 | rc 0, identical | rc 0, identical |
| g09 | `python3 scripts/check_sh_idiom.py` | rc 0 | rc 0, identical | rc 0, identical |
| g10 | `python3 sw/builder/test_builder.py` | rc 0 | rc 0; only temp-dir names, seeds and the first-finding text of a seeded restage self-test differ, every self-test OK | rc 0, the same kind of lines |
| g11 | `python3 scripts/lint_rtl.py --check` | rc 0 | rc 0; one finding's message text differs (below) | rc 0, the same |
| g12 | `make -j8 -O -C tb/verilator/pp_shadow` | rc 0, 2,184 PASS | rc 0, the 2,184 PASS lines identical | rc 0, identical |
| g13 | `make -j8 -O -C tb/verilator/nvm_cosim lint` | rc 0 | rc 0, identical | rc 0, identical |
| g14 | `make -j8 -O -C tb/verilator/nvm_cosim quick JOBS=4 POOL=2` | rc 0 | rc 0, identical | rc 0, identical |
| g15 | `make -j8 -O -C tb/verilator/milan_dp SIM_JOBS=2` | rc 0, 13 legs PASS | **rc 2**: the notify leg fails G9's two GET_STREAM_INFO rows (above), and the pool starts no later leg | rc 0, 13 legs PASS; the notify leg 423 → 424 checks (G9's push-equals-solicited row, which runs only when a push is expected); every other leg's tally identical |
| g16 | `make -j8 -O -C tb/verilator/milan_dp_render` | rc 0 | rc 0; only build-report lines differ | rc 0, the same |
| g17 | `python3 scripts/xvlog_gate.py --check` (under the host's Vivado lock) | rc 0 | rc 0; the pin line names 21855f6c | rc 0, the same |

The g11 difference is `KL_i2s_playback.sv:317-318`, a parent file this change does not
touch. Its WIDTHEXPAND says `ms_div_r` "generates 17 bits" at base and "16 bits" at head.
`lint_rtl.py` elaborates its tops in a thread pool and dedupes on (file, line, col, code),
so the message text kept is that of the first elaboration to finish (`as_completed`); the
finding, its key and the counts are the same. Apart from those two lines, the log is
identical.

Without the adoption, the prescribed head fails one consumer gate, g15, on rows that pin
the defect. With it, all 17 gates are rc 0 at the head. Issue #192's last acceptance item,
"the parent's consumer gates pass", therefore needs the adoption at the pin bump, as #176's
did, and the PR says "Refs #192".

## Lane state

`git status --short --ignored` in the lane is empty at `21855f6`. Its five commits have
one-line subjects with no body or trailer. The branch has no upstream. The scratch
clones, the scratch parent and the worktree for the adoption patch live outside the lane
and are never pushed.

## Receipts

See `receipts/INDEX.md` and its per-directory files under `receipts/index/`, generated
by `receipts/scripts/index.py` from the files present. `receipts/stopped-6127c6b/` holds
the gates and campaigns the first resumed session stopped at `6127c6b` once it found
the F06.14 text; they were superseded and are not cited. Each oversized log is listed in
`receipts/OVER-200KB.sha256` with its sha256 and size; its verdict lines are kept beside it
as `<log>.excerpt.txt`. Campaign units' source-tree copies and build directories are not
copied. `receipts/scripts/` holds the helper scripts that ran every gate. Host paths are
masked in every receipt.

REVIEW READY: comment 6297035325 on processor issue #192 (2026-10-20 17:30:48 UTC), "[A660] REVIEW READY 21855f6cce6d8771f5b1e84de3d875d7683e23f1".
