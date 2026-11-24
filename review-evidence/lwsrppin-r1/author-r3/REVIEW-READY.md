[A834] REVIEW READY
Commit: 507bce7f9fe50fcaf7b0abe6a198bdb4d0ea4698. It is a merge commit, first parent `30796098` (the pin, PR #992's
reviewed head) and second parent `2509db68` (dev-soft-core, the flip train PR #988). It is on `20-lwsrp-pin-d1bb4f4`
locally and is not pushed. Message: `Merge dev-soft-core 2509db68 (the flip train, PR #988) into the lwSRP d1bb4f4e pin`
(one line, no trailers).

## The merge

`git fetch https://github.com/kebag-logic/milan-fpga.git dev-soft-core` gave FETCH_HEAD `2509db68`. Then
`git merge --no-ff` (a merge, not a rebase). The merge base is `aa30d77f`. The train changes 145 paths and the pin
changes 18. Eight paths are changed by both sides: two conflicted, and six merged automatically.

### Conflicts and how each was resolved (both sides kept)

| File | Conflict | Resolution |
|---|---|---|
| `sw/firmware/ctrl/test/srp_arms.py` | Both sides add a function after `listener_arms`. The pin adds `own_leaveall_arms` (srp_own_leaveall.cpp at 8x8/1if and 1x1/1if). The train adds the `LINK_PASS` constant and `link_pass_arms` (#973, srp_link_pass.cpp at 1x1/1if and 8x8/1if) | Both kept verbatim: the pin's function, then the train's constant and function, with the file's two-blank-line spacing |
| `sw/firmware/ctrl/test/test_ctrl_firmware.py`, `run_suites` | Both sides add one `outcomes.extend(...)` after `listener_arms` | Both kept: `own_leaveall_arms`, then `link_pass_arms`, both before `mbx_entity_arms` |
| `sw/firmware/ctrl/test/test_ctrl_firmware.py`, docstring `srp` entry | Both sides add the last clause of the same sentence. The pin adds the own-LeaveAll arms, and the train adds the loop-pass link arms | Both clauses kept, the pin's first, re-wrapped to the entry's column. The text of each is unchanged: "...a Listener withdrawn 5 to 200 ms after the board's own LeaveAll sent as Lv within 240 ms, and none deregistered across LeaveAlls when none is withdrawn, against an lwSRP MSRP peer (lwSRP #20, srp_own_leaveall.cpp) at 8x8/1if on every input and at 1x1/1if; a link that comes up at each phase of a loop pass as SRP's first UP (#973, srp_link_pass.cpp) at 1x1/1if and 8x8/1if, each run a process of its own;" |

The train's other changes in `test_ctrl_firmware.py` merged automatically and are intact: the `srp_early_mutants` and
`srp_link_mutants` imports, and both campaigns' prefix lists.

### Checks on the merge (`receipts/merge/merge-checks.txt`)

- **Each side's change is kept.** For every path a side changed, its sorted +/- lines against `aa30d77f` equal the
  merge's sorted +/- lines against the other parent. Pin: 17 of 18 paths are SAME. Train: 144 of 145 are SAME. The
  one DIFF on each side is `test_ctrl_firmware.py`, the hand-resolved docstring. Its diff against each parent is in
  the receipt.
- **The merge differs from the train only by the pin's paths.** `git diff --name-only 2509db68 507bce7f` gives the
  same 18 paths as `aa30d77f..30796098`.
- **Pin sites in the six automatically merged files.** Each still names lwSRP `d1bb4f4e` where the pin did. The
  counts of `d1bb4f4` and `08ee86e8` equal the pin head's in every file:

  | File | `d1bb4f4` | `08ee86e8` |
  |---|---:|---:|
  | `docs/design/MAILBOX_SPLIT.md` | 1 | 0 |
  | `docs/reference/SUBMODULES.md` | 1 | 0 |
  | `sw/firmware/ctrl/README.md` | 1 | 0 |
  | `sw/firmware/ctrl/srp/README.md` | 3 | 0 |
  | `tb/verilator/milan_dp/Makefile` | 0 | 0 |
  | `tb/verilator/milan_dp/README.md` | 0 | 0 |

  The milan_dp Makefile and README carry the pin's twin changes, not a pin string. The train's content in each of these
  files is intact (144 of 145 SAME, above).
- The gitlink is `third_party/lwSRP` = `d1bb4f4e5954af6dabe7f210a6bf7adbb76bdd6b`. Outside `third_party/`, `08ee86e8`
  remains at only the two sites that record a measurement, kept deliberately since round 1:
  `ci/image/exec-audit-receipt.json` and `docs/design/SPLIT_CONTROL_MEMORY.md`. The train's insertions moved the latter
  from line 491 to line 509.

## Gates at the merge head 507bce7f

| Gate | Command | Result |
|---|---|---|
| Firmware gate, 4 shards (`receipts/firmware/`) | `test_ctrl_firmware.py --require-rv32 --self-test --shard k/4 --jobs 4`, k = 0-3, in parallel | rc 0 each, 11:35 to 12:39. Shard 0: 98 of 98 arms `[ok]`, 85 verdicts, 3,001 cases in PASS verdicts, 0 failing, 47 SRP arms all `[ok]`, among them both `srp_own_leaveall` arms and both `srp_link_pass` arms. Shard 1: mutants 844 of 844 caught. Shard 2: 398 `[ok]`. Shard 3: 664 `[ok]`, and the pin controls name `d1bb4f4e` (an edited `src/` is refused, and `97677fcb` is refused). No line starts with FAIL, MISSED, ESCAPED or REFUSED in any shard. Inventory: 2,005 live invocations, each in exactly one shard, sizes [98, 845, 399, 663] |
| srp_own_leaveall arms (`receipts/own-leaveall/`) | round 1's `own_la.py` (unchanged) | rc 0. 8x8/1if: 44 of 44 tests; 387 withdrawals, 0 never sent, worst 185 ms (limit 240), 0 over. 1x1/1if: 44 of 44; 86 withdrawals, 0 never sent, worst 185 ms, 0 over. The no-withdrawal leg holds: 101 board frames, 5 board LeaveAlls, 2 peer LeaveAlls |
| `twin_mrp.py --selftest` (`receipts/selftests/`) | `cd tb/verilator/milan_dp && python3 -B twin_mrp.py --selftest` | `OK (11 checks)`, rc 0 |
| `make twin` (`receipts/twin/`) | pinned Verilator 5.050 | rc 0. Self-test `OK (11 checks)`. `twin: 0 finding(s)`: all-fabric MSRP 88, MVRP 24; split MSRP 87, MVRP 82 frames. LeaveAll room (round 1's `la_room.py`): 0 full frames, least spare 1,359 octets, the same as round 1 |
| `make -j2 twin-plants`, twice | the same | rc 0 both. Run 1: 16 of 16 plants REFUSED, 32 refusals, 0 not refused (12:48 to 12:59). Run 2: the same (12:59 to 13:07) |
| `kept_grade.py --selftest` (train) | `cd tb/verilator/ctrl_service_budget && python3 -B kept_grade.py --selftest` | `kept_grade selftest: PASS (32 checks)`, rc 0. The tool has no `--require-rv32` option |
| `ctrl_boundary.py --require-rv32 --selftest` (train) | in the route's merge-head worktree (the same commit, porcelain 0 before and after), with `MAKEFLAGS="-j8 --no-print-directory"` | `ctrl_boundary: PASS`, rc 0. 0 findings. 117 boundary, 192 pin and 4 figure controls, 0 misbehaved. 313 `[ok]`, 0 FAIL, 16 "stopped at its link", the same control counts as the train's own run at `300da99b`. Capture: 4,984 invocations from 29 builder runs. The first run, without that MAKEFLAGS, was REFUSED; see note 1 |
| plat_ledger (`receipts/ledger/`) | `plat_ledger.py --build-dir` at `2509db68`; `--self-test` at the merge head | PASS at both, 0 findings. Controls 9 of 9 as required. Image figures below |
| `docs.yml` steps (`receipts/docs/`) | round 2's `docs_gates_r2.py`: every run step except the hosted runner's, then the two renderer steps with the pinned renderer | 46 of 46 rc 0, including both builder legs (`docs-gates-1#14`, `docs-gates-2#14`). Em-dash as a push from `2509db68`: 0 findings over 27 added lines in 5 pages, arms 339 of 339. Em-dash also as a push from `30796098`: 0 findings over 772 lines in 33 pages. TOC gate OK (160 pages). `docs_check` without git: 0 findings. Python idiom gate: 54 of 54. The lane checkout had porcelain 0 before and after |

### Image ledgers (`receipts/ledger/image-hashes.txt`, `image-deltas.txt`)

The images changed, both against `2509db68` and against `30796098`.

| Point | ROM `30796098` | ROM `2509db68` | ROM merge | vs train | SRAM merge (= train) | RAMB36 merge (= train) | RAMB36 pin |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1x1/1if | 126,592 | 127,512 | 127,568 | +56 | 56,736 | 45.5 | 45 |
| 1x1/2if | 128,192 | 129,296 | 129,352 | +56 | 59,168 | 46.5 | 46 |
| 8x8/1if | 139,368 | 141,616 | 141,680 | +64 | 100,096 | 59.5 (override) | 58.5 |
| 8x8/2if | 140,944 | 143,368 | 143,432 | +64 | 117,632 | 64.5 (override) | 63 |

- **Against `2509db68`.** Every `ctrl_app.elf` changes (8 of 8). The reason is the pin alone: `.text` is +60 B in
  every image, and lwSRP's `mrp_mad.o` goes from 13,155 to 13,219 B. No other section, object or stack frame
  changes. RAMB36, SRAM and `ctrl_plat` are unchanged. The AEM, NVM and gPTP microcode images are byte-identical.
- **Against `30796098`.** Every ELF changes. So do the 8x8 AEM descriptor and NVM-shape image (`a34ea856…`, equal to
  the train's). The reason is the train's content: its firmware, its `configs/endstation_ax7101_8x8.yaml` and its
  memory ledger. The 1x1 AEM and both gPTP microcode images are unchanged. Every ROM, SRAM and tile figure in the
  merge column equals the train's figure plus the pin's measured +56 or +64. The tile growth against the pin
  (+0.5 to +1.5) is the train's, accepted by its ledger. Here, plat_ledger passes every point.
- 8x8 ROM fit at the merge head (from the self-test's controls): 8x8/1if is 141,680 B in 143,360; 8x8/2if is
  143,432 B in 145,408.

### Routed 8x8/1if merge condition (`receipts/route/`), re-shown because the image changed

The recipe is round 1's (`route/tools/`, unchanged apart from the head worktree path). It uses the split recipe
export, the identity gate, and `pp_baseline.py --placement full-split`, then the first directive
(ExtraPostPlacementOpt) through `vivado-slot.sh`. The head ran in slot 2 and the base in slot 1, from 11:43 to 12:50.
Two Vivado runs ran at once, and MemAvailable was 61 GB at the start. Then `signoff.py`.

| | Merge `507bce7f` | Base `2509db68` | Merge - base |
|---|---:|---:|---:|
| Slice LUTs (post-route) | **45,958** | **45,982** | **-24** (bound +50) |
| Slice Registers | 53,337 | 53,337 | 0 |
| RAMB36 / RAMB18 / tiles / DSP | 82 / 33 / 98.5 / 13 | 82 / 33 / 98.5 / 13 | 0 |
| Worst WNS (Slow_85C/0C) | +0.038 | +0.035 | |
| Worst WHS (Fast_85C/0C) | +0.036 | +0.036 | |

- Fast-corner WNS is +1.536 at the merge and +1.636 at the base. Slow-corner WHS is +0.102 at both.
- Both sides have 0 failing endpoints and 0 nets with routing errors (93,792 and 93,776 routed nets).
- The IOB pack check passes; its only non-PASS row is the documented INERT `eth0_rx_er`.
- 0 CRITICAL WARNING and 0 ERROR lines at either side. The `Place 30-722` on 8x8's parked `tdm_dout` that round 1
  recorded no longer appears.
- **The merge condition is met.** The design fits and meets the #818 floor (WNS >= +0.030, WHS >= 0) and the stricter
  WHS >= +0.030 at every corner on its first directive, at both sides. The LUT delta is -24.
- The image the merge head embeds (`route/head/fw-identity.txt`): repo `507bce7f`, lwSRP `d1bb4f4e`, ELF
  `a2be09e1…`. The ROM banks hold the ELF, and the identity gate passed. `mrp_mad.o` `.text` is 8,196 B against
  8,136 B at the base (+60).
- The post-route hierarchy delta is in `route/hier-delta.txt`: top -24 LUT; `KL_mbx_dma` -20; its AxiLite4 bridge
  -18/-25.

## Acceptance (round-3 brief)

1. Merge (not a rebase), every conflict resolved keeping both sides: met. No combined figure in the conflicted text
   needed re-deriving; neither side's arm text states a count. The automatically merged pin sites name `d1bb4f4e` and
   the train's content is intact (checks above).
2. Gates at the merge head: met (table above). The image ledgers are reported against both `2509db68` and
   `30796098`, with the reason for each change. The images changed, so the routed 8x8/1if merge condition was
   re-shown: it is met.

Open risks/questions: none blocking; see notes 1 to 3 in `HANDOFF-r3.md`.
