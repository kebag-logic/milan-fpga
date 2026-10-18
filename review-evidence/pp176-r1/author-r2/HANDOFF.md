# [A629] #176 SET_STREAM_INFO accepts the IEEE 1722.1-2013 body — HANDOFF

## Round 2

Status: DONE. Head bee33ff2: every processor gate and every campaign that builds a changed file is
rc 0 at the merged base and at head, with identical records apart from the 5 new pp_top checks. Every
new check fails under a planted mutant. The parent consumer gates are as round 1 left them: 22 of 23
pass at both with the two scratch patches, and the patch controls below show which rows each patch is
for. So the PR body keeps "Refs #176". REVIEW READY posted on issue #176 (comment 6248817225) with the head (see "Final
state").

- Resume after the 05:03 host crash: the head commit bee33ff2 and the mutant arms were complete. The
  records the crash cut (head `run_suites`; base acmp, adp_engine and elab_guards campaigns) were
  renamed `*.crashed.log` and rerun; the records never started were run. Build outputs in the lane,
  the submodule and the parent's milan_dp, milan_dp_render, nvm_cosim and pp_shadow benches were
  removed (`git clean -fdX`) before the reruns.
- Resume after the 10:57 host crash: the lane was clean at bee33ff2 (nothing uncommitted), every
  processor gate and campaign record was complete, and no zero-byte file was left in the lane or the
  parent. The head consumer run had stopped inside pp_shadow, whose `.rc` was never written. That
  log is kept as `r2/cons/head/pp_shadow.crashed.log`. The parent's pp_shadow, nvm_cosim and
  milan_dp_render build outputs were removed, and pp_shadow, nvm_cosim lint and quick,
  milan_dp_render and milan_dp ran at head. Then the patch controls ran.

- Assignment: PR #183 comment 6244127636. Ruling: issue #176 comment 6243713960. Reviews: R645-1
  (6243715823) and R644-1 (6244122972), both NEGATIVE at 29f58ad3.
- Step 0: `git fetch origin`, then one merge commit of processor main f0b1b9d8 (contains PR #180):
  `e59804d8` "Merge processor main f0b1b9d8 into 176-ssi-2013-body". The textual merge was clean.
- Merged base: e59804d8. Head: `bee33ff2ed353b1a9b0ec16197249af7cbfb6b09`, one commit on the merge,
  "SET_STREAM_INFO: refuse every length but cdl 60 and 96, and pin the 2021 ip-block echo (#176)".
  Not pushed.
- Scratch parent: kebag-logic/milan-fpga dev `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f` (dev's tip when
  fetched), the round-1 clone moved there, with two patches applied in its working tree only:
  - `pp178-a634/parent-evidence-classification.patch` (sha256 76625170…495e, 2,689 B);
  - `pp176-a629/parent-adoption-milan_dp-67.patch` (sha256 e142e2e7…66d3, 1,541 B), unchanged: the new
    contract changes neither parent #67 row (see "Parent rows").
- Scratch root for round 2: $VALIDATION_STORAGE/pp176-a629/r2 (records rec/, camp/, cons/, mutants/, probe/).

### Length probe (R645-1 verification)

A scratch-only insertion at the top of W24 (`bin/probe_insert.py`) sends, on Stream Output 0, a valid
MSRP_ACC_LAT_VALID body at each length with latency 600000 + cdl, prints the answer and the offset row,
then exits. The rows run in order, so the offset is the last applied latency. Script and outputs:
`probe/` (probe_insert.py, base-e59804d8.txt, head-bee33ff2.txt; both runs rc 0).

| cdl | merged base e59804d8: status / response cdl / offset row | head: status / response cdl / offset row |
|---|---|---|
| 59 | BAD_ARGUMENTS (7) / 96 / 0 (row unset) | BAD_ARGUMENTS / 96 / 0 (row unset) |
| 60 | SUCCESS (0) / 96 / 600060 | SUCCESS / 96 / 600060 |
| 61 | BAD_ARGUMENTS / 96 / 600060 (kept) | BAD_ARGUMENTS / 96 / 600060 (kept) |
| 95 | BAD_ARGUMENTS / 96 / 600060 (kept) | BAD_ARGUMENTS / 96 / 600060 (kept) |
| 96 | SUCCESS / 96 / 600096 | SUCCESS / 96 / 600096 |
| 97 | **SUCCESS / 97 / 600097** | BAD_ARGUMENTS / 96 / 600096 (kept) |
| 100 | **SUCCESS / 100 / 600100** | BAD_ARGUMENTS / 96 / 600096 (kept) |
| 140 | **SUCCESS / 140 / 600140** | BAD_ARGUMENTS / 96 / 600096 (kept) |

### Round-2 changes (file:line at bee33ff2)

R645-1-F1 (the contract: exactly cdl 60 and 96):

- `hdl/aecp/KL_aecp_engine.sv`
  - :803-812: the comment names the only two bodies, and `SI21_CDL_C` (96) joins the localparams.
  - :1567-1571: `si21_w`, a SET_STREAM_INFO of exactly cdl 96, walked whole (84 bytes), beside `si13_w`.
  - :3593-3603: the dispatch-arm comment: exactly two lengths, any other shorter or longer is refused.
  - :3616-3620: the wrong-length route to E_SIBAD is now `!si13_w && !si21_w` (was: not `si13_w` and
    `cdl < 96 || walked < 84`, which let every longer body through to the setter).
  - The A_RUN length (:3765-3767) is unchanged: an accepted echo is now always 84 bytes.
- `hdl/aecp/ucode/gen_ucode.py:2348-2355`: E_SIBAD's comment covers shorter and longer commands.
  Comment-only; the generated ROM equals main's (`a3b62cab…bcb3`, the digest decode.json records).
- `hdl/aecp/ucode/aecp_commands.json:148`: Scope says "accepts exactly the 2021 body (cdl 96) and the
  2013 48-byte body (cdl 60)"; F06.14 regenerated (`docs/architecture/06_aecp_engine.md:261`).
- `docs/architecture/06_aecp_engine.md:493` (§6.3: "exactly two shapes"; any other length, shorter or
  longer, refused BAD_ARGUMENTS at the 2021 length, writes nothing) and `:1245` (§8.1).
- `docs/architecture/09_verification.md:184` (§8.1 adds W24n/W24n1, W24o/W24o1) and `:612-614` (§8.11:
  the sweep holds the refusal between and above, to cdl 100; W24n/W24o grade 97 and 140).
- `tb/aecp_cmds/sim_main.cpp:311-313`: the valid MSRP_ACC_LAT_VALID templates (with and without
  bit 31) run at cdl 60, 96, 97 and 100. 100 keeps the sweep inside its documented 12-100 range.
  `tb/aecp_cmds/decode.json` re-recorded (`make -C tb/aecp_cmds record`), and `README.md:32-36, 84-88`.
- `tb/pp_top/sim_main.cpp:8286-8320`: `w24n_bodies_longer_than_the_2021_body()`, W24n/W24n1 (cdl 97) and
  W24o/W24o1 (cdl 140), called from W24 at :8201.

R644-1-F1 (the 2021 ip-block echo):

- `tb/pp_top/sim_main.cpp:8149-8160`: W24a3, a 2021 SUCCESS whose ip block @70..@107 carries a non-zero
  pattern, graded byte-exact against the command. It sends the offset already stored, so the
  rows after it are unchanged.

Residue:

- R644-1-R1: `09_verification.md:184` "W24h, W24j-W24m" became "W24h-W24m" (the new W24n/W24o
  refusals are a separate clause after it).
- R645-1-F2, its exact correction: `issue #176, REQ-AEM-009` at every new behavioural comment anchor
  (engine :803, :1563, :1568, :2582, :3599, :3766; gen_ucode.py :2330, :2349; pp_top :8096, :8151,
  :8216, :8220, :8291, :8366; aecp_cmds sim_main.cpp :312); "(W24g-W24l, issue #176)" became "(issue #176, REQ-AEM-009)" and
  "(W24m)" was dropped (:8094-8097); the W24g-W24m banner and its "Run from W24..." navigation became
  "Exercise the legacy body and an unsupported short body; preserve the stored offset across the
  refusal checks (issue #176, REQ-AEM-009)." (:8215-8216); the W24g/W24g2/W24i-W24l/W24m/W25b3
  comment prefixes were removed (:8197, :8220, :8238, :8245, :8266, :8365); "back to W24a's value"
  became "back to the initial offset" (:8238). Function names, assertion strings and the findings
  tables are unchanged. The new comments follow the same rule.
- `tb/pp_top/README.md:1040-1041` (M45, M46) and `:1063-1068` (when M38-M46 were measured).

### Accepted lengths and refusal cases (round 2)

| SET_STREAM_INFO command | Result |
|---|---|
| cdl 60, all 48 bytes walked (2013 body) | accepted: the routes below, answered in the 2021 form (cdl 96, @70..@107 zero) |
| cdl 96, all 84 bytes walked (2021 body) | accepted: the routes below, byte-exact echo (cdl 96) |
| any other cdl, shorter or longer (12-59, 61-95, 97 and above), or a slot shorter than its cdl | BAD_ARGUMENTS at cdl 96, {type, index} over a zero body, no offset write (E_SIBAD) |

Routes of both accepted bodies, in order: Stream Input → NOT_SUPPORTED; streaming output →
STREAM_IS_RUNNING; flags not exactly MSRP_ACC_LAT_VALID → NOT_SUPPORTED; latency bit 31 →
BAD_ARGUMENTS; foreign lock → ENTITY_LOCKED; locate miss → NO_SUCH_DESCRIPTOR; otherwise SUCCESS, the
offset written. Nothing is applied on any refusal.

The record (`tb/aecp_cmds/decode.json`, AEM 0x000E): SINFO, SIRUN, BADARG and NSUPPE at cdls "60, 96",
each answering cdl 96; SIBAD at "12-59, 61-95, 97-100", answering cdl 96.

### New checks and planted mutants (round 2)

New `tb/pp_top` checks, default build, section W (10,004 checks at head):

| Check | What it holds |
|---|---|
| W24a3 | a 2021 body with a non-zero ip block (@70..@107) is SUCCESS and echoed byte-exact |
| W24n / W24n1 | a valid MSRP_ACC_LAT_VALID body at cdl 97 (85 bytes, non-zero tail) is BAD_ARGUMENTS at cdl 96, {type,index} over a zero body, byte-exact; its latency 640000 is not applied |
| W24o / W24o1 | the same at cdl 140 (128 bytes) |

Arms: `mutants/round2/patches/*.patch` against the head engine, generated by exact text edits. Each arm ran
in its own extract (default build through every section, then the tb/aecp_cmds suite with `docs/`).
Full lists: `mutants/round2/RESULTS.txt`; log hashes `mutants/round2/LOGS.sha256` (logs in the scratch
root). The extracts were taken from the working tree that was then committed unchanged as bee33ff2
(the record's input digests and the head's files agree).

| Arm | Edit | Default build (of 10,004) | Failing words | tb/aecp_cmds |
|---|---|---|---|---|
| control | none | 0 failures | none | rc 0, 176/176 |
| sinfo-upper-bound-reopened (M45) | `si21_w` compares `>=` (the old open upper bound) | 7 | `W24n: a SET_STREAM_INFO one byte longer than the 2021 body (cdl 97) refuses BAD_ARGUMENTS at cdl 96, {type,index} over a zero body, byte-exact`, `W24n1: ...and its latency was NOT applied`, `W24o: a SET_STREAM_INFO 44 bytes longer than the 2021 body (cdl 140) refuses ...`, `W24o1: ...`, + W24h2, W25b2, W25b3 | rc 2: AEM 0x000E SINFO/BADARG observed "60, 96-97, 100", NSUPPE "60, 96-100", SIBAD "12-59, 61-95" |
| sinfo13-pad-every-sinfo (M46) | `si13_pad_w = ssinfo_r && ...` | 1 | `W24a3: a 2021 SET_STREAM_INFO with a non-zero ip block is echoed byte-exact` | rc 2 on the engine digest only (the sweep does not grade bytes) |
| sinfo13-refused (M38) | `!si13_w` → `1'b1` | 8 | W24g, W24g1, W24g2, W24i-W24l, W25b3 | rc 2: SINFO floor 96 |
| sinfo13-echo-length (M39) | `pld_r <= pld_cmd_r` | 7 | W24g, W24g2, W24i-W24l, W25b3 | rc 2: "echo" answers |
| sinfo13-tail-echoed (M40) | `si13_pad_w` tied 0 | 6 | W24g, W24i-W24l, W25b3 | digest only |
| sinfo13-reserved-echoed (M41) | `SI13_ECHO_C` 48 | 6 | W24g, W24i-W24l, W25b3 | digest only |
| sinfo13-any-shorter-body (M42) | `si13_w` compares `>=` | 11 | W24a3, W24m, W24m1, W24m2, W24n, W24n1, W24o, W24o1, + W24h2, W25b2, W25b3 | rc 2: 0x000E lengths |
| sinfo13-latency-uncaptured (M43) | `silat_r` arms gated `!si13_w` | 10 | W24g1, W24g2, W24k, W24l2, W24m1, W24n1, W24o1, + W24h2, W25b2, W25b3 | rc 2: BADARG floor 96 |
| sinfo-flag-gate-open (M44) | flag compare → `1'b0` | 11 | W24d, W24e, W24f, W24j, W24l2, W24m1, W24n1, W24o1, + W24h2, W25b2, W25b3 | digest only |

Every new check fails by name under at least one arm: W24a3 (M46, M42), W24n/W24n1/W24o/W24o1 (M45, M42).
Every round-1 check still fails under its round-1 arms.

### Base and head records (round 2)

Base is the merged base `e59804d8`, head `bee33ff2`. Base ran from the scratch parent's submodule
checked out at e59804d8; head ran from the lane. Pinned Verilator 5.050 and sv2v 0.0.12. Records are in
`r2/{rec,camp,cons}/{base,head}` under the scratch root. Each `.rc` is written by the wrapper from the
command's own exit status, never through a pipe. "Identical" means: both processor roots mapped to one
name, host paths, times and digests normalized, `KL_aecp_engine.sv:N`, `all.v:N` and `sim_main.cpp:N`
line numbers normalized (the added lines shift them), lines sorted (parallel completion order). The
per-record diffs are `r2/camp/*.cmp.diff` (all empty).

Processor gates:

| Gate | Base e59804d8 | Head bee33ff2 | Identical? |
|---|---|---|---|
| `scripts/run_suites.sh` | rc 0, 1,029,982 checks, 0 failing | rc 0, 1,029,987 checks, 0 failing | only `pp_top` differs: 10,501 → 10,506 (W24a3, W24n, W24n1, W24o, W24o1). Every other suite line, `aecp_cmds` included, is identical |
| `scripts/lint_hdl.sh` | rc 0, 41 LINT OK | rc 0, 41 | yes |
| `make check` | rc 0 (aecp commands selftest: 231 planted defects, 231 caught; matrix 94 rows) | rc 0 | yes |
| `scripts/gen_matrix.py --check` | rc 0, 94 rows, 0 untested | rc 0 | yes |
| `syn/yosys/run.sh` (host Yosys 0.66) | rc 0, 42 tops + Xilinx KL_aecp_engine OK | rc 0 | yes, after line normalization |
| `syn/yosys/run.sh` under Yosys 0.33 (CI's distribution version, container `c10-yosys033`, tree mounted read-only) | rc 0 | rc 0 | yes, after line normalization |

The head `run_suites` record is the rerun after the crash; the cut one is `run_suites.crashed.log`.

Campaigns that build a changed file (`KL_aecp_engine.sv`, `tb/pp_top/sim_main.cpp`,
`tb/aecp_cmds/sim_main.cpp`, the ROM inputs `gen_ucode.py` and `aecp_commands.json`):

| Campaign | Base | Head | Identical? |
|---|---|---|---|
| `make -C tb/aecp_cmds mutants` | rc 0, 16 of 16 controls detected | rc 0, 16 of 16 | yes |
| `make -C tb/pp_top aecp-dispatch-mutants` | rc 0, all killed, 49/49 restored | rc 0 | yes |
| `make -C tb/pp_top aecp-mutants` | rc 0, all killed, 67/67 restored | rc 0 | yes |
| `make -C tb/pp_top ctr-mutants` | rc 0, all killed, 18/18 restored | rc 0 | yes |
| `tb/pp_top/gsi_mutants.py --jobs 4` | rc 0, 20 detected | rc 0, 20 | yes |
| `tb/pp_top/name_wr_mutant.py` | rc 0, killed | rc 0, killed | yes |
| `tb/pp_top/acmp_mutants.py --jobs 4` | rc 0, 51 of 51 KILLED | rc 0, 51 of 51 | yes |
| `tb/pp_top/notify_mutants.py --jobs 4` | rc 0, 98 of 98 KILLED | rc 0, 98 of 98 | yes |
| `tb/pp_top/d3_mutants.py --jobs 3 --only <chunk>` ×4 (round-1 chunks) | rc 0 ×4: 27+28+27+28 = 110 of 110 KILLED, goldens PASS | rc 0 ×4, 110 of 110 | yes, chunk by chunk |
| `make -C tb/adp_engine mutants` | rc 0, 62/62 restored | rc 0 | yes |
| `make -C tb/maap mutants` | rc 0, 32/32 restored | rc 0 | yes |
| `make -C tb/elab_guards mutants` | rc 0, 160 of 160 killed | rc 0, 160 of 160 | yes |
| `make -C tb/name_state mutants` | rc 0, all KILLED | rc 0 | yes |

Not run, as in round 1, because they build none of the changed files: srp_top, srp_admission and
acmp_talker retry_mutants.

### Scratch-parent consumer gate table (round 2)

Setup:

- Parent: kebag-logic/milan-fpga dev `e9cbb676`. Its own processor pin is 2cbed0a9, an ancestor of
  the merged base. The protocol-processor gitlink was staged at each revision with the submodule
  checked out there. `r2/cons/{base,head}/STATE.txt` records the parent HEAD, the staged gitlink, the
  submodule status and the sha256 of the parent's working-tree diff (`ef322a60…`, both patches; the
  same at base and head).
- Both patches applied in the working tree only:
  - classification = `pp178-a634/parent-evidence-classification.patch`;
  - #67 = `pp176-a629/parent-adoption-milan_dp-67.patch`.
- Gate set: round 1's 22 gates, plus `check_baremetal_only.py --check` (dev e9cbb676 runs it in CI).
- Resume note: the head `pp_shadow` record was cut by the 10:57 crash before its `.rc` was written
  (`pp_shadow.crashed.log`). The parent's pp_shadow, nvm_cosim and milan_dp_render build outputs
  were removed (`git clean -fdX`), and pp_shadow and the gates after it were rerun.

| Parent consumer command | Base e59804d8 | Head bee33ff2 | Base vs head |
|---|---|---|---|
| `python3 scripts/check_cpp_idiom.py` | 0 | 0 | identical (`long function: 0 <= 0`) |
| `python3 scripts/check_py_idiom.py` | 0 | 0 | only the line total: 258,771 → 258,772 (gen_ucode.py nets +1 comment line) |
| `python3 scripts/check_rtl_source_lists.py` | 0 | 0 | identical |
| `python3 scripts/pp_srcs.py --check --selftest` | 0 | 0 | identical |
| `python3 scripts/check_port_contracts.py` | 0 | 0 | identical |
| `python3 scripts/measure_naming.py --check` | 0 | 0 | identical |
| `python3 scripts/measure_test_evidence.py --check` | 0 | 0 | identical (`0 <= 0 unexplained DUT-source reader(s)`) |
| `python3 scripts/docs_check.py` | 0 | 0 | identical |
| `python3 scripts/check_sh_idiom.py` | 0 | 0 | identical |
| `python3 scripts/check_hygiene.py --check` | 0 | 0 | identical |
| `python3 scripts/check_sv_idiom.py` | 0 | 0 | identical |
| `python3 scripts/check_submodule_docs.py` | 1 | 1 | identical: `protocol-processor: documented pin differs from Git` and the pin diagram is stale. Fails for any gitlink other than the documented one (see the controls below); the adoption records the pin |
| `python3 scripts/check_baremetal_only.py --check` | 0 | 0 | identical |
| `python3 sw/builder/test_builder.py` | 0 | 0 | `ALL GATES PASS EXCEPT 1 NOT RUN` at both (gate 11 needs a build tree that is not on this host). The same 70 NVM self-test arms are `OK` at both. Their "caught by N named finding(s)" counts vary from run to run, because the threaded walk stops at the first finding (`sw/firmware/nvm_hosttest/test_nvm_firmware.py:790-809`); they also differ between round 1's base and head. Other differences: temp dirs and timings |
| `python3 scripts/lint_rtl.py --check` | 0 | 0 | identical: 90 violations ≤ ratchet 90 |
| `cd tests && behave --no-capture -f plain` | 0 | 0 | identical: 1977 steps passed |
| `flock $VIVADO_LOCK python3 scripts/xvlog_gate.py --check` | 0 | 0 | identical except the line naming the processor pin; 0 findings |
| `make -j16 -C tb/verilator/pp_shadow` | 0 | 0 | 2,184 checks (609 + 609 + 649 + 317, four binaries), 0 failures at both. The four binaries build and run in parallel, so lines interleave; the per-binary totals are identical |
| `make -j16 -C tb/verilator/nvm_cosim lint` | 0 | 0 | identical except Verilator's timings |
| `make -j16 -C tb/verilator/nvm_cosim quick JOBS=4 POOL=2` | 0 | 0 | identical |
| `make -j16 -C tb/verilator/milan_dp_render` | 0 | 0 | check lines identical; only Verilator's source size (+11 KB, the engine) and timings move |
| `make -j16 -C tb/verilator/milan_dp SIM_JOBS=2` | 0 | 0 | every check line identical (10,465 `[ok]`, 1,127 `[PASS]`, 0 failures; per-leg 182, 182, 236, 236, 233, 193, 6). Only Verilator's source sizes and timings, and the render phases' timestamps, differ. Both #67 SET_STREAM_INFO rows pass in all four legs |

22 of 23 gates are rc 0 at both base and head. `check_submodule_docs` fails identically at both.
Per-record diffs: `r2/cons/*.cmp.diff`.

### Parent rows each patch is needed for (round 2)

Each control reverses one patch (`bin/ctl_r2.sh`, chained by `bin/ctl_chain_r2.sh`), runs the gates
that patch touches through the same wrapper, then applies the patch again. Records are in
`r2/cons/<control>/`, each with its STATE.txt. Afterwards the parent's working-tree diff hashes to
`ef322a60…` again, and the gitlink is staged at bee33ff2.

| Control | Gate | rc | Verdict |
|---|---|---|---|
| head-noclass (bee33ff2, #67 only) | measure_test_evidence | 1 | `FAIL: 3 unexplained DUT-source reader(s) > ratchet 0`: tb/aecp_cmds/mutants.py, tb/elab_guards/guards.py, tb/elab_guards/mutants.py (all on processor main before this branch) |
| head-noclass | check_py_idiom | 0 | 258,756 lines (the patch's 16 lines removed) |
| base-noclass (e59804d8, #67 only) | measure_test_evidence | 1 | the same three readers |
| devpin-none (dev's pin 2cbed0a9, neither patch) | measure_test_evidence | 0 | `0 <= 0 unexplained DUT-source reader(s)` |
| devpin-none | check_submodule_docs | 0 | `submodule documentation: OK (6 exact gitlinks)` |
| devpin-none | check_cpp_idiom | 0 | — |
| head-no67 (bee33ff2, classification only) | check_cpp_idiom | 0 | — |
| head-no67 | milan_dp | 2 | `[FAIL] #67 the 2013-length SET_STREAM_INFO refuses at cdl 96 got=0x0 exp=0x1`, `[FAIL] #67 no refusal moved the stored offset got=0x0 exp=0xb71b0`; 2,550 `[ok]` before sim_pool stops the later legs |
| base-no67 (e59804d8, classification only) | milan_dp | 2 | the same two FAIL lines (identical after sorting), 2,550 `[ok]` |

So:

- The classification patch is needed by `measure_test_evidence` alone, at base and head. The three
  readers it classifies came from processor main, not from this lane.
- The #67 patch is needed by milan_dp's two #67 SET_STREAM_INFO rows alone, at base and head. They
  pin the 2013 refusal that round 1 removed; the merged base already carries round 1.
- Round 2 changes neither row. The #67 rows send only a 2013 body and a 2021 body, whose answers did
  not change, so `parent-adoption-milan_dp-67.patch` is unchanged from round 1.
- milan_dp was not run at dev's own pin. There the unpatched rows pin the refusal that pin still
  gives, so the #67 patch belongs with the pin adoption.

### Output directory (round 2 additions)

| File | Contents |
|---|---|
| `probe/` | probe_insert.py and the base/head length-probe outputs |
| `mutants/round2/patches/*.patch` | the nine round-2 arms (M38-M46) against the head engine |
| `mutants/round2/RESULTS.txt`, `LOGS.sha256` | each arm's tallies and FAIL lines; sha256 and size of the full logs |
| `EXTERNAL-RECORDS.csv` | now also lists every `r2/` record (gates, campaigns, consumer gates, controls, comparison diffs) |
| `parent-adoption-milan_dp-67.patch` | unchanged from round 1 |

### Final state (round 2)

- Lane: branch `176-ssi-2013-body` at bee33ff2, clean. On top of PR #183's head 29f58ad3 it has the merge
  e59804d8 (bringing in main's commits up to f0b1b9d8) and bee33ff2. No untracked or ignored files: the
  build outputs of the head runs were removed with `git clean -fdX`, as were those in the parent's
  submodule. Not pushed; the PR was not edited.
- Scratch parent: dev e9cbb676, the protocol-processor gitlink staged at bee33ff2, both patches in its
  working tree. Nothing committed or pushed.
- No job of this lane is still running.
- On issue #176, round 2 posted only "[A629] REVIEW READY" with head bee33ff2 (comment 6248817225). TAKEN was not posted
  again, and no existing comment was edited.

(Sections below the line "Round 1" are the round-1 record, kept unchanged.)

## Round 1

Status: DONE. REVIEW READY posted on issue #176 (comment 6243576614) with head 29f58ad3.

- Every processor gate and every campaign that builds a changed file is rc 0 at base and at head, with
  identical records apart from the 9 new pp_top checks.
- Every new check fails under at least one planted mutant.
- Parent consumer gates: 18 of 21 pass at both revisions.
  - Two fail identically at base and head because dev's pin lags processor main.
  - milan_dp fails at head on the two parent rows that pin the old 2013 refusal. With a two-row parent
    patch (scratch only) it passes.
  - So this PR says "Refs #176", not "Closes": the adoption has to carry that parent change.

- Processor repository: Mister-M-alt/protocol-processor-control-plane-avb-milan (origin verified)
- Lane: $LANES/pp176-ssi, branch `176-ssi-2013-body`
- Base: main `22c139a4323bc96c779d13e3f6774480c5fb9b75`
- Head: `29f58ad30a97327d92b50f17f49d085cd97066a5` (one commit, one-line subject, no body, no trailers;
  not pushed). An earlier head `4c7220c6` (same subject) failed the parent's C++ long-function rule and was
  amended. Its records are kept as `*/head-4c7220c6` in the scratch root and are superseded
- TAKEN: issue #176 comment 6236145831
- Scratch parent: kebag-logic/milan-fpga at dev `7d79ffb26308ac51eaeeab6ec43d798d057ae0cd` under
  $VALIDATION_STORAGE/pp176-a629/parent. When cloned, dev had already moved to e9cbb676; the assigned commit is used.
  Never committed or pushed. Only the staged protocol-processor gitlink is changed.
- Scratch root (logs, records, builds): $VALIDATION_STORAGE/pp176-a629

## Design

- IEEE 1722.1-2013 Figure 7.46 (48 payload bytes, cdl 60) is the first 48 bytes of IEEE 1722.1-2021
  Figure 7-40 (84 bytes, cdl 96). The one difference: 2021 turns the 2013 reserved word at @70 into
  `ip_flags`, then appends `source_port`, `destination_port` and the two 16-byte addresses.
  `flags` @28 and `msrp_accumulated_latency` @48 are at the same offsets in both. (Checked against the
  2013 PDF page image of Figure 7.46 and the 2021 Figure 7-40 text.)
- The engine accepts the 2013 body only at exactly cdl 60 with all 48 bytes walked from the RX slot
  (`si13_w`). It then takes every route the 2021 body takes.
- Every answer is the 2021 form, cdl 96:
  - a 2021 command keeps its byte-exact echo, as before;
  - a 2013 command gets its own @24..@69 echoed and zeros from @70 to @107.
  The reserved word at @70 is deliberately not echoed: in the 2021 response @70 is `ip_flags`, a
  field the 2013 command does not carry.
- The ROM is unchanged: generated `ucode.hex` sha256
  `518b900c4a5650902c3ea9125941e434857ba2f379b6c92268a67fef459d37f8` at base and head, the value
  decode.json records. Only comments change in gen_ucode.py.
- STOP conditions checked: no register-map, top-level port or parameter change.
  `git diff 22c139a4 29f58ad3 -- hdl/top hdl/common hdl/packet_engine docs/architecture/07_memory_maps.md
  docs/architecture/02_interfaces.md docs/guides` is empty.
- In the raw `git diff 22c139a4 29f58ad3 -- hdl/`, the only `+`/`-` lines matching
  `parameter|input|output|inout` are the two versions of aecp_commands.json's Scope prose
  ("**output only** (Δ11)"). No SystemVerilog port or parameter line changes. The four new names are
  module-internal localparams.

## Changes (file:line at the head)

- `hdl/aecp/KL_aecp_engine.sv`
  - :803-813: the two accepted bodies, as localparams `SI21_PLD_C` 84, `SI13_CDL_C` 60,
    `SI13_PLD_C` 48 and `SI13_ECHO_C` 46.
  - :1558-1563: `si13_w`, a SET_STREAM_INFO of exactly cdl 60, walked whole.
  - :2573-2584: `si13_pad_w` and the `frame_byte` mux. A 2013 echo is zero from @70.
  - :3585-3599: the dispatch-arm comment.
  - :3612-3614: the short-command route to E_SIBAD skips `si13_w`. Every later route is unchanged
    and shared.
  - :3709-3714: the latency-capture comment.
  - :3759-3761: at A_RUN an echoed answer to a 2013 command is lengthened to 84 bytes.
- `hdl/aecp/ucode/gen_ucode.py:2309-2312, 2329-2332`: comments only, ROM byte-identical.
- `hdl/aecp/ucode/aecp_commands.json:141`: `"command": {"cdl": 96, "floor": 60}`.
  `:148`: Scope and size notes rendered into F06.14.
- `hdl/aecp/ucode/aecp_fields.json:25`, and its generated copies
  `scripts/check_aecp_commands.py:23-26` and `docs/architecture/09_verification.md:657-660`:
  SET_STREAM_INFO joins the floor-declaring commands.
- `docs/architecture/06_aecp_engine.md`:
  - :261: F06.14, regenerated by `check_aecp_commands.py --write`;
  - :493: §6.3 SET_STREAM_INFO row;
  - :1230: §8.1 status row.
- `docs/architecture/09_verification.md`:
  - :184: §8.1 evidence row;
  - :609-614: §8.11 hand-written limits.
- `tb/aecp_cmds/sim_main.cpp:311`: the flag templates are swept at cdl 60 and 96.
  `tb/aecp_cmds/decode.json`: re-recorded with `make -C tb/aecp_cmds record`.
  `tb/aecp_cmds/README.md:33-35, 84-86`.
- `tb/pp_top/sim_main.cpp`:
  - :8090-8122: the W24 banner, plus `si13_pl` and `si13_rsp`, the independent 2013 stimulus and its
    expected 2021-form answer;
  - :8185-8186: W24 calls the new rows between W24f and W24h;
  - :8200-8269: `w24g_the_2013_body_and_a_body_of_neither_length()`, holding W24g-W24m (they replace the
    old W24g/W24g1/W24g2, which pinned the refusal). They live in their own member function because the
    parent's Rule 11 (`check_cpp_idiom.py`, functions of at most 100 lines) failed on the first head:
    W24 had grown to 137 lines;
  - :8314-8325: W25b3.
- `tb/pp_top/README.md:1033-1039`: mutation-record rows M38-M44.

## Accepted lengths and refusal cases

| Command | Result |
|---|---|
| cdl 60 (2013 body), all 48 bytes walked | accepted: the full SET_STREAM_INFO routes, 2021-form answer (cdl 96) |
| cdl >= 96 with >= 84 bytes walked (2021 body, padding echoed as before) | accepted: unchanged |
| cdl 12-59 and 61-95, or a committed slot shorter than its cdl | BAD_ARGUMENTS at cdl 96, {type, index} over a zero body, nothing applied (E_SIBAD, unchanged) |

The same routes apply to both accepted bodies, in this order:

| Route | Answer |
|---|---|
| target not a STREAM_OUTPUT | NOT_SUPPORTED |
| streaming output | STREAM_IS_RUNNING |
| flags != MSRP_ACC_LAT_VALID exactly | NOT_SUPPORTED |
| latency bit 31 | BAD_ARGUMENTS |
| foreign lock (CHECK_LOCK) | ENTITY_LOCKED |
| locate miss | NO_SUCH_DESCRIPTOR |
| otherwise | SUCCESS, the presentation-time offset written, published and notified |

Nothing is applied on any refusal.

The sweep record (`tb/aecp_cmds/decode.json`, AEM 0x000E) holds this:

- SINFO, SIRUN and BADARG at cdls "60, 96";
- NSUPPE at "60, 96-100", answering cdl 96 at cdl 60 and echoing the rest;
- SIBAD at "12-59, 61-95", answering cdl 96.

Not separately graded in the 2013 form: the ENTITY_LOCKED route. It shares E_SINFO's E_FAILSAFE
echo with the locate miss that W24l grades.

## New checks and planted mutants

New `tb/pp_top` checks, all in the default build, section W:

| Check | What it holds |
|---|---|
| W24g | 2013 body SUCCESS, byte-exact 2021-form answer |
| W24g1 | its latency is the published offset |
| W24g2 | a second 2013 SET sets the offset back (SUCCESS, cdl 96, row 1000000) |
| W24i | Stream Input → NOT_SUPPORTED, byte-exact 2021 form |
| W24j | extra flag → NOT_SUPPORTED, byte-exact 2021 form |
| W24k | bit-31 latency → BAD_ARGUMENTS, byte-exact 2021 form |
| W24l | missing Stream Output → NO_SUCH_DESCRIPTOR, byte-exact 2021 form |
| W24l2 | none of the refused 2013 latencies was applied |
| W24m / W24m1 / W24m2 | a 72-byte body (cdl 84, neither form) → BAD_ARGUMENTS at cdl 96, not applied, zero-body stub |
| W25b3 | 2013 body on a really streaming output → STREAM_IS_RUNNING, byte-exact 2021 form, not applied |

pp_top grows by 9 checks (10,470 → 10,479): the three old W24g rows become eleven, plus W25b3.

Each arm was planted in a scratch copy of the head tree, then the default pp_top build was built
alone (`gsi-build`) and run through every section. Patches and the full FAIL lists are in
`mutants/` (RESULTS.txt; LOGS.sha256 lists the full logs, which are kept in the scratch root).
All arms ran at the final head 29f58ad3, and before that at the superseded 4c7220c6. Every arm's FAIL
list is identical at both.

| Arm (patch) | Edit | Default build | Failing words (new checks) |
|---|---|---|---|
| control | none | 9,985 checks, 0 failures | — |
| sinfo13-refused | `!si13_w` → `1'b1` | 8 failures | `W24g: the 2013-length SET_STREAM_INFO (cdl 60) is SUCCESS`, W24g1, W24g2, W24i, W24j, W24k, W24l, W25b3 |
| sinfo13-echo-length | `pld_r <= pld_cmd_r` for every echo | 7 | W24g, W24g2, W24i-W24l, W25b3 |
| sinfo13-tail-echoed | `si13_pad_w` tied 0 | 6 | W24g, W24i-W24l, W25b3 |
| sinfo13-reserved-echoed | `SI13_ECHO_C` 46 → 48 | 6 | W24g, W24i-W24l, W25b3 |
| sinfo13-any-shorter-body | `si13_w` compares `>=` | 6 | `W24m: a 72-byte SET_STREAM_INFO (cdl 84) refuses at cdl 96`, W24m1, W24m2, W25b3 (+ W24h2, W25b2) |
| sinfo13-latency-uncaptured | `silat_r` arms gated `!si13_w` | 8 | `W24g1: ...and the presentation-offset row published its latency`, W24g2, W24k, W24l2, W24m1, W25b3 (+ W24h2, W25b2) |
| sinfo-flag-gate-open | flag compare → `1'b0` | 9 | `W24j: ... with an extra flag is NOT_SUPPORTED`, `W24l2: ...and no refused 2013-length latency was applied`, W24m1, W25b3 (+ W24d-W24f, W24h2, W25b2) |

Every new check is failed by at least one arm: W24g, W24g1, W24g2, W24i, W24j, W24k, W24l, W24l2,
W24m, W24m1, W24m2 and W25b3.

The tb/aecp_cmds suite was run under three arms (whole suite, own scratch copy):

| Arm | Result |
|---|---|
| control | rc 0, 176/176 |
| sinfo13-refused | rc 2: `decode: SET_STREAM_INFO: the shortest AEM 0x000E the engine dispatches to SINFO is cdl 96, the table's floor is 60`, plus the per-program decode.json lines |
| sinfo13-echo-length | rc 2: SINFO/SIRUN/BADARG/NSUPPE answer "echo" where decode.json records cdl 96 |
| sinfo13-any-shorter-body | rc 2: SIBAD recorded "12-59, 61-95" but observed "12-59"; NSUPPE and SIRUN reached at 60-100 |

## Base and head records

All runs used the pinned Verilator 5.050 and sv2v 0.0.12, with the lane tree at each commit. Records are
in $VALIDATION_STORAGE/pp176-a629/{rec,camp,cons}/{base,head}. Each has a `.log`, and an `.rc` written by
the wrapper from the command's own exit status, never through a pipe.

### Processor gates

| Gate | Base 22c139a4 | Head 29f58ad3 | Identical? |
|---|---|---|---|
| `scripts/run_suites.sh` | rc 0, 1,029,951 checks, 0 failing (53 min) | rc 0, 1,029,960 checks, 0 failing | only `pp_top` differs: 10,470 → 10,479 (the 9 new checks). Every other suite line, aecp_cmds' 176 included, is identical |
| `scripts/lint_hdl.sh` | rc 0, 41 LINT OK | rc 0 | identical |
| `make check` | rc 0 | rc 0 | identical output (aecpcmd: 231 planted defects caught; 31 commands, 84 entries, F06.14 41 rows) |
| `scripts/gen_matrix.py --check` | rc 0, 94 rows, 0 untested | rc 0 | identical |
| `syn/yosys/run.sh` | rc 0, 42 tops + Xilinx KL_aecp_engine OK | rc 0 | identical after normalizing `all.v:N`. Six warnings cite all.v lines shifted +8 by the engine's added lines |

### Campaigns that build a changed file

The changed files built by campaigns are `hdl/aecp/KL_aecp_engine.sv`, `tb/pp_top/sim_main.cpp`,
`tb/aecp_cmds/sim_main.cpp`, and `ucode.hex`'s inputs (`gen_ucode.py`, `aecp_commands.json`; the ROM is
unchanged).

- Not run, because they build none of these: srp_top, srp_admission and acmp_talker retry_mutants.
- Base campaigns ran from the scratch parent's submodule checked out at 22c139a4. Head campaigns ran
  from the lane at 29f58ad3.
- d3_mutants (110 arms) needs about 2.5 h on this shared host, more than one run may take. It ran in four
  `--only` chunks of 27/28/27/28 arms, each with its own goldens. Together the chunks cover the 110 arms
  exactly once. `tb/pp_top/d3_mutants.py` is identical at base and head.

"Identical" means the verdict lines are identical after sorting (parallel completion order) and after
normalizing host paths, times, digests and source line numbers. The source line numbers are
`KL_aecp_engine.sv:N` and `all.v:N`, which the added engine lines shift.

| Campaign | Base | Head | Identical? |
|---|---|---|---|
| `make -C tb/aecp_cmds mutants` | rc 0, 16 of 16 controls detected | rc 0, 16 of 16 | yes |
| `make -C tb/pp_top aecp-dispatch-mutants` | rc 0, 44/44 | rc 0, 44/44 | yes |
| `make -C tb/pp_top aecp-mutants` | rc 0, 67/67 | rc 0, 67/67 | yes |
| `make -C tb/pp_top ctr-mutants` | rc 0, 18/18 | rc 0, 18/18 | yes |
| `tb/pp_top/gsi_mutants.py --jobs 4` | rc 0, 20 detected | rc 0, 20 detected | yes |
| `tb/pp_top/name_wr_mutant.py` | rc 0, killed | rc 0, killed | yes |
| `tb/pp_top/acmp_mutants.py --jobs 4` | rc 0, 51 of 51 KILLED | rc 0, 51 of 51 | yes |
| `tb/pp_top/notify_mutants.py --jobs 4` | rc 0, 93 of 93 KILLED | rc 0, 93 of 93 | yes |
| `tb/pp_top/d3_mutants.py --jobs 3 --only <chunk>` ×4 | rc 0 ×4: 27+28+27+28 = 110 of 110 KILLED, goldens PASS | rc 0 ×4: 27+28+27+28 = 110 of 110 KILLED, goldens PASS | yes, chunk by chunk |
| `make -C tb/adp_engine mutants` | rc 0, 62/62 | rc 0, 62/62 | yes |
| `make -C tb/maap mutants` | rc 0, 32/32 | rc 0, 32/32 | yes |
| `make -C tb/elab_guards mutants` | rc 0, 160 of 160 killed | rc 0, 160 of 160 | yes (engine/all.v line numbers only) |
| `make -C tb/name_state mutants` | rc 0 | rc 0 | yes |

Superseded and stopped runs are kept beside the records. None of them is counted above.

- `*.stopped.log`: d3 runs stopped at a time limit, or stopped by me to relieve memory pressure.
- `camp/head-4c7220c6`, `rec/head-4c7220c6`, `cons/head-4c7220c6`: the first head's records.
- `cons/base/milan_dp.stopped.log`: milan_dp stopped at the 2 h limit under load, then rerun to rc 0.

## Scratch-parent consumer gate table

Setup:

- Parent: dev 7d79ffb2. The protocol-processor gitlink was staged at each revision with the submodule
  checked out there; `cons/*/STATE.txt` records both.
- Gate set: the 17 consumer gates the previous processor lane (#170) ran, plus check_hygiene,
  check_sv_idiom, check_submodule_docs and the BDD conformance suite. The BDD suite parses the engine
  and F06.14.
- `devpin` is the gitlink at dev's own pin 2cbed0a9. It was used only as a control for the two gates
  that fail at both base and head.

| Parent consumer command | devpin 2cbed0a9 | Base 22c139a4 | Head 29f58ad3 | Result / boundary |
|---|---|---|---|---|
| `python3 scripts/check_cpp_idiom.py` | | 0 | 0 | Identical. The first head 4c7220c6 failed here (`long function 1 > ratchet 0`: W24 had grown to 137 lines) and was amended |
| `python3 scripts/check_py_idiom.py` | | 0 | 0 | Only the line total moves, 248,196 → 248,200 |
| `python3 scripts/check_rtl_source_lists.py` | | 0 | 0 | Identical |
| `python3 scripts/pp_srcs.py --check --selftest` | | 0 | 0 | Identical |
| `python3 scripts/check_port_contracts.py` | | 0 | 0 | Identical |
| `python3 scripts/measure_naming.py --check` | | 0 | 0 | Identical |
| `python3 scripts/measure_test_evidence.py --check` | 0 | 1 | 1 | Identical at base and head: `FAIL: 3 unexplained DUT-source reader(s)`. The three readers are tb/aecp_cmds/mutants.py and tb/elab_guards/{guards,mutants}.py, added on processor main after dev's pin (c814a42, eb7e596, ef86ea8), before this lane's base. The adoption classifies them; this lane did not write dispositions for other lanes' files |
| `python3 scripts/docs_check.py` | | 0 | 0 | Identical |
| `python3 scripts/check_sh_idiom.py` | | 0 | 0 | Identical |
| `python3 scripts/check_hygiene.py --check` | | 0 | 0 | Identical |
| `python3 scripts/check_sv_idiom.py` | | 0 | 0 | Identical |
| `python3 scripts/check_submodule_docs.py` | 0 | 1 | 1 | Identical: `protocol-processor: documented pin differs from Git` and the pin diagram is stale. Any gitlink other than the documented one fails here; the adoption records the pin |
| `python3 sw/builder/test_builder.py` | | 0 | 0 | `ALL GATES PASS EXCEPT 1 NOT RUN` at both |
| `python3 scripts/lint_rtl.py --check` | | 0 | 0 | Identical: 90 violations ≤ ratchet 90 |
| `cd tests && behave --no-capture -f plain` | | 0 | 0 | Identical |
| `flock $VIVADO_LOCK python3 scripts/xvlog_gate.py --check` | | 0 | 0 | Identical except the line naming the processor pin; 0 findings |
| `make -j16 -C tb/verilator/pp_shadow` | | 0 | 0 | 2,184 checks (609 + 649 + 609 + 317, four binaries), 0 failures at both |
| `make -j16 -C tb/verilator/nvm_cosim lint` | | 0 | 0 | Identical |
| `make -j16 -C tb/verilator/nvm_cosim quick JOBS=4 POOL=2` | | 0 | 0 | Identical |
| `make -j16 -C tb/verilator/milan_dp_render` | | 0 | 0 | Check lines identical. Head reused the AEM image the base run generated in the same scratch tree, so the generator's output appears at base only |
| `make -j16 -C tb/verilator/milan_dp SIM_JOBS=2` | | 0 | **2** | Head fails exactly the two #67 rows that pin the old refusal: `[FAIL] #67 the 2013-length SET_STREAM_INFO refuses at cdl 96 got=0x0 exp=0x1` and `[FAIL] #67 no refusal moved the stored offset got=0x0 exp=0xb71b0` (the parent's 2013 probe carries latency 0, which is now applied). sim_pool then stops the later legs |
| the same, with `parent-adoption-milan_dp-67.patch` applied in the scratch parent only | | | 0 | Both #67 rows pass in all four legs, and the per-leg tallies equal base (423, 416, 162, 1967, 1969, 3751, 1967, 33 checks; 0 failures). The patch expects SUCCESS at cdl 96 for the 2013 body and sends the stored 750000 so the next row is unchanged. It is not committed anywhere; it is for the adoption lane |

Parent texts that will be stale after this change and that no gate reads as behaviour:

- `tests/steps/aecp_engine_steps.py:186-190` says "the 2013 60-byte shape is itself a truncated command
  on the real engine; pp_top W24g pins that". Its verdict, BAD_ARGUMENTS at cdl 96 for the sweep's cdl-20
  probe, is still true and the BDD gate passes.
- `tb/verilator/milan_dp/sim_nxn.cpp:6862`.

## Tool identities

- Verilator 5.050 (rev v5.050): $VALIDATION_TOOLS/pinned-verilator-5.050/verilator. The host default 5.052
  was not used.
- sv2v 0.0.12: $VALIDATION_TOOLS/sv2v-v0.0.12/sv2v, sha256
  b29952bc8f400ca90207507db0ff6763263e03d3eec711da80338430ed636b9b.
- Yosys 0.66 (git sha1 86f2ddebc-dirty, package 0.66-1): /usr/bin/yosys, sha256
  ec566d8fbb0d24e09ce7ab4e86c55c7169f24097d90611ee354b446925f36b5b. No Yosys exists under
  $VALIDATION_TOOLS (searched); the host's is the only one. CI installs the distribution Yosys and
  sv2v "latest".
- behave 1.3.3 (host) for the parent BDD suite; Vivado 2026.1 xvlog under the exclusive
  $VIVADO_LOCK.

## Output directory

| File | Contents |
|---|---|
| HANDOFF.md | this file |
| PR-BODY.md | the processor PR description |
| mutants/patches/*.patch | the seven planted arms against the head engine |
| mutants/RESULTS.txt | every arm's default-build tally and FAIL lines, and the aecp_cmds runs |
| mutants/LOGS.sha256 | sha256 and size of the full logs (kept in the scratch root) |
| parent-adoption-milan_dp-67.patch | the two-row parent change the pin adoption needs, validated in the scratch parent only |
| EXTERNAL-RECORDS.csv | sha256, size and path of every gate, campaign and consumer record in the scratch root |

## Final state

- The lane is at 29f58ad3: clean, no untracked or ignored files (the build outputs of my runs were
  removed with `git clean -fdX`), not pushed.
- The scratch parent is at dev 7d79ffb2. Its only change is the staged protocol-processor gitlink at
  29f58ad3. The milan_dp adoption patch was reverted after its validation run. Nothing committed or
  pushed.
- No job of this lane is still running.
- On issue #176 this lane posted only "[A629] TAKEN" (6236145831) and "[A629] REVIEW READY" (6243576614, with the head).
- No PR was created, nothing was pushed, and no existing comment was edited.

