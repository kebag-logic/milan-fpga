[A822] REVIEW READY
Commit: 87b2fc0f2867ef132b9388e22ec262fc626cbb57
Round 3, PR #978; local branch `pf-973-1`, PR base `dev-soft-core`. Four local commits after `5759780f`.

R896-2-F1 (stale uncarried-UP mark): fixed. When the register read DOWN, the poll skipped the mark update, so the
mark of an UP that was later elided survived the DOWN. A fresh UP after a later pass's take could then be taken on
the old mark, and its own LINK reset the interface a second time. `carried_up` now runs on every poll with the
level the register read. While no LINK has carried an UP, a DOWN read writes 0 and clears the mark
(`srp_mbx.c:1286-1294`, the poll at `:1309`). So the mark holds only while every poll reads the link up, and an UP
after a DOWN is taken from its own LINK: the first keeps the startup participants, and a later one resets once.
- Unchanged: re-attach / elided-DOWN recovery, the immediate fail-closed DOWN, carried-UP handling, and the
  first-UP and later-UP reset rules.
- Size: `.text` is byte-identical at 1x1/1if and 8x8/1if, and +4 B at 2if.
- Stated assumption: a DOWN that no poll reads lasts less than the gap between two polls. A dropped autonegotiated
  link waits at least `break_link_timer`, 1,200 ms (IEEE 802.3-2022 28.3.2), before it renegotiates. The code
  comment, the SRP README and the PR state this.

Tests first (`d9f8929d`): `SrpLinkPassElided.AnElidedUpAuthorizesNoFreshFirstUp` and `...FreshLaterUp`, in the link
suite's own process at 1x1/1if and 8x8/1if.
- Both FAIL at `5759780f` at both shapes, PASS with `9a71daa9`'s SRP sources, and PASS at this head.
- The reviewer's unmodified `probe_stale_mark.cpp` and `run_focused.py` pass at both shapes (10/10).
- Their `run_controls.py` passes 4/4: the prior-production control and the re-attach probe.
- Plants: `link-pass-mark-survives-a-down`, `-later` and `link-pass-mark-masked-before-the-shift` are new; the
  changed lines' plants are replanted.
- `rv-poll-resets-on-register-up`, `rv-sink-double-reset` and `link-pass-attach-carries-an-up` stay killed.
- My first form of the `mark-survives` plants did not compile. Its raw ESCAPED result is kept and not counted;
  `9509dbd3` corrects it.
- README lines 120-123 and the code comment now state when the mark's observation is valid.

R895-1-F1 (retained): the source fix is unchanged. The local boundary gate passes at this head. The hosted
`firmware-boundary` job at the pushed head is still needed, and the PR body says so.

Validation at this exact head:
- `test_ctrl_firmware.py --require-rv32 --self-test --shard K/4 --jobs 8`, K=0..3: PASS.
  - 77 suite verdicts; control 826 caught; AECP 385 `[ok]`; SRP 585 `[ok]`; 0 escaped.
  - All 14 link plants are killed at 1x1/1if, 8x8/1if and 1x1/2if.
- `ctrl_boundary.py --require-rv32 --selftest`: PASS. 4,455 compiled sources, 0 findings; 117 boundary, 185 pin and
  4 figure controls; 0 misbehaved.
- `fw_coverage.py --selftest` and `--check`: PASS, 40 files.
- `make -C tb/verilator/milan_dp twin twin-plants twin-maps twin-maps-plants`: PASS.
- CPU `run.py` at `1x1` and `8x8-1if`, all ten groups: PASS.
  - 88 / 86 probes; 0 refusals, budget misses or share misses; no verdict changed against base or round 2.
  - Largest base/head difference 0.204 ms against 20 ms.
- `flip_grade.py --check` at both shipping points, `load_grade.py --check` and `shape_costs.py --check`: PASS,
  byte-identical to base.
  - Loads 0.511 / 0.744 against 0.70 / 0.75.
  - 1x1: last notice 127.31 ms, ACMP 29.06 ms, txL 47.88 ms. The stored last-notice gate stays 130 ms.
- `plat_ledger.py`: PASS at all four points, 0 findings.
  - ROM 126,488 / 128,112 / 139,256 / 140,856 B; 45 / 46 / 58 / 63 RAMB36 unchanged.
  - 1x1/1if and 8x8/1if are identical to the previous head in every size field.
- Docs workflow steps: 104/104 PASS. Builder legs 0 / 1: PASS, with the same declared NOT RUN arm each as before.
- Split boot: 1x1 and 8x8 PASS; self-test native controls and planted defects caught.

No RTL, mailbox contract, loop, budget bound or budget harness change. The working tree is clean; no push or PR
edit was made.

Still required: the manager's push, the hosted and local workflow reruns, independent re-review, merge-candidate
validation, the existing fit/timing obligations and the post-merge bench scenarios. This is author evidence, not
review approval or LAB qualification.
