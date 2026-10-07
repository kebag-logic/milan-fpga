# [A553] HANDOFF: processor #163 (transmit-arbiter input cone)

Current Round 4 status: REVIEW READY at `8947bafdd62b4bf991debf7bfd8cdb73994a3a81`; tests and documentation only.
See the Round 4 section at the end.

Prior round-3 handoff: REVIEW READY at `c4539ff107a6a4c7d2e4a4844182b00a2bf33c82`.
Its parent is merge `5fe5ea57` (parents `ff581556` and `c9f74b68`); it preserves every check and mutant, and
was unpushed at that handoff and subsequently became the published PR #166 head.
The earlier round records below are retained.


Status (round 2): REVIEW READY at `ff58155657c3496d862710dab48357fd8f8d4102`, the
`--no-ff` merge of `main` `2ad2f845` (#42) on top of `cd9825c9`. Not pushed, and no PR
edited. Every processor suite, gate and campaign and all 17 parent consumers return rc 0 at
`2ad2f845` and at the merge. The records are identical except the ones this PR names, and
`pp_top` is 10,462 = 10,459 + 3. Round 1 (REVIEW READY at `cd9825c9`, PR #166) follows from
section 1 on.

## R2. Round 2: merge of `main` `2ad2f845` (#42)

Assignment: issue #163 comment 6023618295. `main` `2ad2f845` (#42, PR #164) adds section
DN and its nine controls in `tb/pp_top`. It was merged with `--no-ff` on top of
`cd9825c9`: no rebase, no amend, and the round-1 commits are unchanged.

- Merge commit `ff58155657c3496d862710dab48357fd8f8d4102`, "Merge main 2ad2f845 (#42) into
  pp163-txarb-cone" (parents `cd9825c9`, `2ad2f845`).
- No STOP condition was hit. No port, register-map or parameter change. `hdl/`, `syn/`,
  `scripts/` and `docs/architecture/03_packet_engine.md` are identical to `cd9825c9`, so
  the round-1 OOC measurement (sections 1 and 4) still applies to the merge.

### R2.1 Conflict resolution (both sides kept)

| File (merge) | Conflict | Resolution |
|---|---|---|
| `tb/pp_top/sim_main.cpp:14071, 14091-14092` | both sides added a flag to `one_section` and a section call after CS (the flags themselves, `:14061` and `:14063`, merged cleanly) | `one_section` ends `\|\| dn_only \|\| withdraw_only;`, then `run_domain_notify(h)` and `run_withdraw(h)`: DN (main's) first, then WD |
| `tb/pp_top/notify_phases.hpp:1642-1812, 1814-1996, 2028-2040` | both sides added a phase after `RndPhase` and a `run_*` after `run_spacing` | `DomainNotifyPhase` then `WithdrawStagePhase`, and `run_domain_notify` then `run_withdraw`; both bodies unchanged |
| `tb/pp_top/notify_mutants.py:21-26, 355-431` | the module docstring's control list; the arm tuples and `MUTANTS` | the docstring names both (#42's DN, then #163's WD and CX); `DOMAIN_NOTIFY` then `WITHDRAW_STAGE`, and `MUTANTS = (... + DEREG_MID_ROUND + DOMAIN_NOTIFY + WITHDRAW_STAGE)` |
| `tb/pp_top/README.md:2238-2241, 2466-2555, 2578-2587, 2647-2658` | the run-flag sentence; the new sections after CS; the mutation record's narrative; its last rows | both flags; section DN then section WD; #42's sentence then #163's, now "for 68 of 68 with #42's nine"; DN's nine rows then WD's three |

One auto-merged line needed a fix: both sides had changed "seven sections" to "eight"
(`tb/pp_top/README.md:2229`). With DN and WD both present it reads "nine sections".

Each section builds its own model (`NotifyBench` owns a fresh `Model`), so the DN-then-WD
order changes no result. A line-multiset comparison confirms both sides are kept. The
merge's change against `2ad2f845` is exactly the round-1 change, and its change against
`cd9825c9` exactly #42's. The only exceptions are the conflict-region prose above and the
joined `one_section` line. Every code line of both sides is present.

### R2.2 Before any run

- Every `tb/**/*.patch` (283) applies with `git apply --check` on an export of `2ad2f845`
  and of the merge: 0 refused (`evidence/patch-audit-m2base.json`, `-m2head.json`).
- Every one of the 68 `notify_mutants.py` arms, #42's nine included, finds each of its
  exact-text edits exactly once in the merged tree. #42's top-level arms (`AVB_OR`,
  `ev_asp_i`, `restore_done_o`) do not touch the lines this PR changed.
- The parent's light consumers (01-08, 11, 13, 17) ran first at the merge: all rc 0.

### R2.3 `tb/pp_top` and `tb/aecp_notify`

| Run | `2ad2f845` | Merge `ff581556` |
|---|---|---|
| `scripts/run_suites.sh`: `pp_top` (six builds) | 10,459 checks, 0 failing | 10,462, 0 failing (+3: WD1-WD3) |
| `scripts/run_suites.sh`: `aecp_notify` | 45, 0 failing | 46, 0 failing (+1: CX1) |
| `make gsi-build`, `--domain-notify-only` | DN: 15 checks, 0 failures | DN: 15 checks, 0 failures |
| `make withdraw` (`--withdraw-only`) | (no section WD) | WD: 3 checks, 0 failures |

DN's lines are the same at both revisions. Each link-edge GET_AVB_INFO leaves 466 clocks
after its edge and each Domain one 495 clocks after `feed()` returns, as #42's README
states, and the section takes 8,167 ms of the timebase. So the registered withdraw mask
moves no DN timing. WD's two clock traces at the merge equal round 1's: the acceptance
case sends 1 probe, and the selection case sends none.

`pp_top` is 10,462 = 10,459 + 3, the figure the assignment asks for.

### R2.4 Processor suites and gates (`2ad2f845` and the merge)

Each run used its own `git archive` export, log, rc and command/time record (`logs/m2base`,
`logs/m2head`). `make check` ran in the lane: at `2ad2f845` on a detached checkout, then
back on the branch at the merge.

| Gate | `2ad2f845` rc | Merge rc | Records |
|---|---:|---:|---|
| `scripts/run_suites.sh` | 0 | 0 | 1,028,250 checks at `2ad2f845`, 1,028,254 at the merge, 0 failing at both. Every suite line is identical except `aecp_notify` 45 -> 46 and `pp_top` 10,459 -> 10,462. Against `cd9825c9`, only `pp_top` (10,447 -> 10,462, DN's 15) differs |
| `scripts/lint_hdl.sh` | 0 | 0 | byte-identical (also to `86a7b0c5` and `cd9825c9`) |
| `make check` | 0 | 0 | identical when sorted (concurrent recipe order) |
| `python3 scripts/gen_matrix.py --check` | 0 | 0 | byte-identical, `matrix: OK (94 rows, 0 untested)` |
| `syn/yosys/run.sh` | 0 | 0 | identical except the lowered `all.v` line numbers in four memory-to-register warnings (the arbiter's source is 11 lines longer), as in round 1. The merge's log is byte-identical to `cd9825c9`'s, and `2ad2f845`'s to `86a7b0c5`'s |

### R2.5 Campaigns (`2ad2f845` and the merge)

Every campaign driver in the tree, `--jobs 2`, at both revisions. No arm was REFUSED.
Seconds are wall time on a shared, saturated host.

| Campaign | `2ad2f845` | Merge | Comparison |
|---|---|---|---|
| `tb/pp_top/notify_mutants.py` | rc 0, 65 of 65 KILLED, goldens PASS (1976 s) | rc 0, 68 of 68 KILLED, goldens PASS (2466 s) | named only: +3 arms (`withdraw_unregistered` WD1, WD2; `withdraw_abort_ignored` WD2, WD3; `cancel_one_clock_late` CX1, IX3), +1 golden (`--withdraw-only`), `ix_new_identity_unset` also fails CX1. The other 64 records are identical, DN's nine among them. Against `cd9825c9`, exactly DN's nine arms and its golden differ |
| `tb/pp_top/d3_mutants.py` | rc 0, 110 of 110 KILLED, goldens PASS (7130 s) | rc 0, same (7376 s) | records identical; driver log identical when sorted |
| `tb/pp_top/aecp_mutants.py` | rc 0, `67 checks: 67 PASS` (1695 s) | rc 0, same (2312 s) | driver log byte-identical |
| `tb/pp_top/aecp_dispatch_mutants.py` | rc 0, 40 KILLED, `44 checks: 44 PASS` (1527 s) | rc 0, same (1461 s) | driver log byte-identical |
| `tb/pp_top/acmp_mutants.py` | rc 0, 33 of 33 KILLED (2286 s) | rc 0, same (2132 s) | records identical; driver log identical when sorted |
| `tb/pp_top/gsi_mutants.py` | rc 0, 20 detected, golden and restored PASS (1367 s) | rc 0, same (1237 s) | driver log byte-identical |
| `tb/pp_top/ctr_mutants.py` | rc 0, `18 checks: 18 PASS` (614 s) | rc 0, same (488 s) | driver log byte-identical |
| `tb/pp_top/name_wr_mutant.py` | rc 0, decode killed, golden and restored PASS (71 s) | rc 0, same (125 s) | driver log byte-identical |
| `tb/adp_engine/mutants.py` | rc 0, `43 checks: 43 PASS` (828 s) | rc 0, same (919 s) | driver log byte-identical |
| `tb/maap/mutants.py` | rc 0, `32 checks: 32 PASS` (676 s) | rc 0, same (460 s) | driver log byte-identical |
| `tb/srp_top/mutants.py` | rc 0, `137 checks: 137 PASS` (3203 s) | rc 0, same (2779 s) | driver log byte-identical |
| `tb/srp_admission/mutants.py` | rc 0, `12 checks: 12 PASS` (570 s) | rc 0, same (574 s) | driver log byte-identical |
| `tb/acmp_talker/retry_mutants.py` | rc 0, 62 killed, 7 equivalence and 1 performance controls (538 s) | rc 0, same (722 s) | driver log byte-identical |

Every campaign except `notify_mutants.py` also has records identical to round 1. That
holds for `86a7b0c5` against `2ad2f845` and for `cd9825c9` against the merge, since #42
changes no other campaign's records.

### R2.6 Parent consumer set (17), dev `28f9666f` + 148 + 22

The same scratch parent as round 1 (section 7): dev `28f9666f`, the 148 and then the 22
patch applied with `git apply`, never committed or pushed. Both patches still
reverse-check. The processor gitlink was staged at `ff581556` and then at `2ad2f845`. Every
submodule's top level was checked before each Git command and each consumer. The previous
runs' generated files were moved aside before each revision ran.

| Consumer | `2ad2f845` rc | Merge rc | Comparison |
|---|---:|---:|---|
| 01_cpp | 0 | 0 | identical |
| 02_py | 0 | 0 | named: first-party Python lines 200,043 -> 200,075 (+32: the three arms, and the merged docstring is one line longer than round 1's) |
| 03_sources | 0 | 0 | identical |
| 04_pp_sources | 0 | 0 | identical |
| 05_ports | 0 | 0 | named: test-only hierarchical observations 317 -> 323 (the wrap's 6 reads, as round 1) |
| 06_naming | 0 | 0 | identical |
| 07_evidence | 0 | 0 | identical |
| 08_docs | 0 | 0 | identical |
| 09_xvlog | 0 | 0 | under the Vivado lock, alone, after every other run of this lane ended; 0 findings at both (73 parent and 52 pinned-processor sources); identical except the pinned-revision line |
| 10_builder | 0 | 0 | identical except temp-directory names and durations; the one gate arm recorded before as not run (gate 11's reference build tree) |
| 11_lint | 0 | 0 | identical |
| 12_shadow | 0 | 0 | 606, 606, 646 and 311 checks, 0 failures at both; every per-check line identical (the only differences are lines interleaved by concurrent output) |
| 13_nvm_lint | 0 | 0 | identical except Verilator wall-time lines |
| 14_nvm_quick | 0 | 0 | byte-identical, nvm_cosim 315 of 315 PASS |
| 15_datapath | 0 | 0 | all 1,150 result lines identical (as multisets) |
| 16_render | 0 | 0 | identical result lines (65 and 245 checks, 5 leg-defect arms) |
| 17_shell | 0 | 0 | identical |

Against round 1 every consumer at `2ad2f845` equals `86a7b0c5`, and at the merge equals
`cd9825c9`, except 02_py: #42's DN arms add 46 lines at `main` and 47 at the merge.

### R2.7 Postings and retained evidence

- Issue #163: TAKEN was not posted again. REVIEW READY with the merge head is posted
  (comment 6026958634). No existing comment was edited or deleted. Nothing was pushed, and no PR
  was created or edited.
- Method as in section 8: the pinned Verilator 5.050, two build slots service-wide (each
  build `-j 2`), `MAKEFLAGS=-j8`, `VERILATOR_JOBS=2`, campaign drivers `--jobs 2`, and a
  20-second memory logger. Peak anonymous memory in round 2 was 4.3 GB. Vivado (09
  only) ran alone under the lock.
- The scratch parent is left with the processor gitlink staged at the merge
  (`ff581556`), uncommitted. Each run's generated files are under
  `stale-parent-m2-head/` and `stale-parent-m2-base/` in the scratch root.

Round-2 artifacts (scratch-relative; the two patch audits are also in `evidence/` here):

| Scratch-relative artifact | Bytes | sha256 |
|---|---:|---|
| `evidence/patch-audit-m2base.json` | 88 | fe538195f16e4f8c123f38d9bfbe18dcae7dc18a3e37e77b23ba944aaa7c8c6a |
| `evidence/patch-audit-m2head.json` | 88 | 84ab4659533d238fa0207536dd9d7c7dd8faf168cfb3b5207e9c42a9a2458c6c |
| `logs/m2base/camp-acmp.log` | 2904 | 801e9cf181e106d83d2a40a39075db65924b9dc53ab7b012ee61ad55730602a7 |
| `logs/m2base/camp-adp.log` | 33445 | f69c577b96367e850478d3068e7bca2d77be103f747ff6e9bd1cceec8485e95e |
| `logs/m2base/camp-aecp_dispatch.log` | 28893 | 0dd8b97ab8f9a89f6dad0388f0e6c83eb7bd37eb5a6f5bf47eda9954ff4222f6 |
| `logs/m2base/camp-aecp.log` | 78512 | 53d881784de32314b33d1e973813dacb1f3d85468dc2d1e6e94b1efe1d5ab698 |
| `logs/m2base/camp-ctr.log` | 11207 | dcd55eac8ffb06c36b2366e59a0ef5c517271e7751a3e948aa650dcffa178570 |
| `logs/m2base/camp-d3.log` | 8131 | eb2150c0fba8d91550b17379d107e28cbf1293249cd7d534a44a886357ad66c9 |
| `logs/m2base/camp-gsi.log` | 4150 | 5f6d67707db7bfed9d8aa1e323a7f3b0884134404c78e43b0b2afbd99953237b |
| `logs/m2base/camp-maap.log` | 7591 | 823ef7e638f720b03e151b4954e75a5b023fa034efda1171f57264a208ff3c81 |
| `logs/m2base/camp-name_wr.log` | 2550 | 055560a7d55d359d9281385f1d47fcddba0b082ac963195a2ce4201fdd4efe7a |
| `logs/m2base/camp-notify.log` | 5318 | b1a9f2eb3e5458700e8b13dd6b6b59ffcf8442095cdfda5933ecbe4adc1f3724 |
| `logs/m2base/camp-retry.log` | 3865 | 7bda8adf83703e45161d30a04b76f39855701cbb5b9b7c1979473aa7ba6c2512 |
| `logs/m2base/camp-srp_admission.log` | 479 | 6977d367d954c85cbb07f2f44ac0fb7a5ab3267f627556647a22a1bf95b798fc |
| `logs/m2base/camp-srp_top.log` | 9988 | ec920575b69b9fccc7fa3d0a279308d3465887cc59c7c5747aea6a374be00467 |
| `logs/m2base/lint.log` | 1056 | 9a3703ba1ec6767b277e9d5102c94a93fe107454da19d13cab518ba312cd1e81 |
| `logs/m2base/matrix.log` | 33 | 7a2c98136a0892f195fa6a08ad82dfe7e36e8a81d0732cb304584f31e966e097 |
| `logs/m2base/pp-dn.log` | 27308 | 049abc3f8c4d3beb95b4ad18971686e5f6c1b6ad8197315968a5c63d4f5d1b6a |
| `logs/m2base/suites.log` | 1750 | b37107cafb110e9a76737445437ee30a81673f33ec403875c8c27b1f5840c64a |
| `logs/m2base/yosys.log` | 3548 | 5918894aeb86257a2ba105f0914f534c8ab77338863151178375bed543a51a82 |
| `logs/m2head/camp-acmp.log` | 2904 | 9fe6faf1a3bdca6b86269e62092031aedc376653afb14fd12cda44cf41466430 |
| `logs/m2head/camp-adp.log` | 33445 | f69c577b96367e850478d3068e7bca2d77be103f747ff6e9bd1cceec8485e95e |
| `logs/m2head/camp-aecp_dispatch.log` | 28893 | 0dd8b97ab8f9a89f6dad0388f0e6c83eb7bd37eb5a6f5bf47eda9954ff4222f6 |
| `logs/m2head/camp-aecp.log` | 78512 | 53d881784de32314b33d1e973813dacb1f3d85468dc2d1e6e94b1efe1d5ab698 |
| `logs/m2head/camp-ctr.log` | 11207 | dcd55eac8ffb06c36b2366e59a0ef5c517271e7751a3e948aa650dcffa178570 |
| `logs/m2head/camp-d3.log` | 8131 | 6aa195d987e603f0a545ac522a1c51625f0f506f7e078dc1a387ece8af814477 |
| `logs/m2head/camp-gsi.log` | 4150 | 5f6d67707db7bfed9d8aa1e323a7f3b0884134404c78e43b0b2afbd99953237b |
| `logs/m2head/camp-maap.log` | 7591 | 823ef7e638f720b03e151b4954e75a5b023fa034efda1171f57264a208ff3c81 |
| `logs/m2head/camp-name_wr.log` | 2550 | 055560a7d55d359d9281385f1d47fcddba0b082ac963195a2ce4201fdd4efe7a |
| `logs/m2head/camp-notify.log` | 5596 | c05e1393a1780c9961402812a7bef1dd1216bbc503ab77dd269bbd52007b4ddc |
| `logs/m2head/camp-retry.log` | 3865 | 7bda8adf83703e45161d30a04b76f39855701cbb5b9b7c1979473aa7ba6c2512 |
| `logs/m2head/camp-srp_admission.log` | 479 | 6977d367d954c85cbb07f2f44ac0fb7a5ab3267f627556647a22a1bf95b798fc |
| `logs/m2head/camp-srp_top.log` | 9988 | ec920575b69b9fccc7fa3d0a279308d3465887cc59c7c5747aea6a374be00467 |
| `logs/m2head/lint.log` | 1056 | 9a3703ba1ec6767b277e9d5102c94a93fe107454da19d13cab518ba312cd1e81 |
| `logs/m2head/matrix.log` | 33 | 7a2c98136a0892f195fa6a08ad82dfe7e36e8a81d0732cb304584f31e966e097 |
| `logs/m2head/pp-dn-wd.log` | 28150 | 06b3380ccc112cac6ba5848f935e2211096295d560656509eee365973f540a24 |
| `logs/m2head/suites.log` | 1750 | 552a83967eb954f771ac7159ca137a43776975d4cff1468de8653137d14623e8 |
| `logs/m2head/yosys.log` | 3548 | bee608b28b73fa2fa502b40b30dbdeada7560af46bd0a21f0bece4b3ca0b23fb |
| `logs/m2-base-check.log` | 410 | fad87ccf02c091933a949c5f25052c68e8ba20056ada5a8c5cf431d174ed90b6 |
| `logs/m2-head-check.log` | 410 | fad87ccf02c091933a949c5f25052c68e8ba20056ada5a8c5cf431d174ed90b6 |
| `camp/m2base/camp-notify/results.json` | 115917 | 7b39f37424ba03535f7a0d88da8df4ad9486733d45ace05a78dc653466d272e2 |
| `camp/m2head/camp-notify/results.json` | 118001 | 2eaa4fb81a9caa59a4fc2171de46e868948bcf68e74c83351829be131f7900de |
| `camp/m2base/camp-d3/results.json` | 155047 | 1c78122d57e98873393e35b03ec8e9a673d5c2569139f7b5b430f9e971230211 |
| `camp/m2head/camp-d3/results.json` | 155047 | 7686c12282a26a00a8f3143b74ecd3b29dae79204705aecd75f4000c670c6f1d |
| `camp/m2base/camp-acmp/results.json` | 96457 | e18bd8d6de71c268369198b659f5f941649a34c70f46f50ecca248b217b14a92 |
| `camp/m2head/camp-acmp/results.json` | 96457 | 3532b6a307c9d4f0c0c4cee7c1d672d8f1100f87bcda3bc0e0e28fa31593677d |
| `camp/m2base/camp-aecp_dispatch/results.json` | 7629 | f82db07ae244a5947b85a1b3c55b8afb4930eba7267667179945155db01c5167 |
| `camp/m2head/camp-aecp_dispatch/results.json` | 7629 | f82db07ae244a5947b85a1b3c55b8afb4930eba7267667179945155db01c5167 |
| `logs/parent-m2-base/01_cpp.log` | 315 | 20d9e296340ae6319c913211b7a2b7d63b6cc89798c011092c87908916634810 |
| `logs/parent-m2-base/02_py.log` | 461 | aeb4098d042f84aaa8c780d62165fd474c441b36173c2907f20e43c245243820 |
| `logs/parent-m2-base/03_sources.log` | 153 | ed979d7e26c3cd7a6f14364c11994089b77632424d04252613eeed458ebc8a95 |
| `logs/parent-m2-base/04_pp_sources.log` | 955 | fad5e1b9dd5f465b7fcb2334e2abe6c6db44be93b5bb12afb3a35f3ebf432e1a |
| `logs/parent-m2-base/05_ports.log` | 421 | b04fbab06614655f710f529fa8d2cdbd59073e9a63f179b308734b9e21f35c23 |
| `logs/parent-m2-base/06_naming.log` | 36608 | db23d3d49d070f855b77fbe71e83f3cc24b00ae81d2c288082eb016ac2820e77 |
| `logs/parent-m2-base/07_evidence.log` | 13902 | bb9aadc07a14eb4e219e87fa681571c7886f1ef0be545cbae69d099b66fd7f44 |
| `logs/parent-m2-base/08_docs.log` | 127 | 6a6b0baa714d34c94d863882cab86a5eac8309164fc1a6c99cb5659f049510ee |
| `logs/parent-m2-base/09_xvlog.log` | 721 | a986da5e0c7b69d8a64fd8877e317f7000b2b6f02886dcd18bdab0df162391d2 |
| `logs/parent-m2-base/10_builder.log` | 101822 | 316152fe32b3c5d24fec05667d3aee17b911e18202da3e801b96271f8d5878ce |
| `logs/parent-m2-base/11_lint.log` | 14186 | 9087b44973869192bcab894931d990c7976fb895a8d92b6c243c555087f69d6e |
| `logs/parent-m2-base/12_shadow.log` | 276059 | c5989f514332e0bd5b7ed1e3779b8b218dbf7a766b495b2a42b5139264cf00f7 |
| `logs/parent-m2-base/13_nvm_lint.log` | 29864 | 1bc5763ec4c3e287ed88b1c7fcd7e1e2098be90bc4346c8f87e3cbd00a295d86 |
| `logs/parent-m2-base/14_nvm_quick.log` | 394 | cb802d0dfa07167eca0a998f0c041397eedf41d13b79f86c5090bc932b00c174 |
| `logs/parent-m2-base/15_datapath.log` | 1951596 | 0da978a47d9cd356382a806a9a4a6d80f7e437e2a30e1a8aff6d91de2464cb16 |
| `logs/parent-m2-base/16_render.log` | 156092 | 7d5af9af4744b12c2f625b9f8b1c8809b2e1a38bc873c2a6c0575460e04123bf |
| `logs/parent-m2-base/17_shell.log` | 235 | 7ace602f03fa0e411862de119cff9d337583f1f2170d920dff65a0e0f39ee6d9 |
| `logs/parent-m2-head/01_cpp.log` | 315 | 20d9e296340ae6319c913211b7a2b7d63b6cc89798c011092c87908916634810 |
| `logs/parent-m2-head/02_py.log` | 461 | 68c5c7810fbfc9d4d626f72a7fc89ce2c9caa498717efdcdc48467753d3f6fe4 |
| `logs/parent-m2-head/03_sources.log` | 153 | ed979d7e26c3cd7a6f14364c11994089b77632424d04252613eeed458ebc8a95 |
| `logs/parent-m2-head/04_pp_sources.log` | 955 | fad5e1b9dd5f465b7fcb2334e2abe6c6db44be93b5bb12afb3a35f3ebf432e1a |
| `logs/parent-m2-head/05_ports.log` | 421 | 774375e7ac9c65d58d1828460de6529193dc26a096daa71c548e214bb3404380 |
| `logs/parent-m2-head/06_naming.log` | 36608 | db23d3d49d070f855b77fbe71e83f3cc24b00ae81d2c288082eb016ac2820e77 |
| `logs/parent-m2-head/07_evidence.log` | 13902 | bb9aadc07a14eb4e219e87fa681571c7886f1ef0be545cbae69d099b66fd7f44 |
| `logs/parent-m2-head/08_docs.log` | 127 | 6a6b0baa714d34c94d863882cab86a5eac8309164fc1a6c99cb5659f049510ee |
| `logs/parent-m2-head/09_xvlog.log` | 721 | 395644690a72d2df130f40ff1571d53c92fa546addc0e424edf67a6fb97cef03 |
| `logs/parent-m2-head/10_builder.log` | 101822 | a8c8bdbee5a84a25c4d79c8ea95c32ddc32dcdf2d15dff768adc1a63cf493f75 |
| `logs/parent-m2-head/11_lint.log` | 14186 | 9087b44973869192bcab894931d990c7976fb895a8d92b6c243c555087f69d6e |
| `logs/parent-m2-head/12_shadow.log` | 273214 | a456b314e184b695c970003cdb56967c00d9a29f5a1f031453738dca34359827 |
| `logs/parent-m2-head/13_nvm_lint.log` | 29864 | 653a2a7536de4f36be6df0e0b7470d80e0c5d0e53ef1a8552d8eca1c3461f8aa |
| `logs/parent-m2-head/14_nvm_quick.log` | 394 | cb802d0dfa07167eca0a998f0c041397eedf41d13b79f86c5090bc932b00c174 |
| `logs/parent-m2-head/15_datapath.log` | 1949058 | b60749e05b61164b8cbebb527c430ad36da6fa81757c7a043a256a74979a9d91 |
| `logs/parent-m2-head/16_render.log` | 155211 | e17178802135e2b895c899aed81e043eebfa0c4ce284038f302c7771adf60313 |
| `logs/parent-m2-head/17_shell.log` | 235 | 7ace602f03fa0e411862de119cff9d337583f1f2170d920dff65a0e0f39ee6d9 |

## Round 1

Status: REVIEW READY at `cd9825c947cf67b735d26cc1c42541ccd9d7f637` (not pushed; no PR opened).

- Branch `pp163-txarb-cone` from processor `main` `86a7b0c5`. Head
  `cd9825c947cf67b735d26cc1c42541ccd9d7f637` (four commits, not pushed):
  - `912ee6ef` Cut the transmit-arbiter input cone: register the withdraw mask, rank
    requesters in parallel (RTL)
  - `916f53c7` Grade the withdraw stage in tb/pp_top (WD) and tb/aecp_notify (CX), with
    planted mutants (benches, mutant driver, READMEs, 03 §8 row)
  - `2ef802cb` Declare section WD's clock-sample members one per line (the parent's C++
    idiom gate refused one multi-declarator line in `916f53c7`)
  - `cd9825c9` Record the #163 notify-campaign re-run and CX1 in the ix_new_identity_unset
    rows (README text only)
- TAKEN posted on #163 (comment 6015592098); REVIEW READY posted with the head (comment
  6023577480). The previous session was ended by the service
  memory cap before any commit; this session resumed from a clean tree and posted nothing
  twice.
- No port, register-map or parameter change. No STOP condition was hit.
- Acceptance: items 1 and 2 and the area half of item 3 are met here. The parent
  three-directive sweep on the merged pin (item 3's second half) belongs to the pin
  adoption, so the PR body says "Relates to #163".

## 1. Measurement, OOC 1x1 at 50 MHz (#638 recipe)

Recipe: the scratch parent at dev `28f9666f` with the 148 and then the 22 patch, processor
gitlink staged at the revision, `sw/litex/build.sh ax7101 --dry-run` export, integrated
elaboration, `syn/ooc/pp_baseline.py --integrated-clock` (KL_pp_shadow, `synth_design
-directive AreaOptimized_high -mode out_of_context`, 20.000 ns clock), then
`pp_resource_gate.py record` and `check` for the `ooc-1x1` endpoint. Vivado v2026.1, run
alone under the Vivado lock. The head run (at `912ee6ef`; `hdl/` and `syn/` are identical
at `cd9825c9`) re-elaborated at its own revision. The wrapper parameters it bound are
identical to base's.

Base OOC timing summary: WNS -3.562 ns, TNS -37.519 ns, 16 failing endpoints of 62840,
WHS +0.159 ns. Every failing endpoint is in the transmit arbiter.

Cone survey (scratch `scripts/arb_cone.tcl`): every startpoint in the fan-in of the 187
arbiter sequential cells (561 endpoint pins), and the worst path from each startpoint to
each endpoint.

| | Before | After |
|---|---:|---:|
| Startpoints in the arbiter's input cone | 1,631 | 328 |
| Start/end pairs (worst path each) | 263,154 | 17,990 |
| Pairs above 20 levels | 146,535 | 0 |
| Deepest (levels) | 51 | 16 |

Per arbiter endpoint (deepest path, worst slack):

| Arbiter endpoint | Levels before | Slack before (ns) | Levels after | Slack after (ns) |
|---|---:|---:|---:|---:|
| `slot_r` | 51 | -3.562 | 16 | +11.912 |
| `owner_r` | 50 | -3.417 | 15 | +12.057 |
| `arb_st_r` (FSM) | 46 | -2.106 | 12 | +12.848 |
| `start_sent_r` | 46 | -1.514 | 12 | +13.440 |
| `age_r` | 35 | +2.490 | 9 | +13.827 |
| `cnt_r` | 34 | +3.371 | 8 | +14.710 |
| `gnt_r` | 34 | +4.001 | 8 | +15.341 |
| `pend_r` | 34 | +4.152 | 8 | +15.393 |
| `pace_nonsol_r` | 33 | +4.491 | 8 | +15.341 |

Every source above 20 levels before (assignment item 1), with its deepest path. That path
ends at `slot_r` for every source; `owner_r`, the FSM and `start_sent_r` follow, and the
counters, `pend_r` and `pace_nonsol_r` are shallower (the per-endpoint table above):

| Source | Levels | Worst slack (ns) | Route into the arbiter |
|---|---:|---:|---|
| notify `wr_ix_r` | 51 | -2.981 | identity-index row read (`rows_r[wr_ix_r]`), own-row compare (`ix_own_w`), command hit, CA cancel pick, originator cancel, withdraw mask, lane head, arbiter select |
| rx validator `hdr_src_mac_r` | 50 | -1.795 | notify index / originator response CAM, withdraw mask, arbiter |
| notify `rows_r` LUTRAM (all 64 column pairs) | 41-50 | -2.527 | as `wr_ix_r` |
| notify `pend_r` | 47 | -3.562 | parked-expiry drain pick, CA cancel, originator, mask, arbiter |
| rx validator `hdr_ctlr_eid_r` | 46 | -1.753 | as `hdr_src_mac_r` |
| notify `ca_probe_r` | 43 | -1.341 | CA cancel |
| rx validator `hdr_msg_type_r`, `hdr_protocol_r` | 41 | -1.047 | originator response valid |
| notify index chunk memories, `n_st_r`, `ix_set_r`, `ix_clr_r` | 40-41 | -1.389 | command hit |
| originator `key_r` | 41 | +2.962 | response CAM |
| rx validator `cp_r` (header valid) | 40 | -0.233 | response/command valid |
| notify `valid_r` | 39 | +0.078 | command hit |
| rx validator `hdr_target_eid_r` | 37 | +3.456 | response CAM |
| `entity_id_i` (port) | 36 | unconstrained | response valid |
| originator `seq_r`, rx validator `hdr_seq_r` | 33 | +3.510 | response CAM |
| rx validator `hdr_opcode_r` | 32 | +3.852 | response valid |
| originator `owner_r`, `valid_r`, `cancel_pend_r` | 29-32 | +3.671 | cancel pick, mask |
| originator `exp_pend_r`, `accept_pend_r`, `txs_r`, `retried_r` | 25-27 | +6.525 | mask |
| originator `release_*_o`, CA builder `cancel_release_*_o`, release merge `pending_r` | 24-25 | +7.698 | released head drop, arbiter select |
| top `laneq_org_r`, `laneq_org_cnt_r`, tx slots `st_r` | 21 | +9.371 | lane head ready, arbiter select |

Two structures made every one of these deep:
1. Every deep cone reached the arbiter through the originator's combinational
   `withdraw_slot_mask_o`, which fed the originator lane's request, the lane-queue
   compaction and the arbiter's `start_abort_i`.
2. The arbiter's selection was a serial best-so-far loop, 17 levels from `req_valid_i` to
   `slot_r`/`owner_r` (19 in a standalone synthesis of the module; 8 after), so even
   registered requesters (release, lane queue) landed at 21-25.

After: the deepest sources are the registered releases (originator `release_*_o`, CA builder
`cancel_release_*_o`, 16 levels, +11.912 ns), then release merge `pending_r` (15), then
`org_withdraw_mask_r`, tx slots `st_r` and `laneq_org_r` (12). The cut cone now ends at the
new register: `notify wr_ix_r -> org_withdraw_mask_r` 28 levels, +7.229 ns. The lane queue
gains too: worst path into `laneq_org_r` was 37 levels, +0.424 ns (from notify `pend_r`),
now 14 levels, +12.303 ns; `laneq_org_cnt_r` 35 levels, +1.591 ns, now 10, +13.582 ns.

## 2. Changes

RTL (`912ee6ef`):

| File:line | Change |
|---|---|
| `hdl/top/protocol_processor_top.sv:4371-4386` | `org_withdraw_mask_r`, an 8-bit register of the originator's `withdraw_slot_mask_o` (block `withdraw_mask_stage`), with the reason |
| `hdl/top/protocol_processor_top.sv:4407` | originator lane head withdrawal reads `org_withdraw_mask_r` |
| `hdl/top/protocol_processor_top.sv:4427` | lane-queue compaction reads `org_withdraw_mask_r` |
| `hdl/top/protocol_processor_top.sv:4505` | the arbiter's `start_abort_i` (`arb_start_abort_w`) reads `org_withdraw_mask_r` |
| `hdl/packet_engine/KL_pp_tx_arbiter.sv:161-196` | selection: the serial best-so-far scan replaced by a pairwise rank (winner = the eligible requester no other eligible one outranks; ties to the lowest index), the same function |

All three readers of the mask move together: a lane that dropped its head on the
combinational mask while the arbiter accepted it on the registered one would pop twice.
No existing register could be moved instead: the arbiter's existing `pend_r` cut is
re-entered by `start_abort_i` and the live request, and both carry the mask in the clock
the originator decides, so a cut on this cone necessarily delays that decision by one
clock. The selection restructure adds no clock.

Benches and documentation (`916f53c7`, `2ef802cb`, `cd9825c9`):

| File:line | Change |
|---|---|
| `tb/pp_top/notify_phases.hpp:1642-1824, 1856-1861` | section WD (`WithdrawStagePhase`), `run_withdraw` |
| `tb/pp_top/sim_main.cpp:836-838, 1620-1624, 2058` | harness: let a byte held at eof go on a bit of the validator's commit shift |
| `tb/pp_top/sim_main.cpp:14062, 14069-14070, 14090` | `--withdraw-only`; WD in the default run (after CS, before the counters and AQ) |
| `tb/pp_top/pp_top_wrap.sv:487-495, 905-910` | taps `dbg_rxv_commit_o`, `dbg_arb_st_o`, `dbg_arb_owner_o`, `dbg_arb_sent_o` |
| `tb/pp_top/Makefile:122-124, 228` | `make withdraw` |
| `tb/pp_top/notify_mutants.py:353-384` | arms `withdraw_unregistered`, `withdraw_abort_ignored` (suite `--withdraw-only`), `cancel_one_clock_late` (`tb/aecp_notify`) |
| `tb/aecp_notify/sim_main.cpp:84, 98-147, 273, 717-750` | section CX (`cancel_clock`); `registers()`/`draws()` split out of `register_row`/`complete_draw` so CX's setup adds no unmutated check |
| `tb/pp_top/README.md:2229-2241, 2466-2501, 2503-2595` | the C6 intro, section WD, the notify mutation record (three rows, the re-run, `ix_new_identity_unset` +CX1) |
| `tb/aecp_notify/README.md` | build table, mutation record row, `ix_new_identity_unset` +CX1, section CX (204-220) |
| `tb/tx_arbiter/README.md:53, 59-67` | M3's planted text, the M1-M5 re-plant and the equivalence proof |
| `docs/architecture/03_packet_engine.md:488` | a "Withdrawal" rule row in §8 |

### Pre-edit grep (assignment item 3)

Before the RTL edit, every removed line (12) was searched with `git grep -F` at `86a7b0c5`
across `tb/**/*.patch`, `tb/**/*.py` (every exact-text driver table) and `tb/**/README.md`,
then across all of `tb`, `scripts`, `syn` and `docs`: 0 hits for every line. No patch or
exact-text arm carries a changed line.

Every arm still plants:
- All 283 `tb/**/*.patch` apply (`git apply --check` on an export) at base and at the head,
  0 refused.
- Every campaign arm planted at the head: no REFUSED verdict in any campaign (sections 6).
- The arbiter README's M1-M5 (hand-planted records) were re-planted at base and head in
  scratch copies, with identical failing-check lists at both: M1 13, M2 6, M3 23, M4 30 and
  M5 2 of 66. M3's text moved with the selection (`<=`/`<` to `>=`/`>`), the same inversion.

### Arbiter equivalence

Yosys `equiv_make`, `equiv_simple -seq 2`, `equiv_induct -seq 2` and `equiv_status -assert`
on the old and the new `KL_pp_tx_arbiter` (lowered with sv2v, memories mapped to flops):
438 of 438 `$equiv` cells are proven at the top's parameters (8 lanes, the top's priority
map and solicited mask), and 386 of 386 at the module defaults. Control: the same proof
with the tie compare `<=` planted as `<` leaves 3 unproven and fails. The selection adds no
cycle and changes no behaviour; `tb/tx_arbiter` passes 66 of 66, unchanged.

## 3. The added cycle, its graded checks and mutants

One cycle is added. A cancellation (the originator's response, cancel or final-expiry
choice) now reaches the originator lane, the lane compaction and the arbiter's pre-start
abort one clock after the originator takes it. That is the clock its registered release
reaches the slot pool. The protocol-visible effect is that the race between a cancellation
and the serializer's acceptance moves by one clock:

- A probe whose cancellation lands on its acceptance clock is now sent (before, it was
  withdrawn). Its exchange is gone (no timer, no retry), the originator drops the
  acceptance, and the pool frees the slot after the last byte.
- A cancellation on the selection clock still withdraws the probe, one clock later and
  before the pool starts it.

| Check | Bench | Grades | Mutant(s) that fail it |
|---|---|---|---|
| WD1 | `tb/pp_top` (section WD, `--withdraw-only` and the default run) | cancellation on the acceptance clock: the probe leaves once, byte-exact; no retry and no deregistration in 1.5 s; both answers leave; 5 slots, the originator and its lane idle | `withdraw_unregistered` (the three readers back on the combinational mask) |
| WD2 | `tb/pp_top` | cancellation on the selection clock: the arbiter's start state holds that selection the next clock, aborted, and is idle the clock after; no pool start | `withdraw_unregistered`, `withdraw_abort_ignored` (`start_abort_i` tied low) |
| WD3 | `tb/pp_top` | that probe never reaches the wire; answers leave; slots, the originator and its lane idle | `withdraw_abort_ignored` |
| CX1 | `tb/aecp_notify` | the registry monitor's cancellation is in the command's own clock and in none of the 8 after it: the notification module adds no clock, so the top's stage is the only one | `cancel_one_clock_late` (also fails the existing IX3); `ix_new_identity_unset` (existing arm) now fails it too |

In the campaigns (section 6), `notify_mutants.py` kills all three new arms by exactly their
named checks at the head, and its goldens (`tb/aecp_notify` run, `tb/pp_top
--withdraw-only`) pass. WD's clock trace at the head:
- acceptance case: `[-1 idle] [0 start, lane 7, not started, pool start] [+1 started]`,
  1 probe;
- selection case: `[0 idle, head queued] [+1 start, lane 7, not started, no pool start]
  [+2 idle]`, 0 probes.

WD lets every waiting lane age past T-TX-AGING (12 ms) before the race. Without that, an
aged SRP frame outranks the fresh probe and WD has no probe to race (seen and fixed during
development).

Records the assignment names, so expected to differ base to head:
- `tb/pp_top`: +3 checks (WD in the default build).
- `tb/aecp_notify`: +1 check (CX1).
- `notify_mutants.py`: +3 arms and +1 golden; `ix_new_identity_unset` fails CX1 as well.
- Two parent-consumer counts move with those files: the parent's Python idiom gate counts
  31 more first-party Python lines (the new arms), and the port-contract gate 6 more
  test-only hierarchical observations (the 6 internal nets the new wrap taps read).

## 4. OOC 1x1 area and timing, before and after

| Scope (#638 recipe, OOC 1x1) | LUT before | LUT after | delta | FF before | FF after | delta |
|---|---:|---:|---:|---:|---:|---:|
| wrapper (KL_pp_shadow) | 23179 | 23160 | -19 | 19779 | 19787 | +8 |
| `u_pp` (processor) | 22517 | 22478 | -39 | 18941 | 18951 | +10 |
| `(u_pp)` own logic | 939 | 780 | -159 | 2033 | 2039 | +6 |
| `u_tx_arbiter` | 185 | 234 | +49 | 187 | 187 | 0 |
| `u_originator` (unchanged) | 697 | 676 | -21 | 885 | 885 | 0 |
| `u_notify` (unchanged) | 2125 | 2157 | +32 | 1256 | 1258 | +2 |

The STOP bar (60 LUT, 120 FF) is not reached on any scope. The processor is -39 LUT / +10
FF, the two changed blocks' own logic -110 LUT / +6 FF together, and the arbiter alone +49
LUT. `pp_resource_gate.py check` RESULT PASS at both (against the parent's recorded
baseline: LUT -18, FF +11 at head). Unchanged blocks move by synthesis noise only.

| OOC timing summary | Before | After |
|---|---:|---:|
| WNS (ns) | -3.562 | +3.337 |
| TNS (ns) | -37.519 | 0.000 |
| Failing endpoints | 16 of 62840 | 0 of 62857 |
| WHS (ns) | +0.159 | +0.159 |
| Worst path | notify `pend_r` -> arbiter `slot_r`, 47 levels | `u_aecp/u_ucpu desc_base_r` -> `u_aecp/u_d3 deb_cnt_r`, 32 levels (not this cone) |

Worst five paths into the arbiter (`report_timing -to` the arbiter's sequential cells):

| # | Before: source -> endpoint, levels, slack (ns) | After: source -> endpoint, levels, slack (ns) |
|---|---|---|
| 1 | notify `pend_r[2]` -> `slot_r[0]`, 47, -3.562 | CA builder `cancel_release_slot_o[2]` -> `slot_r[0]`, 16, +11.912 |
| 2 | notify `pend_r[2]` -> `slot_r[1]`, 47, -3.562 | same -> `slot_r[1]`, 16, +11.912 |
| 3 | notify `pend_r[2]` -> `slot_r[2]`, 47, -3.562 | same -> `slot_r[2]`, 16, +11.912 |
| 4 | notify `pend_r[2]` -> `owner_r[0]`, 46, -3.417 | same -> `owner_r[1]`, 15, +12.057 |
| 5 | notify `pend_r[2]` -> `owner_r[1]`, 45, -2.930 | same -> `owner_r[0]`, 14, +12.296 |

The parent three-directive sweep is for the pin adoption (acceptance item 3), not run here.

## 5. Processor suites and gates

Base `86a7b0c5`, head `2ef802cb` (the full set), and final head `cd9825c9` (the full set
again; `2ef802cb..cd9825c9` changes two README files only). Every run has its own `git
archive` export, log, rc and command/time record. `make check` ran in the lane: base on a
detached checkout, then back to the branch.

| Gate | Base rc | `2ef802cb` rc | Final rc | Records |
|---|---:|---:|---:|---|
| `scripts/run_suites.sh` | 0 | 0 | 0 | base 1,028,235 checks, 0 failing; head 1,028,239, 0 failing. Every suite line is identical except `aecp_notify` 45 -> 46 and `pp_top` 10,444 -> 10,447. The final log is byte-identical to `2ef802cb`'s |
| `scripts/lint_hdl.sh` | 0 | 0 | 0 | byte-identical at all three |
| `make -j8 check` | 0 | 0 | 0 | identical sorted records (concurrent recipe order varies) |
| `python3 scripts/gen_matrix.py --check` | 0 | 0 | 0 | byte-identical (`matrix: OK (94 rows, 0 untested)`) |
| `syn/yosys/run.sh` | 0 | 0 | 0 | identical except the lowered `all.v` line numbers cited in four memory-to-register warnings (the arbiter's source is 11 lines longer); every verdict identical. Final byte-identical to `2ef802cb` |

Suites (base / head): acmp_listener 3111, acmp_nvm 388, acmp_talker 1342, adp_engine 1348,
aecp_notify 45 / 46, ca_originator 16, desc_mem_guard 78, desc_store 586, dispatch 211,
dyn_state 118, event_router 81, lsn_admit 18, maap 196, nvm_port 1219, originator 107,
pp_top 10444 / 10447, prng 76, release_merge 18, resp_buf 64, rx_slots 130,
rx_validator 555, scoreboard 3705, side_port 368, srp_admission 991231, srp_decoder 190,
srp_encoder 581, srp_stream_fsms 1347, srp_top 8656, timer_map 1360, timer_service 48,
tx_arbiter 66, tx_slots 95, ucpu 437. All PASS at both.

## 6. Campaigns (base / head)

Every campaign driver in the tree, `--jobs 2`, at base and at `2ef802cb`, then at the final
head. Seconds are wall time under the shared two-build limit. At the final head every
campaign's records equal `2ef802cb`'s (driver logs byte-identical, or identical when sorted
where arms complete in a varying order); no arm was REFUSED at any revision.

| Campaign | Base | `2ef802cb` | Final | Comparison |
|---|---|---|---|---|
| `tb/pp_top/d3_mutants.py` | rc 0, 110 of 110 KILLED, goldens PASS (7794 s) | rc 0, same (8020 s) | rc 0, same (7186 s) | records identical; driver log identical when sorted (completion order) |
| `tb/pp_top/aecp_mutants.py` | rc 0, `67 checks: 67 PASS` (2022 s) | rc 0, same (2144 s) | rc 0, same (1704 s) | driver log byte-identical |
| `tb/pp_top/notify_mutants.py` | rc 0, 56 of 56 KILLED, goldens PASS (1659 s) | rc 0, 59 of 59 KILLED, goldens PASS (1735 s) | rc 0, 59 of 59 KILLED (1594 s) | named: +3 arms, +1 golden; `ix_new_identity_unset` fails CX1 too; the other 55 earlier records identical. Final identical to `2ef802cb` when sorted |
| `tb/pp_top/aecp_dispatch_mutants.py` | rc 0, `44 checks: 44 PASS`, 40 KILLED (1367 s) | rc 0, same (1425 s) | rc 0, same (1147 s) | driver log byte-identical |
| `tb/pp_top/acmp_mutants.py` | rc 0, 33 of 33 KILLED (2051 s) | rc 0, same (2041 s) | rc 0, same (2288 s) | records identical; log identical when sorted |
| `tb/pp_top/gsi_mutants.py` | rc 0, 20 detected, golden and restored PASS (1471 s) | rc 0, same (1408 s) | rc 0, same (729 s) | driver log byte-identical |
| `tb/pp_top/ctr_mutants.py` | rc 0, `18 checks: 18 PASS` (958 s) | rc 0, same (542 s) | rc 0, same (614 s) | driver log byte-identical |
| `tb/pp_top/name_wr_mutant.py` | rc 0, decode killed, golden and restored PASS (151 s) | rc 0, same (165 s) | rc 0, same (80 s) | driver log byte-identical |
| `tb/adp_engine/mutants.py` | rc 0, `43 checks: 43 PASS` (365 s) | rc 0, same (490 s) | rc 0, same (352 s) | driver log byte-identical |
| `tb/maap/mutants.py` | rc 0, `32 checks: 32 PASS` (668 s) | rc 0, same (760 s) | rc 0, same (241 s) | driver log byte-identical |
| `tb/srp_top/mutants.py` | rc 0, `137 checks: 137 PASS` (2515 s) | rc 0, same (2884 s) | rc 0, same (2791 s) | driver log byte-identical |
| `tb/srp_admission/mutants.py` | rc 0, `12 checks: 12 PASS` (521 s) | rc 0, same (541 s) | rc 0, same (730 s) | driver log byte-identical |
| `tb/acmp_talker/retry_mutants.py` | rc 0, 62 killed, 7 equivalence and 1 performance controls (462 s) | rc 0, same (383 s) | rc 0, same (332 s) | driver log byte-identical |

## 7. Parent consumer set (17), dev `28f9666f` + 148 + 22

The scratch parent: a clone at dev `28f9666feab2b2ba287643c63ed3a16b1e0bb863`, the supplied
`parent-adoption-148-6c22d3ca.patch` applied first with `git apply`, then
`parent-adoption-22-28f9666f.patch`; never committed or pushed. Both patches reverse-check
cleanly against the tree, and the tree differs from dev only by them and the staged
processor gitlink. Timing processor `5dce647a` and AXIS dependency `48ff7a7e` stay at their
recorded pins; the external leaf is not initialized. Each submodule's top level is verified
before any Git command in it and before each consumer starts. The OOC recipe's links (the
builder output and two ROM links) were removed before the consumers ran. Each run's
generated files were moved aside before the next revision was staged.

The set ran at base (gitlink `86a7b0c5`), at `2ef802cb` (all but 09) and at the final head
(gitlink `cd9825c9`, where the scratch parent is left). 09 ran last, alone, at base and at
the final head, each after queueing for the shared Vivado lock.

| Consumer | Command | Base rc | `2ef802cb` rc | Final rc | Comparison |
|---|---|---:|---:|---:|---|
| 01_cpp | `python3 scripts/check_cpp_idiom.py` | 0 | 0 | 0 | identical (at `916f53c7` it refused one multi-declarator line: fixed by `2ef802cb`) |
| 02_py | `python3 scripts/check_py_idiom.py` | 0 | 0 | 0 | named: first-party Python lines 199,997 -> 200,028 (the new arms) |
| 03_sources | `python3 scripts/check_rtl_source_lists.py` | 0 | 0 | 0 | identical |
| 04_pp_sources | `python3 scripts/pp_srcs.py --check --selftest` | 0 | 0 | 0 | identical |
| 05_ports | `python3 scripts/check_port_contracts.py` | 0 | 0 | 0 | named: test-only hierarchical observations 317 -> 323 (the wrap's 6 new reads) |
| 06_naming | `python3 scripts/measure_naming.py --check` | 0 | 0 | 0 | identical |
| 07_evidence | `python3 scripts/measure_test_evidence.py --check` | 0 | 0 | 0 | identical |
| 08_docs | `python3 scripts/docs_check.py` | 0 | 0 | 0 | identical |
| 09_xvlog | `python3 scripts/xvlog_gate.py --check` (under the Vivado lock, alone) | 0 | not run | 0 | 0 findings at both (73 parent and 52 pinned-processor sources); identical except the pinned-revision line |
| 10_builder | `python3 sw/builder/test_builder.py` | 0 | 0 | 0 | identical except temp-directory names and durations; 1 gate arm not run at each (gate 11's calibration needs a reference build tree that is not on disk), as recorded before |
| 11_lint | `python3 scripts/lint_rtl.py --check` | 0 | 0 | 0 | identical (90 <= ratchet 90) |
| 12_shadow | `make -j8 -C tb/verilator/pp_shadow` | 0 | 0 | 0 | 606, 606, 646, 311 checks, 0 failures at each (print order varies with build concurrency); per-check lines identical |
| 13_nvm_lint | `make -j8 -C tb/verilator/nvm_cosim lint` | 0 | 0 | 0 | identical except Verilator wall-time lines |
| 14_nvm_quick | `make -j8 -C tb/verilator/nvm_cosim quick` | 0 | 0 | 0 | nvm_cosim 315 checks, 315 PASS at each |
| 15_datapath | `make -j8 -C tb/verilator/milan_dp VERILATOR_JOBS=2` | 0 | 0 | 0 | every tally line identical (sorted) at each |
| 16_render | `make -j8 -C tb/verilator/milan_dp_render VERILATOR_JOBS=2 MUTANT_JOBS=2` | 0 | 0 | 0 | tdm8_render 65 and 245 checks, 0 failures; 5 leg-defect arms PASS; identical at each |
| 17_shell | `python3 scripts/check_sh_idiom.py` | 0 | 0 | 0 | identical |

15_datapath records (each run): gmstep 104; 182 and 182; milan_datapath 236 (1 guarded);
421; 416; 1961, 1961, 3746, 1961; milan_datapath 236 (1 guarded); 33; milan_datapath 233
(5 guarded); media_aclk 193; 6 and 6; all 0 failures.

## 8. Environment and method

- Pinned Verilator 5.050, ahead of the host default on PATH, through a scratch wrapper.
  The wrapper allows two `--build` invocations at once service-wide and turns their
  `--build -j 0` into `-j 2`. `MAKEFLAGS=-j8`, `VERILATOR_JOBS=2`, campaign drivers
  `--jobs 2`.
- The memory logger (20 s) reclaims page cache through the service's `memory.reclaim` when
  memory.current passes 8 GiB. Peak anonymous memory during the gate runs was 5.6 GB (the
  parent's lint fan-out); Vivado's OOC synthesis peaked at 10.2 GB anonymous and ran alone.
- Vivado ran only under the lock and never beside another job of this lane.
- No hardware, bench or flashing; no push, PR or comment other than TAKEN/REVIEW READY.

## 9. Retained evidence (scratch root; sizes and sha256)

Scratch root: `$VALIDATION_STORAGE/pp163-a553`. Scripts: `scripts/` (measure.py, stage.sh, export.sh, arb_paths.tcl, arb_cone.tcl, cone_summary.py, stage_paths.tcl, gates2.py, run_parent.py, patch_audit.py, txarb_mutants.py, compare_camps.py, memlog.sh, wait.sh, wait2.sh). Each gate run keeps a `.log`, `.rc` and command/time `.json` under `logs/base`, `logs/head` (`2ef802cb`), `logs/final` (`cd9825c9`) and `logs/parent-*`. The small evidence files are also copied into `evidence/` beside this handoff.

| Scratch-relative artifact | Bytes | sha256 |
|---|---:|---|
| `evidence/arbiter-equivalence.txt` | 320 | 56a0117007841c866b578ad6c208b59dbf24085f5bb5515894296dda8eb5f8d4 |
| `evidence/arbiter-standalone-levels-base.tsv` | 18958 | a01b06cc4cea9666de79f2d98acd7dda3d95e214a7b6187d0d4aa772e2f2a04f |
| `evidence/arbiter-standalone-levels-head.tsv` | 18953 | bdb82da04751159721a40885f2cd1cfa68e2f5d5ec7d1a52417f5ebb63a5f0d5 |
| `evidence/cone-summary-base-over20.txt` | 98928 | a5c7ee23b571f3b722053e997079d84b845608cba9e4b483a82c6a5c417608d0 |
| `evidence/cone-summary-head-all.txt` | 16459 | 58cc8133286563c8b2f55f6aef68e48801f4cc6c85f607cd61986e8b30646984 |
| `evidence/parent-diff.patch` | 1648 | ef03d745d30bcd624ce76a61d778d7d98dbfa2fbdd37b4540ee926fa0f3bda11 |
| `evidence/patch-audit-base.json` | 88 | 8f6f7008610fe65bf5d8a52336e1e0c4c583cb2a1ce56021d0e6cf3d797e8232 |
| `evidence/patch-audit-final.json` | 88 | f108fd46d3698c439cdaa23b96e09c25743dd50c5d27139c91fc7e379ac13add |
| `evidence/patch-audit-head.json` | 88 | 9d9412f1acc96da0540a686bdb5f57cb2b48f2bda9bd0e7e16378778518b476a |
| `evidence/pre-edit-grep-alltb.txt` | 515 | 18685df0ac73161c162af6619300f8f930b2bbf6878fb3945ecbd293f600944f |
| `evidence/pre-edit-grep.txt` | 589 | 66c8296db91cdbf9cd74c4d0103bfa369f036c94bb22fd024e94d3498cd50db5 |
| `evidence/rtl-old-lines.txt` | 554 | b4101fbcbaf0eeffb70bcab8722e0aac52abed2e21dd1b747680c17873af947e |
| `evidence/stage-paths-base.tsv` | 562 | 6d462ddec875a4c14568e03b1db303146aa77d78167db3921eaf1bf8c4bbfaf1 |
| `evidence/stage-paths-head.tsv` | 951 | f449b7f5d0745b093814ee56d06206bb26b6c9fa99c1bf4cd54985bc0e454d65 |
| `evidence/txarb-m1-m5-base.json` | 1085 | da93656a59b071291ecc1ed345fc610dc5eb79b51753c92f6500ab069150b535 |
| `evidence/txarb-m1-m5-head.json` | 1085 | da93656a59b071291ecc1ed345fc610dc5eb79b51753c92f6500ab069150b535 |
| `meas/paths-base/arb_cone.tsv` | 23794238 | f847be597785eacc0748770ee088ab56ffbbfefab46b6a37af23cbab47c7a132 |
| `meas/paths-base/arb_worst5.rpt` | 94864 | 5bd1965e1f417346aca683fbf8d9d234080cd79d24e22598ed0d831fa98af784 |
| `meas/paths-base/arb_deep5.rpt` | 96657 | 6159610327c57e38d6d6283540643a87aa52c1b97e7ddef556b5246cd158db32 |
| `meas/paths-base/arb_timing_summary.rpt` | 175884 | 390f5eac466068362bce9f35ebcd978cd9a580f678455f880950b1bb613f7846 |
| `meas/ooc-base/baseline_timing.rpt` | 175838 | aaf226628c53e1cf849a2e0acdf49fb5a7f44fece170b5dc02c00fcdbff0f0ad |
| `meas/ooc-base/baseline_hierarchy.rpt` | 10264 | a0892e836ee2f3393f5ef385a3ff092e1ad132d063fe151ba1d7d007269a1181 |
| `meas/ooc-base/baseline_synth.dcp` | 8906633 | d82658c001fe58f3c8eb3951ff3367ee623f3da872db310af11970a6154721ba |
| `meas/ooc-base/baseline_parameters.json` | 638 | 62cff771bc5f5552dccea38044605d4d146e039201a43993f95514c359538f4c |
| `meas/record-base.stdout` | 6945 | b583d463c9e7ce70b300c115f7b925c60d3e83ff5641ead47aacc989d881ed9d |
| `meas/gate-base.stdout` | 856 | f4e435b6625858d4727638dc95d0e73292662cffaa124d4ce87102a45ea5205b |
| `meas/paths-head1/arb_cone.tsv` | 1467745 | d859df8d7d8dc5993980804a35cb1f99101fa9656ed6e22a6f812069d4a83447 |
| `meas/paths-head1/arb_worst5.rpt` | 43261 | 25b8853af6b545aca2393a6f33f91b9d7cc03436a9c3df52fe13e06750850996 |
| `meas/paths-head1/arb_deep5.rpt` | 45343 | b30160923cdce7d404992639bd7c6772f32b154e5a9ca66b404e86329fd76a99 |
| `meas/paths-head1/arb_timing_summary.rpt` | 155738 | f7854dac2c73c637ed2402cd0bed3c316cb8da0475aa540b7b7a8054dc11673c |
| `meas/ooc-head1/baseline_timing.rpt` | 155691 | 8af230c3804166c7321679ae4b44c0f438f91d95c2fd59bfe4e34fb2faf582c6 |
| `meas/ooc-head1/baseline_hierarchy.rpt` | 10264 | 2b2e177b330cd354fc27dd77174a3e342885a2e0bde5aa666df33a24deeab7a8 |
| `meas/ooc-head1/baseline_synth.dcp` | 8896835 | 158c11f359d9d5163cce8a48a839686af0664100576c7abd41c84e8abf46f183 |
| `meas/ooc-head1/baseline_parameters.json` | 638 | 62cff771bc5f5552dccea38044605d4d146e039201a43993f95514c359538f4c |
| `meas/record-head1.stdout` | 6944 | 0aa0e19eeec986168f27e860b8e2556fe570bc28e4aa652446bf61bbcf92111e |
| `meas/gate-head1.stdout` | 862 | 538a97c7863f0c74b609be7e1bdfb697caf017b858b62bb7cac9136db0715cf2 |
| `logs/base/suites.log` | 1750 | df917fd7f7c567301910a597e0d8b8f4fb8f6423c269b6dace013323b7d5e751 |
| `logs/base/check.log` | 410 | 4988bca941797441c2381dcd8f2a89caa2d9efe1b1b89cedecedfd2cf2cbf9d7 |
| `logs/base/lint.log` | 1056 | 9a3703ba1ec6767b277e9d5102c94a93fe107454da19d13cab518ba312cd1e81 |
| `logs/base/matrix.log` | 33 | 7a2c98136a0892f195fa6a08ad82dfe7e36e8a81d0732cb304584f31e966e097 |
| `logs/base/yosys.log` | 3548 | 5918894aeb86257a2ba105f0914f534c8ab77338863151178375bed543a51a82 |
| `logs/base/camp-notify.log` | 4605 | 561658100a8cdf3a4aafcfe5ad13501ad478e59fc1227133a59066344769bfce |
| `logs/base/camp-d3.log` | 8131 | 64ff44059ffa0c9d990ef26621d85cf8c6f1278329aa7f1c47d929b0ed7f537d |
| `logs/base/camp-aecp.log` | 78512 | 53d881784de32314b33d1e973813dacb1f3d85468dc2d1e6e94b1efe1d5ab698 |
| `logs/base/camp-aecp_dispatch.log` | 28893 | 0dd8b97ab8f9a89f6dad0388f0e6c83eb7bd37eb5a6f5bf47eda9954ff4222f6 |
| `logs/base/camp-acmp.log` | 2904 | 16c1e07d5077b54ba84a5d7e187ecacd3a9cf3622d6fa6c221fe3427365e1963 |
| `logs/base/camp-gsi.log` | 4150 | 5f6d67707db7bfed9d8aa1e323a7f3b0884134404c78e43b0b2afbd99953237b |
| `logs/base/camp-ctr.log` | 11207 | dcd55eac8ffb06c36b2366e59a0ef5c517271e7751a3e948aa650dcffa178570 |
| `logs/base/camp-name_wr.log` | 2550 | 055560a7d55d359d9281385f1d47fcddba0b082ac963195a2ce4201fdd4efe7a |
| `logs/base/camp-adp.log` | 33445 | f69c577b96367e850478d3068e7bca2d77be103f747ff6e9bd1cceec8485e95e |
| `logs/base/camp-maap.log` | 7591 | 823ef7e638f720b03e151b4954e75a5b023fa034efda1171f57264a208ff3c81 |
| `logs/base/camp-srp_top.log` | 9988 | ec920575b69b9fccc7fa3d0a279308d3465887cc59c7c5747aea6a374be00467 |
| `logs/base/camp-srp_admission.log` | 479 | 6977d367d954c85cbb07f2f44ac0fb7a5ab3267f627556647a22a1bf95b798fc |
| `logs/base/camp-retry.log` | 3865 | 7bda8adf83703e45161d30a04b76f39855701cbb5b9b7c1979473aa7ba6c2512 |
| `logs/head/suites.log` | 1750 | db2b89a5fc8c41c9f40f791c12e5713560694cefbdb2a19d6ef64600d4922bfb |
| `logs/head/check.log` | 410 | ad4d29d74bf789a44ee31cc6398be449e4d465735b95f3bb8c25564c62e8b2bb |
| `logs/head/lint.log` | 1056 | 9a3703ba1ec6767b277e9d5102c94a93fe107454da19d13cab518ba312cd1e81 |
| `logs/head/matrix.log` | 33 | 7a2c98136a0892f195fa6a08ad82dfe7e36e8a81d0732cb304584f31e966e097 |
| `logs/head/yosys.log` | 3548 | bee608b28b73fa2fa502b40b30dbdeada7560af46bd0a21f0bece4b3ca0b23fb |
| `logs/head/camp-notify.log` | 4883 | 7312611052d60315c351cfcd62143efe69b7b79f5a5f4516381435a2560718c9 |
| `logs/head/camp-d3.log` | 8131 | d78468b85c9902d16b9e35c883312ecccd10650b0dc23ffd8177e4c9914ab36b |
| `logs/head/camp-aecp.log` | 78512 | 53d881784de32314b33d1e973813dacb1f3d85468dc2d1e6e94b1efe1d5ab698 |
| `logs/head/camp-aecp_dispatch.log` | 28893 | 0dd8b97ab8f9a89f6dad0388f0e6c83eb7bd37eb5a6f5bf47eda9954ff4222f6 |
| `logs/head/camp-acmp.log` | 2904 | da12ea3006e0fe79e1cc637417ba9cb195e02b550523b5a4eb2fc376de19fc85 |
| `logs/head/camp-gsi.log` | 4150 | 5f6d67707db7bfed9d8aa1e323a7f3b0884134404c78e43b0b2afbd99953237b |
| `logs/head/camp-ctr.log` | 11207 | dcd55eac8ffb06c36b2366e59a0ef5c517271e7751a3e948aa650dcffa178570 |
| `logs/head/camp-name_wr.log` | 2550 | 055560a7d55d359d9281385f1d47fcddba0b082ac963195a2ce4201fdd4efe7a |
| `logs/head/camp-adp.log` | 33445 | f69c577b96367e850478d3068e7bca2d77be103f747ff6e9bd1cceec8485e95e |
| `logs/head/camp-maap.log` | 7591 | 823ef7e638f720b03e151b4954e75a5b023fa034efda1171f57264a208ff3c81 |
| `logs/head/camp-srp_top.log` | 9988 | ec920575b69b9fccc7fa3d0a279308d3465887cc59c7c5747aea6a374be00467 |
| `logs/head/camp-srp_admission.log` | 479 | 6977d367d954c85cbb07f2f44ac0fb7a5ab3267f627556647a22a1bf95b798fc |
| `logs/head/camp-retry.log` | 3865 | 7bda8adf83703e45161d30a04b76f39855701cbb5b9b7c1979473aa7ba6c2512 |
| `logs/final/suites.log` | 1750 | db2b89a5fc8c41c9f40f791c12e5713560694cefbdb2a19d6ef64600d4922bfb |
| `logs/final/check.log` | 410 | ad4d29d74bf789a44ee31cc6398be449e4d465735b95f3bb8c25564c62e8b2bb |
| `logs/final/lint.log` | 1056 | 9a3703ba1ec6767b277e9d5102c94a93fe107454da19d13cab518ba312cd1e81 |
| `logs/final/matrix.log` | 33 | 7a2c98136a0892f195fa6a08ad82dfe7e36e8a81d0732cb304584f31e966e097 |
| `logs/final/yosys.log` | 3548 | bee608b28b73fa2fa502b40b30dbdeada7560af46bd0a21f0bece4b3ca0b23fb |
| `logs/final/camp-notify.log` | 4883 | 44b7646ab978406dd9d2910cec7f27da2525559a5c93ff0e6032622ab33ea55d |
| `logs/final/camp-d3.log` | 8131 | edaf2137c3bb27ae3aaad71228fca4d9fa7324562e36afdbab85556b1432a50e |
| `logs/final/camp-aecp.log` | 78512 | 53d881784de32314b33d1e973813dacb1f3d85468dc2d1e6e94b1efe1d5ab698 |
| `logs/final/camp-aecp_dispatch.log` | 28893 | 0dd8b97ab8f9a89f6dad0388f0e6c83eb7bd37eb5a6f5bf47eda9954ff4222f6 |
| `logs/final/camp-acmp.log` | 2904 | c670e10aaf6a258f7f11d11b168c11840913b288dc60c295d5e65c4ef96de163 |
| `logs/final/camp-gsi.log` | 4150 | 5f6d67707db7bfed9d8aa1e323a7f3b0884134404c78e43b0b2afbd99953237b |
| `logs/final/camp-ctr.log` | 11207 | dcd55eac8ffb06c36b2366e59a0ef5c517271e7751a3e948aa650dcffa178570 |
| `logs/final/camp-name_wr.log` | 2550 | 055560a7d55d359d9281385f1d47fcddba0b082ac963195a2ce4201fdd4efe7a |
| `logs/final/camp-adp.log` | 33445 | f69c577b96367e850478d3068e7bca2d77be103f747ff6e9bd1cceec8485e95e |
| `logs/final/camp-maap.log` | 7591 | 823ef7e638f720b03e151b4954e75a5b023fa034efda1171f57264a208ff3c81 |
| `logs/final/camp-srp_top.log` | 9988 | ec920575b69b9fccc7fa3d0a279308d3465887cc59c7c5747aea6a374be00467 |
| `logs/final/camp-srp_admission.log` | 479 | 6977d367d954c85cbb07f2f44ac0fb7a5ab3267f627556647a22a1bf95b798fc |
| `logs/final/camp-retry.log` | 3865 | 7bda8adf83703e45161d30a04b76f39855701cbb5b9b7c1979473aa7ba6c2512 |
| `camp/base/camp-notify/results.json` | 108474 | 20944a574eae961e9ff19ee5da60c9496ed8d0c3068cf5038521f44cb775bedb |
| `camp/base/camp-d3/results.json` | 155047 | 17f15ea2380a1ba3ecb84bb0876a1433825cbba2f57b977e2eaffc928f6f4d2f |
| `camp/base/camp-acmp/results.json` | 96457 | f21adc920863fd17d46e096d1799fb7134bb140c0ac1e11790eca49c8ba7bea0 |
| `camp/base/camp-aecp_dispatch/results.json` | 7629 | f82db07ae244a5947b85a1b3c55b8afb4930eba7267667179945155db01c5167 |
| `camp/head/camp-notify/results.json` | 110558 | dd5a904ddbbbef908591f6182eaf47ddef8415521bbe2f08d8477f2bd2f0b523 |
| `camp/head/camp-d3/results.json` | 155047 | bfc74e3034cd9e59531a2430057852ab8843f4df1ae9be5a71c8f856e1296e40 |
| `camp/head/camp-acmp/results.json` | 96457 | 10ce2ad4196ff1e3919ceec4b07c663966464578d7d2db9ae4706bd53158136b |
| `camp/head/camp-aecp_dispatch/results.json` | 7629 | f82db07ae244a5947b85a1b3c55b8afb4930eba7267667179945155db01c5167 |
| `camp/final/camp-notify/results.json` | 110558 | 38a8d4255f840468aa64213ce1d66a4c3e72c77c9dfe9e027c14fc0691546a54 |
| `camp/final/camp-d3/results.json` | 155047 | 543192023b2940a82fb4cb3d4d43da9ab822e4ecb17bec6cb884702288db2b90 |
| `camp/final/camp-acmp/results.json` | 96457 | 5ba1a4604dfd9a3996963d42f701178cff49054acd01fd821cdd705f2764d0ba |
| `camp/final/camp-aecp_dispatch/results.json` | 7629 | f82db07ae244a5947b85a1b3c55b8afb4930eba7267667179945155db01c5167 |
| `logs/parent-base/01_cpp.log` | 315 | 20d9e296340ae6319c913211b7a2b7d63b6cc89798c011092c87908916634810 |
| `logs/parent-base/02_py.log` | 461 | f88c9566c9b5ef80cc54f722065566445a1849097ba87a7c50f07f2be6ecf0c6 |
| `logs/parent-base/03_sources.log` | 153 | ed979d7e26c3cd7a6f14364c11994089b77632424d04252613eeed458ebc8a95 |
| `logs/parent-base/04_pp_sources.log` | 955 | fad5e1b9dd5f465b7fcb2334e2abe6c6db44be93b5bb12afb3a35f3ebf432e1a |
| `logs/parent-base/05_ports.log` | 421 | b04fbab06614655f710f529fa8d2cdbd59073e9a63f179b308734b9e21f35c23 |
| `logs/parent-base/06_naming.log` | 36608 | db23d3d49d070f855b77fbe71e83f3cc24b00ae81d2c288082eb016ac2820e77 |
| `logs/parent-base/07_evidence.log` | 13902 | bb9aadc07a14eb4e219e87fa681571c7886f1ef0be545cbae69d099b66fd7f44 |
| `logs/parent-base/08_docs.log` | 127 | 6a6b0baa714d34c94d863882cab86a5eac8309164fc1a6c99cb5659f049510ee |
| `logs/parent-base/09_xvlog.log` | 721 | 764444287ab24c7e9a58eae8261d5ee31e46da0ca6e59798c254107bef0a47c3 |
| `logs/parent-base/10_builder.log` | 101822 | 0b6afed831b34f10a78416a619988086839f37805d03af5fc5082c5d1657d0c3 |
| `logs/parent-base/11_lint.log` | 14186 | 9087b44973869192bcab894931d990c7976fb895a8d92b6c243c555087f69d6e |
| `logs/parent-base/12_shadow.log` | 276059 | 6a48c4ea0e1210f146e6c42bec83dd02a1b9ca595e0122e0b29b440a0ed4f3ee |
| `logs/parent-base/13_nvm_lint.log` | 29864 | b7bfe3b4cf82fd4b2cba2f271aa60c8463295dbc91bd0e3c6974780b50e3f276 |
| `logs/parent-base/14_nvm_quick.log` | 394 | cb802d0dfa07167eca0a998f0c041397eedf41d13b79f86c5090bc932b00c174 |
| `logs/parent-base/15_datapath.log` | 1951604 | 135b056afc3372be44b8036064b1ad3b2c81c059d9091fab33edb49f62bd14df |
| `logs/parent-base/16_render.log` | 156092 | e5f13d743645e338156ad940e80a54f44395cdfdd159337f9f0a3609c270d74c |
| `logs/parent-base/17_shell.log` | 235 | 7ace602f03fa0e411862de119cff9d337583f1f2170d920dff65a0e0f39ee6d9 |
| `logs/parent-head/01_cpp.log` | 315 | 20d9e296340ae6319c913211b7a2b7d63b6cc89798c011092c87908916634810 |
| `logs/parent-head/02_py.log` | 461 | e69f71258598b816549611332bba555ed3bfd91bf372cc7291568a2ee9870c2e |
| `logs/parent-head/03_sources.log` | 153 | ed979d7e26c3cd7a6f14364c11994089b77632424d04252613eeed458ebc8a95 |
| `logs/parent-head/04_pp_sources.log` | 955 | fad5e1b9dd5f465b7fcb2334e2abe6c6db44be93b5bb12afb3a35f3ebf432e1a |
| `logs/parent-head/05_ports.log` | 421 | 774375e7ac9c65d58d1828460de6529193dc26a096daa71c548e214bb3404380 |
| `logs/parent-head/06_naming.log` | 36608 | db23d3d49d070f855b77fbe71e83f3cc24b00ae81d2c288082eb016ac2820e77 |
| `logs/parent-head/07_evidence.log` | 13902 | bb9aadc07a14eb4e219e87fa681571c7886f1ef0be545cbae69d099b66fd7f44 |
| `logs/parent-head/08_docs.log` | 127 | 6a6b0baa714d34c94d863882cab86a5eac8309164fc1a6c99cb5659f049510ee |
| `logs/parent-head/10_builder.log` | 101822 | bca8346974b814e489bd69f28d3c994ffd1fad535a745e7250bcd1d01030117e |
| `logs/parent-head/11_lint.log` | 14186 | 9087b44973869192bcab894931d990c7976fb895a8d92b6c243c555087f69d6e |
| `logs/parent-head/12_shadow.log` | 273214 | 0f2901c31d7216d22e49be11a2f50dedf1cc4616f3fb8cc0b396f156c64dc339 |
| `logs/parent-head/13_nvm_lint.log` | 29864 | 849367624676a1ad5458ab831f0fff82337c9d532cde64d5a213db58801a8430 |
| `logs/parent-head/14_nvm_quick.log` | 394 | cb802d0dfa07167eca0a998f0c041397eedf41d13b79f86c5090bc932b00c174 |
| `logs/parent-head/15_datapath.log` | 1949053 | 52b52e94554f8ad5435791b3444250d337a564c68c6344e3e5230d430bb4bd0b |
| `logs/parent-head/16_render.log` | 155211 | d9d30767301c23059aea90c01b1360e0d731b5157ceae310e19dd072f6007d8b |
| `logs/parent-head/17_shell.log` | 235 | 7ace602f03fa0e411862de119cff9d337583f1f2170d920dff65a0e0f39ee6d9 |
| `logs/parent-final/01_cpp.log` | 315 | 20d9e296340ae6319c913211b7a2b7d63b6cc89798c011092c87908916634810 |
| `logs/parent-final/02_py.log` | 461 | e69f71258598b816549611332bba555ed3bfd91bf372cc7291568a2ee9870c2e |
| `logs/parent-final/03_sources.log` | 153 | ed979d7e26c3cd7a6f14364c11994089b77632424d04252613eeed458ebc8a95 |
| `logs/parent-final/04_pp_sources.log` | 955 | fad5e1b9dd5f465b7fcb2334e2abe6c6db44be93b5bb12afb3a35f3ebf432e1a |
| `logs/parent-final/05_ports.log` | 421 | 774375e7ac9c65d58d1828460de6529193dc26a096daa71c548e214bb3404380 |
| `logs/parent-final/06_naming.log` | 36608 | db23d3d49d070f855b77fbe71e83f3cc24b00ae81d2c288082eb016ac2820e77 |
| `logs/parent-final/07_evidence.log` | 13902 | bb9aadc07a14eb4e219e87fa681571c7886f1ef0be545cbae69d099b66fd7f44 |
| `logs/parent-final/08_docs.log` | 127 | 6a6b0baa714d34c94d863882cab86a5eac8309164fc1a6c99cb5659f049510ee |
| `logs/parent-final/09_xvlog.log` | 721 | 38138808e435728c8d32be1f3dabe801b8271e08e30edb5df7bdd79df0757fba |
| `logs/parent-final/10_builder.log` | 101822 | 9d84bbc6a4e2ae5cad10ea22bd7ff027c58d6de7166d50d325abe4d0ae4d76a4 |
| `logs/parent-final/11_lint.log` | 14186 | 9087b44973869192bcab894931d990c7976fb895a8d92b6c243c555087f69d6e |
| `logs/parent-final/12_shadow.log` | 273214 | aba35820297764884f80b1d66b34b434fa30957955dba537b433e9f66bfd9c86 |
| `logs/parent-final/13_nvm_lint.log` | 29864 | 1c9a26a8fa9b575506a1af900dbfb2653291af049608c20a6a745f87650d46f0 |
| `logs/parent-final/14_nvm_quick.log` | 394 | cb802d0dfa07167eca0a998f0c041397eedf41d13b79f86c5090bc932b00c174 |
| `logs/parent-final/15_datapath.log` | 1949056 | e66dc7a14fed57ff9aafe738cd71a35946b654e5a73694b7143ee91864c74713 |
| `logs/parent-final/16_render.log` | 155211 | 980b9675c2c29a2689eeae4041061411475489ca6b3cb5d0d70dd1e3182ec101 |
| `logs/parent-final/17_shell.log` | 235 | 7ace602f03fa0e411862de119cff9d337583f1f2170d920dff65a0e0f39ee6d9 |


## Round 3 — merge of #69 (complete)

Starting head verified as `ff58155657c3496d862710dab48357fd8f8d4102`; the origin URL is
the processor repository and the worktree is clean. The exact round-3 assignment is
processor #163 comment 6028791146. Merge target: `c9f74b6866a63dd3c0e4534724bfc07a86ad142b`.
No new TAKEN comment is needed. Earlier rounds and their evidence are retained above.

Completed: merge with both sides of all five test conflicts; WD/CX and CA/PD
checks and every mutant preserved. Final-head bank, notify campaign, plant audit and
documentation gates pass, with the required comparisons against both parents.
All required round-3 validation is complete. Fresh shipping 1x1 OOC retains
the timing and cone result; the final artifact inventory is recorded below.

Memory plan: at most two simulation builds, eight compile workers per build, two
build slots and campaign concurrency at most four. Physical-design work runs alone
and under the shared lock. Memory is monitored against the 9 GB working ceiling.

| Round-3 evidence | Status |
|---|---|
| Merge and preserved checks | `5fe5ea57`; 89 arms, all parent names and required checks retained |
| Suite bank / both-parent comparison | 33 suites at both, rc 0: main 1,028,286 / final 1,028,290; complete both-parent table below |
| WD/CX and CA/PD controls | WD 3/3; notify 65/65; IF 6/6; all WD/CX and CA/PD controls KILLED with unchanged failure records |
| Notify campaign / plant audit | main 86/86, final 89/89 KILLED; 10/11 goldens PASS; all 298 patches and 96 final exact-text edits plant |
| Documentation and synthesis gates | `make check`, HDL lint, matrix freshness and portable synthesis rc 0 at new main and final head |
| OOC WNS / >20-level pairs / area | +3.337 ns / zero / own logic -110 LUT, +6 FF; fresh before/after tables below |
| Parent consumers | 17/17 rc 0 at main and final; limited NVM repeats and locked compiler gate complete |

Resolution details: `tb/aecp_notify/sim_main.cpp` keeps CX then the incoming
`#elif defined(AECP_NOTIFY_IDENT)` guard; the README keeps CX and all PT/CK/PD/CA
counts. `tb/pp_top/Makefile` retains `withdraw`, `interfaces`, `interfaces-build`
and `if-guards`. Its README retains both histories and all mutant rows.
`notify_mutants.py` combines both mutant groups. `cancel_one_clock_late` now
anchors the command choice in `g_ca_own`, where #69 moved it; its immediate
TIME_LIMITED drain and delayed command behavior are preserved. The
`ctr_last_r [0:N_CTR_DESC_C-1]` declaration and #69's counter changes are unchanged.
CA4 observes the notify engine before the top's withdraw register, so its
four-cycle lower bound needs no re-grading.

Plant audit: all 298 patch files apply at `c9f74b68` and `5fe5ea57`. All 86
notify arms (89 edits) at main and all 89 arms (96 edits) at the merge match
exactly once; detailed audit artifacts are included in the evidence inventory.

Memory note: the initial two-slot wrapper limited builds but not lint invocations.
The parent's parallel lint gate briefly reached 9,539 MiB (service peak), above
the requested 9 GB working ceiling; no job was killed or failed. The wrapper now
limits every compiler invocation to two slots, including lint. A 7.5 GB soft
service limit and five-second monitoring with cache reclamation at 7 GB are in
place for the remaining work. This excursion is recorded rather than claiming
the working ceiling held for the entire run.

The WD and DN golden timing records match `ff581556` exactly (WD 3/3, DN 15/15;
DN latency 466 and 495 clocks). The first ADP campaign launcher ended before
completion; its incomplete exports/logs are retained under `aborted-m3-adp-launch/`
and contribute no result. The replacement foreground-monitored runs completed with rc 0 at both pins.

### Round-3 merge resolutions (file:line at `5fe5ea57`)

| File:line | Retained behavior |
|---|---|
| `tb/aecp_notify/sim_main.cpp:724` | CX cancellation-clock check retained; incoming identify guard at :754 and interface include at :940 retained |
| `tb/aecp_notify/README.md:24` | first build retains CX; :32 records combined 65 = 42 + 4 + 19; :37 retains PT/CK/PD/CA and their controls |
| `tb/pp_top/Makefile:245` | phony targets retain withdrawal, interfaces and interface guards; targets at :125, :211 and :230 remain callable |
| `tb/pp_top/README.md:2607` | both campaign histories and all 89 controls; WD/CX and interface mutation rows retained |
| `tb/pp_top/notify_mutants.py:413` | all three withdrawal arms retained; delayed-command arm re-anchored to the one-interface choice |
| `tb/pp_top/notify_mutants.py:452` | all interface-row controls retained |
| `tb/pp_top/notify_mutants.py:499` | all depth/probe controls retained; :541 combines the complete union |

The merge adds no cycle of its own. The previously graded +1 withdrawal cycle
remains at `hdl/top/protocol_processor_top.sv:4454`, with all three readers at
:4480, :4500 and :4578. The arbiter ranking at
`hdl/packet_engine/KL_pp_tx_arbiter.sv:161` is unchanged. Relative to new main,
there is no new port, parameter or register-map change. The incoming #69
interface contract is retained as assigned. `hdl/aecp/KL_aecp_notify.sv:446`
keeps the `N_CTR_DESC_C` counter-stamp shape unchanged from new main.

The merged bank has 33 passing suites and 1,028,290 checks. Against round 2,
ADP gains 11 checks, notify gains 19 and the top bench gains 6; all other suite
tallies are unchanged. The arbiter golden has 66/66 at new main and merge.
Its M1–M5 mutants fail 13, 6, 23, 30 and 2 checks respectively, with identical
complete failure lists at both revisions.

### Round-3 complete bank

| Suite | Round 2 `ff581556` | Main `c9f74b68` | Final `c4539ff1` |
|---|---:|---:|---:|
| `acmp_listener` | 3,111 | 3,111 | 3,111 |
| `acmp_nvm` | 388 | 388 | 388 |
| `acmp_talker` | 1,342 | 1,342 | 1,342 |
| `adp_engine` | 1,348 | 1,359 | 1,359 |
| `aecp_notify` | 46 | 64 | 65 |
| `ca_originator` | 16 | 16 | 16 |
| `desc_mem_guard` | 78 | 78 | 78 |
| `desc_store` | 586 | 586 | 586 |
| `dispatch` | 211 | 211 | 211 |
| `dyn_state` | 118 | 118 | 118 |
| `event_router` | 81 | 81 | 81 |
| `lsn_admit` | 18 | 18 | 18 |
| `maap` | 196 | 196 | 196 |
| `nvm_port` | 1,219 | 1,219 | 1,219 |
| `originator` | 107 | 107 | 107 |
| `pp_top` | 10,462 | 10,465 | 10,468 |
| `prng` | 76 | 76 | 76 |
| `release_merge` | 18 | 18 | 18 |
| `resp_buf` | 64 | 64 | 64 |
| `rx_slots` | 130 | 130 | 130 |
| `rx_validator` | 555 | 555 | 555 |
| `scoreboard` | 3,705 | 3,705 | 3,705 |
| `side_port` | 368 | 368 | 368 |
| `srp_admission` | 991,231 | 991,231 | 991,231 |
| `srp_decoder` | 190 | 190 | 190 |
| `srp_encoder` | 581 | 581 | 581 |
| `srp_stream_fsms` | 1,347 | 1,347 | 1,347 |
| `srp_top` | 8,656 | 8,656 | 8,656 |
| `timer_map` | 1,360 | 1,360 | 1,360 |
| `timer_service` | 48 | 48 | 48 |
| `tx_arbiter` | 66 | 66 | 66 |
| `tx_slots` | 95 | 95 | 95 |
| `ucpu` | 437 | 437 | 437 |
| **Total** | **1,028,254** | **1,028,286** | **1,028,290** |

All 33 suites pass, all three banks return rc 0. Every tally is identical except
the assigned WD/CX and #69 interface additions listed above. No check was removed.

Round-3 lint and matrix logs are byte-identical at main and merge. Portable
synthesis also passes at both; its only four differing warning lines are shifted
`all.v` source locations (five referenced locations), with identical warning text
and verdicts.

### Round-3 withdrawal-cycle controls

The golden WD run passes 3/3, and CX passes in the 65-check notify bank. Each
complete failure line from the three planted controls is identical to round 2.
The moved cancellation anchor therefore preserves the original grading.

| Planted control | Required / observed failures | Result |
|---|---|---|
| `withdraw_unregistered` | WD1, WD2 / WD1, WD2 | KILLED |
| `withdraw_abort_ignored` | WD2, WD3 / WD2, WD3 | KILLED |
| `cancel_one_clock_late` | CX1 / IX3, CX1 | KILLED |

### Parent C++ gate finding and integration follow-up

At merge `5fe5ea57`, parent consumer `01_cpp` returned rc 1: the combined
`tb/pp_top/sim_main.cpp` main function is 102 lines. Round 2 is 99 lines and
new main is 100, both within the parent's 100-line limit. This was a real gate
failure, not an unavailable dependency. The other completed parent consumers
remain recorded at their measured pin.

Follow-up commit `c4539ff107a6a4c7d2e4a4844182b00a2bf33c82` extracts the existing
tally reporting into `report_build` at `tb/pp_top/sim_main.cpp:14018`; main calls
it at :14122. Every statement, check, diagnostic, output format and early-return
behavior is preserved. The gate's scanner now reports zero long functions.
The merge is not amended, and no RTL changes. No new check or cycle is added.

Final validation completed at the follow-up head. Unfinished extra campaigns at
the superseded merge were retired and retained as partial artifacts, never counted
as passing validation. Both new-main and final-head runs completed; final-head
results replace the intermediate merged-head column.

### Completed notify comparison at the merge

At `5fe5ea57`, 11 goldens pass and all 89 controls are killed. All 77 round-2
records are exactly preserved; the only additions are #69's 21 controls and two
interface goldens. Against new main, the only changes are the WD golden, the
three WD/CX controls, and CX1 added to `ix_new_identity_unset`'s failures.
The final follow-up repeated this campaign with all 100 records identical.

| Retained #69 control | Required failed checks | Merge result |
|---|---|---|
| `avb_counter_any_index` | CK4 | KILLED |
| `avb_counter_name_overlaps_clock` | CK5 | KILLED |
| `avb_counter_named_clock` | CK1 | KILLED |
| `avb_counter_row_collapsed` | CK1 | KILLED |
| `avb_counter_row_dropped` | CK1 | KILLED |
| `cancel_one_per_command` | CA1, CA1b | KILLED |
| `depth_not_keyed` | PD1 | KILLED |
| `depth_shared` | PD1 | KILLED |
| `dereg_matches_other_port` | IF3b | KILLED |
| `expiry_port_dropped` | PD3 | KILLED |
| `monitor_tag_port_bits` | PD2 | KILLED |
| `owner_turns_dropped` | CA3, CA4 | KILLED |
| `port_not_compared` | PT2 | KILLED |
| `port_not_latched` | PT2 | KILLED |
| `port_not_stored` | PT3 | KILLED |
| `registry_tag_port_bits` | PD2 | KILLED |
| `report_fail_ignores_probe` | CA2, CA3 | KILLED |
| `report_rsp_ignores_probe` | CA2 | KILLED |
| `rgy_port_from_latest_frame` | IF3, IF3b | KILLED |
| `rgy_port_tied_zero` | IF3 | KILLED |
| `settle_dropped` | CA4 | KILLED |

### Final-head validation artifacts

The final comparison is `logs/m3base/` (`c9f74b68`) against `logs/m3final/`
(`c4539ff1`); `logs/m3head/` is the intermediate merge, not the final head.
`gates-m3-final.log` records the fresh final-head bank, gates and all campaigns.
The old extra-campaign controller completed new-main work; its unfinished merge
arms were explicitly retired in `superseded-m3head-campaigns.json`.
`parent-m3-final-all.log` records the final parent rerun. Unchanged-RTL build
products were reused after the follow-up, which changes only the bench reporting
helper; every consumer program ran again at the final gitlink. The locked compiler
consumer and explicit two-worker NVM repeats then completed. Timing began only
after all 18 individual processor jobs at both pins, both documentation checks
and the final parent pass had returned zero.

At the final head, all 11 notify goldens pass; WD and DN timing/tally records match
both round 2 and the intermediate merge exactly. Documentation, lint, matrix and
portable synthesis pass and match new main's records (source locations normalized
in the four existing synthesis-warning lines). All 298 patch controls apply;
all 89 notify arms and 96 exact-text edits plant once.

The full parent C++ idiom gate now passes at final gitlink `c4539ff1`, rc 0,
with a byte-identical log to new main. This closes the 102-line runner finding.
The intermediate merge datapath run also completed rc 0 before the pin changed;
the final parent consumer pass completed rc 0.

Parent record audit: parallel make output interleaved parts of 29 shadow check
lines even though every leg passed. The saved base and final executables were
replayed separately with their original ROMs, with binary/image hashes and one
log per leg, to compare complete records without interleaving.

The NVM quick target supplied its own `--jobs 8 --pool 8` defaults in the initial
runs despite the global two-build limiter. Its canonical base/final consumer
records were repeated with explicit `JOBS=2 POOL=2`; initial records are kept
separately. The actual compiler concurrency remains globally limited to two.

### Final bank and notification records confirmed

At `c4539ff1`, the full 33-suite bank passes 1,028,290 checks and is identical
to the intermediate merge. The table above now names the final head. Against
new main, only notify (+1 CX) and the top bench (+3 WD) move; against round 2,
only ADP (+11), notify (+19) and the top bench (+6) move as #69 specifies.
All 11 notify goldens pass and all 89 controls are KILLED. Every one of the
100 structured campaign records equals the intermediate merge, so all parent
preservation comparisons and the WD/CX and CA/PD failure tables above also hold
at the final head. No check meaning or cycle bound was weakened.

All eight separate shadow replays completed rc 0. Each of the four replay logs is
byte-identical at base and final, including diagnostics and tallies; both ROM image hashes match.
The render consumer has 117 identical diagnostic, tally and verdict records
when sorted for parallel completion order. The original interleaved logs remain
available; the replay hashes and per-leg counts are in
`evidence/parent-shadow-replay-m3.json` under the scratch root.

The final parent consumer controller has completed its 16 non-timing consumers,
all rc 0. Datapath has 11,916 identical graded/diagnostic records after sorting
parallel completion order. Builder and NVM lint logs match after normalizing
only temporary names and run durations; the inherited calibration arm remains
NOT RUN at both pins. The serialized timing compiler gate and both limited NVM quick repeats also
completed before OOC.
CTR, GSI and name-write final campaigns also pass with identical base/final logs.

### Round-3 parent consumer comparison

Pins: new main `c9f74b68` and final `c4539ff1`, scratch parent dev `28f9666f`
with adoption 148 then 22. Each row has its own command, log, rc and revision
record. The simulation comparisons include every verdict form and tally; parallel
completion order is normalized. Temporary names and elapsed build times are
metadata, not graded records.

| Parent consumer | Main rc | Final rc | Compared records |
|---|---:|---:|---|
| C++ source idioms | 0 | 0 | byte-identical; merged runner finding fixed by reporting helper |
| Script source idioms | 0 | 0 | all idiom counts identical; 317 modules, source lines 200,247 to 200,281 |
| RTL source lists | 0 | 0 | 108 closure files, four consumers, 42/42 processor tops |
| Processor source list/self-test | 0 | 0 | byte-identical |
| Port contracts | 0 | 0 | 3,826 ports unchanged; test-only observations 318 to 324 |
| Naming | 0 | 0 | 95 recorded candidates; byte-identical |
| Test evidence | 0 | 0 | 72/77 suites, 10/10 unseeded sites, 0 unexplained source readers, 3/3 wall-clock files |
| Documentation | 0 | 0 | no findings; 189 markdown + 987 scrubbed files, 23/23 and 4/4 controls |
| Timing compiler | 0 | 0 | zero findings; identical logs after normalizing the processor pin; serialized under the shared lock |
| Builder | 0 | 0 | identical except temporary names and elapsed times; inherited calibration arm NOT RUN |
| RTL lint | 0 | 0 | 90 findings at ratchet 90, 17 waived; byte-identical |
| Processor shadow | 0 | 0 | separate saved-executable replays: 606, 606, 646, 311; all 2,169 check records identical |
| NVM lint | 0 | 0 | identical except elapsed times |
| NVM quick, explicit two-worker run | 0 | 0 | 315/315; complete logs identical; explicit `JOBS=2 POOL=2` |
| Datapath | 0 | 0 | 11,916 verdict, diagnostic and tally records identical |
| Render | 0 | 0 | 117 verdict, diagnostic and tally records identical; 65/65, 245/245 and 5/5 |
| Shell source idioms | 0 | 0 | byte-identical |

Datapath tallies: 104; 182 twice; 236 twice; 421; 416; 1,961 three times;
3,746; 33; 233; 193; and both six-check mutant groups. Every tally has zero
failures at both pins. The comparison retains the GM-step, render, listener,
talker, timestamp-latency and coincidence diagnostics as well as individual
checks. `parent-full-simulation-comparison-m3.json` records its exact selection.

ACMP (33 mutants, four goldens), SRP admission (12 checks), MAAP (32 checks)
and ADP (62 checks) have now completed at the final head, rc 0, with identical
new-main records. ADP preserves all 43 round-2 records and adds exactly #69's
16 interface mutants and three goldens; their complete failure lists are retained
in `adp-final-vs-round2.json`.

The retry campaign is complete at the final head: 62 killed mutants, seven
equivalence controls, one performance control, baseline and restored rc 0.
Its driver log and all 73 individual run logs are byte-identical to new main.
The final arbiter golden is 66/66; M1–M5 fail 13, 6, 23, 30 and 2 checks, with
identical full failure lists and result objects at both pins.

### Round-3 complete campaign table

Every campaign below returned rc 0 at new main `c9f74b68` and final `c4539ff1`.
All full result objects, named failures and missing-check lists match except the
specified notify differences. For drivers without structured records, complete
driver logs match; parallel completion order is normalized for ACMP and D3.

| Campaign | New main | Final | Record comparison |
|---|---|---|---|
| Notify | 10 goldens, 86 killed | 11 goldens, 89 killed | WD golden and three WD/CX arms added; existing identity arm also fails CX1 |
| D3 | 6 goldens, 110 killed | same | all 116 full records identical |
| ACMP | 4 goldens, 33 killed | same | all 37 full records identical |
| AECP | 67/67 | same | complete driver log identical |
| AECP dispatch | 4 goldens, 40 killed | same | all 44 full records and driver log identical |
| CTR | 18/18 | same | complete driver log identical |
| GSI | 20 named mutants; golden/restored pass | same | all 22 full records and driver log identical |
| Name write | decode killed; golden/restored pass | same | all three full records and driver log identical |
| ADP | 62/62 | same | all control verdicts, full failures and driver log identical |
| MAAP | 32/32 | same | complete driver log identical |
| SRP top | 137/137; 86/86 assertion coverage | same | complete driver log identical |
| SRP admission | 12/12 | same | complete driver log identical |
| Retry | 62 killed; 7 equivalent; 1 performance; baseline/restored pass | same | driver and all 73 individual logs byte-identical |
| Arbiter | golden 66/66; M1–M5 fail 13, 6, 23, 30, 2 | same | full failure lists and result objects identical |

Against round 2, all existing records remain unchanged. The only additions are
#69's 21 notify controls and two interface goldens, plus 16 ADP interface controls
and three goldens. The arbiter's fresh comparison is against new main; its RTL
and bench remain the previously proved versions. `campaigns-final-m3.json`
records both-parent comparisons; `adp-final-vs-round2.json` includes all 19
ADP additions and their complete failures. All 18 individual processor job rc
files are zero at each final comparison pin; both separate documentation checks
also return zero. Superseded intermediate campaigns are excluded.

All 17 canonical parent consumers now return rc 0 at both exact processor pins.
The explicit two-worker quick repeats retain identical complete logs, 315/315.
The locked compiler gate reports zero findings over 73 parent and 52 processor
source files; its complete logs differ only in the recorded processor pin.
The inherited builder calibration arm remains NOT RUN, as disclosed above.
Fresh shipping OOC completed under the shared lock; both integrated elaborations
and parameter extractions passed, with parameters identical to the original
measurement recipe.

### Physical-design memory retry

The first fresh new-main synthesis used the generated recipe's concurrency of
32, which spawned seven worker processes. The resource guard suspended that
invocation when service memory reached 8,557,981,696 bytes, below 9 GB. All its
processes were then terminated normally; no memory-limit kill or timing result
occurred. Its partial synthesis rc is -15 and its controller rc is 1. These are
excluded operational artifacts under `aborted-m3-ooc-workers/`, not passing gates.
All 17 parent consumer records had already completed and remain valid.

Both fresh OOC pins were measured with `general.maxThreads` set to 2 in the
scratch elaboration, synthesis and timing-query scripts. No source, generic,
clock, timing constraint, synthesis directive or image changes. Each generated
synthesis recipe records the hash before and after that single concurrency-line
replacement in `baseline_concurrency.json`. The shipping parameter objects must
still match the original recipe exactly. The concurrency setting is described
in the [synthesis documentation](https://docs.amd.com/r/en-US/ug901-vivado-synthesis/Multi-Threading-in-RTL-Synthesis).

During this physical-design phase, the soft memory threshold is 8.7 GB and a
resident guard suspends this lane's physical-design processes at 8.5 GB, before
the 9 GB working ceiling. The shared lock still encloses each entire measurement,
and no other heavy job runs in this lane. The earlier 9,539 MiB lint excursion
remains disclosed above; it is not hidden by this retry.

### Final review anchors against new main

At `c4539ff1`, these are the starting lines of every changed hunk against
`c9f74b68`. They supplement the behavioral and cycle descriptions above; the
preceding rounds retain their original revision-specific references.

| File | Final hunk-start lines |
|---|---|
| `docs/architecture/03_packet_engine.md` | `488` |
| `hdl/packet_engine/KL_pp_tx_arbiter.sv` | `162`, `177`, `186`, `188`, `193` |
| `hdl/top/protocol_processor_top.sv` | `4444`, `4480`, `4500`, `4578` |
| `tb/aecp_notify/README.md` | `13`, `24`, `31`, `246`, `248`, `255`, `267`, `302` |
| `tb/aecp_notify/sim_main.cpp` | `86`, `100`, `115`, `119`, `122`, `137`, `144`, `275`, `719` |
| `tb/pp_top/Makefile` | `124`, `245` |
| `tb/pp_top/README.md` | `2229`, `2231`, `2239`, `2520`, `2582`, `2605`, `2656`, `2680` |
| `tb/pp_top/notify_mutants.py` | `28`, `404`, `542` |
| `tb/pp_top/notify_phases.hpp` | `1814`, `2035` |
| `tb/pp_top/pp_top_wrap.sv` | `493`, `921` |
| `tb/pp_top/sim_main.cpp` | `838`, `1622`, `2060`, `14018`, `14088`, `14096`, `14117`, `14122` |
| `tb/tx_arbiter/README.md` | `53`, `58` |

### Matching the resource-check reference to the measured flow

The two-thread new-main synthesis completed rc 0. The first resource comparison
returned rc 2, NOT COMPARABLE, because the stored reference identifies a
32-thread recipe. That refusal is retained under `identity-refusal-m3/`.
The checker itself requires a fresh baseline under the new identity.

The completed new-main measurement is therefore recorded into a scratch copy,
`meas/resource_baseline_m3.json`, using the existing record operation. Every
policy field and every other endpoint is unchanged; the parent repository's
reference file is unchanged. The copied reference's policy check returns rc 0,
and the new-main resource check against it returns rc 0. The final head used
the same reference and passed. The separate assignment limits of 60 LUT and 120 FF for own
logic remain unchanged and are evaluated from the before/after hierarchy table.

New-main figures reproduce the original lane baseline exactly: wrapper 23,179
LUT / 19,779 FF, processor 22,517 LUT / 18,941 FF, WNS -3.562 ns and WHS +0.159 ns.
Only the reference identity, recorded input hash and fresh baseline record change;
no limit is loosened. `resource-reference-m3.json` records the old and new
reference objects and the unchanged-policy assertions. Cone measurement resumes
from this successfully synthesized checkpoint; it does not re-use an old design.

The fresh new-main cone survey completes rc 0: 1,631 startpoints, 561 queried
endpoint pins (543 with paths), 263,154 reported pairs, 146,535 above 20 levels,
maximum 51. Its area, setup/hold summaries, complete level histogram and worst
five paths exactly reproduce the original baseline. The final-head measurement
completed with the same two-thread recipe and fresh reference.

### Fresh shipping 1x1 OOC, main versus final

Both measurements use the same 50 MHz clock, shipping parameters, images and
two-thread recipe. All synthesis, resource, path and cone commands complete
rc 0. The resource comparison uses the freshly measured new-main reference;
all policy limits are unchanged.

| Measurement | Main `c9f74b68` | Final `c4539ff1` |
|---|---:|---:|
| WNS (ns) | -3.562 | 3.337 |
| TNS (ns) | -37.519 | 0.0 |
| Failing setup endpoints | 16 | 0 |
| WHS (ns) | 0.159 | 0.159 |
| Failing hold endpoints | 0 | 0 |
| Arbiter startpoints queried | 1631 | 328 |
| Arbiter endpoint pins queried | 561 | 561 |
| Arbiter pairs reported | 263154 | 17990 |
| Pairs above 20 logic levels | 146535 | 0 |
| Maximum logic levels | 51 | 16 |
| Worst arbiter slack (ns) | -3.562 | 11.912 |
| Pairs with no slack annotation | 12219 | 187 |

Pairs without a slack annotation are included in the level census.
The survey asks for every startpoint against all non-clock input pins of the
arbiter sequential cells, one worst path per endpoint, with a path limit above
the endpoint count. Raw pair tables remain in scratch; the artifact manifests
record their byte sizes and hashes.

| Area scope | Main LUT | Final LUT | Delta | Main FF | Final FF | Delta |
|---|---:|---:|---:|---:|---:|---:|
| `KL_pp_shadow` | 23179 | 23160 | -19 | 19779 | 19787 | +8 |
| `u_pp` | 22517 | 22478 | -39 | 18941 | 18951 | +10 |
| `(u_pp)` | 939 | 780 | -159 | 2033 | 2039 | +6 |
| `u_tx_arbiter` | 185 | 234 | +49 | 187 | 187 | +0 |
| `u_originator` | 697 | 676 | -21 | 885 | 885 | +0 |
| `u_notify` | 2125 | 2157 | +32 | 1256 | 1258 | +2 |

Own logic (top's own scope plus arbiter): -110 LUT, +6 FF; within the 60 LUT / 120 FF STOP limits.

| Rank | Before: source -> endpoint; levels; slack (ns) | After: source -> endpoint; levels; slack (ns) |
|---|---|---|
| 1 | `u_pp/u_notify/pend_r_reg[2]/C` -> `u_pp/u_tx_arbiter/slot_r_reg[0]/D`; 47; -3.562 | `u_pp/u_ca_builder/cancel_release_slot_o_reg[2]/C` -> `u_pp/u_tx_arbiter/slot_r_reg[0]/D`; 16; +11.912 |
| 2 | `u_pp/u_notify/pend_r_reg[2]/C` -> `u_pp/u_tx_arbiter/slot_r_reg[1]/D`; 47; -3.562 | `u_pp/u_ca_builder/cancel_release_slot_o_reg[2]/C` -> `u_pp/u_tx_arbiter/slot_r_reg[1]/D`; 16; +11.912 |
| 3 | `u_pp/u_notify/pend_r_reg[2]/C` -> `u_pp/u_tx_arbiter/slot_r_reg[2]/D`; 47; -3.562 | `u_pp/u_ca_builder/cancel_release_slot_o_reg[2]/C` -> `u_pp/u_tx_arbiter/slot_r_reg[2]/D`; 16; +11.912 |
| 4 | `u_pp/u_notify/pend_r_reg[2]/C` -> `u_pp/u_tx_arbiter/owner_r_reg[0]/D`; 46; -3.417 | `u_pp/u_ca_builder/cancel_release_slot_o_reg[2]/C` -> `u_pp/u_tx_arbiter/owner_r_reg[1]/D`; 15; +12.057 |
| 5 | `u_pp/u_notify/pend_r_reg[2]/C` -> `u_pp/u_tx_arbiter/owner_r_reg[1]/D`; 45; -2.930 | `u_pp/u_ca_builder/cancel_release_slot_o_reg[2]/C` -> `u_pp/u_tx_arbiter/owner_r_reg[0]/D`; 14; +12.296 |

Source-group census (maximum level and minimum slack may be different pairs):

| Source group | Main pairs; max levels; minimum slack (ns) | Final pairs; max levels; minimum slack (ns) |
|---|---|---|
| notification wr_ix_r | 752; 51; -2.981 | no direct combinational path |
| RX header fields | 40044; 50; -1.795 | no direct combinational path |
| registered withdraw mask | no direct combinational path | 1504; 12; +13.512 |

Both fresh measurements reproduce the original lane's respective area, setup/hold
summaries, complete cone histograms and worst-five paths exactly, despite the
reduced worker setting. No round-3 timing or area STOP condition is reached.
The merge adds no cycle; the retained +1 withdrawal cycle remains graded by
WD1–WD3 and CX1, and every WD/CX and CA/PD control retains its failure record.

The parent three-directive implementation sweep remains the pin-adoption step,
not a claim of this lane. The PR body therefore retains `Relates to #163`.
No push, PR edit or parent commit was performed.

### Final artifact and worktree state

Final processor head: `c4539ff107a6a4c7d2e4a4844182b00a2bf33c82`, on
`pp163-txarb-cone`. The worktree is clean, including ignored files. Merge parents
are exactly `ff58155657c3496d862710dab48357fd8f8d4102` and
`c9f74b6866a63dd3c0e4534724bfc07a86ad142b`; the only follow-up file is the
bench reporting helper. Both new commit messages are one-line subjects with no
body or trailers.

Scratch parent remains at dev `28f9666feab2b2ba287643c63ed3a16b1e0bb863`, with
only the two supplied patches and the processor gitlink at the final head.
Both patches reverse-check cleanly; all initialized submodule worktrees are
clean. Generated build products and the temporary measurement links have been
removed from the tree and preserved in scratch storage. No parent commit or
push was made. No heavy process remains.

The completed two-thread measurements did not trigger the memory guard. Their
observed service peak was 7,664,832,512 bytes; the service records zero OOM
and zero OOM-kill events. The earlier lint excursion and the deliberately
terminated 32-thread synthesis attempt remain disclosed above. The monitoring
process has stopped and the soft threshold is restored to 7.5 GB.

The two manifests below inventory 1,879 validation artifacts with SHA-256 and
byte size, using paths relative to `$VALIDATION_STORAGE/pp163-a553`. Small comparison
records are also copied into `evidence/`. Files over 200 KB, raw cone tables,
checkpoints, build trees and environments remain outside this output directory.
Canonical results use `m3base` / `m3final` and `parent-m3-base` /
`parent-m3-final`; retired attempts and refusals are explicitly named and are
not counted as passing gates.

| Manifest | Bytes | SHA-256 |
|---|---:|---|
| `ARTIFACTS-R3-01.tsv` | 179892 | `5894be57f663ffc22b9132fe0cc8953327fceb5298bab058a518274b518c7cb5` |
| `ARTIFACTS-R3-02.tsv` | 39201 | `3ec792a8723ef4dc344e12b76dbf07b6617b6b1cd6142ad7166c34fa320cabc5` |

## Round 4

Status: REVIEW READY at `8947bafdd62b4bf991debf7bfd8cdb73994a3a81`. Initial identity was confirmed at
`c4539ff107a6a4c7d2e4a4844182b00a2bf33c82` on `pp163-txarb-cone`, with the processor
origin. Assignment comment 6033185530, the complete issue, the parent timing
comments and the review report plus probes were read. No second TAKEN was posted.
No STOP condition was hit. No RTL behavior, port, register map or parameter change.
The only HDL edit is a comment; its non-comment tokens are unchanged. All 581
tracked files match the final validation exports.

WD4 reaches a TIME_LIMITED cancellation parked behind another exchange's matched
response while the arbiter selects the cancelled probe. It grades the withdrawal
on the next clock, before pool start, and confirms the probe never reaches the
wire. Both new controls fail only WD4 with setup, coincidence and release order
intact. They assert pool start at c+1; the withdrawal and wire-completion
predicates fail. The review control passes and all four
requested review probes are killed at WD4.

The compressed default wrapper's 400 ms TIME_LIMITED timer expires before its
30–60 s monitor interval. The C++ fixture postpones only the actual armed row-0
deadline by 70 s, preserving owner and armed state. It deposits no cancellation,
response, mask, queue or arbiter state. All registration traffic, probe generation,
backpressure, matching, cancellation and withdrawal run through the top. The
existing sixth build replays the same case with the production 300,000 ms timeout,
without any deposit: four checks pass, rc 0. This also demonstrates that the
parked case occurs at the top with the production timeout.

Commits (one-line subjects; no bodies or trailers):

- `740b15b346baad13fc17954cc4c8aa6335872c58`: Grade parked probe withdrawal at the top
- `8947bafdd62b4bf991debf7bfd8cdb73994a3a81`: Separate withdrawal fixture declarations

The second commit resolves two grouped-declaration findings in the parent C++
gate. Its final run passes. Runs started on the first commit were stopped and
marked superseded; they are not final validation. The exported-tree documentation
attempt lacked Git metadata (rc 2); the tracked-tree run passes. The standalone
shipping-timeout replay initially lacked `obj_dir` for tally output: its four
checks passed, but the process returned rc 1. Creating that directory and rerunning
the unchanged binary returned rc 0. Both records are retained; no failure is
counted as a pass.

### Changes

| File:line | Change |
|---|---|
| `tb/pp_top/notify_phases.hpp:2005` | Fresh parked-cancellation setup, calibrated response collision and WD4 grading; one added check |
| `tb/pp_top/notify_phases.hpp:2038` | Locate the armed TIME_LIMITED timer; postpone only its deadline in the compressed fixture; use the unchanged production timeout in the alternate replay |
| `tb/pp_top/notify_phases.hpp:2148` | Grade both live exchanges, response match, distinct releases, arbiter selection and abort, wire absence and eventual idle |
| `tb/pp_top/notify_phases.hpp:2200` | One named WD4 check grades setup, coincident events, release order, next-clock withdrawal and wire completion |
| `tb/pp_top/notify_phases.hpp:2250` | Run WD4 after the unchanged WD1–WD3 phase |
| `tb/pp_top/notify_mutants.py:424` | Two added arms: remove the mask at all three readers, or delay it two clocks; require WD4 |
| `tb/pp_top/sim_main.cpp:41` | Generated root header for the timer fixture and read-only queue/report/release observations |
| `tb/pp_top/sim_main.cpp:14064` | Existing shipping-timeout build can replay WD using --withdraw-only |
| `hdl/top/protocol_processor_top.sv:4449` | Comment: the parked mask leads the cancelled slot release by one clock |
| `docs/architecture/03_packet_engine.md:488` | State immediate and parked cancellation timing in the stage table |
| `docs/architecture/09_verification.md:313` | Add WD/CX catalogue entries and the withdrawal invocation; correct the shipping-timeout build count |
| `tb/pp_top/README.md:2520` | WD4 scenario, fixture disclosure, production-timeout replay and mutation records |

### Cycles, area and timing

No cycle is added in Round 4. WD1–WD3 and CX1 retain their meanings. WD4 grades the
existing added withdrawal cycle in the parked case. It reads the actual selected
slot, response report and distinct releases; it does not read the mask register.
Removing the mask's readers therefore still builds and must fail behaviorally.

| Clock | Event / release | Arbiter for the cancelled probe |
|---|---|---|
| c | TIME_LIMITED cancellation and another exchange's matching header | IDLE selects the queued probe |
| c+1 | Other exchange's matched-response report and slot release | START holds the cancelled slot; pool start stays 0 |
| c+2 | Cancelled slot release | IDLE, with no start |

After the race, WD4 observes another 1.5 s: row 0 has no wire probe, row 1 has
exactly its one initial byte-exact probe, row 0 has exactly one DEREGISTER, both
solicited answers leave, and all five slots plus the originator return idle.

| Added cycle / check | Planted control | Failing checks |
|---|---|---|
| Existing one-cycle mask stage, immediate cancellation | `withdraw_unregistered` | WD1, WD2, WD4 |
| Existing abort of a selected probe | `withdraw_abort_ignored` | WD2, WD3, WD4 |
| Existing one-cycle mask stage, parked cancellation | `withdraw_mask_dropped` | WD4 only |
| Existing one-cycle mask stage, parked cancellation | `withdraw_two_clocks` | WD4 only |
| No extra cancellation stage before the top | `cancel_one_clock_late` | CX1, IX3, unchanged |

The Round 3 OOC 1x1 record stands, as assigned. The following Round 4 before/after
values are carried forward by unchanged implementation; they are not new timing
measurements. The earlier Round 3 section contains the complete original-vs-lane
level/slack tables, worst five paths, source cones and area scopes.

| Metric | Before c4539ff1 | After 8947baf |
|---|---:|---:|
| WNS / WHS (ns) | +3.337 / +0.159 | +3.337 / +0.159 |
| TNS / failing setup endpoints | 0 / 0 | 0 / 0 |
| Maximum arbiter depth | 16 | 16 |
| Arbiter pairs above 20 levels | 0 | 0 |
| Worst arbiter slack (ns) | +11.912 | +11.912 |
| Processor LUT / FF | 22,478 / 18,951 | 22,478 / 18,951 |
| Own-logic delta versus original | -110 LUT / +6 FF | -110 LUT / +6 FF |

| Worst arbiter endpoint | Before levels / slack (ns) | After levels / slack (ns) |
|---|---|---|
| `slot_r[0]` | 16 / +11.912 | 16 / +11.912 |
| `slot_r[1]` | 16 / +11.912 | 16 / +11.912 |
| `slot_r[2]` | 16 / +11.912 | 16 / +11.912 |
| `owner_r[1]` | 15 / +12.057 | 15 / +12.057 |
| `owner_r[0]` | 14 / +12.296 | 14 / +12.296 |

All five start at CA builder `cancel_release_slot_o_reg[2]/C`. Round 4 changes
0 LUT and 0 FF. The parent implementation sweep remains at pin adoption, so the
PR body retains `Relates to #163`.

### Processor suites and gates

The complete bank, notify campaign and all processor gates were rerun at the
Round 4 base and final head. The unchanged campaigns and parent consumers compare
against their prior complete rc-0 records at the exact same base `c4539ff1`.
No baseline is inferred from a different source revision.

| Suite | Base checks | Final checks | Base / final rc |
|---|---:|---:|---|
| `acmp_listener` | 3,111 | 3,111 | 0 / 0 |
| `acmp_nvm` | 388 | 388 | 0 / 0 |
| `acmp_talker` | 1,342 | 1,342 | 0 / 0 |
| `adp_engine` | 1,359 | 1,359 | 0 / 0 |
| `aecp_notify` | 65 | 65 | 0 / 0 |
| `ca_originator` | 16 | 16 | 0 / 0 |
| `desc_mem_guard` | 78 | 78 | 0 / 0 |
| `desc_store` | 586 | 586 | 0 / 0 |
| `dispatch` | 211 | 211 | 0 / 0 |
| `dyn_state` | 118 | 118 | 0 / 0 |
| `event_router` | 81 | 81 | 0 / 0 |
| `lsn_admit` | 18 | 18 | 0 / 0 |
| `maap` | 196 | 196 | 0 / 0 |
| `nvm_port` | 1,219 | 1,219 | 0 / 0 |
| `originator` | 107 | 107 | 0 / 0 |
| `pp_top` | 10,468 | 10,469 | 0 / 0 |
| `prng` | 76 | 76 | 0 / 0 |
| `release_merge` | 18 | 18 | 0 / 0 |
| `resp_buf` | 64 | 64 | 0 / 0 |
| `rx_slots` | 130 | 130 | 0 / 0 |
| `rx_validator` | 555 | 555 | 0 / 0 |
| `scoreboard` | 3,705 | 3,705 | 0 / 0 |
| `side_port` | 368 | 368 | 0 / 0 |
| `srp_admission` | 991,231 | 991,231 | 0 / 0 |
| `srp_decoder` | 190 | 190 | 0 / 0 |
| `srp_encoder` | 581 | 581 | 0 / 0 |
| `srp_stream_fsms` | 1,347 | 1,347 | 0 / 0 |
| `srp_top` | 8,656 | 8,656 | 0 / 0 |
| `timer_map` | 1,360 | 1,360 | 0 / 0 |
| `timer_service` | 48 | 48 | 0 / 0 |
| `tx_arbiter` | 66 | 66 | 0 / 0 |
| `tx_slots` | 95 | 95 | 0 / 0 |
| `ucpu` | 437 | 437 | 0 / 0 |
| **Total (33 suites)** | **1,028,290** | **1,028,291** | **0 / 0** |

Only `pp_top` gains one check, WD4. Its default build is 9,975 checks, and the
seven-build aggregate is 10,469. All other suite counts and all passing/failing
records are unchanged. The default run and the `--withdraw-only` run both include
WD4; no existing check was removed or relaxed.

| Gate | Base / final rc | Result |
|---|---|---|
| `scripts/lint_hdl.sh` | 0 / 0 | pass |
| `make -j16 check` | 0 / 0 | pass in tracked tree |
| `scripts/gen_matrix.py --check` | 0 / 0 | pass |
| `syn/yosys/run.sh` | 0 / 0 | pass |
| Plant audit | 0 / 0 | 298/298 patches; notify 89→91 arms and 96→101 edits; no refusals |
| Shipping-timeout WD replay | — / 0 | four checks, zero failures, no deadline deposit |

Before changing the top comment, every old comment line was searched across patch
and exact-text mutation contexts; none occurred. The final plant audit also
confirms D3 110 arms/119 edits, ACMP 33/33 and GSI 20/20, without refusals.

### Campaigns

| Campaign | Base / final rc | Base / final result |
|---|---|---|
| `camp-acmp` | 0 / 0 | identical: ACMP mutations: 33 of 33 KILLED by their named checks; goldens PASS |
| `camp-adp` | 0 / 0 | identical: 62 checks: 62 PASS, 0 FAIL |
| `camp-aecp` | 0 / 0 | identical: 67 checks: 67 PASS, 0 FAIL |
| `camp-aecp_dispatch` | 0 / 0 | identical: 44 checks: 44 PASS, 0 FAIL |
| `camp-ctr` | 0 / 0 | identical: 18 checks: 18 PASS, 0 FAIL |
| `camp-d3` | 0 / 0 | identical: D3 mutations: 110 of 110 KILLED by their named checks; goldens PASS |
| `camp-gsi` | 0 / 0 | identical: GSI mutations: 20 detected by named checks; golden and restored PASS |
| `camp-maap` | 0 / 0 | identical: 32 checks: 32 PASS, 0 FAIL |
| `camp-name_wr` | 0 / 0 | identical: Name-write mutation: decode killed; golden and restored PASS |
| `camp-notify` | 0 / 0 | 89→91 killed; 11 goldens pass; only the four named WD records differ |
| `camp-retry` | 0 / 0 | identical: PASS: 62 mutants killed; 7 equivalence controls; 1 performance controls; baseline and restored rc 0 |
| `camp-srp_admission` | 0 / 0 | identical: 12 checks: 12 PASS, 0 FAIL |
| `camp-srp_top` | 0 / 0 | identical: 137 checks: 137 PASS, 0 FAIL |
| `camp-txarb` | 0 / 0 | identical: M5 {"rc": 2, "tally": "66 checks: 64 PASS, 2 FAIL", "failing": 2, "first": ["H withdrawn selection produces no grant or frame", "H aborted start leaves the committed slot untouched"]} |

Notify retains every earlier arm. Its golden WD tally rises from three to four
checks. Comparisons below concern structured verdicts and failing-check records,
not compiler progress or elapsed time. The 98 other records are identical; the two
existing WD controls gain WD4 and the two new controls fail WD4 only. Every other
campaign's failing-check records match the base, including the arbiter's five
controls. Refused edits, failed builds and missing tallies are not kills.

| Review probe | Result | Failing checks |
|---|---|---|
| `ctl-withdraw` | PASS | none |
| `r-wd-two-clocks` | KILLED | WD4 only |
| `r-wd-mask-dropped` | KILLED | WD4 only |
| `r-full-mask-dropped` | KILLED | WD4 only |
| `r-full-two-clocks` | KILLED | WD4 only |

The review script was run unchanged, against the final source export. Each
mutated run builds successfully and prints its completed tally. The isolated
runs have four checks; the complete default runs have 9,975 checks.

### Scratch parent consumers

The scratch parent remains at dev `28f9666feab2b2ba287643c63ed3a16b1e0bb863`, with
the supplied 148 patch followed by the 22 patch and the processor gitlink staged
at the final head. No parent commit or push. Submodule roots were verified before
Git operations. The 17-consumer set passes at both exact processor pins.

| Consumer | Base rc | Final rc |
|---|---:|---:|
| `01_cpp` | 0 | 0 |
| `02_py` | 0 | 0 |
| `03_sources` | 0 | 0 |
| `04_pp_sources` | 0 | 0 |
| `05_ports` | 0 | 0 |
| `06_naming` | 0 | 0 |
| `07_evidence` | 0 | 0 |
| `08_docs` | 0 | 0 |
| `09_xvlog` | 0 | 0 |
| `10_builder` | 0 | 0 |
| `11_lint` | 0 | 0 |
| `12_shadow` | 0 | 0 |
| `13_nvm_lint` | 0 | 0 |
| `14_nvm_quick` | 0 | 0 |
| `15_datapath` | 0 | 0 |
| `16_render` | 0 | 0 |
| `17_shell` | 0 | 0 |

The static findings and completed build tallies match the base. Parallel build
output interleaves some per-check lines; the four complete shadow-build tallies
are compared as a multiset. The Python inventory grows by
14 source lines for the two assigned arms; its 317 modules and all findings are
unchanged. The inherited builder calibration skip remains unchanged. The locked HDL analysis
consumer ran after the heavy work completed. Cleanup leaves only the adopted
parent patches and the staged processor gitlink; generated products remain in
scratch outside tracked trees.

### Reproduction and artifacts

The final source export is bound to `8947bafdd62b4bf991debf7bfd8cdb73994a3a81` by a 581-file SHA-256 inventory.
Use the repository commands above and the normal campaign drivers with `--jobs 2`
where offered. The compiler is pinned to 5.050; the shared build slots admit at
most two compiler builds. Invocations use `make -j16`; early compiler subprocesses
used eight jobs and later ones sixteen. Independent suites and campaigns run
concurrently, each with its own log and rc file. Memory high is 7.5 GB; the service
peak is 7,507,382,272 bytes, below 9 GB, with no OOM or kill events.

For the alternate replay in a fresh export, from `tb/pp_top`:

```sh
make -j16 timer-defaults-build
mkdir -p obj_dir
./obj_tdf/Vpp_top_tdf --withdraw-only
```

`evidence-round4/` contains the compact records and comparison audit. Its
`wd4-traces.json` excerpts the three race clocks for the golden, both new
controls and the production-timeout replay, with source-log sizes and hashes. The
`ARTIFACTS-R4-*.tsv` manifests give byte sizes and SHA-256 values for retained
scratch evidence. Logs or other artifacts over 200 KB are referenced by hash and
size, never copied into this packet. Source exports, build trees, packages and
the environment remain outside the output directory. Development, superseded and
missing-directory attempts are labelled separately from accepted final records.
No push, PR creation/edit, parent commit, hardware access or flashing occurred.
