[A647] READ_DESCRIPTOR CONTROL carries the IDENTIFY value; the LOCK_ENTITY notification echoes the command's flags (#185, #186)

Branch `185-186-control-unlock` from main `08ae0013`, three commits: one for #185 and
two for #186 (the second follows the correction on #186 that both unlock notifications
carry UNLOCK). Then main `246cbc22` is merged in (`a2cf652`) and one README record follows
(`f42c886`); see Round 1c.

## #185: READ_DESCRIPTOR CONTROL's current value (198f1b1)

After SET_CONTROL(255), READ_DESCRIPTOR CONTROL 0 still reported the image's
`current[0]`. IEEE 1722.1-2021 §7.2.22 and §7.3.6.2 (Table 7-122) give `value_details` the
control's current setting. Milan v1.2 §5.3.12 makes the IDENTIFY value 0 after reset and
255 in identification mode.

- The engine re-dispatches READ_DESCRIPTOR of a configuration-0 CONTROL (cdl >= 20) at the
  @28 seam to a new program, `E_RDESCCT` (ROM 600). The other four overlaid types of #82
  use the same seam.
- `E_RDESCCT` serves the image with `current[0]` @108 taken from the IDENTIFY row of the
  dynamic store. That is the row GET_CONTROL reads, with no image arm, so the descriptor
  agrees with GET_CONTROL before the first SET_CONTROL (0), after every SET_CONTROL, and
  after a power cycle (0 again), whatever the image holds at @108.
- The overlay applies only where §7.2.22 puts the value. That means `values_offset` 104, a
  one-octet linear value (CONTROL_LINEAR_INT8 or _UINT8), and a descriptor of at least
  112 bytes. Any other CONTROL is served whole from its image. A configuration index past
  the count and a locate miss answer as `E_RDESC` does (BAD_ARGUMENTS and
  NO_SUCH_DESCRIPTOR, each with the 4-byte stub).

Accepted and refused:

| Case | Answer |
|---|---|
| cdl 12..19 | BAD_ARGUMENTS echo (unchanged) |
| CONTROL in configuration 0, `values_offset` 104, LINEAR_INT8/UINT8, length >= 112 (cdl 20 or padded) | SUCCESS, `current[0]` = GET_CONTROL's value |
| the same CONTROL with another `values_offset`, another value type, or shorter than 112 bytes | SUCCESS, the image whole |
| CONTROL index absent | NO_SUCH_DESCRIPTOR stub |
| any other configuration or type | unchanged |

## #186: the LOCK_ENTITY notification's flags (c826171, fcb6b51)

The unsolicited LOCK_ENTITY sent after an UNLOCK carried flags 0. IEEE 1722.1-2021 §7.5.2
sends a notification "by using an unsolicited response to the command", and §7.4.2.1
(Table 7-143) gives the response the command's flags. Milan v1.2 §5.4.5.1 says only that
the notifications carry the same information, so IEEE decides.

- `KL_aecp_notify` latches the command's whole flags word beside the exclusion when a LOCK
  or UNLOCK changes the lock. On the timeout, coalesced or not, it latches UNLOCK (1).
  The notification job carries the word in its two arguments.
- The engine lands the job's arguments where a LOCK_ENTITY's walk leaves them. It packs
  r14[31:0] exactly as for `E_LOCKEN`, and `E_LOCKUNS` emits the word @24.
- A LOCK's or UNLOCK's notification therefore echoes that command's flags, reserved bits
  included, as its response does. Milan v1.2 Table 5.22 says only that a notification is
  sent when the entity automatically unlocks itself after the one-minute timeout, so its
  flags come from IEEE, whose unlock response carries UNLOCK (§7.4.2.1, Table 7-143).
  Both unlock notifications, the command-driven one and the automatic one, therefore
  carry flags UNLOCK with `locked_id` 0. `locked_id` is unchanged: the holder now.
- Two internal module ports carry the word (`KL_aecp_engine.rgy_flags_o`,
  `KL_aecp_notify.rgy_flags_i`), wired inside `protocol_processor_top`. There is no
  register-map, top-level port or parameter change.

## Tests and planted mutants

- `tb/pp_top` section AX, RDC0 to RDC6, grades each READ_DESCRIPTOR byte-exact, against the
  image with the expected value at @108: before any SET_CONTROL, after SET_CONTROL(255)
  and three refused ones, after SET_CONTROL(0) under the lock, either side of a power
  cycle, and for the three layouts that keep the image (values_offset 106,
  CONTROL_LINEAR_INT16, a 111-byte CONTROL) and the INT8 one that is overlaid. `tb/ucpu`
  RC1 and RC2 run the program on a conformant 113-byte IDENTIFY. Nine dispatch arms
  (`rdc-*`) are all KILLED, each by its named check.
- `tb/pp_top` L5b and L6d grade the UNLOCK's and the auto-unlock's notifications with
  flags 1, and TD1 grades the auto-unlock at the top's 60 s default the same way. Section
  RN's independent lock model predicts UNLOCK on both unlocks' pushes. Section AX LN0 to
  LN4 grade a second controller's LOCK and UNLOCK carrying reserved bits in both halves
  of the word, and the auto-unlock after that LOCK (flags UNLOCK). `tb/aecp_notify`
  section LF grades the latch, including a timeout coalesced over a pending LOCK (UNLOCK)
  and a LOCK over a pending timeout (its own flags). `tb/ucpu` L3 and L3b grade the
  program. Sixteen notify controls are all KILLED, each by its named check. Three of them
  plant the automatic unlock with flags 0 and fail LN2, L6d and LF2.
- The command records (`aecp_commands.json`, the re-swept `tb/aecp_cmds/decode.json`),
  docs/architecture/06_aecp_engine.md (§6.1, §6.8, F06.14, the opcode answers), the
  compliance review's decision rows 15 and 16, 09 and the suite READMEs record both.

## Gates

Every processor gate and every campaign that builds a changed file ran at base `08ae0013`
and at the head, all rc 0. The head records were taken at `c8261711` (round 1) and again at
`fcb6b513` (round 1b). Pinned Verilator 5.050; sv2v 0.0.12 and Yosys 0.33 as in CI.

| Gate | Base | Head fcb6b513 | Comparison |
|---|---|---|---|
| scripts/run_suites.sh | rc 0, 1,030,000 checks | rc 0, 1,030,094 checks | every suite line identical except UPC map 61 → 62 constants and 90 → 91 entries; aecp_notify 67 → 73 (LF); pp_top 10,519 → 10,599 (AX 239 → 279: RDC +28, LN +12, in the default and line builds); ucpu 437 → 445 (RC, L3b). Identical to the c8261711 record |
| executed REQ-tag check | rc 0 | rc 0 | evidence identical but for pp_top source lines |
| scripts/lint_hdl.sh | rc 0 | rc 0 | identical |
| make check | rc 0 | rc 0 | links 1196 → 1198, aecp entries 84 → 85, ids 592 → 601 files (nine new patches); otherwise identical |
| scripts/gen_matrix.py --check | rc 0 (94 rows, 0 untested) | rc 0 | identical |
| syn/yosys/run.sh | rc 0, 42 tops | rc 0 | identical but for six all.v line numbers |
| tb/elab_guards/guards.py --frontend yosys | rc 0 | rc 0 | identical but for source line numbers |

| Campaign | Base | Head fcb6b513 |
|---|---|---|
| tb/pp_top/aecp_dispatch_mutants.py | 58 checks PASS | 67 checks PASS: the 9 `rdc-*` arms KILLED; 3 earlier arms also fail new RDC/LN checks (`lk-sctrl-lock-nop` 12 → 13, `rd-tail-uncut` 9 → 16, `rd-str-short-guard-nop` 1 → 6), every base failure kept; README rows updated |
| tb/pp_top/notify_mutants.py | 98 of 98 KILLED | 114 of 114 KILLED: the 16 lock controls added; every earlier control fails the same checks |
| tb/aecp_cmds/mutants.py | 17 of 17 | identical |
| tb/pp_top/aecp_mutants.py, ctr_mutants.py, gsi_mutants.py, name_wr_mutant.py | 67 PASS, 18 PASS, 20 detected, killed | identical (TD1's message names flags UNLOCK) |
| tb/name_state, tb/maap, tb/adp_engine mutants | 16 KILLED, 32 PASS, 62 PASS | identical |
| tb/elab_guards/mutants.py | 160 of 160 | identical but for engine and notify line numbers |
| tb/pp_top/acmp_mutants.py | 51 of 51 KILLED | identical (L6d's message names flags UNLOCK) |
| tb/pp_top/d3_mutants.py | 110 of 110 KILLED | identical |

Parent consumer gates on a scratch milan-fpga at dev `e9cbb676`, with the protocol-processor
gitlink staged at the head and the #180 and #176 parent patches applied (uncommitted). There
were 17 gates (C++, Python and shell idiom, RTL source lists, pp_srcs, port contracts,
naming, test evidence, docs, RTL lint, the builder tests, pp_shadow, nvm_cosim lint and
quick, milan_dp, milan_dp_render, and the xvlog gate). All are rc 0 at base and at
`fcb6b513`. The PASS/FAIL records are identical. The differences are the two new
documented ports, the added Python lines, `ucode.hex` 90 → 91 programs, timing, and the
pin line.

## Round 1b

The correction on #186 withdrew the instruction that the lock-timeout notification
keeps flags 0. Milan v1.2 Table 5.22 does not define the automatic unlock's flags, so
IEEE 1722.1-2021 decides: §7.5.2's notification is an unsolicited response, and an
unlock response carries UNLOCK (§7.4.2.1, Table 7-143). `fcb6b51` therefore latches
UNLOCK on the timeout, coalesced or not. Both unlock notifications now carry flags
UNLOCK with `locked_id` 0.

| Cause | Notification flags | locked_id |
|---|---|---|
| a LOCK that took the lock | the LOCK's whole word | the new holder |
| an UNLOCK that released it | the UNLOCK's whole word (UNLOCK set) | 0 |
| the automatic unlock after the timeout, no round pending | UNLOCK | 0 |
| the timeout coalesced into a pending lock round | UNLOCK | 0 |
| a LOCK coalesced over a pending timeout | the LOCK's word | the holder now |

- Checks changed: LN2 (default and line builds), L6d, TD1 (the 60 s default), RN's lock
  model, `tb/aecp_notify` LF2, `tb/ucpu` L3b. RN's model now also predicts the UNLOCK's
  flags on the push after the holder's UNLOCK, a path its fixed seed does not reach.
- Planted mutants of the automatic unlock with flags 0, the round-1 behavior:
  `lock_timeout_flags_zero` fails LN2, `lock_auto_unlock_flags_zero` fails L6d, and
  `lock_coalesced_timeout_flags_zero` fails LF2. Planted by hand across the whole pp_top
  suite, the same edit fails L6d, LN2 and RN in the default build, LN2 in the line build
  and TD1 in the defaults build. E_LOCKUNS fed from r12 fails L3 and L3b in `tb/ucpu`.
- The microcode and the ROMs are unchanged. There is no register-map, top-level port or
  parameter change.

## Round 1c: merged with main 246cbc22

Main moved on to `246cbc22`, with the #181 notify-queue cut (#187) and the #184 MSRP
Domain re-declaration (#191). The branch takes it in one merge commit, `a2cf652`, with
no rebase. One README-only commit follows, `f42c886`. Both sides keep their behaviour:

- `KL_aecp_notify`'s emission pick keeps the lock arm's flags arguments (`lockf_r`).
  Its command-queue arm reads #181's registered occupancy `cmdq_nempty_r`. The
  occupancy writes, `amap_busy_o`, the event router's scan and the flags latch are each
  side's code unchanged.
- `tb/aecp_notify` runs section LF, then CQ, then OC1 last, so LF also runs under the
  occupancy monitor. The suite has 86 checks (57 in the first run).
- `notify_mutants.py` keeps both control sets (`OCCUPANCY + LOCK_FLAGS`). 09 §8.4 lists
  LF, CQ and OC ("ten of the notification block's").
- Two of #181's controls, `occupancy_push_unseen` and `occupancy_reset_set`, now also
  fail LF checks, because LF's SET_NAME round goes through the queue.
  `tb/aecp_notify/README.md` records their new failing sets (`f42c886`).

Every processor gate ran at the merged base `246cbc22` and at the head, all rc 0. The
head records were taken at `a2cf652` and, for the gates, again at `f42c886`, byte-identical.

| Gate | Base 246cbc22 | Head |
|---|---|---|
| scripts/run_suites.sh | rc 0, 1,030,029 checks | rc 0, 1,030,123: UPC map 61 → 62 / 90 → 91, aecp_notify 80 → 86, pp_top 10,519 → 10,599, ucpu 437 → 445; nothing else differs |
| executed REQ-tag check | rc 0 | rc 0, identical (source lines masked) |
| scripts/lint_hdl.sh, scripts/gen_matrix.py --check | rc 0 | rc 0, identical |
| make check | rc 0 | rc 0: links 1202 → 1204, aecp entries 84 → 85, ids 608 → 617 |
| syn/yosys/run.sh (Yosys 0.33 and 0.66), elab guards under Yosys | rc 0 | rc 0, identical but for line numbers |

| Campaign | Base 246cbc22 | Head a2cf652 |
|---|---|---|
| aecp_dispatch_mutants.py | 58 checks PASS | 67 PASS: the 9 `rdc-*` arms; 3 earlier arms fail more (as recorded) |
| notify_mutants.py | 109 of 109 KILLED | 125 of 125: the 16 lock controls (identical to round 1b); 2 occupancy controls also fail LF |
| aecp_cmds, aecp, ctr, gsi, name_wr, name_state, maap, adp, acmp, elab_guards, d3 | all rc 0 | all rc 0, identical (TD1's message names flags UNLOCK in aecp) |

Parent consumer gates ran on a committed local scratch milan-fpga at dev `e9cbb676`. It
carries the #180 and #176 parent patches as two local commits, and the
protocol-processor gitlink as a third, at the base for the base pass and at the head for
the head pass. Nothing was pushed. All 17 gates are rc 0 at base and at `f42c886`, and
the PASS/FAIL records are identical. The differences are the lane's two documented
internal ports and its Python lines, `ucode.hex` 90 → 91 programs, timing and output
order, and the pin line.

No register-map, top-level port or parameter change. Two internal module ports
(`KL_aecp_engine.rgy_flags_o`, `KL_aecp_notify.rgy_flags_i`) are wired inside
`protocol_processor_top`.

Closes #185
Closes #186
