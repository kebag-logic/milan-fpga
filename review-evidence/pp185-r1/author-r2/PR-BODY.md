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

## Round 2: one cause per lock notification; the overlay only for IDENTIFY

Five commits on `b0f6f9c3` (the round-1c head plus main `b48312e1`), answering
R668-1 and R667-1: `43a7987` (#186), `4ba8c02` (#185), `acc059a` (docs and records),
`7368215` (two README rows the head campaigns moved) and `4865184` (the new bench
section split into functions under 100 lines, as the parent's C++ idiom gate requires;
its output is unchanged). Head `4865184`.

### Every LOCK_ENTITY notification carries one cause (R668-1 F1, R667-1 F1)

A notification's flags are its job's arguments, which the engine loads with the job,
and its `locked_id` is the holder `E_LOCKUNS` reads afterwards through the rgy face.
The two came apart in two ways: a lock expiry on the edge that claimed a pending lock
round (the claim took the LOCK's arguments and cleared the pending bit beside the
expiry, so the round carried the LOCK's flags with `locked_id` 0 and the automatic
unlock was lost), and a lock change after the claim (the round's remaining jobs kept
the old flags while the holder read was live, so a LOCK by another controller during
an UNLOCK round gave UNLOCK with that controller's id). An expiry between a job's load
and its holder read could split a frame the same way.

The rule, from IEEE 1722.1-2021 §7.5.2, §7.4.2.1 and Table 7-143 and Milan v1.2
Table 5.22: a LOCK's notification carries its flags word and its holder; an UNLOCK's,
or the automatic unlock's, carries UNLOCK (or the UNLOCK's whole word) with
`locked_id` 0.

The mechanism is in `KL_aecp_notify` alone; the engine, the microprogram, every port
and the register map are unchanged (06 §6.8, "One cause per notification"):

- The lock expiry is owed from its strobe and held back while a LOCK job is presented
  and in the cycle a state query is taken, so a job's holder read answers the state
  its arguments came from. Otherwise it applies at once, within one job of the strobe.
- In an idle cycle in which the expiry applies, the round claim waits a cycle, so a
  lock round claimed next takes the automatic unlock's flags and empty exclusion with
  the pending bit.
- An expiry, a LOCK that takes the lock or an UNLOCK that releases it during a lock
  round re-latches that round's arguments and exclusion for its jobs not yet
  presented, and pends the next lock round as before, so the controllers already
  reached see the change too.
- A LOCK or UNLOCK in the cycle an expiry applies decides on the released lock, so a
  holder's re-lock then takes the lock anew and notifies.

The LOCK/UNLOCK command-word echo and #181's queue are kept (sections LF, LN, L5b, CQ
and OC1 unchanged and passing). The owner-acceptance alternative was not used.

`tb/aecp_notify` section LC serves every lock job as the engine does (arguments at the
load, then the holder read through the face) and grades each frame's @24..@35 bytes,
destination and sequence_id, 45 checks: the expiry one clock before, on, one and two
clocks after the claim, after LOCK words 0 and 0x00010000 with the former owner
registered (LC1); between a job's load and its holder read and in the cycle the read
is taken (LC2, LC3); another controller's LOCK during an UNLOCK round, its requester
skipped (LC4, LC5); the holder's UNLOCK during its LOCK round (LC6); and its re-lock
after an expiry owed while a job waits (LC7). At `b0f6f9c3` twelve of these fail,
among them the reviewers' two reproductions. Ten new notify controls are each KILLED
by their named LC check, and the reviewers' claim-collision and mid-round probes pass
at the head.

### The CONTROL overlay serves the IDENTIFY CONTROL only (R667-1 F2)

IEEE 1722.1-2021 §7.2.22 and §7.3.6.2 give every CONTROL its own current values, and
the dynamic row the overlay reads is the IDENTIFY's (Milan v1.2 §5.3.12). A new
program, `E_RDESCID` (ROM 656), tests `control_type` @82..@89 against IDENTIFY,
90-E0-F0-00-00-00-00-01 (Table 7-98), as model rule L8 does, in four 16-bit words, and
serves any other CONTROL whole from its image. It runs inside the engine's
microprogram; `identify_index_i` would have needed a top-level wiring change, so it
was not used.

| CONTROL in configuration 0 | READ_DESCRIPTOR answer |
|---|---|
| `control_type` IDENTIFY, `values_offset` 104, LINEAR_INT8/UINT8, length >= 112 | SUCCESS, `current[0]` = GET_CONTROL's value |
| any other `control_type` (a vendor type, or one word off IDENTIFY) | SUCCESS, the image whole |
| the other layouts (another `values_offset` or value type, shorter than 112 bytes) | SUCCESS, the image whole (unchanged) |
| index absent | NO_SUCH_DESCRIPTOR stub (unchanged) |

`tb/pp_top` RDC7 serves the image whole for a vendor type and for four types that each
differ from IDENTIFY in one word; `tb/ucpu` RC3 for a type off in its last octet. RDC0
to RDC6 still pass. Six dispatch arms (the test bypassed, the program before this
round; each word comparison dropped; the refusal arm's status kept) are each KILLED by
their named RDC7 check.

### Records and wording (R667-1 F3, R1; R668-1 F2)

- `tb/pp_top/README.md` states the merged notify-campaign total, 125 (98, #181's
  eleven, #186's sixteen), and the round's ten for 135.
- 06 §6.8 and the compliance review's row 16 say "on `T-LOCK-UNLOCK` expiry".
- The new comments carry no bench labels, as R668-1 F2 lists them; a scan of every
  comment line the PR adds finds none.

### Gates

Every processor gate and all 13 campaigns that build a changed file ran at base
`b0f6f9c3` and at `acc059a`, all rc 0; every gate ran again at the final head
`4865184`, byte-identical, with the notify campaign (the one that builds the split
bench) identical too.

| Gate | Base b0f6f9c3 | Head |
|---|---|---|
| scripts/run_suites.sh | rc 0, 1,030,132 checks | rc 0, 1,030,205: UPC map 91 → 92 entry points, aecp_notify 86 → 131 (LC), pp_top 10,608 → 10,634 (RDC7 in two builds), ucpu 445 → 447 (RC3); nothing else differs |
| executed REQ-tag check | rc 0 | rc 0, identical (two aecp_notify source lines moved at the final head) |
| scripts/lint_hdl.sh, scripts/gen_matrix.py --check | rc 0 | rc 0, byte-identical |
| make check | rc 0 | rc 0: ids 617 → 623 files (the six new patches) |
| syn/yosys/run.sh (Yosys 0.33 and 0.66), elab guards under Yosys | rc 0 | rc 0, identical but for line numbers |

| Campaign | Base b0f6f9c3 | Head |
|---|---|---|
| aecp_dispatch_mutants.py | 67 checks PASS | 73 PASS: the 6 `rdc-ctype-*` arms; `rdc-base-no-overlay`, `rdc-unit-shift-8` and `rd-tail-uncut` also fail RDC7's last read, every base failure kept |
| notify_mutants.py | 125 of 125 KILLED | 135 of 135: the 10 lock-cause controls; four LF controls and `occupancy_reset_set` also fail LC checks, every base failure kept |
| aecp_cmds, aecp, ctr, gsi, name_wr, name_state, maap, adp, acmp, elab_guards, d3 | all rc 0 | all rc 0, identical |

Parent consumer gates ran on a local scratch milan-fpga at dev `e9cbb676` with the #180
and #176 parent patches (local commits, never pushed), at base `b0f6f9c3` and at
`4865184`. Sixteen of the 17 are rc 0 at both with identical PASS/FAIL records (the
differences are the drivers' Python lines, `ucode.hex` 91 → 92 programs, timing and the
pin line). Gate 11, `lint_rtl.py --check`, is rc 1 at both, byte-identical: three new
findings in the parent's own `hdl/milan` files, chiefly `KL_pp_shadow.sv` driving
`cfg_tspec_max_frame_i`, which processor main `b48312e1` (#190) widened to 128 bits,
with 16. It comes with that merge, before any round-2 commit, and needs the parent's
adoption of #190; this lane does not change it. A first head pass at `7368215` failed
gate 1 on this lane's own 164-line bench function; `4865184` fixed that, and gate 1 is
rc 0 at the head.

No register-map, top-level port or parameter change in round 2: the RTL change is
`KL_aecp_notify.sv` and the microprogram (`gen_ucode.py`), and the engine, `hdl/top`
and `hdl/common` are untouched.

Closes #185, closes #186
